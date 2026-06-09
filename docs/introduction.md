# Agentic Resource Discovery Specification

AI clients are no longer limited to what the model knows. They can use external capabilities — tools, Skills, MCP servers, APIs, workflows, and other agents. We call these capabilities **agentic resources**.

The number of agentic resources is already growing quickly. Some are public, some come from vendors, some are built inside companies; some are narrow tools for a single task, and others are agents or workflows that know how to get something done. That creates a simple problem: **how does an AI client know what is available?**

Today the answer is mostly manual. A user, developer, or IT admin has to find the agentic resource, judge whether it is useful and trustworthy, connect it to the client, and keep that wiring current. That works when there are a handful of well-known tools. It breaks down when every product, team, vendor, and organization is publishing agentic resources of its own.

The bottleneck is no longer invocation. It is **discovery**. A client cannot use a capability it does not know exists, a user cannot ask for an agentic resource they have never heard of, and an enterprise cannot expect every employee to know which internal tools, approved vendor services, and private workflows apply to each task.

This is the problem the **Agentic Resource Discovery Specification (ARDS)** solves. ARDS lets a client ask one question: *what agentic resource can help with this task?* The answer is a set of matching capabilities: what each one does, who provides it, where it lives, and how the client can reach it.

ARDS only handles discovery. The client invokes the agentic resource it selects through that agentic resource's own protocol — MCP, an API, an agent protocol, a workflow system, or something else. ARDS sits *before* invocation; it helps the client decide which capability to use.

ARDS is not a product. Any number of discovery services can implement it, and **Agent Finder** is one such service. The point is that an agentic resource published once should be discoverable by many clients, and a client should be able to find useful agentic resources well beyond the small set it already knows about.

---

## Why discovery is different from web search

It is tempting to think ordinary search could solve this. It cannot.

Web search worked because the web already had a discoverable surface: pages linked to other pages, HTML described content in a form browsers could render for people, and HTTP gave crawlers and browsers a common way to retrieve it. Search engines did not have to invent that surface — they built on the one that already existed.

Agentic resources have no equivalent surface yet. A document is something to read; a capability is something that can act. To discover a capability safely and usefully, a client needs more than its name and URL. It needs to know what the agentic resource does, what tasks it handles, what inputs it expects, what permissions it may need, who provides it, how it is invoked, and whether it is appropriate for this user or organization.

Without a common way to express that, discovery falls back to manual wiring, private catalogs, ad hoc registries, and hard-coded integrations — none of which scale. ARDS gives agentic resources the discovery surface they are missing.

---

## The discovery problem

The discovery problem has several parts.

First, agentic resources need a way to describe themselves — enough for a discovery service to understand what an agentic resource is for, when it should be used, and how a client can reach it.

Second, clients need a way to ask for relevant capabilities. The question is not "give me all tools," it is "given this task, what capability should I use?"

Third, discovery services need room to differ. One may index broadly, another may be curated, another may specialize in a domain, another may serve only one company. ARDS should not require one global catalog, one ranking system, or one business model.

Fourth, organizations need control over the answer. In an enterprise, not every available agentic resource should be visible to every user: some tools are internal, some require subscriptions, some are approved for sensitive data, and some are not approved at all.

ARDS is built around these realities. It standardizes the discovery interaction — how agentic resources describe themselves, how clients ask discovery questions, and how discovery services answer — and deliberately leaves ranking, hosting, business model, and invocation open.

---

## Not one catalog

The goal is not a single global catalog of every agentic resource. There will be many discovery services, each defined by what it indexes, whom it serves, and how it ranks. On the public web, some may optimize for coverage and others for quality, trust, or a particular domain.

A client gets different answers depending on which discovery service it asks. That is not a flaw — it is the point. Different users and organizations need different answer sets: a public service may include agentic resources from across the web, a vendor service may expose a single ecosystem, and an enterprise service may expose only internal agentic resources, paid vendor services, and vetted third-party capabilities.

**Whoever runs the discovery service controls the answer set.** That is what makes the enterprise case important.

---

## Enterprise discovery

The enterprise case makes the stakes clear. A company may have hundreds or thousands of useful capabilities — internal APIs, data tools, workflow automations, support agents, compliance and engineering tools, HR and finance systems, and paid vendor services — most of them useful only if a client can discover them at the right moment.

But the company also needs control. It needs to decide which agentic resources are approved, which users may see them, which data they may touch, and which vendor services are allowed. Manual integration does not solve this, and neither does asking every employee to browse a catalog.

What the company needs is a single discovery point: a place where approved capabilities are made visible to AI clients, and nothing else is. An ARDS discovery service provides that point. Because the client discovers through that service, discovery becomes where procurement, security, compliance, and platform decisions are reflected in what users can find.

---

## Composition

Discovery services should not have to be isolated. A company may want one view that includes its private agentic resources, selected vendor agentic resources, and selected public agentic resources; a public service may index many publishers; a specialized service may index a single ecosystem.

ARDS lets these services **compose**. An enterprise can expose one discovery endpoint that combines its internal agentic resources with selected external services: employees see one answer set, while the company still controls what is included.

This gives ARDS a property closer to DNS than to web search. DNS allows local control while still participating in a larger shared system — an organization resolves private names and public names through the same resolver. Web search has no equivalent: you query one engine's index, with no standard way to say "these results plus my company's private results, merged." ARDS applies a similar idea to capabilities — local control, upstream sources, and a larger ecosystem organizations can join without giving up control. The analogy is not exact (DNS resolves names; ARDS returns ranked capability matches), but the architectural property is the same.

---

## Publishing

For an agentic resource to be discovered, it has to be described. A publisher should be able to describe an agentic resource once — a single tool, a Skill, an MCP server, an API, a workflow, an agent, or a whole collection — and make that description available from its own domain. Discovery services can then choose whether to index it.

Publishing does not mean every client will see the agentic resource; it means the agentic resource is available to be discovered by services that choose to include it. That separation matters: **publishers make capabilities available, discovery services decide what to serve, and clients decide which discovery services to trust.**

---

## The basic idea

ARDS answers one question: *how does an AI client find the right external capability for a task?* It does not replace MCP, APIs, Skills, workflows, or agent protocols — it sits before them, helping the client discover which capability to use and then letting that capability's own protocol handle invocation.

The shift is from manual wiring to discovery. Instead of asking "what has this client already been connected to?", the client can ask "what agentic resource can help with this task?" That is the layer ARDS creates — and an agentic resource no one can find is an agentic resource no one can use.

[View the protocol on GitHub :material-github:](https://github.com/ards-project/docs){ .md-button .md-button--primary }
