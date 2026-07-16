---
name: customize
description: >
  corporate practice profileを1項目ずつ安全に変更する。会社情報、Japan entity/organ、M&A materiality、board precedent、FIEA/JPX、entity、matter、integration、保存・接続設定をcurrent→proposed→impact→confirmでexact SharePoint recordへ反映する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Corporate profile customization

旧来の参照labelは
`/corporate-legal:customize [section name, or describe what you want to change]`。

## 目的

full setupをやり直さず、profile/stateの1 changeをreviewして反映する。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、state gatewayをlive
   preflightする。失敗時はread-only change planで停止する。
2. exact company/corporate practice/user profileをcanonical keyで読む。
   missing、paused、substantive `[PENDING]`ならcold-startを案内する。
3. company、corporate practice、user、matter/deal、stateのscopeを判定する。
   matter secretをshared profileへ入れない。
4. matter/deal-specific changeはactive authorized unexpired bindingとmatter
   `status: active`を要求する。archived/revokedでは拒否する。
5. entity form、organ、law、threshold、deadline、FIEA/JFTC/FEFTA/APPI amendment、
   licence statusを変える場合はcurrent official sourceを確認する。
6. viewer、retention、legal hold、clean-team、保存・flow DLPを確認する。
7. legal position、materiality、approval threshold、trust level、日本法review
   statusを人のreviewなしに緩和しない。
8. section/history/auditをdeleteしない。廃止はstatusとimpactを記録する。
9. 一度に1 change。複数changeはqueueにし、each changeにfresh confirmationと
   separate idempotencyを使う。
10. exact `itemId`、latest`eTag`、unique`idempotencyKey`でconditional update。
    stale/partialでは停止し再読取りする。
11. Cowork内DLP必須なのにproduction enabledへ変更する依頼は拒否する。

provenanceは
`references/common/source-provenance-and-review.md`、
Japan statusは
`references/common/currency-watch.md`を使う。

## 会話state

`select-section` → `show-current` → `collect-new` → `verify-source` →
`check-consistency` → `explain-impact` → `confirm` →
`conditional-update` → `audit`

confirmation前にwriteしない。success後に次changeを自動開始しない。

## Customizable map

`references/profile-fields.md`を使い、current valueを1行で示す。

- Company / organization
- User / attorney route
- Active modules
- Japan entity/governance
- M&A / materiality / VDR / AI handoff
- Board / minutes / consent precedent
- Public Company / FIEA / JPX
- Entity compliance
- Closing / integration
- Matter / clean-team
- Integrations / storage / DLP
- Outputs / reviewer / dashboard

## Impact examples

- internal contract threshold ¥250m→¥500m:
  future diligence triageが変わる。PA definition/statutory threshold、existing
  findings/scheduleは自動変更しない。
- `art370Authorized: false→true`:
  articles exact amendment/effective/registrationを確認するまでprofile factとして
  確定しない。
- public module on:
  EDINET/TDnet/FIEA fieldsを追加する。Form 4/§16 defaultを追加しない。
- AI trust `full re-review→spot-check`:
  sensitive/legal conclusionのfull verification gateを解除しない。
- entity source item変更:
  entity compliance rebuild candidateになるが、自動rebuildしない。
- matter isolation on:
  server ACL/binding/gatewayが必要。profile flagだけで分離済みと表示しない。
- `ja-JP`追加:
  Japan draft moduleを適用するがqualified review completeにならない。
- policy says Cowork DLP mandatory:
  production enabledをfalse/blockerへ変更する。

## Consistency

flag:

- Japan entityなのにentity form/organ/articlesなし
- board skill activeだがminutes/consent precedentなし
- Art. 370 enabledだがarticles evidenceなし
- public listedだがEDINET/TDnet/insider ownerなし
- M&A activeだがtransaction structure/deal intake fieldなし
- internal materialityをstatutory thresholdとして保存
- JFTC/FEFTA/FIEA thresholdがsource/dateなし
- APPI 2026 amendmentをeffectiveと保存
- 2026 Companies Act proposalをcurrent lawと保存
- matter isolation onだがcross-matter default true
- Cowork DLP mandatoryだがproduction enabled

どちらを直すか人に選んでもらう。

## Guardrail degradation

次は無効化しない。

- `[review]`, provenance tag, current-law check
- no fabricated authority/quote
- user/session/matter isolation
- expiring bindingとfresh-session practice mode
- archived/revoked rejection
- switch/noneのnew-session requirement
- close時全binding revoke
- destination/privilege/clean-team check
- board/consent/filing/materiality/security gate
- large-input coverage
- recoverable-error bias/severity floor
- no autonomous send/sign/file/approve/close
- exact ID/eTag/idempotency/create-update separation
- immutable canonical audit
- Cowork DLP blocker

削除依頼は拒否し、目的を満たす安全なadjustmentを提案する。

## Write

1. exact current record/latest`eTag`を再取得。
2. current→proposed exact diff。
3. source/currencyとdownstream impact。
4. destination/viewer/retention/DLP。
5. `Confirm this one change? yes/no`。
6. conditional update。
7. item ID、old/new eTag、idempotency、review statusをaudit。

company-levelはcompany profile、corporate-specificはcorporate practice、user
role/contactはuser profile、deal/matterはmatter/deal record、tracker/cursorはstate。

## Complete

> 変更を保存しました。次回の出力から反映されます。既存のminutes、consent、
> diligence finding、schedule、checklist、entity、integration recordは自動更新して
> いません。

gateway failure時は「保存しました」と言わず、change planとblockerを示す。

## 行わないこと

- full setupをsilent overwrite
- multiple changesのbatch approval
- matter secretをshared profileへ移す
- law/effective statusをuser assertionだけで変更
- guardrail/counsel pending statusを解除
- existing artifacts/trackersを自動rebuild
- local configを編集
