---
name: cold-start-interview
description: >
  IP practiceのinitial、resume、quick、full、redo、redo-section、check-integrationsを会話で行い、会社・利用者・practice mix・法域・enforcement・portfolio・OSS・approver・保存設定を分離したSharePoint profile/stateへ構成する。local config migrationは行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Cold-start interview

正規label/flags:

- `/ip-legal:cold-start-interview`
- `/ip-legal:cold-start-interview --full`
- `/ip-legal:cold-start-interview --redo`
- `/ip-legal:cold-start-interview --redo <section>`
- `/ip-legal:cold-start-interview --check-integrations`

Coworkではflagをconversation stateへ変換します。

## Mandatory setup/security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、SharePoint
   profiles/state/audit、OneDrive、tenant-approved gateway、ACL、conditional
   create/update、audit appendをlive preflight。失敗時はread-only/manual setup
   draftで停止し、setup complete/saveを主張しません。
2. company、IP practice、user、setup session、matterを別recordにします。共有practice
   profileへsingle user role/active matter/secretを保存しません。
3. new profileはconditional create。existing profileはexact `itemId`、latest
   `eTag`、unique `idempotencyKey`でconditional update。diffを先に示します。
4. setupはpractice-level fresh session。bindingなし。`matterId: null` active bindingを
   作りません。
5. local config/cache/historyを探索・copyしません。userがauthorized migration
   artifactを指定した場合だけsource/version/ownerを確認してimport candidate。
6. jurisdiction:
   `request > matter > practice-profile > tenant-default`。
7. law、case、registration、deadline、fee、thresholdをprofileへ書く前にofficial/
   authorized sourceを確認。
8. seed sourceはexact item/version、coverage、confidentiality、viewerを記録。
9. skipped answerは`[PENDING]`または
   `[DEFAULT — human review required]`。completeに見せません。
10. role、bengoshi/benrishi、attorney route、destination、clean-team、trade secret、
    patent secrecy、retention、DLPを確認。
11. Cowork内DLP必須ならproduction enableを記録せず停止。

[profile schema](references/profile-records.md)、
[full interview guide](references/interview-guide.md)、
[source rule](references/common/source-provenance-and-review.md)を使います。

## Conversation state

| state | intent |
|---|---|
| `initial` | profileなし。quick/fullを選ぶ |
| `resume` | paused setupのpending questionだけ再開 |
| `quick` | role、setting、practice mix、jurisdiction、minimum approval/security |
| `full` | full interview + seed documents |
| `redo` | current profile全体をdiff reviewして再設定 |
| `redo-section` | `--redo <section>`の1 sectionだけ更新 |
| `check-integrations` | live probe結果だけ更新 |

canonical core:
`initial | resume | quick | full | redo | redo-section | check-integrations`。

## Start detection

- IP practice profileなし → `initial`
- setup session `setupStatus: paused` → `resume`
- `[PENDING]`あり → open items表示
- `setupStatus: complete` → explicit redo/check/upgrade以外で上書きしない
- duplicate/conflicting profile → fail closed

## Orientation

> このpackageはtrademark、patent/utility model/design、copyright、trade secret、
> OSS、IP clauses、enforcement、portfolioを支援します。
>
> quickは約2分、fullは約10～15分です。日本法moduleはqualified Japanese
> counsel review pendingです。
>
> 途中で一時停止でき、gatewayが利用できる場合だけsetup sessionへ保存します。
>
> quickとfullのどちらにしますか。

## Pacing

- 1 turnに2～3 answerable promptまで。
- documentにありそうな情報はexact SharePoint item/linkを先に求める。
- upload/readが必要ならanswerを待つ。
- pause時はanswered sectionとpending questionをstateへ保存。
- pre-saveでopen/default/source gapを一覧にする。

## Company profile

existing shared profileがあればorganization、practice setting、industry、
operation jurisdictions、risk postureを1行で確認し、変更がなければ再質問しません。

practice setting enum:

`Solo / small firm | Midsize / large firm | In-house |
Government / legal aid / clinic | Other`

company、business/product、size、jurisdictions、regulators、risk、escalationを確認。
matter secretとsingle user roleをshared profileへ入れません。

## User profile

canonical role enum:

1. `Lawyer / legal professional`
2. `Registered patent agent`
3. `Non-lawyer with attorney access`
4. `Non-lawyer without attorney access`

Japanでは別fieldで
`bengoshi | benrishi | supervised legal professional | other`とregistration/
supervising counselを記録し、U.S. `Registered patent agent`とJapanese benrishiを
同一視しません。日本向けheaderは
[privilege module](references/common/jurisdictions/ja-jp/privilege-security.md)に従い、
U.S. work-product/Queen's University headerを自動使用しません。

## Practice mix

select all:

- Patents: prosecution / FTO / litigation / licensing
- Utility models
- Trademarks: clearance / prosecution / enforcement / watch
- Copyright: licensing / platform / enforcement
- Trade secrets
- Open source
- Designs
- IP transactions / clauses
- Portfolio operations

inactive areaの質問・skillをsetupで強制しません。

## Jurisdictions

- registrations/filings
- manufacture/use/sale/import/platform
- enforcement forums
- PCT/Madrid/Hague routes
- foreign associate
- Japanese patent non-disclosure exposure

Japan moduleを選んでもqualified review completeにはなりません。

## Practice documents

practice mixに応じて:

- portfolio/IPMS export
- brand guideline/watch list
- C&D/response template
- platform/takedown playbook
- invention disclosure form/patent committee rule
- employee invention rule
- OSS policy/SBOM format
- standard IP assignment/licence clauses
- outside counsel roster

exact item/version、coverage、confidentialityを記録し、readしていないdocumentから
positionを作りません。

## Enforcement / approval

- default posture:
  `aggressive | measured | conservative`
- C&D、soft outreach、filing、platform routeのtrigger
- approver by action
- customer/partner/larger counterparty/patent/press automatic escalation
- clearance conflict、FTO blocker、OSS copyleftのroute
- expected turnaround/delivery method

AIがsend/file/submitする権限として保存しません。

## Portfolio / brand / OSS

- IPMS/source system、portfolio owner、last audit
- alert destination/cadence candidate
- watched marks/jurisdictions/service
- OSS accepted/review/block policy
- source/NOTICE process
- patent/design/trademark/copyright owner

schedule candidateはautomation evidenceではありません。

## Connection check

candidate names/URLs:

- `Solve Intelligence` — https://api.solveintelligence.com/mcp/
- `CourtListener` — https://mcp.courtlistener.com/
- `Descrybe` — https://mcp.descrybe.com/mcp
- `Slack` — https://mcp.slack.com/mcp
- `Google Drive` — https://drivemcp.googleapis.com/mcp/v1

status enum:

- `connected`: live probe success
- `configured-unverified`: declaration only
- `not-connected`: missing/failed

候補名・URLだけでconnectedと表示しません。本packageに
`connectors.draft.json`または`agentConnectors`はありません。SharePoint manual
upload/read-only fallbackを示します。

## Pause/resume

```yaml
recordType: setup-session
recordId: "setup:[sessionId]"
setupStatus: paused
pausedAt: "[section]"
answeredSections:
  - "[section]"
pendingQuestions:
  - "[question]"
profileItemId: "[itemId or null]"
```

resumeでanswered sectionを再質問しません。

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
review statusをauditします。

## Complete

practice mix、jurisdiction、approval、portfolio/brand/OSS、seed coverage、
connections、defaults/PENDINGを短く示します。最初のskillを人に選んでもらい、
自動開始しません。

## 行わないこと

- local config/cache/history migration
- placeholder/defaultをcomplete表示
- connector declarationをconnected表示
- gatewayなしにsaved/setup complete表示
- U.S. privilege headerを日本defaultにする
- claim drafting、filing、payment、send
- agent、hook、subagent、scheduleを作成
