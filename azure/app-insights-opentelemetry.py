from azure_monitor import AzureMonitorMetricsExporter
from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider, ValueObserver, ValueRecorder
from opentelemetry.sdk.metrics.export.controller import PushController
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--instrumentation_key', help='Instrumentation Key')
    args = parser.parse_args()

    metrics.set_meter_provider(MeterProvider())
    meter = metrics.get_meter(__name__)
    exporter = AzureMonitorMetricsExporter(
        connection_string='InstrumentationKey=' + args.instrumentation_key
    )
    controller = PushController(meter, exporter, 5)
    job_duration = meter.create_metric(
        name="job_duration",
        description="job_duration",
        unit="1",
        value_type=int,
        metric_type=ValueRecorder,
        label_keys=("environment", "task")
    )

    testing_labels = {"environment": "testing", "task":"preprocess"}
    job_duration.record(25, testing_labels)
    testing_labels = {"environment": "testing", "task":"process"}
    job_duration.record(35, testing_labels)
    time.sleep(10)  # give push_controller time to push metrics