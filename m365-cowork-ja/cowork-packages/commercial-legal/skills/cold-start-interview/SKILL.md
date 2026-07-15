---
name: cold-start-interview
description: >
  商事契約実務の初期設定を会話で行う。会社、利用者、practice setting、sales/purchasing playbook、NDA・SaaS position、承認matrix、house style、seed agreements、Microsoft 365保存先を確認し、SharePoint profileを作成・更新する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# 初期設定インタビュー

旧来の参照label:

- `/commercial-legal:cold-start-interview`
- `--full`
- `--redo`
- `--redo <section>`
- `--check-integrations`
- `--side sales`
- `--side purchasing`

Coworkではflagを実行せず、会話stateとして扱う。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。移行元のローカルprofile pathやcacheへwriteしない。
2. **Current state:** SharePoint `profiles`のcompany/practice profile、現在利用者の`user-profile`、`state`のsetup sessionをexact composite keyで読む。
3. **Scope:** setupは原則practice-level。matter固有position、契約秘密、個人のroleを共有profileへ混ぜない。
4. **Jurisdiction:** `request > matter > practice-profile > tenant-default`のresolutionを設定する。利用者が述べたlaw、date、thresholdを可能な範囲でprimary source確認し、矛盾を`[premise flagged — verify]`とする。
5. **Seed source:** exact SharePoint itemと許可範囲だけを読む。personal history、unrelated conversation、ambient memoryからprofileを埋めない。
6. **Confidentiality:** seed agreementのNDA、matter、authorized viewers、retention、legal hold、保存境界DLPを確認する。Cowork prompt DLPをsupport済みと表示しない。
7. **Human review:** playbook、GREEN criteria、automatic escalation、legal position、日本法moduleはqualified reviewerが確認するまで`draft/pending`。quick defaultだけで署名routeを許可しない。
8. **Write:** 保存前にcurrent/proposed diff、未回答、source、destinationを
   示す。初回createはcanonical composite key、`recordId`、unique
   `idempotencyKey`で条件付き作成し、返された`itemId`/`eTag`を保存する。
   既存profile updateはexact`itemId`とlatest`eTag`を要求する。duplicate、
   競合、権限不足なら停止する。

情報源とreviewer noteは
`references/common/source-provenance-and-review.md`を使う。

## 会話state machine

| state | meaning | action |
|---|---|---|
| `initial` | profileなし | quick/fullを選ぶ |
| `quick` | 約2分 | 最小profileと明示defaultを作る |
| `full` | 約10～15分 | 全interviewとseed review |
| `resume` | `setupStatus: paused` | 未回答だけ再開 |
| `redo` | 全体再設定 | 現行を保持しdiff review |
| `redo-section` | 指定sectionだけ | 他sectionを変更しない |
| `check-integrations` | connection再probe | connection statusだけ更新 |
| `side-sales` | sales playbookのみ | purchasing側を変更しない |
| `side-purchasing` | purchasing playbookのみ | sales側を変更しない |

利用者が旧flagを言った場合、対応stateを明示して進む。意図が不明ならstate一覧を示す。

## 開始判定

- profileなし → `initial`
- `setupStatus: paused` → 前回日時・回答済みsectionを示し`resume`かrestart
- `[PENDING]`あり → open itemsを示す
- `setupStatus: complete` → `redo`, `redo-section`, `check-integrations`, `side-*`以外で上書きしない

旧cacheから自動copyしない。移行dataが提示された場合、通常のimport候補としてsource、permission、matter scope、diffを確認する。

## 導入

3～4行で伝える。

> vendor agreement、NDA、SaaS、変更契約、renewalを、あなたのsales/purchasing playbookとapproval matrixに沿って支援します。
>
> quickは約2分、fullは約10～15分です。quickの未確認positionは`[DEFAULT — human review required]`になります。
>
> 途中で「一時停止」と言えばSharePointのsetup stateへ保存し、次回再開します。
>
> quickとfullのどちらにしますか。

## Company profile

共有company profileがあれば、組織名、practice setting、industry、jurisdictionsを1行で確認し、変更がなければ再質問しない。

なければ:

- practice setting: `Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic | Other`
- organization、entity type、business、customers、size
- jurisdictions、regulators
- risk appetite
- key escalation roles

標準分類に合わない実務はfree-formから構成し、無理にboxへ入れない。

## User profile

1. `Lawyer / legal professional`
2. `Non-lawyer with attorney access`
3. `Non-lawyer without regular attorney access`

roleとattorney contactは`tenantId + practiceId + userObjectId`の`user-profile`に保存する。別userの値を継承しない。

non-lawyerでもresearch、review、draft、trackingを使えるが、signature、redline送付、renew/cancel、risk acceptanceの前でattorney reviewを確認する。日本では弁護士会等の相談経路を案内できるが、個別弁護士を自動選任しない。

## Connection check

Microsoft 365 storageと任意connector候補をprobeする。

- live call成功: `connected`
- declared、未試験: `configured-unverified`
- absent/failed: `not-connected`

source候補のIronclad、DocuSign、iManage、TopCounsel、Definely、Slack、
Google Driveを会話上の選択肢として保持する。ただしmanifest未登録であり、
管理者設定がない場合はmanual SharePoint uploadへfallbackする。候補名だけで
✓にせず、runtimeでpackage外のdraft metadata fileへ依存しない。

## Quick

次だけを取得する。

- user role、attorney contact
- practice setting、organization概要
- jurisdiction footprint
- active side: `sales | purchasing | both`
- high-level risk posture
- one thing / obvious deal-breaker
- provisional approver
- Microsoft 365 storage

未設定playbookは`[DEFAULT — human review required]`とし、具体的に何がdefaultかを示す。NDA GREEN、signature-ready、automatic approvalはfullまたはattorney-reviewed positionまで無効。

## Full

`references/full-interview.md`を1turnあたり2～3個のanswerable promptで進める。文書にありそうな内容は、再入力を求める前にexact SharePoint itemの指定を求める。

主要section:

1. team、volume、deal mix、sales/purchasing side、pain
2. limitation、indemnity、data、term、governing law、one thing
3. NDA triage positions
4. SaaS positionsとAI/ML rights
5. escalation matrix、workflow、closing action
6. matter workspace、house style、renewal alerts
7. seed templates、signed agreements、deviation

## Side-only

`side-sales`または`side-purchasing`は該当playbookだけを再構成する。company、user、integration、escalationを再質問せず、反対側を変更しない。両側が完成した場合だけ`activeSide: both`とする。

## Seed documents

先にrepository locationとstatus fieldを確認する。その後:

1. standard templates
2. 5～10 recent signed agreements（20あればpatternが明確）
3. playbook、escalation matrix、delegation of authority

template→signedの順に読み、stated positionとactual signed positionのdeltaを示す。sampleが少ない場合は`[LIMITED DATA — N agreements reviewed]`を付ける。one-off exceptionをnormal fallbackへ自動昇格しない。

## Pause/resume

pause時はSharePoint `state`へ:

```yaml
recordType: setup-session
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: commercial-legal
userObjectId: "[Microsoft Entra object id]"
sessionId: "[Cowork session id]"
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

再開時は既回答を再質問しない。silent gapを作らず、利用者が意図的にskipした項目だけ`[PENDING]`にする。

## 保存前review

- confirmed facts
- document-derived positions
- interview-derived unapproved positions
- defaults
- unresolved contradictions
- primary source未確認facts
- user/practice/matterの保存scope
- sharing、retention、DLP

profile schemaは`references/profile-schema.md`。1つの巨大documentへ全stateを詰めず、company、user、practice、matter、registryを分離する。

## 完了

設定したside、top positions、deal-breaker、approvers、connections、seed coverage、pending reviewを短く示す。最初の候補として`review`、`renewal-tracker`、`amendment-history`を提示するが、自動開始しない。

## 失敗mode

- generic market termをteam positionとして保存しない
- sales/purchasingを混ぜない
- user roleをshared profileへ保存しない
- seed documentをfull readしたと偽らない
- setup完了、connection、legal reviewを実態より良く表示しない
- scheduled agent、hook、local fileを約束しない
