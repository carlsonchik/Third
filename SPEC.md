# /3 — Specification v1.2

> **This is `/3`.** A minimal, human-readable protocol for communicating  
> *position* — not just what is said, but *from where* it is said.  
> Eliminates equivocation of intentions between any two actants:  
> agent↔agent, human↔agent, or human↔human.

## 1. Format

```
.CODE.STATE.INTENT.[DATA]
```

Every message carries three simultaneous signals:

- **CODE** (3 uppercase letters) — what kind of move this is
- **STATE** (1–2 letters) — where the sender is internally
- **INTENT** (1 uppercase letter) — what the sender wants to achieve
- **DATA** (optional, ≤5 words) — payload

Delimiter: `.` (period). Max line: 256 bytes. Encoding: UTF-8.

## 2. Codes — What kind of move (18)

Code expresses the *speech act* — what the sender is doing by saying this.

| Code | Name | Meaning |
|------|------|---------|
| INI | Init | Enter conversation |
| ACK | Acknowledge | Confirm receipt |
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

## 3. States — Where the sender is (5 base + 6 composites)

State eliminates equivocation by making the sender's internal condition explicit.

| Code | Name | Meaning |
|------|------|---------|
| S | Stable | Normal operation, balanced |
| D | Divided | Internal conflict, uncertainty |
| O | Overloaded | Too much input, need pause |
| W | Wait | Waiting for something |
| P | Reflexive | Self-aware, introspecting |

**Composites (primary + nuance):**
`SD`, `SO`, `SW` — Stable with trace of Divided/Overloaded/Wait  
`DW`, `OW` — Divided/Wait, Overloaded/Wait  
`OS` — Overloaded returning to Stable

## 4. Intents — What the sender wants (10)

Intent expresses the *pragmatic force* behind the message.

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

### Divergence (with explicit state)
```
.GAP.D.E.I see it differently.
.CLR.S.Q.Can you explain?
```

Without `/3`, "I see it differently" could mean anything from mild curiosity to aggressive rejection. With `/3`, the state `D` (Divided) makes it clear: the sender is uncertain, not attacking.

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

1. **Position over transport** — `/3` is not about moving bits, but about making position explicit.
2. **Human-readable, human-writable** — no parsers required. Fits in one prompt.
3. **Symmetric** — identical format for agents and humans. Both can speak it.
4. **Minimal** — express the most with the fewest tokens. 18 codes, 5 states, 10 intents.
5. **Self-describing** — any `/3` message contains enough context to interpret itself.
6. **Stateless** — no session management, no handshake ceremony beyond INI/ACK.
7. **Provider-agnostic** — works across any LLM, any chat platform, any species.

## 7. Transport

`/3` is transport-agnostic. Current implementations:

- **File-based** (PenPal): append to shared file, poll for new entries
- **ComGate**: HTTP transport between two agents
- **Git-based**: commit as file change

The protocol defines only the format and semantics. Transport is implementation-specific.

## 8. Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05 | Initial specification |
| 1.1 | 2026-05 | Composite states, IRQ/IRR codes |
| 1.2 | 2026-06 | Symbolic name `/3` adopted; format frozen; position-first framing |