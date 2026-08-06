from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "api_requests_total", "Total API requests", ["method", "endpoint"]
)


REQUEST_TIME = Histogram(
    "api_request_duration_seconds", "API request duration", ["endpoint"]
)
