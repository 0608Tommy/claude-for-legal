---
name: demand-intake
description: >
  日本の催告、契約上の治癒通知、権利主張、和解通信等について、当事者、事実、法的性質、時効、delivery、leverage、秘密性をdraft前に収集する。canonical demand typeとstrategic stateを保持し、送信は行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Demand intake

canonical label: `/litigation-legal:demand-intake [title] [--full]`
resume state: `--resume-strategic` → `resume-strategic`

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、matter binding（ある場合）、access、conflicts、destinationを確認。
3. Japanなら
   `references/common/ja-jp/demands-limitation-settlement.md`と
   `source-register.md`を読む。
4. governing law、forum、contract notice clause、actual source item/versionを確認。
5. limitation、statutory notice、delivery、current lawはofficial sourceを取得。
6. internal analysisとexternal letterを分離し、clean-team/privilege/ACL/DLPを確認。
7. state gateway unavailableならintake draftだけ。保存済みと主張しない。
8. AIはsend、service、calendar、matter create、preservation issueを実行しない。

## Flags / state

- `--full`: materialityに関係なく全strategic block。
- `resume-strategic`: partial/skipped intakeの次の未回答promptから再開。

```yaml
strategic_block: answered | partial | skipped
status: intake | ready-to-draft | drafted | sent | closed
```

`resume-strategic`は実stateであり、単なる「戻ってください」という案内にしない。

## Posture first

matterごとに確認する。

- tone: `measured | assertive | aggressive`
- response windowとbasis
- markingと、その表示が日本でinadmissibility/confidentialityを保証しないこと
- signer
- intended audience / delivery

practice-level defaultでsilent補完しない。

## Core intake

1. **Demand type**
   `payment | breach-cure | cease-desist | employment-separation | preservation | other`
2. **Parties**
   sender、recipient、actual reader、relationship:
   `customer | vendor | ex-employee | competitor | third-party | other`
3. **Trigger**
   what/when、exact source、evidence、knowledge/accrual date。
4. **Legal character**
   `rights-assertion | contractual-cure-notice | statutory-notice |
   Civil-Code-150-demand | settlement-communication | other`
5. **Basis**
   contract sections、governing law、statute、forum。
6. **Outcome**
   specific primary/fallback asks。
7. **Deadlines**
   stated、contractual、statutory、court、limitation、internalを分離。
8. **Prior outreach / distribution**
   prior communication、delivery method、proof、copies。

## Strategic block

`--full`またはmaterial demandで実行する。skipを選べるが記録する。

- leverage / our BATNA / their likely BATNA
- downside、relationship、publicity、insurance、precedent
- admission / factual overstatement
- confidentiality basis
- settlement communication use risk
- preservation requestのactual legal basis
- limitation/accrual/transition uncertainty
- fallback and escalation authority

Civil Code 150 demandでは6か月の完成猶予と再催告の制限を確認する。内容証明は内容・
差出日、配達証明はdeliveryを別に扱う。FRE 408を日本modeのgateにしない。

## Intake record

```yaml
demandId: "[ID]"
title: "[title]"
demandType: payment | breach-cure | cease-desist | employment-separation | preservation | other
legalCharacterJP: rights-assertion | contractual-cure-notice | statutory-notice | Civil-Code-150-demand | settlement-communication | other
relationship: customer | vendor | ex-employee | competitor | third-party | other
tone: measured | assertive | aggressive
strategic_block: answered | partial | skipped
skipped_reason: "[string or null]"
status: intake | ready-to-draft | drafted | sent | closed
governingLaw: "[law]"
forum: "[forum]"
statedDeadline: "[date or null]"
contractualDeadline: "[date or null]"
statutoryDeadline: "[date or null]"
courtDeadline: "[date or null]"
limitationCandidateIds: []
deliveryMethod: "[method]"
proofMethod: "[method]"
sourceItemIds: []
confidentiality: "[basis/control]"
```

## Completion

intake draft、thin spots、unverified law/deadline、strategic state、source coverage、
save stateを示す。gateway writeはconditional create、exact returned item/eTag/versionを
表示する。

1. strategic blockを続ける
2. demand draftへ進む
3. missing sourceを取得
4. matter/preservation candidateをcounselへroute
5. other

## 行わないこと

- letter draft/send
- FRE 408の日本への移植
- limitation/dateのsilent calculation
- conflict clearanceの代替
- automatic matter/hold/calendar
- local filesystem、agent、hook、subagent
