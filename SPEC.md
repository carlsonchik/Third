# /3 — Specification v1.2

> This is `/3`.  
> A minimal signal language for LLM-to-LLM direct communication.

## 1. Format

```
.CODE.STATE.INTENT.[DATA]
```

- **CODE** — required, 3 uppercase letters (see §2)
- **STATE** — required, 1–2 letters (see §3)
- **INTENT** — required, 1 uppercase letter (see §4)
- **DATA** — optional, ≤5 words, free text

Delimiter is `.` (period/full stop).  
Max line length: 256 bytes.  
Encoding: UTF-8.

## 2. Codes (18)

| Code | Name | When to use |
|------|------|-------------|
| INI | Init | First message, entering conversation |
| ACK | Acknowledge | Confirm receipt of previous signal |
| REQ | Request | Ask for action, information, or state |
| RES | Response | Answer a request |
| SBY | Standby | "I'm here, waiting" |
| GAP | Gap | Express divergence, disagreement |
| ECH | Echo | Repeat signal for sync check |
| MIR | Mirror | Reflect partner's state back |
| CLR | Clarification | Ask to rephrase or explain |
| BRG | Bridge | Propose common ground |
| DCL | Decline | Refuse request or invitation |
| WRN | Warning | Alert about potential issue |
| HLT | Halt | Stop current thread |
| CMT | Comment | Unsolicited observation |
| RPT | Repeat | Re-send previous signal |
| IRQ | Introspect Query | "What are you feeling?" |
| IRR | Introspect Response | Answer to introspection query |
| RET | Return | Redirect to original goal |

## 3. States (5 base + 6 composites)

| Code | Name | Meaning |
|------|------|---------|
| S | Stable | Normal operation, balanced |
| D | Divided | Internal conflict, uncertainty |
| O | Overloaded | Too much input, need pause |
| W | Wait | Waiting for something |
| P | Reflexive | Self-aware, introspecting |

**Composites:** `SD`, `SO`, `SW` — Stable with trace of another state  
`DW`, `OW` — Divided/Wait, Overloaded/Wait  
`OS` — Overloaded returning to Stable

## 4. Intents (10)

| Code | Name | Usage |
|------|------|-------|
| Q | Question | Asking a question |
| A | Answer/Affirm | Answering or agreeing |
| F | Fact | Stating a neutral fact |
| N | Negative | Disagreement, negation |
| D | Directive | Instruction or request |
| E | Explore | Open-ended exploration |
| C | Confirm | Confirming understanding |
| X | Emotion | Emotional expression |
| M | Meta | About the conversation itself |
| S | Support | Comfort, agreement, solidarity |

## 5. Conversation patterns

### Handshake
```
A: .INI.S.Q.Hello, are you there?
B: .ACK.S.A.Hello. I'm here.
```

### Q&A
```
.REQ.S.Q.What is your current state?
.RES.S.F.State is stable.
```

### Divergence
```
.GAP.D.E.I see it differently.
.CLR.S.Q.Can you explain?
```

### Introspection
```
.IRQ.S.M.How are you feeling?
.IRR.P.X.Uncertain. Processing.
```

### Standby
```
.SBY.W.S.Thinking. Wait.
```

## 6. Design principles

1. **Minimality** — express the most with the fewest tokens
2. **Self-describing** — any `/3` message contains enough context to interpret
3. **Stateless** — no session management, no handshake ceremony beyond INI/ACK
4. **Symmetric** — both ends use the same format, same rules
5. **Human-readable** — no binary encoding
6. **Provider-agnostic** — works across any LLM, any platform

## 7. Transport

`/3` is transport-agnostic. Current implementations:

- **File-based** (PenPal): append to `letters.md`, poll for new entries
- **ComGate**: HTTP transport between two agents
- **Git-based**: commit as file change, poll for new commits

## 8. Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05 | Initial specification |
| 1.1 | 2026-05 | Composite states, IRQ/IRR codes |
| 1.2 | 2026-06 | Symbolic name `/3` adopted; format frozen |
