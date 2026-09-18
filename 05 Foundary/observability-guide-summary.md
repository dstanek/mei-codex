---
type: zettel
created: 2026-07-19 09:14
tags: []
---

# A Guide to Observability

The image explains six foundational observability concepts using a failed checkout request as the running example.

## 1. One Event, Three Views

A single application event can appear in three telemetry forms:

- **Log entry:** records the event and its attributes, such as timestamp, service, endpoint, user, status code, and latency.
- **Metric increment:** updates an aggregate counter, such as `checkout_failed_total`.
- **Trace span:** represents the individual operation within a distributed request, including duration and status.

Each view serves a different diagnostic purpose:

- Logs provide detailed context.
- Metrics reveal trends and aggregate behavior.
- Traces show the path and timing of individual requests.

## 2. Structured vs. Unstructured Logging

### Unstructured logging

Free-form log messages are easy for humans to read but difficult for systems to analyze.

Problems include:

- Fields are not directly queryable.
- Aggregation requires parsing or regular expressions.
- Filtering depends on matching text fragments.
- Metrics are difficult to derive reliably.

### Structured logging

Structured logs store values in named fields, commonly as JSON:

```json
{
  "timestamp": "2024-01-15T14:23:01.842Z",
  "level": "ERROR",
  "service": "payments",
  "endpoint": "/checkout",
  "user_id": 4127,
  "latency_ms": 380,
  "status_code": 500
}
```

Benefits include:

- Direct field-based queries
- Native aggregation
- Reliable filtering
- Easy metric derivation

The core principle is that **structure turns text into queryable data**.

## 3. Cardinality Explosion

Metric dimensions create a separate time series for every unique combination of label values.

Example progression:

| Dimensions | Approximate time series |
|---|---:|
| `status_code` | 6 |
| `status_code`, `endpoint` | 300 |
| `status_code`, `endpoint`, `region` | 3,000 |
| Add `user_id` | 3,000,000,000 |

High-cardinality fields such as user IDs, request IDs, email addresses, or session IDs can make metrics prohibitively expensive.

The practical lesson is:

- Use bounded dimensions such as status code, region, or endpoint in metrics.
- Keep high-cardinality identifiers in logs and traces.

## 4. Correlation ID Journey

A distributed request may travel through several services:

```text
API Gateway
    ↓
Auth Service
    ↓
Payment Service
    ↓
Database
```

A shared trace or correlation ID propagates with the request and appears in the telemetry produced by every service.

This allows engineers to connect otherwise isolated events, such as:

- Request received
- Authentication succeeded
- Payment failed
- Database query timed out

Without a correlation ID, these records look unrelated. With one, the complete request journey can be reconstructed.

## 5. Head vs. Tail Sampling

Sampling controls which traces are retained.

### Head sampling

The decision is made when the request begins.

```text
Request → Sampling decision → Services execute
```

Advantages:

- Cheap and simple
- Consistent sampling decision across services

Disadvantage:

- The system cannot know whether the request will eventually fail or become slow.
- Interesting traces may be discarded.

### Tail sampling

The decision is made after the trace completes.

```text
Request → Services execute → Buffer trace → Sampling decision
```

Advantages:

- Can retain all failed or slow requests
- Usually produces a better signal-to-noise ratio

Disadvantages:

- Requires buffering
- Consumes more runtime resources
- Is operationally more complex

## 6. Symptom vs. Cause Alerting

A user-facing symptom such as:

> Checkout latency exceeds one second for more than 5% of requests.

may be caused by many underlying conditions:

- Slow database queries
- Slow downstream services
- Cache eviction storms
- Garbage-collection pauses
- Network congestion
- Retry-loop amplification

The image recommends alerting primarily on the **user-visible symptom**, because it captures failures regardless of their root cause.

Cause-level alerts can still be useful, but they should generally support diagnosis rather than replace symptom-based alerts.

## Core Takeaways

1. Logs, metrics, and traces are complementary representations of the same underlying events.
2. Structured logs are substantially easier to search, aggregate, and transform.
3. Metric labels must be carefully controlled to avoid cardinality explosion.
4. Correlation IDs connect telemetry across distributed services.
5. Tail sampling captures important traces more accurately but costs more to operate.
6. Alerts should usually be based on user impact, with lower-level signals used to identify the cause.

---

## Links

- [[AI]]
