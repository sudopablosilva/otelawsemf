import os
import time
import random
from typing import Iterable
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry import metrics

# Get OTLP endpoint from environment variable
endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")

# Set up MeterProvider and OTLP Metric Exporter
resource = Resource(attributes={"service.name": "test-service"})
metric_exporter = OTLPMetricExporter(endpoint=endpoint, insecure=True)

# Set export interval to 3 seconds (3000 milliseconds)
metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=3000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Create meter and a counter
meter = metrics.get_meter("test-meter")
counter = meter.create_counter(
    "test_requests_counter",
    unit="1",
    description="Counts requests",
)

# Define possible environment values
environments = ["development", "staging", "production"]

# Register the asynchronous gauge with the callback function
gauge = meter.create_gauge(
    "requestdurationms",
    unit="Milliseconds",  # Set unit to 'Milliseconds' for CloudWatch compatibility
    description="Request Duration in milliseconds")

histogram = meter.create_histogram(
    "myhistogramms",
    unit="Milliseconds",  # Set unit to 'Milliseconds' for CloudWatch compatibility
    description="Histogram of Request Duration in milliseconds")

histogram2 = meter.create_histogram(
    "my.histogram.ms",
    unit="Milliseconds",  # Set unit to 'Milliseconds' for CloudWatch compatibility
    description="Histogram of Request Duration in milliseconds")


# Loop to continuously send metrics every 3 seconds with random environment and duration
while True:
    random_environment = random.choice(environments)
    counter.add(1, {"environment": random_environment})
    gauge.set(random.randint(200, 1400), {"environment": random_environment})  # Set gauge as integer
    histogram.record(random.randint(200, 1400), {"environment": random_environment})
    histogram2.record(random.randint(200, 1400), {"environment": random_environment})
    # print("Counter metric sent!")
    # print("Gauge metric sent!")
    # print("Histogram metric sent!")
    # print("Histogram2 metric sent!")
    time.sleep(5)
