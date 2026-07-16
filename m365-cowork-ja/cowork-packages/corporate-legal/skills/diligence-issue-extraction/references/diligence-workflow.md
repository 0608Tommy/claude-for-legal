> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のVDR review向けに変更した派生ファイルです。

# Diligence workflow and output

## Batch

- 1 batchごとにexact source item list/versionを固定する。
- 重要category、missing、unreadableを先に示す。
- 🔴 candidateはfull category完了を待たず人へ提示する。
- batch間duplicateはsource ID、issue type、actionで判定する。
- aggregate時にseverityをsilentに下げない。

## Category minimum checks

| Category | Minimum check |
|---|---|
| Corporate | registry、articles、shareholder register、books、approvals |
| Contracts | CoC、claim/obligation/position transfer、notice、consent |
| Labour | structure-specific succession、rules、union、claims、benefits |
| Privacy | purpose、clean team、foreign transfer、security、My Number |
| IP | title、employee/contractor assignment、moral rights、recordal、OSS |
| Public | EDINET、TDnet、tender offer、large holding、insider |
| Competition | JFTC threshold、market、high-value consultation |
| Foreign investment | FEFTA investor/control/business/exemption |
| Sector | licence/control/transfer/prior consent |

## Finding display

```markdown
### [Finding ID] [Title]

**Category:** [category]
**Severity:** [level]
**Transaction structure:** [value]
**Source:** [item/version/location]
**State:** [answered/not_present/unclear/needs_review]
**Layer:** [law/listing/guidance/contract/internal]

**Fact:** [source-based fact]
**Issue:** [why it matters]
**Deal impact:** [price/structure/closing/integration]
**Options:** [human choices]
**Pre-closing candidate:** [yes/no/unknown]
```

## Gap

- request item with no responsive document
- referenced exhibit/amendment missing
- unreadable/OCR failure
- current official rule not retrieved
- management representation unsupported
- different source versions conflict

gapをno issueへ変換しない。
