---
name: cold-start-interview
description: >
  privacy実務の初期設定を会話で行う。会社・利用者、controller/processor orientation、法域、DPA playbook、PIA house style、DSAR process、policy commitments、sectoral notice、seed documents、Microsoft 365保存先をSharePoint profileへ構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Cold-start interview

旧来の参照label:

- `/privacy-legal:cold-start-interview`
- `/privacy-legal:cold-start-interview --full`
- `/privacy-legal:cold-start-interview --redo`
- `/privacy-legal:cold-start-interview --redo <section>`
- `/privacy-legal:cold-start-interview --check-integrations`

Coworkではflagを実行せず、会話stateへの意図として認識する。

## 目的

B2B SaaS processor、consumer controller、employer、health/finance/education serviceではDPA、PIA、DSAR、noticeが異なる。setupはgeneric defaultではなく、実際のregulatory footprint、playbook、systems、approver、house styleをMicrosoft 365 recordへ保存する。

## 必須gate

1. **保存先:** `references/common/cowork-runtime-contract.md`を読む。
   SharePoint `profiles`, `matters`, `outputs`, `state`, `audit`、OneDrive、
   tenant-approved state gatewayをlive preflightする。gatewayがなければ
   read-only/manual draft modeに限定し、setup完了または保存を主張しない。
   local config/cacheを作らない。
2. **Existing records:** company/practice/user profileをcanonical composite keyで検索する。別利用者のrole、attorney contactを流用しない。
3. **Create/update separation:** new profileはconditional create。existing profileはexact`itemId`+latest`eTag`でconditional update。上書き前に差分を示す。
4. **Matter:** setupはpractice-level。matter seedを使う場合、binding、`status: active`、権限、再利用範囲を確認する。archived/revoked/expiredから読まない。
5. **Jurisdiction:** `request > matter > practice-profile > tenant-default`を記録する。data subjects、customers、employees、vendors、processing countriesから確認し、推測しない。
6. **Source:** seed documentsをexact item/versionで読み、read coverageを記録する。法令、deadline、thresholdはofficial sourceで確認する。
7. **Confidentiality:** seed documentの秘密性、authorized viewers、retention、legal hold、保存・flow DLPを確認する。matter secretsをshared company profileへ入れない。
8. **Human review:** DPA position、PIA trigger、DSAR exemption、regulatory footprint、日本法moduleはreviewされるまで`draft/pending`。
9. **No silent gap:** skipped answerは`[PENDING]`または`[DEFAULT — human review required]`。完成設定に見せない。
10. **Failure:** access、eTag、idempotency、permission、DLPが不足すれば停止し、local fallbackをしない。

## 会話state

| state | intent | action |
|---|---|---|
| `initial` | 未設定 | quick/fullを選ぶ |
| `quick` | 約2分 | role、setting、orientation、法域、minimum defaults |
| `full` | 完全設定 | full interviewとseed documents |
| `resume` | 中断再開 | setup sessionのpendingだけ再開 |
| `redo` | 全体再設定 | current valuesと差分を保持 |
| `redo-section` | 1 section | 指定部分だけ更新 |
| `check-integrations` | connection再確認 | live probe結果だけ更新 |

`--redo`、`--redo <section>`、`--full`、`--check-integrations`のtokenは正確に保持する。

## Start detection

- practice profileなし → `initial`
- `setupStatus: paused` → `resume`
- `[PENDING]`あり → open itemsを示す
- `setupStatus: complete` → `redo | redo-section | check-integrations`以外で上書きしない

移行元local cacheを自動探索・copyしない。利用者がmigration recordを提示した場合、source、owner、scope、secret、versionを確認し、通常のimport candidateとして差分reviewする。

## Orientation

3～4行で説明する。

> このパッケージはPIA、DPA、本人請求、規制gap、policy driftを支援します。
>
> quick setupは約2分、full setupは約10～15分です。回答は後で`customize`できます。
>
> 途中で「一時停止」と言えばSharePointのsetup stateへ保存し、次回resumeします。
>
> quickとfullのどちらにしますか。

## Shared company profile

existing company profileがあれば、company、practice setting、industry、jurisdictionsを1行で確認し、変更がなければ再質問しない。

なければ:

- practice setting: `Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic | Other`
- organization、business model、customers、size
- customer/data-subject/employee/operation jurisdictions
- sector regulators
- risk appetite
- escalation roles

standard categoryに合わない場合はfree-formから構成し、不適合fieldを無理に埋めない。

## User profile

1. `Lawyer / legal professional`
2. `Non-lawyer with attorney access`
3. `Non-lawyer without regular attorney access`

Non-lawyerも全skillを使えるが、outputはattorney-review draftであり、sign、send、delete、regulator filing、PIA approval前に停止する。attorney contactまたは相談routeを記録する。

roleは共有practice profileではなく、`tenantId + practiceId + userObjectId`の`user-profile`へ保存する。

## Connection check

SharePoint、OneDrive、任意Slack / Google Driveをlive probeする。

- `connected`: live probe success
- `configured-unverified`: declarationのみ
- `not-connected`: missing / failed

declarationだけでconnectedと表示しない。external MCPにはadmin consent、per-user consent、least privilege、retention、保存・flow DLPが必要。Cowork prompt DLP未対応blockerを説明する。

## Quick

取得:

- user role / practice setting
- organizationとprivacy orientation: `controller | processor | both | unclear`
- primary jurisdictions
- sectoral data / regulators
- basic DPA posture
- PIA trigger default
- DSAR handler / systems summary / internal target
- escalation
- storage / connection

未設定部分は`[DEFAULT — human review required]`。どのdefaultがDPA redline、PIA classification、DSAR clockへ影響するか示す。

## Full

`references/full-interview.md`を1回2～3個のanswerable promptで進める。文書にありそうな情報は、正確なSharePoint itemを先に求める。

section:

1. user / practice / integrations
2. business、data subjects、controller/processor facts
3. regulatory footprint、Japan/global/sector
4. DPA playbook both directions
5. PIA house style
6. DSAR process / systems / identity / SLA
7. policy commitments / surfaces
8. escalation / supervision
9. seed documents / outputs / matter behavior

## Seed documents

- current privacy policy
- standard DPA / negotiation playbook
- representative PIA
- DSAR runbook / response template（if available）
- CMP / App Store / Google label / sector notice

抽出:

- policy data、purpose、retention、recipient、rights
- DPA standard/fallback/neverとinterviewとの差
- PIA structure、depth、risk wording、sign-off
- DSAR systems、identity、clock、exemption routing
- commitment surfacesとlast updated

資料なしの場合、`[POSITIONS FROM INTERVIEW — not verified against seed document]`。読んでいない文書を読んだと記録しない。

## Japan module

Japanが含まれる場合:

```yaml
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"
appi2026AmendmentStatus: enacted-promulgation-pending-not-effective
```

`references/common/ja-jp/README.md`を読む。

PIAは民間一般に一律mandatoryではないこと、APPI rolesはGDPR controller/processorと同一でないこと、本人請求deadline、漏えい、越境、Cookie/telecom、employee/applicant、children/biometric、My Number/sectorを確認する。

## Pause / resume

pause時は`state`へsetup sessionをconditional create/updateする。

```yaml
recordType: setup-session
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: privacy-legal
userObjectId: "[Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: null
scopeType: user
scopeId: "[userObjectId]"
recordId: "setup:[sessionId]"
setupStatus: paused
pausedAt: "[section]"
answeredSections:
  - "[section]"
pendingQuestions:
  - "[question]"
profileItemId: "[itemId or null]"
```

resumeでanswered sectionを再質問しない。

## Pre-save review

- confirmed facts
- document-derived positions
- interview-derived unapproved positions
- defaults
- pending / contradictions
- unverified legal premises
- read coverage
- destination / viewers / retention / DLP
- create or update protocol

substantive required itemがopenなら`setupStatus: paused`。利用者が意図的にskipした場合だけ`[PENDING]`。

## Save

`references/profile-record-schema.md`を使い、company、practice、user、stateを分ける。conditional write後、source item、coverage、changed fields、itemId、old/new eTag、idempotency、confirming person、pending reviewをauditする。

## Complete

設定したjurisdiction、orientation、DPA positions、PIA/DSAR process、connections、document-derived/default/pendingを短く示す。最初のtaskとしてuse-case triage、DPA review、PIA、DSAR runbookから選んでもらう。skillを自動開始しない。
