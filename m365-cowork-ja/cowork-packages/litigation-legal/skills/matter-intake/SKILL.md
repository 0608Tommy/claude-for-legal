---
name: matter-intake
description: >
  日本の新規matterを、source互換fieldに加えて手続類型、裁判所・事件番号、mints、record regime、送達、複数deadline、証拠、秘密性、保全、控訴・執行まで構造化するPower Platform front end。conflicts/accessをgateし、conditional createする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter intake

canonical label: `/litigation-legal:matter-intake [optional matter name]`

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、SharePoint、
   ACL、conditional create、auditをlive preflight。
2. exact user/profile、practice、authorityを確認。
3. conflicts statusを
   `cleared | pending | not-run | waived`
   で記録。`not-run`はstop、またはprofileでparallel intakeが許されowner/due date付き
   `pending`。bypassはpermanent rationaleとapproverを要求。
4. Japanならcommon Japan router、civil procedure、evidence、demand、source registerを
   読む。
5. initiating source item/version、party、forum、service、deadlineを確認。
6. confidentiality
   `standard | heightened | restricted | clean-team`
   とauthorized group IDsを確認。
7. hold/evidence/identity mappingを別restricted ACLへ置く。
8. create後にauto-switchしない。switchは別operation/new session。
9. gateway unavailableならintake draftだけで、matter createdと表示しない。

## Source compatibility intake

```yaml
type: contract | employment | ip | regulatory | investigation | product | other
role: plaintiff | defendant | claimant | respondent | investigated
source: demand-letter | complaint-served | subpoena | regulator-inquiry | internal-report | pre-suit-threat
risk: high | medium | low | critical
materiality: reserved | disclosed | monitored | none
initialPosture: fight | settle | investigate | wait
```

tokenをtranslate/renameしない。

## Japan intake

### Identification

- matter name / pseudonymous ID
- party procedural roles
- claim and relief
- governing law/forum
- `proceedingType`:
  `pre_suit | ordinary_civil | provisional_remedy | mediation |
  labor_tribunal | patent_infringement | JPO_trial | appeal | execution | other`
- court、division
- case number: era/year/caseSymbol/serial
- `mintsCaseId`
- `recordRegime`:
  `pre_2026_paper | post_2026_electronic | transitional_mints |
  other_procedure_partial`

### Source / service

- exact initiating item/version/hash
- filedAt
- notification/view/download/record timestamps
- servedAtEffective
- paper/court service evidence

### Risk / materiality / owners

practice profileのcalibrationを使う。thin profileでprecisionをinventしない。
outside counsel、engagement、budget、internal owners、insuranceを記録する。

### Deadlines

1 scalarでなく`deadlineIds[]`。

- court-set answer/submission
- next hearing
- appeal/objection
- limitation
- contractual/internal

各candidateにauthority、trigger、service、calculation、verification、calendar null。

### Evidence / confidentiality / preservation

- evidence register
- court/Patent Act confidentiality order
- clean-team/restricted group
- internal preservation assessment
- formal evidence preservation / court order / sector basis
- provisional remedy、appeal finality、execution

## Create

`references/common/litigation-record-schemas.md`のMatterを使う。

1. slug/display nameをIDにしない。opaque matter IDを作る。
2. exact composite key、`recordId`、unique `idempotencyKey`。
3. `expectedAbsent: true` conditional create。
4. success responseのmatter ID、itemId、eTag、versionを記録。
5. duplicate/timeoutでは再createせず照合。
6. canonical audit。
7. auto-switchせず、switchを別に提案。

## Completion

matter draft、conflicts、procedure、service、deadline candidate、ACL、preservation、
create/audit resultを示す。substantive workを自動開始しない。

## 行わないこと

- conflict clearance自体の代替
- `next_deadline`1値への集約
- auto calendar / auto switch / hold issue
- local folder/matter file作成
- unauthorized restricted sourceの複製
- local filesystem、agent、hook、subagent
