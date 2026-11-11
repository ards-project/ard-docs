# Observability

Distributed tracing helps operators connect an ARD discovery request to the
registries it queried, the consumer's verification and selection decisions, and
the eventual invocation of a resource. It can also reveal where that connection
is lost across service or protocol boundaries.

This guide expands on the [ARD specification's observability guidance](spec.md#55-observability-informative).
It is informative: tracing is optional and adds no conformance requirements,
entry fields, or Registry API response fields.

## Follow discovery through invocation

Instrument the operations that answer these questions:

- Which Registry contributed the selected resource?
- What trust-evidence checks and policy decisions preceded invocation?
- Was a denied candidate blocked at the invocation boundary?
- Did the provider accept the request, and was its outcome separately verified?

Keep discovery, verification, selection, admission, invocation, provider
acceptance, and outcome verification distinguishable. Discovery and selection do
not grant invocation authority. A successful provider response does not, by
itself, establish that the requested outcome occurred.

Use applicable [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
for span names and attributes. This guide does not define an ARD telemetry schema
or require a particular sequence of verification and policy checks.

## Propagate context across boundaries

For Registry HTTP calls, use [W3C Trace Context](https://www.w3.org/TR/trace-context/)
with an OpenTelemetry propagator. Extract and validate inbound context, apply
local acceptance policy, and start the receiving operation's span. On outbound
calls, inject the active context rather than copying the incoming header
unchanged. Tracing instrumentation creates spans and identifiers; propagators
extract and inject context.

| Boundary | Correlation approach |
| --- | --- |
| Client to Registry | Propagate context on `POST /search`, `POST /explore`, and `GET /agents`. |
| Automatic federation | Create client spans for outbound Registry calls and inject their context. |
| Referrals | Correlate each client follow-up call with the discovery operation that returned the referral. |
| Consumer verification and selection | Record checks and decisions with privacy-safe references to the candidate and contributing Registry. |
| Inline native-protocol invocation | Continue context using the selected protocol's supported mechanism, where local trust policy permits. |
| Cached discovery or independent execution | Consider a new trace with a [span link](https://opentelemetry.io/docs/concepts/signals/traces/#span-links) to the earlier discovery context. |

Keep any discovery span context needed for later links separate from cached ARD
entries. If a protocol cannot carry context, record the handoff boundary and use
local correlation. Do not insert trace identifiers into entries or modify
discovered artifacts to preserve a trace.

## Protect context and telemetry

Treat external registries and resource endpoints as trust boundaries. Valid
trace-context syntax does not make the sender trustworthy.

- Apply local policies for accepting external context, starting new traces, and
  sampling. Caller-supplied trace IDs and sampling flags do not override those
  policies.
- Allowlist or omit `tracestate` and baggage before crossing boundaries. Do not
  forward credentials, internal tenant details, or caller metadata by default.
- Minimize query text, resource URLs, identifiers, and trust-evidence contents
  in exported telemetry. Apply redaction, access controls, and retention limits
  appropriate to the deployment.

Trace context is operational metadata, not identity evidence, an authorization
grant, a `trustManifest` claim, or an input to relevance `score`. A trace records
what the instrumentation observed; it does not establish that a policy decision
was valid. Sharing a trace ID does not make spans signed attestations or
tamper-evident audit records. Apply the W3C specification's security and privacy
guidance when propagating context and handling telemetry.

## Check correlation and enforcement separately

Test more than whether operations appear under one trace ID. Check that outbound
spans have the intended parents and that independent work links to the correct
discovery context. Exercise federation, referral follow-up, cached results, and
native-protocol handoffs used by the deployment.

For denied candidates, pair decision telemetry with enforcement assertions or
downstream request counts. Missing invocation spans are not proof that no
invocation occurred: sampling, failed export, and broken propagation can all
leave gaps. Likewise, record provider acceptance separately from any independent
verification of the requested outcome.

## Prototype: Agent Gateway policy instrumentation

The [ARD Lifecycle Instrumentation prototype](https://github.com/91pavan/ard-lifecycle-instrumentation)
demonstrates tracing of MCP tool discovery and admission policy using Agent
Gateway, an external policy processor, a synthetic MCP skill registry, an
OpenTelemetry Collector, and Jaeger. It illustrates instrumentation relevant to
ARD consumers, rather than an end-to-end ARD Registry discovery flow. These
observations refer to
[revision `d3dfa34`](https://github.com/91pavan/ard-lifecycle-instrumentation/tree/d3dfa34a2be2d02880886ff18d135b72bd12b92d).

Agent Gateway is the MCP host and enforcement point. Its `mcpGuardrails`
configuration evaluates `tools/list` responses and `tools/call` requests through
the external processor. Skill manifests use MCP `_meta["x-skill-manifest"]`;
the experiment found that custom annotation fields did not survive this boundary.
This is a prototype-specific carrier, not an ARD entry extension.

The processor emits one discovery span and four spans for each candidate, nine
in total for the two-fixture discovery response:

| Experimental span | Prototype observation |
| --- | --- |
| `ard.discovery` | Candidate discovery and source context. |
| `ard.provenance` | Stubbed provenance check. |
| `ard.governance` | Governance metadata completeness. |
| `ard.trust` | Stubbed trust-signal evaluation. |
| `ard.decision` | Policy outcome and candidate identity. |

These names are not standardized ARD, OpenTelemetry, or AAIF conventions. The
provenance and trust checks do not perform production cryptographic verification.
The example policy allows `summarize@2.1` and denies `scrape@0.9`, which has an
absent signature and malformed governance metadata. This is a test policy, not a
recommended ARD verification pipeline.

### Propagation finding

Agent Gateway and the MCP registry shared context, but the external processor
did not automatically inherit the Gateway's active span. The
[Gateway configuration](https://github.com/91pavan/ard-lifecycle-instrumentation/blob/d3dfa34a2be2d02880886ff18d135b72bd12b92d/gateway/config.yaml)
forwards the client's `traceparent` through `mcpGuardrails.metadata`; the
processor extracts it before starting its spans.

This fallback places the operations in the supplied trace. It does not establish
that the processor's spans are children of the Gateway's active span. In a
production integration, inject active context at each supported outbound
boundary and validate both trace identity and parent/link structure. Do not
interpret the fallback as permission to trust arbitrary external headers.

### Reproduce the experiment

The pinned [README](https://github.com/91pavan/ard-lifecycle-instrumentation/blob/d3dfa34a2be2d02880886ff18d135b72bd12b92d/README.md)
provides setup, MCP initialization, policy assertions, and Jaeger queries. Its
checks show that `tools/list` advertises only `summarize`, while a direct
`tools/call` for `scrape` returns JSON-RPC error `-32001` over HTTP 200. With the
documented test `traceparent`, Gateway, registry, and policy operations appear
under the supplied trace ID.

The fixed context in that experiment is for local testing only. Production
instrumentation generates identifiers as needed and propagates accepted active
context. The prototype's Go tests (`cd gateway` followed by `go test ./...`)
cover filtering, direct-call denial, candidate spans, decisions, and supplied
trace-ID propagation.

## Further reading

- [Observability proposal and maintainer discussion (issue #89)](https://github.com/ards-project/ard-spec/issues/89)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry context propagation](https://opentelemetry.io/docs/concepts/context-propagation/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)