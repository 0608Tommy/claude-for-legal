---
name: cold-start-interview
description: >
  litigation practiceの初期設定をquick/fullで行い、role、side、日本の裁判所・手続、mints、証拠、時効、秘密性、risk、outside counsel、restricted workspaceをSharePoint profileへ構造化する。connectorはlive probeし、setup stateを安全にresumeする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cold-start interview

canonical label:
`/litigation-legal:cold-start-interview [--redo | --check-integrations]`

also accepted:

- `--full`
- `--redo <section>`
- `--new-matter`

Coworkでは会話state。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact current user identity、tenant/practice、existing company/practice/user profileを
   読む。他userのrole/attorney contactを流用しない。
3. 初回write前にstate gateway、profiles/state/audit、conditional create/updateを
   live preflight。失敗時はinterview summary/read-only profile draftだけ。
4. Japanならcommon Japan router、全jurisdiction module、source register、
   currency watchを読む。
5. setup sessionは`setup:[sessionId]`、status/version/answersをstateへ保存し、resumeする。
6. profile writeはexact diffとfresh confirmation。
7. connectorはactual tool probe成功だけ`connected`。draft declarationで✓にしない。
8. Cowork内DLP必須ならconfidential seed documentを取り込まずproduction setupを停止。
9. local config、home directory、cacheへread/writeしない。

## Existing setup

- no profile → start
- active setup session → resume / restartを選ぶ
- profile draft/incomplete → missing sectionを示す
- approved profile → no flagならoverwrite確認
- `--redo` → fullまたはsection diff
- `--check-integrations` → connector statusだけ。profile substantive fieldを変更しない
- `--new-matter` → practice profileを変更せずmatter-intakeへroute

## Interview pacing

- quick / fullを最初に選ぶ。
- typed answerが必要なpromptは1 turnに2～3個。
- seed documentはexact SharePoint/OneDrive item指定、paste、skipから選ぶ。
- skipped fieldをsilent defaultにしない。
- pause時はsetup sessionへlast completed stateと`pending`を保存。
- user-stated statute、deadline、case number、thresholdをprofileへ入れる前に確認。

## Part 0 — user / role / side

### User role

```yaml
userRole: lawyer-or-legal-professional | non-lawyer-with-attorney | non-lawyer-without-attorney
attorneyContact: "[name/team or null]"
```

Non-lawyerでも全draft機能を使えるが、send/file/calendar/settlement/hold/release/close前に
attorney review gate。

### Practice role

```yaml
practiceRole: in-house | firm-associate | solo | other
```

- in-house: portfolio、OC、risk/materiality、board/finance
- firm-associate: case theory、brief、evidence、witness prep
- solo: caseload、client expectation、fee/economics、SOL + firm drafting
- other: freeformで無理に分類しない

### Side

```yaml
side: plaintiff | defense | both-default-plaintiff | both-default-defense | varies-by-matter
```

source wordingの`both [default plaintiff/defense] | varies`を意味的に保持する。

## Part 1 — Japan procedure profile

- frequent courts/divisions/forums
- matter types / `proceedingType`
- case number convention: era/year/symbol/serial
- mints use、covered representative、notification checking owner
- record regime: pre-2026 / post-2026 / transitional / partial other procedure
- ordinary civil、labor tribunal、mediation、provisional remedy、appeal、execution
- court-set answer/submission deadline owner
- lawyer + docketing owner dual verification
- holiday/calculation convention
- public judgment database limitation acknowledgement

answer deadlineやcalendar ruleをdefaultでinventしない。

## Part 2 — Evidence / confidentiality / preservation

- exhibit naming: 甲/乙、page/paragraph/line
- evidence register owner、hash/collection/translation/chain of custody
- document-production / inquiry / court request handling
- attorney secrecy / withholding / court confidentiality
- standard / heightened / restricted / clean-team
- authorized Entra groups
- hold roster/evidence/identity mapping ACL
- internal preservation instruction approver
- configurable refresh cadence
- formal evidence preservation / specific order escalation
- witness interview / 陳述書 / witness-party examination convention

米国discovery、privilege、work product、Rule 37(e)、Rule 45、depositionをJapan defaultに
しない。

## Part 3 — Risk / landscape

roleに応じて:

- risk appetite
- severity × likelihood
- materiality / reserve（in-house only）
- case value / exposure（firm/solo）
- settlement authority / client approval
- insurance/tender
- dispute patterns / frequent adversaries
- outside counsel bench / engagement / budget
- internal owners / escalation
- conflicts method:
  `corporate-legal | outside-counsel | system-check | informal | other`
- parallel intake permission / pending owner and due date

source canonical risk/materiality enumsを保持する。

## Part 4 — Demand / limitation / settlement

- demand type pattern
- governing law/notice clause review
- Civil Code 150/151 review owner
- accrual/knowledge/2020 transition
- content-certified mail / delivery certificate practice
- admission and confidentiality review
- settlement communication convention
- no automatic FRE 408 assurance
- preservation request wording

tone、response window、marking、signerはmatter-levelで再確認する。

## Part 5 — Drafting / review style

- pleading/document types
- structure、tone、citation/exhibit format
- exact quote/pinpoint rule
- reviewer note / marker usage
- OC status style
- internal/external version separation
- seed brief、notice、chart、chronology、review protocol
- approved artifact renderer availability

native Word tracked changes、exact Office fidelityを設定上のcapabilityとして約束しない。

## Part 6 — Matter workspace / automation

```yaml
matterWorkspaces:
  enabled: true | false
  crossMatterAccess: false
  bindingTtl: "[duration]"
restrictedMatterIsolation: true
```

- practice mode = fresh session / no binding
- active binding = non-null matterId + expiry
- switch/none = new session
- close = all binding revoke
- restricted/clean-team matter works even if general workspace off

docket automation:

- reader / mapper / writer / delivery separation
- Japanese source priority
- candidate deadlines never automatic calendar
- flow/version/identity/last run display rule

## Integrations

source connector namesを保持:

- Slack
- Google Drive
- Everlaw
- TopCounsel
- CourtListener
- Aurora
- Trellis

Japanのmints/court record connectorが存在するとinventしない。CourtListener/Trellisは
日本docket sourceではない。probe outcome:

```yaml
status: connected | configured-unverified | unavailable
testedAt: "[ISO-8601 or null]"
```

## Profile records

company profile:
`tenantId + profileType`

practice profile:
`tenantId + practiceId + pluginId`

user profile:
`tenantId + practiceId + userObjectId`

practice profileへ単一user role/active matterを保存しない。

legal source registry:

```yaml
checkedThrough: "2026-07-16"
originalJurisdictionTranslation: pending
japanLawLocalization: pending
qualifiedReviewerRecorded: false
```

## Write / confirmation

1. captured answersを順にre-read。
2. contradiction、drift、missing、seed coverage、legal fact uncertaintyを表示。
3. quick defaultは`default-unreviewed`、skipは`pending`として明示。
4. full profile diffを表示。
5. fresh confirmation。
6. createは`expectedAbsent: true`、updateはexact item/eTag。
7. returned item/eTag/versionとaudit IDを表示。
8. gateway unavailableならcopyable profile draftだけ。

## Completion

configured role/side、Japan procedure、evidence/ACL、demand/limitation、workspace、
connector probe、legal review pending、write resultを示す。最初のtaskを1つ提案するが
自動開始しない。

## 行わないこと

- local CLAUDE.md/config作成
- other user profileの利用
- defaultをapproved positionと表示
- connector declarationをconnectedと表示
- US law defaultの日本への移植
- state gateway/automationのprovision済み主張
- local filesystem、agent、hook、subagent
