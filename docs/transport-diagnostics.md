# Transport diagnostics

The confirmed defect was loss of failure information, not a proven Jev outage.
An old S20 receipt stopped after 30.056 seconds with a generic JevError. That is
consistent with the 30-second socket timeout but cannot identify the cause or
phase retrospectively. The unchanged failure is in the
[historical report](../evals/TRIAGE_SMOKE_TEST.md).

The CLI now returns safe JSON on stderr, exit 1, with `error_kind` (`timeout`,
`dns`, `tls`, `connection`, `http`), `phase` (`connect_or_headers` or
`response_body`), and `http_status` when received. These extra fields describe
transport errors; validation/setup errors may contain only `error`.
It never emits raw exceptions, keys, request headers or provider error bodies.

```json
{"error":"OpenRouter timeout failure during response_body; no automatic retry was made","error_kind":"timeout","phase":"response_body","http_status":200}
```

This example is from the local failure path, not the original online incident.
A timeout before headers cannot distinguish connection delay from slow upstream
computation. `--timeout` is a socket-operation timeout, NOT a total job deadline;
a peer that slowly streams bytes can keep a call active longer. Host schedulers
need their own overall job limits. There are no automatic retries or redirects.

## Validation

- Regression first failed for lost diagnostic fields, then passed.
- A local server independently stalled before headers and after HTTP 200; both
  timeout paths retained the correct phase and status.
- Injected DNS, TLS and connection errors retain categories without sensitive text.
- Additional field/error audit reproduced an uncaught truncated-body exception;
  HTTP protocol/body truncation now produces safe JSON instead of a traceback.
- Duplicate JSON fields are rejected instead of silently taking the last value.
- Authorized replay of the exact S20 request returned billing in about 0.321 s;
  the S10 control returned bug in about 0.329 s. Both used the same 30-second
  timeout, no retries. This does not establish what happened in the original run.

[Actual replay requests and responses](../evals/results/followups-2026-09-21/)
are separate from the original receipts. A repeatable service failure would need
fresh captured diagnostics and potentially provider-side tracing, not just a
larger timeout or repeated calls until one succeeds.

## Review follow-up: overflow numeric fields

The Spec review reproduced a P2 defect: JSON `1e999` became Python infinity,
which made strict receipt serialization fail and lose the report. The runtime
now rejects overflow floats at the JSON parse boundary, before either provider
response can enter the ledger. A fake HTTP response regression covers both arms,
retains both in-flight error receipts with unknown costs, and writes a review
report. Literal NaN/Infinity and duplicate object fields are also rejected.
The bad provider body is not logged; the safe error receipt is preserved.
