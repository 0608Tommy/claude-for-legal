> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Amendment history workflow

## Working index

内部index:

| Order | itemId | Title | Type | Executed | Effective | Parties | Provisions touched | Coverage |
|---|---|---|---|---|---|---|---|---|

同じamendmentのdraft/executed版が混在する場合、statusを確認し、draftをexecuted chainへ混ぜない。

## Summary output

```markdown
# Amendment History: [Counterparty] — [Agreement type]

**Base agreement:** [date, item/version]
**Amendments:** [N] ([first] → [last])
**Last effective change:** [date]

## What changed — chronological

### Amendment [N] — [date]
**Purpose:** [stated purpose; omit if unknown]

- [Provision] (§[X]): [before → after]
- [Added/Deleted] (§[X]): [practical effect]

## Net current state

| Provision | Current candidate position | §Ref | Last changed | Source item/version |
|---|---|---|---|---|

## Watch items

- [party/priority/conflict/renumbering/missing schedule]
```

すべてのfindingにsection referenceを付ける。番号が変わった場合はbaseとamendment双方を示す。

## Provision trace output

```markdown
# Provision Trace: [Provision]
## [Counterparty] — [Agreement type]

### Original — [date], §[X], [item/version]
> "[full relevant text]"

*Plain language:* [...]

### Amendment [N] — [date], §[X]
**Was**
> "[prior text]"

**Now**
> "[replacement text]"

*Effect:* [...]

## Current candidate language
**§[X] — [source item/version, date]**
> "[text]"

## Watch items
```

quoteは条件、exception、cross-referenceを落とさない。長すぎる場合はrelevant subsectionをquoteし、omission位置を示す。

## Conflict types

- amendmentが既にdeletedされたsectionを再度modify
- priority clause同士が矛盾
- effective dateがexecution orderと逆
- assignment/novationでpartyが変わる
- order formがmaster termsをoverride
- incorporation URLがversion不明
- section numberingだけ変更されsubstanceが不明

これらは`[review]`であり、AIがdocument hierarchyを最終決定しない。
