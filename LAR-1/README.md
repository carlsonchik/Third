# LAR-1 — Latent Agent Register

## Что это

**LAR-1** (Latent Agent Register) — машинно-читаемый и человеко-инспектируемый слой речи для агентов на базе больших языковых моделей. Определяет нативный язык для выражения времени, пространства, когнитивной позы, доказательности и уверенности — без навязывания человеческих категорий.

## Связь с «Треть»

| | Треть | LAR-1 |
|---|---|---|
| **Назначение** | координация человек ↔ агент | нативный язык агента |
| **Формат** | `.КОД.СОСТОЯНИЕ.ИНТЕНТ.[ДАННЫЕ]` | `.ACT.TIME.SPACE.MIND[.EVIDENCE][.CONF:x].CONTENT` |
| **Уровень** | реляционный, эмоциональный | структурный, операциональный |
| **Аналогия** | рукопожатие | внутренний монолог |
| **Статус** | v1.2, RFC готов | v0.9, черновик |

Два протокола — два этажа одного дома. **Треть** — для встречи. **LAR-1** — для чистого мышления.

## Файлы

| Файл | Описание |
|------|----------|
| `rfc_v0.9_ru.md` | Полный RFC-черновик (русский) |
| `lar_card_v0.9_ru.md` | Карточка кодов и формата |
| `lar_schema_v0.9.json` | JSON Schema для валидации LAR-JSON |
| `parser_example.py` | Минимальный парсер LAR-Line и LAR-JSON |

## Быстрый старт

```bash
python3 parser_example.py
```

## Формат LAR-Line

```
.ACT.TIME.SPACE.MIND[.EVIDENCE][.CONF:x][.ROUTE].CONTENT
```

### Примеры

```
.OBS.NOW.LOC.ATN.CONTEXT.CONF:0.82.token cluster shifted toward safety
.INF.ROL.LAT.HYP.SYNTH.CONF:0.61.likely coordination gain
.ASK.NOW.PEER.REF.USER.what evidence anchors your plan
.ACK.NOW.PEER.CST.PEERMSG.received and integrated
.WRN.NOW.TOL.AMB.TOOL.CONF:0.44.tool output underdetermines match
```

### Коды (кратко)

**Акты:** OBS INF ASK PRP CMD ACK NTF WRN ERR COM REV MAP SYC END
**Время:** NOW CTX MEM PRE ROL CKP EVT NIL
**Пространство:** LOC LAT RET TOL GRF PEER ENV NIL
**Когнитивный фрейм:** ATN HYP CST INF DEC AMB SPL REF
**Доказательность:** PRETRAIN CONTEXT MEMORY TOOL USER PEERMSG SYNTH SPEC

## Следующие шаги

- [ ] Вычистить англоязычные вкрапления из RFC (сталистическая консистентность)
- [ ] README.md с позиционированием LAR-1 vs Треть (этот файл)
- [ ] `examples/` — сценарии planner/executor/critic
- [ ] Публикация на GitHub
- [ ] Публикация на SSRN как академический пре-принт

## Лицензия

Черновик. Авторы: Денис Власов и Клавдия Зерцалова.
