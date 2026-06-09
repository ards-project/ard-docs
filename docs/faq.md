# Frequently Asked Questions (FAQ)

## Is ARDS a replacement for MCP or OpenAPI?

**No.** ARDS is a **discovery protocol (an envelope)**, not an execution protocol. It wraps existing execution standards (like MCP, A2A, and OpenAPI) using standard and proposed IANA media types so clients can find agentic resources dynamically. Once discovered, the client connects to and invokes the agentic resource using its native protocol (e.g., JSON-RPC for MCP).

---

## How is ARDS different from built-in tool search in AI clients?

They're closely related. At one level, a client's built-in tool search is itself an implementation of agentic resource discovery — scoped to the tools that client already has. It chooses among a known, client-managed set, which works well within that boundary.

ARDS describes the same idea more generally, and decouples discovery from any single client. The capabilities a task might need can come from many places — internal systems, vendor services, public catalogs, Skills, MCP servers, APIs, workflows, or agents — and ARDS lets a client or organization discover which of them should be available in the first place, rather than that universe being fixed by the client implementation.

The two compose naturally. An ARDS discovery service can produce a policy-filtered toolbox that a client's built-in tool search then ranks over, or a client can query the discovery service dynamically at task time. Because discovery is decoupled, ranking and filtering can also draw on signals a single client usually can't see on its own: policy, permissions, provenance, trust, usage history, success rates, cost, latency, region, compliance requirements, and deprecation state.

Decoupling discovery from the client is what makes this useful in practice:

- **Enterprise control** — an organization can decide which resources are approved, and which are *preferred* for a given task, and apply policy, permissions, and compliance rules once, centrally, instead of configuring every client by hand.
- **Federation** — discovery services compose. A company can run its own service that merges internal resources with selected vendor and public sources and expose it as a single endpoint, while still controlling what is included.
- **Portability** — because the discovery layer is separate, the same resources can be found and used across different AI clients and harnesses, rather than being locked to one client's tool universe.
- **Independent evolution** — resources can be added, updated, or deprecated without changing the client; a newly published capability becomes discoverable the moment a service indexes it.

In short: built-in tool search selects among known tools; ARDS is the layer that decides which tools should be known — and a client's tool search is one natural way to consume it.

---

## How does discovery work without consuming context window tokens?

Traditional tool selection requires stuffing every available schema into the system prompt. ARDS moves this calculation outside the LLM into a dedicated discovery service (`POST /search`). The orchestrator queries the service with natural language, and it returns only the top two or three most relevant schemas to inject into the prompt.

---

## Do I need to register my agentic resources on a central directory?

**No.** You have absolute publishing sovereignty. You host `ai-catalog.json` on your own domain (`yourdomain.com/.well-known/ai-catalog.json`) to advertise your agentic resources. Any compliant discovery service can find and index your endpoint organically, without requiring permission.

---

## What is the difference between ARDS and Agent Finder?

ARDS is the **protocol**. **Agent Finder** is a product — one discovery service built on ARDS, among the many the protocol makes possible. A publisher describes an agentic resource once; any number of discovery services, named or not, can then choose to index and serve it.

---

## Where does trust come from in ARDS?

**From the curation of the registry, not from the protocol.** ARDS does not make any agentic resource trustworthy — it gives publishers a way to *assert* verifiable identity and provenance, and clients a way to *verify* it. The actual trust decision lives in two places the protocol does not own: the **registry that curates what it indexes and serves**, and the **client that checks the signals before invoking**. ARDS's job is to communicate trust, not to confer it.

---

## What trust signals can ARDS communicate?

The protocol's role here is narrow and deliberate: it gives a publisher a **mechanism to assert verifiable claims**, and a registry or client a **standard way to check them**. ARDS itself verifies nothing and vouches for no one. An entry can carry:

- **Domain-anchored identity** — a mechanism to declare a publisher domain in the entry's URN (`urn:ai:acme.com:...`), so identity is rooted in DNS rather than a self-asserted label and can be checked by whoever consumes the entry.
- **Verified publishers** — a mechanism for a publisher to *demonstrate* they are who they claim: a `trustManifest.identity` (e.g. `did:web`, SPIFFE) that a registry or client cryptographically verifies against the publisher's domain. The protocol carries the claim; the registry or client performs the verification.
- **Signed metadata** — a mechanism to attach a detached JWS `signature` over the trust manifest, so a client can confirm the record was not altered in transit or by an intermediary.
- **Provenance** — a mechanism to declare lineage (`derivedFrom`, `publishedFrom`) that records where a resource came from.
- **Attestations** — a mechanism to reference verifiable compliance artifacts (SOC2, HIPAA, GDPR, …) so they can be fetched and checked.

In every case ARDS *enables the communication* of a trust signal. Whether the signal checks out, and what weight to give it, is the registry's and the client's decision — not the protocol's.

---

## What makes a registry trustworthy?

A registry is a **trust boundary defined by its curation policy** — what it chooses to index, whom it verifies, and what it refuses to serve. A curated registry vouches for what it returns; an enterprise registry serves only internally approved resources; a vendor registry exposes one ecosystem. Clients decide which registries to query, and registries compose, so an organization can merge its own curated answer set with an upstream one. The protocol carries the evidence; the registry supplies the judgment.

---

## Does ARDS verify that a tool or agent is safe?

**No — and it does not claim to.** Safety is not a property a discovery protocol can compute. What ARDS does is let the relevant facts travel so others can judge. It enables a publisher to **communicate a verifiable identity** (a domain-anchored URN), to **show they are a verified publisher** (a `trustManifest.identity` such as `did:web` or SPIFFE that a registry or client checks against their domain), to ship **signed metadata** (a detached JWS signature proving the record is unaltered), and to declare **provenance** for where the resource came from. The safety call is then made by the **registry that curated the result** and the **client that verifies these signals** before invoking — not by the protocol. The relevance `score` returned by a search is *relevance only* and **MUST NOT** be read as a trust, compliance, or safety rating.

---

## Could ARDS make it easier for agents to discover malicious tools?

Discovery is only as permissive as the registry you ask. Because **whoever runs the registry controls the answer set**, a curated or enterprise registry returns only resources it has vetted — a bad actor cannot inject an entry into a registry that did not choose to index it.

ARDS also makes impersonation harder than the status quo, on several concrete fronts:

- **Identity** is anchored to a publisher's domain (`urn:ai:google.com:...`), not a self-asserted label.
- **Verified publishers**: a registry MUST verify that a manifest is actually hosted on — or cryptographically bound (via `did:web`/SPIFFE) to — the domain it claims, so a manifest on `untrusted.com` cannot pose as `urn:ai:google.com:...`.
- **Signed metadata** lets a client confirm a record was not altered in transit, and **provenance** lets it trace where a resource came from.

Compared with today's ad hoc wiring — copy-pasted endpoints with no identity or provenance — ARDS raises the floor by giving every result a verifiable origin. It does not, on its own, decide what is safe; it **communicates the identity, verification, and provenance signals** that let curated registries and clients refuse what is not.
