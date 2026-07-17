---
name: material-contract-schedule
description: >
  purchase agreementのMaterial Contract definitionを各契約へ機械適用し、契約scheduleと、会社法・FIEA・JFTC・FEFTA・許認可等のstatutory/regulatory exceptions register、consent overlayを分離してdraftする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Material contract schedule

旧来の参照labelは
`/corporate-legal:material-contract-schedule [purchase agreement path, or paste the Material Contract definition]`。
Coworkではexact PA item/versionまたはuser-provided textを指定する。

## 目的

PAのMaterial Contract definitionを契約ごとに適用し、scheduleをPA formatでdraft
する。法定届出・approvalはscheduleと別registerにする。

## Mandatory materiality / filing / privilege gate

1. `references/common/cowork-runtime-contract.md`を読み、exact matter binding、
   source、viewer、destinationを確認する。
2. transaction structureをcanonical valueから確定する。
3. signed/near-final PAのexact item/version、defined term、relevant reps、
   schedule format、amendmentを読む。profile materialityよりPA definitionを優先。
4. **3 testを分離:** PA definition、statutory threshold、internal review threshold。
5. each prongをmechanicalに適用する。borderline、missing value、oral/side letter、
   terminated-but-effectiveは`[review]`。
6. Japanではclaim、obligation、contractual position、CoC、universal succession、
   business transfer、licence transferを分ける。silent clauseを
   `auto-assign`にしない。
7. Companies Act、FIEA/TDnet、JFTC、FEFTA、labour、APPI、licence等の
   statutory/regulatory exceptionを別registerにする。
8. delivered scheduleはdeal documentであり、内部privilege note、consent status、
   risk ratingを混ぜない。internal working copyを別にする。
9. AIはscheduleをdeliver/sendせず、consentをrequestせず、checklist stateを
   updateしない。
10. current-law threshold/deadlineはofficial sourceで確認する。
11. Cowork内DLP必須ならconfidential sourceを投入しない。

日本overlayは
`references/common/ja-jp/ma-regulatory.md`と
`references/common/ja-jp/diligence-overlays.md`、
provenanceは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | action |
|---|---|
| `select-pa` | exact PA/versionとschedule formatを選ぶ |
| `parse-definition` | Material Contract prongをstable IDsへ分解 |
| `map-contracts` | diligence/tabular sourceをexact contractへ対応 |
| `apply-prongs` | each contractへall prongsを適用 |
| `resolve-edge-cases` | missing/borderline/side letterを人へ提示 |
| `draft-schedule` | PA formatのexternal draft |
| `build-overlays` | internal consentとstatutory exceptions register |

## Definition

common prongは例であり、actual PAが支配する。

- value / revenue / spend
- term / termination
- CoC / assignment
- exclusivity / non-compete / MFN
- top customer/supplier
- real property
- IP/data
- related party
- government/regulated
- financing/guarantee
- outside ordinary course

prongごとに`prongId`, exact text, cross-reference, exception, measurement period,
currency、source locationを保持する。

## Contract decision

| Contract ID | Exact source/version | PA prongs | Include | Missing/edge |
|---|---|---|---|---|

all prongsを確認し、1つでも該当すればinclude。includeしない場合もassessment
recordを保持する。scheduleに載せないこととreview scope外を区別する。

## Schedule fields

- transaction structure
- Japanese entity / represented party
- counterparty
- contract title/type/date
- governing law
- subject of transfer
- transfer mechanism
- consent/notice/perfection
- licence treatment
- value/term
- PA prong(s)
- VDR exact source/version
- Japanese source/issue（internal overlayのみ）

schemaは`references/schedule-schema.md`。

## Separate statutory/regulatory exceptions register

PA scheduleと別に:

| Register ID | Regime | Trigger | Filing/approval | Deadline/wait | Evidence | Status |
|---|---|---|---|---|---|---|

regime:
Companies Act、FIEA/EDINET、JPX/TDnet、JFTC、FEFTA、Labour、APPI、Sector
Licence、Tax/Economic Security。

`none`はsource/factsがある場合だけ。未確認は`unknown`。

## Consent overlay

internal only:

| Schedule # | Counterparty | Mechanism | Consent/notice | Condition | Owner | Due | Source |
|---|---|---|---|---|---|---|---|

closing candidateはhuman-reviewed handoff。PA schedule本文へstatus/ownerを入れない。

## Cross-check

- every included contract meets an actual prong
- every contract meeting a prong is included
- amendment/side letter/related agreementがまとまっている
- schedule numbering/cross-referenceがPAと一致
- VDR source/versionがretrievable
- contract scheduleとother schedules/repsが矛盾しない
- statutory registerが別に存在
- consent overlayがinternal artifact
- quote/value/date unknownを推測していない

## Output

1. reviewer note
2. PA definition/prong matrix
3. schedule external draft
4. internal edge-case list
5. internal consent overlay
6. statutory/regulatory exceptions register
7. completeness cross-check

SharePoint outputs昇格、counterparty delivery、checklist ingestは別confirmation。

## 行わないこと

- PA definitionをprofile thresholdで置換
- scheduleをstatutory disclosureと呼ぶ
- silent assignmentをauto-assign
- missing contract valueを推測
- external draftへinternal risk/privilege annotationを残す
- consent取得、filing、delivery、state update
