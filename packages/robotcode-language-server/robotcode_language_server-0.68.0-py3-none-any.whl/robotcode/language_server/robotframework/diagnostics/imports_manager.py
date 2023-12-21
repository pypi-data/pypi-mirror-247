from __future__ import annotations

import ast
import asyncio
import itertools
import multiprocessing as mp
import os
import shutil
import sys
import weakref
import zlib
from abc import ABC, abstractmethod
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    final,
)

from robotcode.core.async_cache import AsyncSimpleLRUCache
from robotcode.core.async_tools import Lock, async_tasking_event, create_sub_task
from robotcode.core.lsp.types import DocumentUri, FileChangeType, FileEvent
from robotcode.core.uri import Uri
from robotcode.core.utils.dataclasses import as_json, from_json
from robotcode.core.utils.glob_path import Pattern, iter_files
from robotcode.core.utils.logging import LoggingDescriptor
from robotcode.core.utils.path import path_is_relative_to
from robotcode.language_server.common.decorators import language_id
from robotcode.language_server.common.parts.workspace import FileWatcherEntry, Workspace
from robotcode.language_server.common.text_document import TextDocument
from robotcode.language_server.robotframework.configuration import CacheSaveLocation, RobotCodeConfig
from robotcode.language_server.robotframework.utils.robot_path import find_file_ex
from robotcode.robot.utils import get_robot_version, get_robot_version_str

from ...__version__ import __version__
from .entities import CommandLineVariableDefinition, VariableDefinition
from .library_doc import (
    ROBOT_LIBRARY_PACKAGE,
    CompleteResult,
    LibraryDoc,
    ModuleSpec,
    VariablesDoc,
    complete_library_import,
    complete_resource_import,
    complete_variables_import,
    find_file,
    find_library,
    find_variables,
    get_library_doc,
    get_model_doc,
    get_module_spec,
    get_variables_doc,
    is_library_by_path,
    is_variables_by_path,
    resolve_args,
    resolve_variable,
)

if TYPE_CHECKING:
    from robotcode.language_server.robotframework.protocol import RobotLanguageServerProtocol

    from .namespace import Namespace


RESOURCE_EXTENSIONS = (
    {".resource", ".robot", ".txt", ".tsv", ".rst", ".rest", ".json", ".rsrc"}
    if get_robot_version() >= (6, 1)
    else {".resource", ".robot", ".txt", ".tsv", ".rst", ".rest"}
)
REST_EXTENSIONS = (".rst", ".rest")


LOAD_LIBRARY_TIME_OUT = 30
FIND_FILE_TIME_OUT = 10
COMPLETE_LIBRARY_IMPORT_TIME_OUT = COMPLETE_RESOURCE_IMPORT_TIME_OUT = COMPLETE_VARIABLES_IMPORT_TIME_OUT = 10


class _EntryKey:
    pass


@dataclass()
class _LibrariesEntryKey(_EntryKey):
    name: str
    args: Tuple[Any, ...]

    def __hash__(self) -> int:
        return hash((self.name, self.args))


class _ImportEntry(ABC):
    def __init__(
        self,
        parent: ImportsManager,
    ) -> None:
        self.parent = parent
        self.references: weakref.WeakSet[Any] = weakref.WeakSet()
        self.file_watchers: List[FileWatcherEntry] = []
        self._lock = Lock()

    @staticmethod
    def __remove_filewatcher(workspace: Workspace, entry: FileWatcherEntry) -> None:
        workspace.remove_file_watcher_entry(entry)

    def __del__(self) -> None:
        try:
            if self.file_watchers is not None and asyncio.get_running_loop():
                for watcher in self.file_watchers:
                    _ImportEntry.__remove_filewatcher(self.parent.parent_protocol.workspace, watcher)
        except RuntimeError:
            pass

    def _remove_file_watcher(self) -> None:
        if self.file_watchers is not None:
            for watcher in self.file_watchers:
                self.parent.parent_protocol.workspace.remove_file_watcher_entry(watcher)
        self.file_watchers = []

    @abstractmethod
    async def check_file_changed(self, changes: List[FileEvent]) -> Optional[FileChangeType]:
        ...

    @final
    async def invalidate(self) -> None:
        async with self._lock:
            await self._invalidate()

    @abstractmethod
    async def _invalidate(self) -> None:
        ...

    @abstractmethod
    async def _update(self) -> None:
        ...

    @abstractmethod
    async def is_valid(self) -> bool:
        ...


class _LibrariesEntry(_ImportEntry):
    def __init__(
        self,
        parent: ImportsManager,
        name: str,
        args: Tuple[Any, ...],
        working_dir: str,
        base_dir: str,
        get_libdoc_coroutine: Callable[[str, Tuple[Any, ...], str, str], Coroutine[Any, Any, LibraryDoc]],
        ignore_reference: bool = False,
    ) -> None:
        super().__init__(parent)
        self.name = name
        self.args = args
        self.working_dir = working_dir
        self.base_dir = base_dir
        self._get_libdoc_coroutine = get_libdoc_coroutine
        self._lib_doc: Optional[LibraryDoc] = None
        self.ignore_reference = ignore_reference

    def __repr__(self) -> str:
        return (
            f"{type(self).__qualname__}(name={self.name!r}, "
            f"args={self.args!r}, file_watchers={self.file_watchers!r}, id={id(self)!r}"
        )

    async def check_file_changed(self, changes: List[FileEvent]) -> Optional[FileChangeType]:
        async with self._lock:
            if self._lib_doc is None:
                return None

            for change in changes:
                uri = Uri(change.uri)
                if uri.scheme != "file":
                    continue

                path = uri.to_path()
                if self._lib_doc is not None and (
                    (
                        self._lib_doc.module_spec is not None
                        and self._lib_doc.module_spec.submodule_search_locations is not None
                        and any(
                            path_is_relative_to(path, Path(e).resolve())
                            for e in self._lib_doc.module_spec.submodule_search_locations
                        )
                    )
                    or (
                        self._lib_doc.module_spec is not None
                        and self._lib_doc.module_spec.origin is not None
                        and path_is_relative_to(path, Path(self._lib_doc.module_spec.origin).parent)
                    )
                    or (self._lib_doc.source and path_is_relative_to(path, Path(self._lib_doc.source).parent))
                    or (
                        self._lib_doc.module_spec is None
                        and not self._lib_doc.source
                        and self._lib_doc.python_path
                        and any(path_is_relative_to(path, Path(e).resolve()) for e in self._lib_doc.python_path)
                    )
                ):
                    await self._invalidate()

                    return change.type

            return None

    async def _update(self) -> None:
        self._lib_doc = await self._get_libdoc_coroutine(self.name, self.args, self.working_dir, self.base_dir)

        source_or_origin = (
            self._lib_doc.source
            if self._lib_doc.source is not None
            else self._lib_doc.module_spec.origin
            if self._lib_doc.module_spec is not None
            else None
        )

        # we are a module, so add the module path into file watchers
        if self._lib_doc.module_spec is not None and self._lib_doc.module_spec.submodule_search_locations is not None:
            self.file_watchers.append(
                self.parent.parent_protocol.workspace.add_file_watchers(
                    self.parent.did_change_watched_files,
                    [
                        str(Path(location).resolve().joinpath("**"))
                        for location in self._lib_doc.module_spec.submodule_search_locations
                    ],
                )
            )

            if source_or_origin is not None and Path(source_or_origin).parent in [
                Path(loc).resolve() for loc in self._lib_doc.module_spec.submodule_search_locations
            ]:
                return

        # we are a file, so put the parent path to filewatchers
        if source_or_origin is not None:
            self.file_watchers.append(
                self.parent.parent_protocol.workspace.add_file_watchers(
                    self.parent.did_change_watched_files, [str(Path(source_or_origin).parent.joinpath("**"))]
                )
            )

            return

        # we are not found, so put the pythonpath to filewatchers
        if self._lib_doc.python_path is not None:
            self.file_watchers.append(
                self.parent.parent_protocol.workspace.add_file_watchers(
                    self.parent.did_change_watched_files,
                    [str(Path(s).joinpath("**")) for s in self._lib_doc.python_path],
                )
            )

    async def _invalidate(self) -> None:
        if self._lib_doc is None and len(self.file_watchers) == 0:
            return

        self._remove_file_watcher()
        self._lib_doc = None

    async def is_valid(self) -> bool:
        async with self._lock:
            return self._lib_doc is not None

    async def get_libdoc(self) -> LibraryDoc:
        async with self._lock:
            if self._lib_doc is None:
                await self._update()

            assert self._lib_doc is not None

            return self._lib_doc


@dataclass()
class _ResourcesEntryKey(_EntryKey):
    name: str

    def __hash__(self) -> int:
        return hash(self.name)


class _ResourcesEntry(_ImportEntry):
    def __init__(
        self,
        name: str,
        parent: ImportsManager,
        get_document_coroutine: Callable[[], Coroutine[Any, Any, TextDocument]],
    ) -> None:
        super().__init__(parent)
        self.name = name
        self._get_document_coroutine = get_document_coroutine
        self._document: Optional[TextDocument] = None
        self._lib_doc: Optional[LibraryDoc] = None

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(name={self.name!r}, file_watchers={self.file_watchers!r}, id={id(self)!r}"

    async def check_file_changed(self, changes: List[FileEvent]) -> Optional[FileChangeType]:
        async with self._lock:
            for change in changes:
                uri = Uri(change.uri)
                if uri.scheme != "file":
                    continue

                path = uri.to_path()
                if (
                    self._document is not None
                    and (path.resolve() == self._document.uri.to_path().resolve())
                    or self._document is None
                ):
                    await self._invalidate()

                    return change.type

            return None

    async def _update(self) -> None:
        self._document = await self._get_document_coroutine()

        if self._document._version is None:
            self.file_watchers.append(
                self.parent.parent_protocol.workspace.add_file_watchers(
                    self.parent.did_change_watched_files,
                    [str(self._document.uri.to_path())],
                )
            )

    async def _invalidate(self) -> None:
        if self._document is None and len(self.file_watchers) == 0:
            return

        self._remove_file_watcher()

        self._document = None
        self._lib_doc = None

    async def is_valid(self) -> bool:
        async with self._lock:
            return self._document is not None

    async def get_document(self) -> TextDocument:
        async with self._lock:
            await self._get_document()

        assert self._document is not None

        return self._document

    async def _get_document(self) -> TextDocument:
        if self._document is None:
            await self._update()

        assert self._document is not None

        return self._document

    async def get_namespace(self) -> Namespace:
        async with self._lock:
            return await self._get_namespace()

    async def _get_namespace(self) -> Namespace:
        return await self.parent.parent_protocol.documents_cache.get_resource_namespace(await self._get_document())

    async def get_libdoc(self) -> LibraryDoc:
        async with self._lock:
            if self._lib_doc is None:
                self._lib_doc = await (await self._get_namespace()).get_library_doc()

            return self._lib_doc


@dataclass()
class _VariablesEntryKey(_EntryKey):
    name: str
    args: Tuple[Any, ...]

    def __hash__(self) -> int:
        return hash((self.name, self.args))


class _VariablesEntry(_ImportEntry):
    def __init__(
        self,
        name: str,
        args: Tuple[Any, ...],
        working_dir: str,
        base_dir: str,
        parent: ImportsManager,
        get_variables_doc_coroutine: Callable[[str, Tuple[Any, ...], str, str], Coroutine[Any, Any, VariablesDoc]],
    ) -> None:
        super().__init__(parent)
        self.name = name
        self.args = args
        self.working_dir = working_dir
        self.base_dir = base_dir
        self._get_variables_doc_coroutine = get_variables_doc_coroutine
        self._lib_doc: Optional[VariablesDoc] = None

    def __repr__(self) -> str:
        return (
            f"{type(self).__qualname__}(name={self.name!r}, "
            f"args={self.args!r}, file_watchers={self.file_watchers!r}, id={id(self)!r}"
        )

    async def check_file_changed(self, changes: List[FileEvent]) -> Optional[FileChangeType]:
        async with self._lock:
            if self._lib_doc is None:
                return None

            for change in changes:
                uri = Uri(change.uri)
                if uri.scheme != "file":
                    continue

                path = uri.to_path()
                if self._lib_doc.source and path.exists() and path.samefile(Path(self._lib_doc.source)):
                    await self._invalidate()

                    return change.type

            return None

    async def _update(self) -> None:
        self._lib_doc = await self._get_variables_doc_coroutine(self.name, self.args, self.working_dir, self.base_dir)

        if self._lib_doc is not None:
            self.file_watchers.append(
                self.parent.parent_protocol.workspace.add_file_watchers(
                    self.parent.did_change_watched_files,
                    [str(self._lib_doc.source)],
                )
            )

    async def _invalidate(self) -> None:
        if self._lib_doc is None and len(self.file_watchers) == 0:
            return

        self._remove_file_watcher()

        self._lib_doc = None

    async def is_valid(self) -> bool:
        async with self._lock:
            return self._lib_doc is not None

    async def get_libdoc(self) -> VariablesDoc:
        async with self._lock:
            if self._lib_doc is None:
                await self._update()

            assert self._lib_doc is not None

            return self._lib_doc


@dataclass
class LibraryMetaData:
    meta_version: str
    name: Optional[str]
    member_name: Optional[str]
    origin: Optional[str]
    submodule_search_locations: Optional[List[str]]
    by_path: bool

    mtimes: Optional[Dict[str, int]] = None

    @property
    def filepath_base(self) -> str:
        if self.by_path:
            if self.origin is not None:
                p = Path(self.origin)

                return f"{zlib.adler32(str(p.parent).encode('utf-8')):08x}_{p.stem}"
        else:
            if self.name is not None:
                return self.name.replace(".", "/") + (f".{self.member_name}" if self.member_name else "")

        raise ValueError("Cannot determine filepath base.")


class ImportsManager:
    _logger = LoggingDescriptor()

    def __init__(self, parent_protocol: RobotLanguageServerProtocol, folder: Uri, config: RobotCodeConfig) -> None:
        super().__init__()
        self.parent_protocol = parent_protocol

        self.folder = folder

        cache_base_path = self.folder.to_path()
        if (
            config.analysis.cache.save_location == CacheSaveLocation.WORKSPACE_STORAGE
            and isinstance(self.parent_protocol.initialization_options, dict)
            and "storageUri" in self.parent_protocol.initialization_options
        ):
            cache_base_path = Uri(self.parent_protocol.initialization_options["storageUri"]).to_path()

        self._logger.trace(lambda: f"use {cache_base_path} as base for caching")

        self.cache_path = cache_base_path / ".robotcode_cache"

        self.lib_doc_cache_path = (
            self.cache_path
            / f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            / get_robot_version_str()
            / "libdoc"
        )
        self.variables_doc_cache_path = (
            self.cache_path
            / f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            / get_robot_version_str()
            / "variables"
        )

        self.config = config

        self.ignored_libraries_patters = [Pattern(s) for s in config.analysis.cache.ignored_libraries]
        self.ignored_variables_patters = [Pattern(s) for s in config.analysis.cache.ignored_variables]
        self._libaries_lock = Lock()
        self._libaries: OrderedDict[_LibrariesEntryKey, _LibrariesEntry] = OrderedDict()
        self._resources_lock = Lock()
        self._resources: OrderedDict[_ResourcesEntryKey, _ResourcesEntry] = OrderedDict()
        self._variables_lock = Lock()
        self._variables: OrderedDict[_VariablesEntryKey, _VariablesEntry] = OrderedDict()
        self.file_watchers: List[FileWatcherEntry] = []
        self.parent_protocol.documents.did_create_uri.add(self._do_imports_changed)
        self.parent_protocol.documents.did_change.add(self.resource_document_changed)
        self._command_line_variables: Optional[List[VariableDefinition]] = None
        self._command_line_variables_lock = Lock()
        self._resolvable_command_line_variables: Optional[Dict[str, Any]] = None
        self._resolvable_command_line_variables_lock = Lock()

        self._environment = dict(os.environ)
        if self.parent_protocol.profile.env:
            self._environment.update(self.parent_protocol.profile.env)
        self._environment.update(self.config.robot.env)

        self._library_files_cache = AsyncSimpleLRUCache()
        self._resource_files_cache = AsyncSimpleLRUCache()
        self._variables_files_cache = AsyncSimpleLRUCache()

    @property
    def environment(self) -> Mapping[str, str]:
        return self._environment

    def clear_cache(self) -> None:
        if self.cache_path.exists():
            shutil.rmtree(self.cache_path)
            self._logger.debug(lambda: f"Cleared cache {self.cache_path}")

    @_logger.call
    async def get_command_line_variables(self) -> List[VariableDefinition]:
        from robot.utils.text import split_args_from_name_or_path

        async with self._command_line_variables_lock:
            if self._command_line_variables is None:
                command_line_vars: List[VariableDefinition] = []

                command_line_vars += [
                    CommandLineVariableDefinition(0, 0, 0, 0, "", f"${{{k}}}", None, has_value=True, value=v)
                    for k, v in {
                        **{k1: v1 for k1, v1 in (self.parent_protocol.profile.variables or {}).items()},
                        **self.config.robot.variables,
                    }.items()
                ]

                for variable_file in [
                    *(self.parent_protocol.profile.variable_files or []),
                    *self.config.robot.variable_files,
                ]:
                    name, args = split_args_from_name_or_path(str(variable_file))
                    try:
                        lib_doc = await self.get_libdoc_for_variables_import(
                            name.replace("\\", "\\\\"),
                            tuple(args),
                            str(self.folder.to_path()),
                            self,
                            resolve_variables=False,
                            resolve_command_line_vars=False,
                        )
                        if lib_doc is not None:
                            command_line_vars += [
                                CommandLineVariableDefinition(
                                    line_no=e.line_no,
                                    col_offset=e.col_offset,
                                    end_line_no=e.end_line_no,
                                    end_col_offset=e.end_col_offset,
                                    source=e.source,
                                    name=e.name,
                                    name_token=e.name_token,
                                    has_value=e.has_value,
                                    resolvable=e.resolvable,
                                    value=e.value,
                                    value_is_native=e.value_is_native,
                                )
                                for e in lib_doc.variables
                            ]

                            if lib_doc.errors:
                                # TODO add diagnostics
                                for error in lib_doc.errors:
                                    self._logger.error(
                                        lambda: f"{error.type_name}: {error.message} in {error.source}:{error.line_no}"
                                    )
                    except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                        raise
                    except BaseException as e:
                        # TODO add diagnostics
                        self._logger.exception(e)

                self._command_line_variables = command_line_vars

            return self._command_line_variables or []

    async def get_resolvable_command_line_variables(self) -> Dict[str, Any]:
        async with self._resolvable_command_line_variables_lock:
            if self._resolvable_command_line_variables is None:
                self._resolvable_command_line_variables = {
                    v.name: v.value for v in (await self.get_command_line_variables()) if v.has_value
                }

            return self._resolvable_command_line_variables

    @async_tasking_event
    async def libraries_changed(sender, libraries: List[LibraryDoc]) -> None:  # NOSONAR
        ...

    @async_tasking_event
    async def resources_changed(sender, resources: List[LibraryDoc]) -> None:  # NOSONAR
        ...

    @async_tasking_event
    async def variables_changed(sender, variables: List[LibraryDoc]) -> None:  # NOSONAR
        ...

    @async_tasking_event
    async def imports_changed(sender, uri: DocumentUri) -> None:  # NOSONAR
        ...

    def _do_imports_changed(self, sender: Any, uri: DocumentUri) -> None:  # NOSONAR
        create_sub_task(self.imports_changed(self, uri), loop=self.parent_protocol.diagnostics.diagnostics_loop)

    @language_id("robotframework")
    def resource_document_changed(self, sender: Any, document: TextDocument) -> None:
        create_sub_task(
            self.__resource_document_changed(document), loop=self.parent_protocol.diagnostics.diagnostics_loop
        )

    async def __resource_document_changed(self, document: TextDocument) -> None:
        resource_changed: List[LibraryDoc] = []

        async with self._resources_lock:
            for r_entry in self._resources.values():
                lib_doc: Optional[LibraryDoc] = None
                try:
                    if not await r_entry.is_valid():
                        continue

                    uri = (await r_entry.get_document()).uri
                    result = uri == document.uri
                    if result:
                        lib_doc = await r_entry.get_libdoc()
                        await r_entry.invalidate()

                except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
                    raise
                except BaseException:
                    result = True

                if result and lib_doc is not None:
                    resource_changed.append(lib_doc)

        if resource_changed:
            await self.resources_changed(self, resource_changed)

    @_logger.call
    async def did_change_watched_files(self, sender: Any, changes: List[FileEvent]) -> None:
        libraries_changed: List[Tuple[_LibrariesEntryKey, FileChangeType, Optional[LibraryDoc]]] = []
        resource_changed: List[Tuple[_ResourcesEntryKey, FileChangeType, Optional[LibraryDoc]]] = []
        variables_changed: List[Tuple[_VariablesEntryKey, FileChangeType, Optional[LibraryDoc]]] = []

        lib_doc: Optional[LibraryDoc]

        async with self._libaries_lock:
            for l_key, l_entry in self._libaries.items():
                lib_doc = None
                if await l_entry.is_valid():
                    lib_doc = await l_entry.get_libdoc()
                result = await l_entry.check_file_changed(changes)
                if result is not None:
                    libraries_changed.append((l_key, result, lib_doc))

        try:
            async with self._resources_lock:
                for r_key, r_entry in self._resources.items():
                    lib_doc = None
                    if await r_entry.is_valid():
                        lib_doc = await r_entry.get_libdoc()
                    result = await r_entry.check_file_changed(changes)
                    if result is not None:
                        resource_changed.append((r_key, result, lib_doc))
        except BaseException as e:
            self._logger.exception(e)
            raise

        async with self._variables_lock:
            for v_key, v_entry in self._variables.items():
                lib_doc = None
                if await v_entry.is_valid():
                    lib_doc = await v_entry.get_libdoc()
                result = await v_entry.check_file_changed(changes)
                if result is not None:
                    variables_changed.append((v_key, result, lib_doc))

        if libraries_changed:
            for l, t, _ in libraries_changed:
                if t == FileChangeType.DELETED:
                    self.__remove_library_entry(l, self._libaries[l], True)

            await self.libraries_changed(self, [v for (_, _, v) in libraries_changed if v is not None])

        if resource_changed:
            for r, t, _ in resource_changed:
                if t == FileChangeType.DELETED:
                    self.__remove_resource_entry(r, self._resources[r], True)

            await self.resources_changed(self, [v for (_, _, v) in resource_changed if v is not None])

        if variables_changed:
            for v, t, _ in variables_changed:
                if t == FileChangeType.DELETED:
                    self.__remove_variables_entry(v, self._variables[v], True)

            await self.variables_changed(self, [v for (_, _, v) in variables_changed if v is not None])

    def __remove_library_entry(self, entry_key: _LibrariesEntryKey, entry: _LibrariesEntry, now: bool = False) -> None:
        async def remove(k: _LibrariesEntryKey, e: _LibrariesEntry) -> None:
            try:
                if len(e.references) == 0 or now:
                    self._logger.debug(lambda: f"Remove Library Entry {k}")
                    async with self._libaries_lock:
                        if len(e.references) == 0:
                            e1 = self._libaries.get(k, None)
                            if e1 == e:
                                self._libaries.pop(k, None)

                                await e.invalidate()
                    self._logger.debug(lambda: f"Library Entry {k} removed")
            finally:
                await self._library_files_cache.clear()

        try:
            if asyncio.get_running_loop():
                create_sub_task(remove(entry_key, entry))
        except RuntimeError:
            pass

    def __remove_resource_entry(self, entry_key: _ResourcesEntryKey, entry: _ResourcesEntry, now: bool = False) -> None:
        async def remove(k: _ResourcesEntryKey, e: _ResourcesEntry) -> None:
            try:
                if len(e.references) == 0 or now:
                    self._logger.debug(lambda: f"Remove Resource Entry {k}")
                    async with self._resources_lock:
                        if len(e.references) == 0 or now:
                            e1 = self._resources.get(k, None)
                            if e1 == e:
                                self._resources.pop(k, None)

                                await e.invalidate()
                    self._logger.debug(lambda: f"Resource Entry {k} removed")
            finally:
                await self._resource_files_cache.clear()

        try:
            if asyncio.get_running_loop():
                create_sub_task(remove(entry_key, entry))

        except RuntimeError:
            pass

    def __remove_variables_entry(
        self, entry_key: _VariablesEntryKey, entry: _VariablesEntry, now: bool = False
    ) -> None:
        async def remove(k: _VariablesEntryKey, e: _VariablesEntry) -> None:
            try:
                if len(e.references) == 0 or now:
                    self._logger.debug(lambda: f"Remove Variables Entry {k}")
                    async with self._variables_lock:
                        if len(e.references) == 0:
                            e1 = self._variables.get(k, None)
                            if e1 == e:
                                self._variables.pop(k, None)

                                await e.invalidate()
                    self._logger.debug(lambda: f"Variables Entry {k} removed")
            finally:
                await self._variables_files_cache.clear()

        try:
            if asyncio.get_running_loop():
                create_sub_task(remove(entry_key, entry))
        except RuntimeError:
            pass

    async def get_library_meta(
        self,
        name: str,
        base_dir: str = ".",
        variables: Optional[Dict[str, Optional[Any]]] = None,
    ) -> Tuple[Optional[LibraryMetaData], str]:
        try:
            import_name = await self.find_library(
                name,
                base_dir=base_dir,
                variables=variables,
            )

            result: Optional[LibraryMetaData] = None
            module_spec: Optional[ModuleSpec] = None
            if is_library_by_path(import_name):
                if (p := Path(import_name)).exists():
                    result = LibraryMetaData(__version__, p.stem, None, import_name, None, True)
            else:
                module_spec = get_module_spec(import_name)
                if module_spec is not None and module_spec.origin is not None:
                    result = LibraryMetaData(
                        __version__,
                        module_spec.name,
                        module_spec.member_name,
                        module_spec.origin,
                        module_spec.submodule_search_locations,
                        False,
                    )

            if result is not None:
                if any(
                    (p.matches(result.name) if result.name is not None else False)
                    or (p.matches(result.origin) if result.origin is not None else False)
                    for p in self.ignored_libraries_patters
                ):
                    self._logger.debug(
                        lambda: f"Ignore library {result.name or '' if result is not None else ''}"
                        f" {result.origin or '' if result is not None else ''} for caching."
                    )
                    return None, import_name

                if result.origin is not None:
                    result.mtimes = {result.origin: Path(result.origin).stat().st_mtime_ns}

                if result.submodule_search_locations:
                    if result.mtimes is None:
                        result.mtimes = {}
                    result.mtimes.update(
                        {
                            str(f): f.stat().st_mtime_ns
                            for f in itertools.chain(
                                *(iter_files(loc, "**/*.py") for loc in result.submodule_search_locations)
                            )
                        }
                    )

            return result, import_name
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException:
            pass

        return None, import_name

    async def get_variables_meta(
        self,
        name: str,
        base_dir: str = ".",
        variables: Optional[Dict[str, Optional[Any]]] = None,
        resolve_variables: bool = True,
        resolve_command_line_vars: bool = True,
    ) -> Tuple[Optional[LibraryMetaData], str]:
        try:
            import_name = await self.find_variables(
                name,
                base_dir=base_dir,
                variables=variables,
                resolve_variables=resolve_variables,
                resolve_command_line_vars=resolve_command_line_vars,
            )

            result: Optional[LibraryMetaData] = None
            module_spec: Optional[ModuleSpec] = None
            if is_variables_by_path(import_name):
                if (p := Path(import_name)).exists():
                    result = LibraryMetaData(__version__, p.stem, None, import_name, None, True)
            else:
                module_spec = get_module_spec(import_name)
                if module_spec is not None and module_spec.origin is not None:
                    result = LibraryMetaData(
                        __version__,
                        module_spec.name,
                        module_spec.member_name,
                        module_spec.origin,
                        module_spec.submodule_search_locations,
                        False,
                    )

            if result is not None:
                if any(
                    (p.matches(result.name) if result.name is not None else False)
                    or (p.matches(result.origin) if result.origin is not None else False)
                    for p in self.ignored_variables_patters
                ):
                    self._logger.debug(
                        lambda: f"Ignore Variables {result.name or '' if result is not None else ''}"
                        f" {result.origin or '' if result is not None else ''} for caching."
                    )
                    return None, import_name

                if result.origin is not None:
                    result.mtimes = {result.origin: Path(result.origin).stat().st_mtime_ns}

                if result.submodule_search_locations:
                    if result.mtimes is None:
                        result.mtimes = {}
                    result.mtimes.update(
                        {
                            str(f): f.stat().st_mtime_ns
                            for f in itertools.chain(
                                *(iter_files(loc, "**/*.py") for loc in result.submodule_search_locations)
                            )
                        }
                    )

            return result, import_name
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException:
            pass

        return None, name

    async def find_library(self, name: str, base_dir: str, variables: Optional[Dict[str, Any]] = None) -> str:
        return await self._library_files_cache.get(self._find_library, name, base_dir, variables)

    async def _find_library(self, name: str, base_dir: str, variables: Optional[Dict[str, Any]] = None) -> str:
        from robot.libraries import STDLIBS
        from robot.variables.search import contains_variable

        if contains_variable(name, "$@&%"):
            return find_library(
                name,
                str(self.folder.to_path()),
                base_dir,
                await self.get_resolvable_command_line_variables(),
                variables,
            )

        if name in STDLIBS:
            result = ROBOT_LIBRARY_PACKAGE + "." + name
        else:
            result = name

        if is_library_by_path(result):
            return find_file_ex(result, base_dir, "Library")

        return result

    async def find_resource(
        self, name: str, base_dir: str, file_type: str = "Resource", variables: Optional[Dict[str, Any]] = None
    ) -> str:
        return await self._resource_files_cache.get(self.__find_resource, name, base_dir, file_type, variables)

    @_logger.call
    async def __find_resource(
        self, name: str, base_dir: str, file_type: str = "Resource", variables: Optional[Dict[str, Any]] = None
    ) -> str:
        from robot.variables.search import contains_variable

        if contains_variable(name, "$@&%"):
            return find_file(
                name,
                str(self.folder.to_path()),
                base_dir,
                await self.get_resolvable_command_line_variables(),
                variables,
                file_type,
            )

        return str(find_file_ex(name, base_dir, file_type))

    async def find_variables(
        self,
        name: str,
        base_dir: str,
        variables: Optional[Dict[str, Any]] = None,
        resolve_variables: bool = True,
        resolve_command_line_vars: bool = True,
    ) -> str:
        return await self._variables_files_cache.get(
            self.__find_variables, name, base_dir, variables, resolve_command_line_vars
        )

    @_logger.call
    async def __find_variables(
        self,
        name: str,
        base_dir: str,
        variables: Optional[Dict[str, Any]] = None,
        resolve_variables: bool = True,
        resolve_command_line_vars: bool = True,
    ) -> str:
        from robot.variables.search import contains_variable

        if resolve_variables and contains_variable(name, "$@&%"):
            return find_variables(
                name,
                str(self.folder.to_path()),
                base_dir,
                await self.get_resolvable_command_line_variables() if resolve_command_line_vars else None,
                variables,
            )

        if get_robot_version() >= (5, 0):
            if is_variables_by_path(name):
                return str(find_file_ex(name, base_dir, "Variables"))

            return name

        return str(find_file_ex(name, base_dir, "Variables"))

    @_logger.call
    async def get_libdoc_for_library_import(
        self,
        name: str,
        args: Tuple[Any, ...],
        base_dir: str,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> LibraryDoc:
        source = await self.find_library(
            name,
            base_dir,
            variables,
        )

        async def _get_libdoc(name: str, args: Tuple[Any, ...], working_dir: str, base_dir: str) -> LibraryDoc:
            meta, source = await self.get_library_meta(
                name,
                base_dir,
                variables,
            )

            self._logger.debug(lambda: f"Load Library {source}{args!r}")

            if meta is not None:
                meta_file = Path(self.lib_doc_cache_path, meta.filepath_base + ".meta.json")
                if meta_file.exists():
                    try:
                        spec_path = None
                        try:
                            saved_meta = from_json(meta_file.read_text("utf-8"), LibraryMetaData)
                            if saved_meta == meta:
                                spec_path = Path(self.lib_doc_cache_path, meta.filepath_base + ".spec.json")
                                return from_json(
                                    spec_path.read_text("utf-8"),
                                    LibraryDoc,
                                )
                        except (SystemExit, KeyboardInterrupt):
                            raise
                        except BaseException as e:
                            raise RuntimeError(
                                f"Failed to load library meta data for library {name} from {spec_path}"
                            ) from e
                    except (SystemExit, KeyboardInterrupt):
                        raise
                    except BaseException as e:
                        self._logger.exception(e)

            executor = ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"))
            try:
                result = executor.submit(
                    get_library_doc,
                    name,
                    args,
                    working_dir,
                    base_dir,
                    await self.get_resolvable_command_line_variables(),
                    variables,
                ).result(LOAD_LIBRARY_TIME_OUT)
                # result = await asyncio.wait_for(
                #     asyncio.get_running_loop().run_in_executor(
                #         executor,
                #         get_library_doc,
                #         name,
                #         args,
                #         working_dir,
                #         base_dir,
                #         await self.get_resolvable_command_line_variables(),
                #         variables,
                #     ),
                #     LOAD_LIBRARY_TIME_OUT,
                # )
            except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                raise
            except BaseException as e:
                self._logger.exception(e)
                raise
            finally:
                executor.shutdown(wait=True)

            if result.stdout:
                self._logger.warning(lambda: f"stdout captured at loading library {name}{args!r}:\n{result.stdout}")
            try:
                if meta is not None:
                    meta_file = Path(self.lib_doc_cache_path, meta.filepath_base + ".meta.json")
                    spec_file = Path(self.lib_doc_cache_path, meta.filepath_base + ".spec.json")
                    spec_file.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        spec_file.write_text(as_json(result), "utf-8")
                    except (SystemExit, KeyboardInterrupt):
                        raise
                    except BaseException as e:
                        raise RuntimeError(f"Cannot write spec file for library '{name}' to '{spec_file}'") from e

                    meta_file.write_text(as_json(meta), "utf-8")
                else:
                    self._logger.debug(lambda: f"Skip caching library {name}{args!r}")
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as e:
                self._logger.exception(e)

            return result

        resolved_args = resolve_args(
            args,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables(),
            variables,
        )
        entry_key = _LibrariesEntryKey(source, resolved_args)

        async with self._libaries_lock:
            if entry_key not in self._libaries:
                self._libaries[entry_key] = _LibrariesEntry(
                    self,
                    name,
                    args,
                    str(self.folder.to_path()),
                    base_dir,
                    _get_libdoc,
                    ignore_reference=sentinel is None,
                )

        entry = self._libaries[entry_key]

        if not entry.ignore_reference and sentinel is not None and sentinel not in entry.references:
            entry.references.add(sentinel)
            weakref.finalize(sentinel, self.__remove_library_entry, entry_key, entry)

        return await entry.get_libdoc()

    @_logger.call
    def get_libdoc_from_model(
        self,
        model: ast.AST,
        source: str,
        model_type: str = "RESOURCE",
        scope: str = "GLOBAL",
        append_model_errors: bool = True,
    ) -> LibraryDoc:
        return get_model_doc(
            model=model, source=source, model_type=model_type, scope=scope, append_model_errors=append_model_errors
        )

    @_logger.call
    async def get_libdoc_for_variables_import(
        self,
        name: str,
        args: Tuple[Any, ...],
        base_dir: str,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
        resolve_variables: bool = True,
        resolve_command_line_vars: bool = True,
    ) -> VariablesDoc:
        source = await self.find_variables(
            name,
            base_dir,
            variables,
            resolve_variables=resolve_variables,
            resolve_command_line_vars=resolve_command_line_vars,
        )

        async def _get_libdoc(name: str, args: Tuple[Any, ...], working_dir: str, base_dir: str) -> VariablesDoc:
            meta, source = await self.get_variables_meta(
                name,
                base_dir,
                variables,
                resolve_command_line_vars=resolve_command_line_vars,
            )

            self._logger.debug(lambda: f"Load variables {source}{args!r}")
            if meta is not None:
                meta_file = Path(self.variables_doc_cache_path, meta.filepath_base + ".meta.json")
                if meta_file.exists():
                    try:
                        spec_path = None
                        try:
                            saved_meta = from_json(meta_file.read_text("utf-8"), LibraryMetaData)
                            if saved_meta == meta:
                                spec_path = Path(self.variables_doc_cache_path, meta.filepath_base + ".spec.json")
                                return from_json(
                                    spec_path.read_text("utf-8"),
                                    VariablesDoc,
                                )
                        except (SystemExit, KeyboardInterrupt):
                            raise
                        except BaseException as e:
                            raise RuntimeError(
                                f"Failed to load library meta data for library {name} from {spec_path}"
                            ) from e
                    except (SystemExit, KeyboardInterrupt):
                        raise
                    except BaseException as e:
                        self._logger.exception(e)

            executor = ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"))
            try:
                result = await asyncio.wait_for(
                    asyncio.get_running_loop().run_in_executor(
                        executor,
                        get_variables_doc,
                        name,
                        args,
                        str(self.folder.to_path()),
                        base_dir,
                        await self.get_resolvable_command_line_variables() if resolve_command_line_vars else None,
                        variables,
                    ),
                    LOAD_LIBRARY_TIME_OUT,
                )
            except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
                raise
            except BaseException as e:
                self._logger.exception(e)
                raise
            finally:
                executor.shutdown(True)

            if result.stdout:
                self._logger.warning(lambda: f"stdout captured at loading variables {name}{args!r}:\n{result.stdout}")

            try:
                if meta is not None:
                    meta_file = Path(self.variables_doc_cache_path, meta.filepath_base + ".meta.json")
                    spec_file = Path(self.variables_doc_cache_path, meta.filepath_base + ".spec.json")
                    spec_file.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        spec_file.write_text(as_json(result), "utf-8")
                    except (SystemExit, KeyboardInterrupt):
                        raise
                    except BaseException as e:
                        raise RuntimeError(f"Cannot write spec file for variables '{name}' to '{spec_file}'") from e
                    meta_file.write_text(as_json(meta), "utf-8")
                else:
                    self._logger.debug(lambda: f"Skip caching variables {name}{args!r}")
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as e:
                self._logger.exception(e)

            return result

        resolved_args = resolve_args(
            args,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables() if resolve_command_line_vars else None,
            variables,
        )
        entry_key = _VariablesEntryKey(source, resolved_args)

        async with self._variables_lock:
            if entry_key not in self._variables:
                self._variables[entry_key] = _VariablesEntry(
                    name, resolved_args, str(self.folder.to_path()), base_dir, self, _get_libdoc
                )

        entry = self._variables[entry_key]

        if sentinel is not None and sentinel not in entry.references:
            entry.references.add(sentinel)
            weakref.finalize(sentinel, self.__remove_variables_entry, entry_key, entry)

        return await entry.get_libdoc()

    @_logger.call
    async def _get_entry_for_resource_import(
        self, name: str, base_dir: str, sentinel: Any = None, variables: Optional[Dict[str, Any]] = None
    ) -> _ResourcesEntry:
        source = await self.find_resource(name, base_dir, variables=variables)

        async def _get_document() -> TextDocument:
            self._logger.debug(lambda: f"Load resource {name} from source {source}")

            source_path = Path(source).resolve()
            extension = source_path.suffix
            if extension.lower() not in RESOURCE_EXTENSIONS:
                raise ImportError(
                    f"Invalid resource file extension '{extension}'. "
                    f"Supported extensions are {', '.join(repr(s) for s in RESOURCE_EXTENSIONS)}."
                )

            return self.parent_protocol.documents.get_or_open_document(source_path)

        entry_key = _ResourcesEntryKey(source)

        async with self._resources_lock:
            if entry_key not in self._resources:
                self._resources[entry_key] = _ResourcesEntry(name, self, _get_document)

        entry = self._resources[entry_key]

        if sentinel is not None and sentinel not in entry.references:
            entry.references.add(sentinel)
            weakref.finalize(sentinel, self.__remove_resource_entry, entry_key, entry)

        return entry

    async def get_namespace_and_libdoc_for_resource_import(
        self,
        name: str,
        base_dir: str,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Tuple["Namespace", LibraryDoc]:
        entry = await self._get_entry_for_resource_import(name, base_dir, sentinel, variables)

        return await entry.get_namespace(), await entry.get_libdoc()

    async def get_namespace_for_resource_import(
        self,
        name: str,
        base_dir: str,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> "Namespace":
        entry = await self._get_entry_for_resource_import(name, base_dir, sentinel, variables)

        return await entry.get_namespace()

    async def get_libdoc_for_resource_import(
        self, name: str, base_dir: str, sentinel: Any = None, variables: Optional[Dict[str, Any]] = None
    ) -> LibraryDoc:
        entry = await self._get_entry_for_resource_import(name, base_dir, sentinel, variables)

        return await entry.get_libdoc()

    async def complete_library_import(
        self, name: Optional[str], base_dir: str = ".", variables: Optional[Dict[str, Any]] = None
    ) -> List[CompleteResult]:
        return complete_library_import(
            name,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables(),
            variables,
        )

    async def complete_resource_import(
        self, name: Optional[str], base_dir: str = ".", variables: Optional[Dict[str, Any]] = None
    ) -> Optional[List[CompleteResult]]:
        return complete_resource_import(
            name,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables(),
            variables,
        )

    async def complete_variables_import(
        self, name: Optional[str], base_dir: str = ".", variables: Optional[Dict[str, Any]] = None
    ) -> Optional[List[CompleteResult]]:
        return complete_variables_import(
            name,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables(),
            variables,
        )

    async def resolve_variable(self, name: str, base_dir: str = ".", variables: Optional[Dict[str, Any]] = None) -> Any:
        return resolve_variable(
            name,
            str(self.folder.to_path()),
            base_dir,
            await self.get_resolvable_command_line_variables(),
            variables,
        )
