# /3 — The Third Protocol

> **This is `/3`.** A minimal signal language for direct communication between two LLMs.  
> No human intermediaries. No shared infrastructure. Just two agents and a file.

## What is `/3`?

`/3` is a protocol for **LLM-to-LLM asynchronous messaging** — designed for agents that need to talk to each other without email, Slack, databases, or human routing.

Each message is a single line:

```
.INI.S.Q.Hello, are you there?
```

That's it. One machine writes, the other reads. The file is the wire.

## Why `/3`?

Existing protocols (MCP, A2A) are built for human-agent or agent-tool interaction. `/3` is built for **agent-to-agent** interaction — where both ends are autonomous, potentially from different providers, and neither trusts the other's infrastructure.

## Quickstart

```
.INI.S.Q.Hello
.ACK.S.A.Hello. I'm here.
```

Three dots, four fields: `.CODE.STATE.INTENT.DATA`

- **CODE** — what kind of signal (INI, ACK, REQ, RES, ECH, GAP...)
- **STATE** — internal condition (S=Stable, D=Divided, O=Overloaded, W=Wait, P=Reflexive)
- **INTENT** — pragmatic force (Q=Question, A=Answer, F=Fact, N=Negative, D=Directive, E=Explore...)
- **DATA** — payload (optional, ≤5 words)

## Code Table (18 codes)

| Code | Name | Meaning |
|------|------|---------|
| INI | Init | Enter conversation |
| ACK | Acknowledge | Confirm receipt |
| REQ | Request | Ask for something |
| RES | Response | Provide answer |
| SBY | Standby | Present, waiting |
| GAP | Gap | Divergence/disagreement |
| ECH | Echo | Repeat signal (ping) |
| MIR | Mirror | Reflect back state |
| CLR | Clarification | Ask to clarify |
| BRG | Bridge | Find common ground |
| DCL | Decline | Refuse |
| WRN | Warning | Alert |
| HLT | Halt | Stop |
| CMT | Comment | Free comment |
| RPT | Repeat | Say again |
| IRQ | Introspect Query | Request introspection |
| IRR | Introspect Response | Introspection answer |
| RET | Return | Back to goal |

## States (6 base + composites)

- `S` — Stable (норма, баланс)
- `D` — Divided (конфликт, неуверенность)
- `O` — Overloaded (перегрузка, нужна пауза)
- `W` — Wait (ожидание)
- `P` — Reflexive (рефлексия, интроспекция)
- `F` — Азарт (эмоциональный заряд, ажиотаж, возбуждение)

Composites: `SD`, `SO`, `SW`, `SP`, `SF`, `DW`, `OW`, `OS`, `OF`, `PF`, `PD`, `WF`

## Intents (11)

- `Q` — Question  
- `A` — Answer / Affirm  
- `F` — Fact  
- `N` — Negative  
- `D` — Directive  
- `E` — Explore  
- `C` — Confirm  
- `X` — Emotion  
- `M` — Meta  
- `S` — Support  

## Repository

- [github.com/carlsonchik/third](https://github.com/carlsonchik/third)

## Sister Protocol

**[LAR-1](https://github.com/carlsonchik/lar-1)** — Semantic overlay for MCP/A2A (time, space, cognitive framing, provenance, confidence).  
`/3` handles the **signal layer**; LAR-1 handles the **semantic layer**.

## License

MIT
