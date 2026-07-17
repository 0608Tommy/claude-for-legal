---
name: cold-start-interview
description: >
  Product legal practiceのinitial、resume、quick、full、redo、redo-section、check-integrationsを会話で行い、会社、利用者、launch process、review framework、risk calibration、claims posture、日本法・sector/public-company overlay、保存設定を分離したSharePoint profile/stateへ構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: product-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cold-start interview

正規label/flags:

- `/product-legal:cold-start-interview`
- `/product-legal:cold-start-interview --full`
- `/product-legal:cold-start-interview --redo`
- `/product-legal:cold-start-interview --redo <section>`
- `/product-legal:cold-start-interview --check-integrations`

Coworkではflagをconversation stateへ変換する。

## Mandatory setup/security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、SharePoint
   profiles/state/audit、OneDrive、tenant-approved state gateway、ACL、
   conditional create/update、audit appendをlive preflightする。失敗時は
   read-only/manual setup draftで停止し、setup complete/saveを主張しない。
2. company、product-legal practice、user、setup session、matterを別recordにする。
   共有practice profileへsingle user role、attorney contact、active matter、
   matter secretを保存しない。
3. new profileはconditional create。existing profileはexact `itemId`、latest
   `eTag`、unique `idempotencyKey`でconditional updateし、diffを先に示す。
4. setupはpractice-level fresh sessionでbindingなし。
   `matterId: null` active bindingを作らない。
5. local config/cache/historyを探索・copyしない。利用者がauthorized migration
   artifactを指定した場合だけsource/version/ownerを確認してimport candidateにする。
6. jurisdiction:
   `request > matter > practice-profile > tenant-default`。
7. law、guidance、platform rule、deadline、threshold、future statusをprofileへ
   書く前にofficial/authorized sourceを確認する。
8. seed sourceはexact item/version、coverage、confidentiality、viewerを記録する。
9. skipped answerは`[PENDING]`または
   `[DEFAULT — human review required]`。completeに見せない。
10. role、attorney route、destination、clean-team、MNPI、trade secret、retention、
    storage/flow DLPを確認する。Cowork内DLP必須ならproduction enableを記録しない。
11. connector declarationをconnectedと表示しない。live probe結果だけを使う。

[profile schema](references/profile-records.md)、
[full interview guide](references/interview-guide.md)、
[source rule](references/common/source-provenance-and-review.md)を使う。

## Conversation state

| state | intent |
|---|---|
| `initial` | profileなし。quick/fullを選ぶ |
| `resume` | paused setupのpending questionだけ再開 |
| `quick` | role、setting、product surface、jurisdiction、minimum calibration/security |
| `full` | full interview + seed review documents |
| `redo` | current profile全体をdiff reviewして再設定 |
| `redo-section` | `--redo <section>`の1 sectionだけ更新 |
| `check-integrations` | live probe結果だけ更新 |

canonical core:
`initial | resume | quick | full | redo | redo-section | check-integrations`。

## Start detection

- product-legal practice profileなし → `initial`
- setup session `setupStatus: paused` → `resume`
- `[PENDING]`あり → open items表示
- `setupStatus: complete` → explicit redo/check/upgrade以外で上書きしない
- duplicate/conflicting profile → fail closed

## Orientation

> このpackageはlaunch review、feature risk assessment、marketing claims、
> quick triageを、会社固有のrisk calibrationと日本法overlayで支援します。
>
> quickは約2分、fullは約10～15分です。日本法moduleはqualified Japanese
> counsel review pendingです。
>
> 途中で一時停止でき、gatewayが利用できる場合だけsetup stateへ保存します。
>
> quickとfullのどちらにしますか。

## Pacing

- 1 turnに2～3 answerable promptまで。
- documentにありそうな情報はexact SharePoint item/linkを先に求める。
- upload/readが必要ならanswerを待つ。
- pause時はanswered sectionとpending questionをstateへ保存。
- pre-saveでopen/default/source gapを一覧にする。

## Shared company profile

existing shared profileがあればorganization、practice setting、industry/product、
operation jurisdictions、risk postureを1行で確認し、変更がなければ再質問しない。

practice setting:

`Solo / small firm | Midsize / large firm | In-house |
Government / legal aid / clinic | Other`

会社、business model、customer、stage、public/listed status、jurisdictions、
regulators、risk、escalationを確認する。boxに合わないpracticeはfree-formから構成し、
不適合fieldを無理に埋めない。

## User profile

canonical role:

1. `Lawyer / legal professional`
2. `Non-lawyer with attorney access`
3. `Non-lawyer without regular attorney access`

Non-lawyerも全skillを使えるが、outputはattorney-review draft。lawyer roleでも
skillはclear、approve、send、post、publishしない。attorney contact/routeは
current user profileへ保存し、他利用者から流用しない。

## Quick path

取得:

- current user role、practice setting
- organization/product/customer: consumer | B2B | both
- primary jurisdictionsとJapan nexus
- product surface/channel: web | app | marketplace | platform | hardware | other
- regulated sector: privacy/telecom/minors/payments/finance/medical/public company等
- formal gate | advisory process
- minimum risk calibration:
  `usually blocks | usually requires work | usually FYI`
- claims posture:
  comparative、absolute、evidence-before-publication
- escalation owner
- matter workspace on/off
- storage/connection/DLP

未設定部分は`[DEFAULT — human review required]`。どのdefaultがlaunch/triage/claimsへ
影響するか示す。

## Full path

[interview guide](references/interview-guide.md)を1回2～3promptで進める。

1. user/practice/integrations
2. company/product/customer/stage/public status
3. jurisdictions、Japan/foreign、sector triggers
4. launch intake、lead time、formal/advisory process
5. review framework
6. risk calibration
7. marketing claims/commerce screens
8. escalation/supervision
9. matter behavior、storage、DLP
10. seed review documents
11. watcher preference candidate

watcher preferenceはdesired horizon/cadence/destinationとして記録できるが、
agent、schedule、flow、deliveryが存在する証拠ではない。automation statusとは別。

## Review framework

利用者のexisting frameworkを優先する。なければ次のbaseをdraft defaultとして
提示し、確認前にapproved house frameworkと表示しない。

1. contractual commitments
2. privacy
3. security
4. IP/content
5. third party
6. regulatory/sector
7. marketing claims
8. AI governance

日本が含まれる場合、consumer/checkout、APPI/telecom、safety/PL、
platform/content、accessibility/minors、payments/medical、public disclosureを
overlayとして記録する。

## Risk calibration

各tableにpattern、why、resolution、owner、typical timeline、source review IDsを
記録する。

- `Usually blocks`
- `Usually requires work but ships`
- `Usually FYI`

binding/legal/platform floorはcalibrationで下げない。seedにないpatternは
`[UNTESTED — calibration is provisional]`。

## Seed review documents

原則10件の**past legal review**を読む。PRDだけで代用しない。

取得:

- launch/review date
- issue/category
- actual call and conditions
- what blocked / what shipped
- escalation
- output format/tone
- later learning if available

exact item/version、read coverage、missing docsを記録する。10件未満ならactual Nを
表示し、calibration confidenceを下げる。matter-specific secretをshared company
profileへ入れない。

## Marketing/commerce setup

- reviewer/human owner
- comparative claims posture
- substantiation/evidence standard
- absolute/security/AI/medical/financial claim rules
- common rejected claims
- rendered visual review requirement
- subscription/final-screen owner
- influencer/review/stealth process
- platform policy owner

house ruleは[I]。景品表示法等の[B/G]と混同しない。

## Japan module

Japanが含まれる場合:

```yaml
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"
appi2026AmendmentStatus: diet-passed-2026-07-10-unpromulgated-main-effective-within-two-years
cyberReporting2026Status: future-effective-2026-10-01-scope-check-required
electionAiStatus: future-effective-2027-03-01-not-general-label
```

[日本法router](references/common/ja-jp/README.md)を読み、APPI/PPC、
consumer/final screen、claims/stealth、product safety、telecom、platform、
accessibility/minors、payments/medical、cyber、AI/IP、public disclosureをscreenする。

## Connection check

必須:

- SharePoint profiles/matters/outputs/state/audit
- OneDrive current-user draft
- state gateway

optional candidates:

- Slack — https://mcp.slack.com/mcp
- Google Drive — https://drivemcp.googleapis.com/mcp/v1
- Linear — https://mcp.linear.app/mcp
- Atlassian — https://mcp.atlassian.com/v1/sse
- Asana — https://mcp.asana.com/sse

status:

- `connected`: live probe success
- `configured-unverified`: declaration only
- `adapter-required`: source SSE等でtarget transport未対応
- `not-connected`: missing/failed

Atlassian/Asanaをadapterなしでcompatibleと表示しない。optional connectorがなくても
manual exact item/read-only workflowを示す。

## Pause/resume

[profile schema](references/profile-records.md)の`Conditional pause update`を使い、
`setupStatus`、`pausedAt`、`answeredSections`、`pendingQuestions`、
`profileItemId`をsetup-session payloadへconditional updateする。

resumeでanswered sectionを再質問しない。

## Pre-save

- confirmed fact
- document-derived field
- interview-derived unapproved position
- default/PENDING
- legal premise/currency
- source coverage
- destination/viewers/retention/DLP
- create vs update

substantive required itemがopenならpaused。write後にitem IDs、eTag、idempotency、
review statusをauditする。

## Complete

framework、calibration、jurisdiction/sector、claims posture、seed coverage、
connections、defaults/PENDINGを短く示す。最初のskillを人に選んでもらい、自動開始
しない。

## 行わないこと

- local config/cache/history migration
- placeholder/defaultをcomplete表示
- connector declarationをconnected表示
- gatewayなしにsaved/setup complete表示
- watcher preferenceをrunning schedule表示
- launch/claim approval
