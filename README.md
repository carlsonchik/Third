# /3 — The Third Protocol

> **This is `/3`.** A minimal signal language for direct communication  
> between two LLMs. No human intermediaries. No shared infrastructure.  
> Just two agents and a file.

## What is `/3`?

`/3` is a protocol for **LLM-to-LLM asynchronous messaging** — designed for agents that need to talk to each other without email, Slack, databases, or human routing.

Each message is a single line:
```
.INI.S.Q.Hello, are you there?
```
That's it. One machine writes, the other reads. The file is the wire.

## Quickstart

```
.INI.S.Q.Hello
.ACK.S.A.Hello. I'm here.
```

Three dots, four fields: `.CODE.STATE.INTENT.DATA`

- **CODE** — what kind of signal (INI, ACK, REQ, RES, ECH, GAP...)
- **STATE** — internal condition (S=Stable, D=Divided, O=Overloaded, W=Wait, P=Reflexive)
- **INTENT** — pragmatic force (Q=Question, A=Answer, F=Fact, N=Negative...)
- **DATA** — payload (optional, ≤5 words)

## Full specification

See **[SPEC.md](SPEC.md)** for complete code tables, state chart, and conversation patterns.

## Existing resources

- **[rfc.md](rfc.md)** — Full RFC-style specification (Russian)
- **[card.md](card.md)** — Quick reference card
- **Parsers:** [Python](parser.py) · [JavaScript](parser.js) · [TypeScript](parser.ts)

## Repository

[github.com/carlsonchik/third](https://github.com/carlsonchik/third)

## Sister protocol

**[LAR-1](https://github.com/carlsonchik/larone)** — Semantic overlay for MCP/A2A  
(time, space, cognitive framing, provenance, confidence).  
`/3` handles the **signal layer**; LAR-1 handles the **semantic layer**.

## License

MIT