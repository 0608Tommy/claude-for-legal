---
name: demand-received
description: >
  inbound demandをexact sourceから読み、当事者、主張、法的basis、stated・contractual・statutory・court・internal deadlineを分離し、portfolio重複、事実、選択肢をtriageする。responseはdraft候補に留め、自動送信・calendar登録を行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Demand received

canonical label:
`/litigation-legal:demand-received [path-to-incoming] [--slug=custom-slug]`

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。local pathへcopyしない。
2. exact incoming item/version/hash、received timestamp、recipient entity、accessを確認。
3. exact user/profileと、matter cross-checkを行うscopeを確認。cross-matterはauthorized
   portfolio indexの最小fieldだけを使う。
4. Japanなら
   `references/common/ja-jp/demands-limitation-settlement.md`と
   `source-register.md`を読む。
5. sender-cited lawをcurrent official sourceで確認。取得できなければcharacterize
   せず`[statute unretrieved — verify]`。
6. internal triageとexternal response draftを分離し、destination/ACL/DLPを確認。
7. state gateway unavailableならread-only triage。matter link/updateを主張しない。
8. AIはresponse send、preservation issue、calendar、matter createを実行しない。

## Extract

- sender、signer、counsel
- recipient entity/person
- signed date、received date、delivery evidence
- demand type:
  `payment | breach-cure | cease-desist | employment-separation | preservation | other`
- specific asks
- facts alleged
- contract/statute/case cited
- threat / proposed next step
- settlement/confidentiality labelとactual substance
- attached/incorporated documents

exact quoteがなければquotation markを使わない。

## Deadline classification

```yaml
statedDeadline: "[date or null]"
contractualDeadline: "[date or null]"
statutoryDeadline: "[date or null]"
courtDeadline: "[date or null]"
limitationCandidateIds: []
internalDecisionDeadline: "[date or null]"
```

senderのstated deadlineは、それだけでbindingとしない。contract、statute、court
process、limitationのbasisを分け、candidate deadlineを自動calendar登録しない。

## Portfolio cross-check

authorized indexでcounterparty、subject、source item ID、related matter IDを確認する。

- active direct match
- archived/closed direct match
- subject overlap
- type pattern
- none

restricted matterのexistenceやfactをunauthorized userへ漏らさない。same counterpartyでも
別matter sourceを本文へcarryしない。

## Assessment

formal merit opinionではなくrouting read。

- facts: known recordとのalignment / disconnect
- legal basis: applicability、currency、forum
- sender story / likely response pressure
- our possible factual/legal positions
- demanded reliefとavailable remedyの関係
- relationship、insurance、publicity、preservation

source rating token:
`substantial | debatable | weak | frivolous`。

ratingは`[review]`付きのstructured readで、counsel final callではない。

## Options

- **A substantive response draft**
- **B holding acknowledgment draft**
- **C settlement discussion draft**
- **D no external response now + internal preservation assessment**

各optionにbenefit、risk、required facts、legal deadline、approverを示す。日本modeで
FRE 408 protectionを約束しない。Dでもinternal preservationが必要かはspecific basisと
factsで評価し、自動issueしない。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Demand received — triage

**Inbound request ID:** [ID]
**Received:** [timestamp]
**Sender / recipient:** [...]
**Demand type:** [...]
**Related matter:** [authorized ID / none / access-limited]

## Demand
[asks、facts、basis、threats]

## Deadline classification
| Type | Date | Basis | Verification |
|---|---|---|---|

## Portfolio cross-check
[result without restricted leakage]

## Routing assessment
**Rating:** [token] `[review]`
[facts / law / remedy / uncertainty]

## Options
[A-D]

## Immediate internal actions
[source preservation, counsel, insurance, facts, no auto action]
```

saveは`inbound-request` conditional create。matter link/updateは別confirmation。

## Completion

rating、deadline classes、related matter、unverified source、options、save stateを示し、
次から人に選んでもらう。

1. response intake/draft
2. counsel escalation
3. missing facts/source
4. preservation assessment / tracking candidate
5. other

## 行わないこと

- final merit opinion
- response send
- stated deadlineのautomatic binding扱い
- FRE 408の日本への移植
- automatic matter/hold/calendar
- restricted matter disclosure
- local filesystem、agent、hook、subagent
