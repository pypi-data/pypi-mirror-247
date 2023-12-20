from logging import getLogger
from typing import Optional, Callable

from opentelemetry.context.context import Context
from opentelemetry.sdk.trace import ReadableSpan, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter

from helios.base.tracing.suppress_tracing import SuppressTracing

_LOG = getLogger(__name__)


class HookedBatchSpanProcessorConfig(object):

    def __init__(self,
                 on_start_hook: Optional[Callable[[Span, Optional[Context]], None]] = None,
                 on_end_hook: Optional[Callable[[ReadableSpan], None]] = None,
                 flush_on_end: Optional[Callable[[ReadableSpan], bool]] = False,
                 max_queue_size: Optional[int] = None):
        self.on_start_hook = on_start_hook
        self.on_end_hook = on_end_hook

        # provide a predicate which will be tested on Span End.
        # If it evaluates to True, processor will trigger a flush call.
        self.flush_on_end = flush_on_end
        self.max_queue_size = max_queue_size


class HookedBatchSpanProcessor(BatchSpanProcessor):

    def __init__(self, exporter: SpanExporter,
                 config: Optional[HookedBatchSpanProcessorConfig] = None):
        super().__init__(exporter, max_queue_size=(config.max_queue_size if config else None))
        self.on_start_hook = config.on_start_hook if config else None
        self.on_end_hook = config.on_end_hook if config else None
        self.flush_on_end = config.flush_on_end if config else None

    def on_start(self, span: Span,
                 parent_context: Optional[Context] = None) -> None:
        if SuppressTracing.is_tracing_suppressed():
            return

        super().on_start(span)
        if self.on_start_hook:
            try:
                self.on_start_hook(span, parent_context)
            except Exception as err:
                _LOG.error('error running onStart hook', err)

    def on_end(self, span: ReadableSpan) -> None:
        if SuppressTracing.is_tracing_suppressed():
            return

        if self.on_end_hook:
            try:
                self.on_end_hook(span)
            except Exception as err:
                _LOG.error('error running onEnd hook', err)
        super().on_end(span)

        if self.flush_on_end:
            try:
                if self.flush_on_end(span):
                    self.force_flush()
            except Exception as err:
                _LOG.error('Error evaluating flushOnSpanEnd predicate', err)
