---
name: cold-start-interview
description: >
  日本のリーガルクリニック初期設定をinitial、resume、quick、full、redo-section、check-integrationsの会話stateで実施するadmin skill。責任弁護士登録、clinic model、student participation、利益相反・受任・scope、data/DLP、緊急route、supervision、practice area、公式sourceを構造化し、gateway成功時だけSharePoint profileへ保存する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: admin
  logical-target-id: ja-jp.admin.legal-clinic.cold-start-interview
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cold-start interview

canonical label:
`/legal-clinic:cold-start-interview [--quick | --full | --redo | --redo <section> | --check-integrations]`

## Mandatory setup authority / safety gate

1. `references/common/cowork-runtime-contract.md`と
   `references/profile-record-schema.md`、
   `references/common/clinic-state-payloads.schema.json`を読む。
2. setup ownerはauthenticated clinic supervisor。client/legal gateを設定するには
   current registered Japanese responsible lawyerのidentity、bar association、
   registration verification dateを人が確認する。faculty titleだけで資格を推定しない。
3. callerがstudent、staff、administratorだけの場合、draft questionnaireは可能だが
   legal profileをapprove/publishしない。
4. clinic modelと弁護士法72条等のpositionはqualified Japanese counsel review pending。
   教育目的・無償を包括的safe harborとしない。
5. conflicts、engagement、scope、student participation、external output review、
   deadline dual verification、data/security、emergency、retention/preservationは
   non-configurable floor。
6. setupではreal client factsを収集しない。seed materialはredacted/synthetic又は
   approved restricted sourceだけ。
7. state gateway、profiles/state/audit、ACL、conditional write、storage/flow DLPを
   live preflight。失敗時はsession内profile draftを返し、setup完了又は保存済みと
   表示しない。
8. connectorはlive probe成功時だけ`connected`。declaration、manifest、設定画面だけで
   connectedとしない。
9. Cowork prompt内DLPがrequiredならreal client production useを`blocked`にする。
10. 日本法moduleはDRAFTのまま。qualified counselとsupervisor reviewが完了するまで
    production-readyにしない。
11. information barrierはconflict clearance/waiverでない。
12. disclaimerだけでactual conductによるengagement/scope成立可能性を否定しない。
13. student participation matrixはinternal policyで、legal authority又はAttorney Act
    72 cureでない。

Japan:
`references/common/jurisdictions/ja-jp/clinic-law-and-supervision.md`、
`references/common/jurisdictions/ja-jp/privacy-client-data.md`、
`references/common/jurisdictions/ja-jp/currency-watch.md`。

## State machine

| state | behavior |
|---|---|
| `initial` | profile/setup recordをexact keyで確認 |
| `resume` | saved setup-sessionのcompleted sectionsから再開 |
| `quick` | mandatory safety floorとminimum operational profile |
| `full` | `references/full-interview.md`の全section |
| `redo-section` | approved profileの1sectionだけdraft revision |
| `check-integrations` | read-only live probes、profile changeなし |

source grammar correctionとして`--full`と`--redo <section>`を受け付ける。setup
sessionは`setup:[sessionId]`、statusは
`draft | paused | review-pending | interview-complete | superseded`。
`interview-complete`はprofile又はlegal review approvalを意味しない。legal reviewは
`pending | in-review | approved | blocked`。

## Initial / resume

exact `clinic-practice-profile`と`setup-session`を読む。

- profileなし: `initial`
- paused sessionあり: completed sections、pending questions、source IDsを示して`resume`
- active又はreview-pending profileあり、redoなし: overwriteせずcurrent summaryと
  revision option
- 複数session又はscope conflict: fail closed

pause時はanswered fieldsとsource IDsだけをsetup-sessionへconditional updateし、
unansweredを`pending`とする。silent defaultで埋めない。

## Quick setup

quickでも次を省略しない。

1. responsible lawyer / supervisor / host model
2. legal model review status
3. conflict-first process
4. information barrierとclearanceを分けたconflict process
5. disclaimer/actual conductを含むengagement/scope process
6. internal-policyとしてのstudent participation matrix
7. substantive lawyer review gate
8. APPI Article 58を含むhost-regime selection、clinic restricted categoryと法定
   要配慮個人情報の区別、data/DLP/retention/preservation decision
9. urgent safety/deadline/child-reporting human route
10. practice area / forum / jurisdiction / source cards
11. Houterasu program roles
12. storage gateway status

practice forms、pedagogy detail、semester dates、seed documents等は`pending`として残せる。
`sensible legal defaults`でlawyer-only activityを緩和しない。

## Full setup

`references/full-interview.md`をsection単位、1turn 2～3 answerable promptsで進める。
link/file/paste又はshort answerを優先し、typed answerが必要な箇所で待つ。skipは明示的に
`pending`とし、downstream impactを示す。

主要section:

- authority / clinic model
- conflicts / engagement / scope
- student participation / supervision / pedagogy
- data / APPI / My Number / DLP / retention / incident
- urgent route / safe contact / accessibility
- practice areas / forum / jurisdiction / Houterasu program roles
- `criminal | immigration | housing | benefits` approved source cards
- 2026-04-01 family reform / DV district-court route / child reporting
- consequential translation legal and language reviewers
- official sources / forms / seed documents
- semester / handoff / access revocation
- integrations / storage / automation proof

## `check-integrations`

read-only branch。connector、SharePoint gateway、Power Platform solutionをleast
privilege probeし、`connected | configured-unverified | unavailable | blocked`を表示する。
profile、binding、state、cursorをwriteしない。

probe result:

```yaml
integrationId: "[ASCII ID]"
status: connected | configured-unverified | unavailable | blocked
testedAt: "[ISO-8601]"
testedOperation: "[read-only operation]"
scope: "[minimum scope]"
failure: "[error class or null]"
```

## Pre-write review

profile draft前に:

- contradictions
- unresolved legal/model review
- missing responsible lawyer
- conflict process without owner
- barrier incorrectly marked as clearance
- disclaimer inconsistent with actual conduct
- student matrix presented as legal authority
- practice area without forum/source
- restricted domain without approved source card
- routine template exception without lawyer approval
- sensitive data without ACL/retention
- emergency route without human owner
- unverified integration or automation claim

を一覧にし、approve可能なものとblockerを分ける。

## Write sequence

1. canonical nested profileとinternal-policy participation matrixをschema validate。
   setup-sessionもcompleted sections、pending questions、sources、status、profile
   reference tupleをschema validate。`profileItemId/profileVersion/profileETag`は全null又は
   全populatedだけ。
2. responsible lawyerとsupervisorのseparate approvalを取得。
3. full canonical key、`expectedAbsent`又はexact item/eTag、unique idempotency。
4. conditional create/update。
5. returned exact item IDs/eTags/versionsを確認。
6. source/approval/write auditをappend。
7. successしたrecordだけをsavedと表示。

profile writeとpractice guide、matter create、student access、flow activationは別operation。

## Completion

次を表示する。

- profile version/status
- responsible lawyer/supervisor verification status
- pending/in-review/approved/blocked legal review sections
- storage/DLP/gateway result
- connected vs unverified integrations
- Japan legal review pending
- next safe action: guide、synthetic ramp、tenant test

real client access又はcourt/agency workを自動開始しない。

## 行わないこと

- studentだけでlegal profileをpublish
- attorney-client relationship、representation、filing authorityの作成
- setup completionをlegal approvalと表示
- information barrierをclearance、matrixをlegal authorityとして表示
- U.S. student practice/ABA/FRCP rulesの日本移植
- unresolved privacy/DLPをsilent default
- connector又はPower Platformを宣言だけでconnected/provisionedと表示
- profile保存、flow activation、student access grantを未検証で主張
