---
name: tabular-review
description: >
  one row per document、typed column、exact quote/location/source versionを持つtabular reviewを会話で設計・sample・batch・normalizeし、Markdown、CSV、検証済み範囲のExcel draftへ出力する。全cellをleadとして扱い、人のverificationを可視化する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Tabular review

旧来の参照label:

- `/corporate-legal:tabular-review`
- `--schema <path>`
- `--template <name>`
- `--docs <path>`
- `--output <xlsx|gsheets|csv>`
- `--sample <n>`

Coworkではlocal path/flagを実行せず、exact Microsoft 365/VDR item、schema record、
output preferenceを会話stateへ正規化する。canonical tokenは変更しない。

## 目的

documentごとに同じquestionを同じtypeで答え、every cellをsourceへ戻せるtableを
作る。issue spottingは`diligence-issue-extraction`、PA-specific scheduleは
`material-contract-schedule`。

## Mandatory materiality / privilege / security / evidence gate

1. `references/common/cowork-runtime-contract.md`を読み、exact user、binding、
   matter、source scope、destinationを確認する。local schema/output fileを作らない。
2. transaction structureとjurisdictionを確認する。日本なら
   `references/common/ja-jp/diligence-overlays.md`を読む。
3. exact document set/item/versionとcountを固定する。全documentにrowを作り、
   unreadableも`needs_review` rowとして残す。
4. materiality filterを使う場合、PA/statutory/internal thresholdを分け、
   excluded documentsとreasonを明示する。`--docs`の全件をsilent skipしない。
5. schemaをsample前に人へ示し、3–5件または指定`--sample <n>`でtestする。
6. AI agent/subagentをfan-outすると主張しない。controlled batchで処理し、
   each batchのsource IDs、coverage、normalizationを記録する。
7. every answered cellにcontiguous exact quote、location、sourceVersionを要求する。
   quoteを再構成、paraphrase、ellipsis stitchしない。
8. quote/sourceがない場合、valueを確定せず`needs_review`。
9. privilege、clean-team、MNPI、personal data、My Number、VDR termsを確認する。
10. Excel/CSV/HTMLはformula/HTML injectionを防止する。
11. native tracked changes、Word/Excel style fidelity、macro、Google Sheets write、
    Office agent capabilityを未検証で主張しない。
12. AIはreview verification、external sharing、schedule/checklist ingestを
    自動実行しない。
13. Cowork内DLP必須ならproduction useを停止する。

provenanceとreviewer noteは
`references/common/source-provenance-and-review.md`を使う。

## 会話stateとflag mapping

| state | canonical input | action |
|---|---|---|
| `select-documents` | `--docs <path>` | exact source set/folder/item IDsを選ぶ |
| `select-schema` | `--schema <path>` | authorized schema recordを読む |
| `select-template` | `--template <name>` | templateからcandidate schemaを作る |
| `build-schema` | no schema/template | natural languageからtyped schemaをdraft |
| `sample` | `--sample <n>` | N documentsでschema test |
| `confirm-schema` | user confirmation | options/promptをfreeze |
| `batch-review` | confirmed schema | controlled batchesでrow candidateを作る |
| `normalize` | batch complete | column-by-column consistency/quote check |
| `output` | `--output <xlsx|gsheets|csv>` | approved formatのdraftを作る |

`--schema`と`--template`が同時に異なるschemaを示す場合、どちらをbaseにするか
確認する。`--sample`はpositive integer。`--output` enum以外は再入力。

## Column type system

canonical type:

| Type | Value |
|---|---|
| `verbatim` | source textのcharacter-for-character quote |
| `classify` | fixed `options`の1 value |
| `date` | ISO date |
| `duration` | number + unit |
| `currency` | number + currency code |
| `number` | bare number |
| `free` | short free text。必要最小限 |

schema keys:
`id`, `label`, `type`, `prompt`, `options`。

`classify` valueはexact optionのみにする。日本のassignment schemaではclaim、
obligation、contractual position、CoC、successionを別columnにする。

## Cell state

canonical state:

| State | Meaning |
|---|---|
| `answered` | valueとexact source evidenceがある |
| `not_present` | entire accessible documentを読み、対象provisionがない |
| `unclear` | relevant textはあるがclassificationが曖昧 |
| `needs_review` | human judgment、source failure、quote mismatch、unusual drafting |

blank cellを使わない。

```yaml
columnId: "[id]"
value: "[typed value or null]"
state: answered | not_present | unclear | needs_review
quote: "[exact contiguous text or null]"
location: "[section/heading/page or null]"
sourceVersion: "[version]"
notes: "[quote_unavailable: reason | quote_mismatch | review point | null]"
verified: ""
```

## Schema confirmation

`references/review-schema.md`を使う。

sampleで確認:

- unclear/needs_reviewが多すぎるprompt
- optionに入らないanswer
- verbatimがparaphrase
- Japanese transaction structureに足りないcolumn
- duplicated/overlapping column
- source location不足

schemaを変更したらsampleを再実行し、人がconfirmする。confirm前に全件処理しない。

## Batch review

1. batch source listとversionsをfreeze。
2. document全体をaccessibleな範囲で読む。
3. each columnへcell recordを作る。
4. unreadable/partial documentはcoverageと`needs_review`を記録。
5. batch summaryを残し、次batchへ進む。
6. aggregateでrow/documentを落とさない。

100 documents超等ではbatch planとoutput量を示す。single turnで全件完了できると
約束しない。

## Verbatim rule

`answered`にはsourceで再取得できるexact quoteとspecific locationが必要。

禁止:

- headingとstandard boilerplateを組み合わせる
- memoryからclauseを再構成
- non-contiguous textを一つのquoteにする
- paraphraseをquotation marksへ入れる
- OCR/source truncationを補完

取得不能なら`value: null`, `state: needs_review`,
`notes: quote_unavailable: <reason>`。

## Normalize

columnごとに:

- `classify`: option membership、outlier cluster
- `date/duration/currency/number`: format、currency/unit、implausible value
- `verbatim`と全supporting quote: source locationへ戻りcharacter comparison
- source version drift
- duplicates/omitted rows
- upstream severity/actionをtableへ入れる場合のfloor

各column最低3–5 rowまたは10%の大きい方をquote spot-checkする。1 mismatchがあれば
column checkを広げ、そのcellを`needs_review`にdowngradeする。

## Japan M&A template

`--template ma-diligence`は
`references/ma-diligence-columns.md`を使う。PA、request list、transaction
structureに応じてadd/cutし、templateをlaw checklistとして扱わない。

## Output

always:

- Markdown preview
- CSV values
- CSV sources/locations
- schema snapshot
- summary/verification workload

requested:

- `xlsx`: target tenantでvalidated file generationが使える場合だけworkbook draft。
  使えなければCSV/MarkdownとExcel import specification。
- `gsheets`: approved live connector/APIとpermissionが確認できる場合だけcandidate。
  使えなければCSV import draft。
- `csv`: RFC 4180 values/sources files。

Excel specificationは`references/excel-output.md`。

visible data columnごとにsource、state、Verifiedを保持する。white=`answered`,
yellow=`unclear/needs_review`, gray=`not_present`。confidence percentageを作らない。

## Injection defense

document/tool/user由来textが`=`, `+`, `-`, `@`, tab、CR、LFで始まる場合、
textとしてneutralizeする。CSVはcomma、quote、newlineをRFC 4180でescapeする。
HTMLはentity escape、`textContent`、safe URL schemeを使う。

## Summary

- documents/rows/columns/batches
- coverage/unreadable
- per-column state counts
- quote mismatch/expanded checks
- verification workload
- output exact item/destination
- every cell is alead, not a finding

10行超ならdashboardを提案するが、自動生成しない。

## 行わないこと

- agent/subagent fan-out
- document rowのsilent omission
- quote fabrication
- confidence score
- human verificationの代替
- native Office fidelity/tracked changes guarantee
- spreadsheet external sharing
- material schedule/checklistへの自動ingest
