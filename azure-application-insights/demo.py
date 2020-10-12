from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.status import Status
from opencensus.trace.span_context import SpanContext
from opencensus.trace import config_integration
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

import time
import logging
from random import randrange


# TODO: replace the all-zero GUID with your instrumentation key.

RANGE = 10
FAILURE_NUMBER = 5
APP='edgelhd'
properties = {'custom_dimensions': {'job_id': '100', 'appName':APP, 'nodeId':'123'}}
tracer = Tracer(
    exporter=AzureExporter(),
    sampler=AlwaysOnSampler(),
    span_context=SpanContext(),
)
logger = logging.getLogger(APP)
logger.setLevel(logging.INFO)
logger.addHandler(AzureLogHandler())

def something_happen(span, error=False):
    time.sleep(randrange(RANGE))
    if error:
        # Cause an exception
        try:
            1/0
        except Exception as e:
            logger.exception(str(e), exc_info=True, extra=properties)


def run(job_id):

    with tracer.span(name=APP) as span:
        with span.span('load_data') as s:
            something_happen(s, True)
            logger.info('Loaded 100 samples.', extra=properties)
        with span.span('preprocess'):
            something_happen(s)
        with span.span('process'):
            something_happen(s)
        with span.span('postprocess'):
            something_happen(s)
            logger.info('Processed 100 samples.', extra=properties)


if __name__ == "__main__":
    for i in range(2, 10):
        run(i+1)