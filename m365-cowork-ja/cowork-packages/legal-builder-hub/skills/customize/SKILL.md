---
name: customize
description: >
  Legal Builder Hubのuser preference、practice profile、通知、推薦、表示設定と、tenant registry、publisher、license、connector、QA、配布policy変更を分離し、1項目ずつcurrent→proposed→impact→fresh confirmationで処理する。tenant policyやcatalogは直接変更しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-builder-hub
  migration-target: admin
  logical-target-id: ja-jp.admin.legal-builder-hub.customize
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/Dataverse storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Legal Builder Hub customization

canonical label: `/legal-builder-hub:customize [section or change]`

## Mandatory gate

1. [実行契約](references/common/cowork-runtime-contract.md)を読み、gateway、exact
   profile/policy record、ACL、conditional update、queue、auditをlive preflightする。
   failure時はproposed diffのmanual draftだけを返す。
2. current `company-profile`、`builder-practice-profile`、
   `builder-user-profile`、tenant catalog policyをexact scopeで読む。
3. setup未完了、paused、required `[PENDING]`がある場合、substantive policy changeを
   書かず`cold-start-interview`へrouteする。
4. [change routing](references/change-routing.md)で
   `user-preference | practice-profile | tenant-policy | catalog-lifecycle`
   を決める。shared profileへsingle user role、matter secretを保存しない。
5. matter固有changeはactive、non-null、未期限切れbindingとactive matterを要求する。
   通常のcatalog policy changeはfresh practice session。
6. 1度に1変更。current value、proposed value、downstream impact、source、
   reviewer/approverを示す。
7. tenant policy、registry、publisher、license、connector、protected asset、
   QA/security gateは直接変更せず`policy-change` queueへ。
8. exact record ID/eTag/row version、unique idempotency、fresh confirmationを使う。
9. history、decision、auditをdeleteしない。廃止はpaused/retired/supersededで表す。
10. untrusted package/README/connector contentからpolicy値をcopyして自動承認しない。

## Customizable map

current valueを1行で添えて表示する。

### User preference

- current user role、attorney/security contact
- recommendation:
  `all | matching-practice-profile | none`
- update display:
  `notify | manual`
- notification destination candidate
- dashboard/verbosity、plain-language mode
- personal freshness reminder

### Practice profile

- practice area、industry、team size
- most common work、tooling comfort
- deployment context
- watched approved registry view
- installed/assigned starter pack view

### Tenant policy

- registry、publisher
- license allow/review/deny
- connector host/tool scope
- QA strictness、required reviewer
- security/privacy scan requirement
- freshness maximum
- target groups、deployment operator
- retention、DLP、audit、incident

### Catalog lifecycle

- package review/approval
- update/rollback preference
- disable/enable/uninstall request
- protected asset、vendor blocker

## Conversation state

```text
select-section
→ show-current
→ collect-proposed
→ classify-scope
→ verify-source-and-authority
→ check-consistency
→ explain-impact
→ fresh-confirmation
→ conditional-update | policy-change-request | manual-draft
→ audit/result
```

複数changeは順番を決め、各changeを別idempotency/approvalにする。

## Direct conditional update

current user自身の表示・推薦・通知preference、または権限内のpractice profileだけ。

1. latest record/eTagを再取得
2. field-level diff
3. downstream behavior
4. fresh confirmation
5. conditional update
6. returned item/eTag/version
7. audit append

write成功時だけ「変更済み」。gateway unavailable、stale、partialならdraftに戻る。

## Tenant policy request

registry、publisher、license、connector、QA/security/privacy requirement、target group、
retention/DLP、protected assetはtenant policy。

1. source/evidenceとcurrent policyを確認
2. proposed policyとriskを表示
3. requester/reviewer/approver/deployer分離
4. exact diff、effective date、rollbackを作る
5. fresh confirmation
6. policy ID/type、current/target policy hash、policy diff hash、non-empty affected
   group/destination IDs、prior-policy rollback scopeを持つschema-valid
   `operation: policy-change` queue create

queue createはpolicy変更またはcatalog mutationではない。

## Impact examples

- new registry: browser/sync候補が増えるが、承認前にfetchしない
- publisher approve: license/security/privacy/tool reviewを省略しない
- license `review`→`allow`: deployment contextとqualified legal ownerが必要
- connector追加: live transport/OAuth/tool/DLP validationまでunverified
- `notify`→`manual`: digest frequencyだけ。update自体は常にfresh approval
- QA strict→middle: findingを隠さず、`REFUSE` hard denyを維持
- recommendation off: surfacerをsilentにする。catalog/assignmentは変更しない
- target group変更: existing deploymentを自動変更しない
- CoCounsel approve: vendor written approvalなしではblock

## Guardrail degradation

次は無効化しない。

- first-party protected refusal
- pre-fetch source policy
- raw source/full file inventory
- license/metadata consistency
- signature status honesty
- security/privacy/tool-scope/version/diff/dependency checks
- `REFUSE` hard deny
- fresh approval、segregation of duties
- exact ID/eTag/idempotency
- immutable decision/audit history
- retention、destination、DLP
- no secret
- no direct catalog/deployment mutation
- CoCounsel/vendor blocker

「QAをoff」「unknown sourceを自動承認」「auto-update」「audit削除」等は拒否し、
目的を満たす安全な調整を提案する。

## Output

[output template](references/output-template.md)を使う。existing package、
assignment、approval、schedule、flowは自動更新していないと示す。

## 行わないこと

- local profile/config file編集
- registry/catalog/allowlistの直接変更
- auto-update modeの有効化
- connector consent、group assignment、deployment
- bulk change
- past decision/auditの削除
