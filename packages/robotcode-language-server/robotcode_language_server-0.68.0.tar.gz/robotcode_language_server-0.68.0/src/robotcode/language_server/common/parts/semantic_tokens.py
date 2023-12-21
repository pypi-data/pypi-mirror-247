from __future__ import annotations

from asyncio import CancelledError
from enum import Enum
from typing import TYPE_CHECKING, Any, Final, List, Union

from robotcode.core.async_tools import async_tasking_event, threaded
from robotcode.core.lsp.types import (
    Range,
    SemanticTokenModifiers,
    SemanticTokens,
    SemanticTokensDelta,
    SemanticTokensDeltaParams,
    SemanticTokensDeltaPartialResult,
    SemanticTokensLegend,
    SemanticTokensOptions,
    SemanticTokensOptionsFullType1,
    SemanticTokensParams,
    SemanticTokensPartialResult,
    SemanticTokensRangeParams,
    SemanticTokenTypes,
    ServerCapabilities,
    TextDocumentIdentifier,
)
from robotcode.core.utils.logging import LoggingDescriptor
from robotcode.jsonrpc2.protocol import rpc_method
from robotcode.language_server.common.decorators import language_id_filter
from robotcode.language_server.common.has_extend_capabilities import (
    HasExtendCapabilities,
)
from robotcode.language_server.common.text_document import TextDocument

if TYPE_CHECKING:
    from robotcode.language_server.common.protocol import LanguageServerProtocol

from .protocol_part import LanguageServerProtocolPart


class SemanticTokensProtocolPart(LanguageServerProtocolPart, HasExtendCapabilities):
    _logger: Final = LoggingDescriptor()

    def __init__(self, parent: LanguageServerProtocol) -> None:
        super().__init__(parent)
        self.token_types: List[Enum] = list(SemanticTokenTypes)
        self.token_modifiers: List[Enum] = list(SemanticTokenModifiers)

    @async_tasking_event
    async def collect_full(
        sender, document: TextDocument, **kwargs: Any  # NOSONAR
    ) -> Union[SemanticTokens, SemanticTokensPartialResult, None]:
        ...

    @async_tasking_event
    async def collect_full_delta(
        sender,
        document: TextDocument,
        previous_result_id: str,
        **kwargs: Any,  # NOSONAR
    ) -> Union[SemanticTokens, SemanticTokensDelta, SemanticTokensDeltaPartialResult, None]:
        ...

    @async_tasking_event
    async def collect_range(
        sender, document: TextDocument, range: Range, **kwargs: Any  # NOSONAR
    ) -> Union[SemanticTokens, SemanticTokensPartialResult, None]:
        ...

    def extend_capabilities(self, capabilities: ServerCapabilities) -> None:
        if len(self.collect_full) or len(self.collect_range):
            capabilities.semantic_tokens_provider = SemanticTokensOptions(
                legend=SemanticTokensLegend(
                    token_types=[e.value for e in self.token_types],
                    token_modifiers=[e.value for e in self.token_modifiers],
                ),
                full=SemanticTokensOptionsFullType1(delta=True if len(self.collect_full_delta) else None)
                if len(self.collect_full) and len(self.collect_full_delta)
                else True
                if len(self.collect_full)
                else None,
                range=True if len(self.collect_range) else None,
            )

    @rpc_method(name="textDocument/semanticTokens/full", param_type=SemanticTokensParams)
    @threaded()
    async def _text_document_semantic_tokens_full(
        self, text_document: TextDocumentIdentifier, *args: Any, **kwargs: Any
    ) -> Union[SemanticTokens, SemanticTokensPartialResult, None]:
        results: List[Union[SemanticTokens, SemanticTokensPartialResult]] = []

        document = self.parent.documents.get(text_document.uri)
        if document is None:
            return None

        for result in await self.collect_full(
            self,
            document,
            callback_filter=language_id_filter(document),
            **kwargs,
        ):
            if isinstance(result, BaseException):
                if not isinstance(result, CancelledError):
                    self._logger.exception(result, exc_info=result)
            else:
                if result is not None:
                    results.append(result)

        # only the last is returned
        if len(results) > 0:
            return results[-1]

        return None

    @rpc_method(
        name="textDocument/semanticTokens/full/delta",
        param_type=SemanticTokensDeltaParams,
    )
    @threaded()
    async def _text_document_semantic_tokens_full_delta(
        self,
        text_document: TextDocumentIdentifier,
        previous_result_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> Union[SemanticTokens, SemanticTokensDelta, SemanticTokensDeltaPartialResult, None]:
        results: List[Union[SemanticTokens, SemanticTokensDelta, SemanticTokensDeltaPartialResult]] = []

        document = self.parent.documents.get(text_document.uri)
        if document is None:
            return None

        for result in await self.collect_full_delta(
            self,
            document,
            previous_result_id,
            callback_filter=language_id_filter(document),
            **kwargs,
        ):
            if isinstance(result, BaseException):
                if not isinstance(result, CancelledError):
                    self._logger.exception(result, exc_info=result)
            else:
                if result is not None:
                    results.append(result)

        # only the last is returned
        if len(results) > 0:
            return results[-1]

        return None

    @rpc_method(name="textDocument/semanticTokens/range", param_type=SemanticTokensRangeParams)
    @threaded()
    async def _text_document_semantic_tokens_range(
        self,
        text_document: TextDocumentIdentifier,
        range: Range,
        *args: Any,
        **kwargs: Any,
    ) -> Union[SemanticTokens, SemanticTokensPartialResult, None]:
        results: List[Union[SemanticTokens, SemanticTokensPartialResult]] = []

        document = self.parent.documents.get(text_document.uri)
        if document is None:
            return None

        for result in await self.collect_range(
            self,
            document,
            range,
            callback_filter=language_id_filter(document),
            **kwargs,
        ):
            if isinstance(result, BaseException):
                if not isinstance(result, CancelledError):
                    self._logger.exception(result, exc_info=result)
            else:
                if result is not None:
                    results.append(result)

        # only the last is returned
        if len(results) > 0:
            return results[-1]

        return None

    async def refresh(self) -> None:
        if (
            self.parent.client_capabilities is not None
            and self.parent.client_capabilities.workspace is not None
            and self.parent.client_capabilities.workspace.semantic_tokens is not None
            and self.parent.client_capabilities.workspace.semantic_tokens.refresh_support
        ):
            await self.parent.send_request_async("workspace/semanticTokens/refresh")
