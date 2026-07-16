---
name: matter-workspace
description: >
  複数依頼者・案件のコンテキストを分離する。SharePoint上の案件を会話で新規作成、一覧、切替、終了、practice-levelへ解除し、サーバー側session–matter bindingと保持・アクセス制御を管理する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# 案件ワークスペース

旧来の参照ラベルは `/ai-governance-legal:matter-workspace`。Coworkでは `new | list | switch | close | none` を実行コマンドではなく会話状態として選ぶ。

## 目的

private practice等で、ある依頼者・案件の資料、判断、出力が別案件へ漏れないようにする。in-houseで単一組織だけを扱う設定では既定で無効であり、practice-level contextを使う。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` の `matterWorkspaces.enabled` と、複合キーが一致する現在利用者の`user-profile`を確認する。`false`ならエラーにせず、単一組織のpractice-level運用であることを説明する。別利用者のroleまたはbindingを流用しない。
2. **案件・権限:** サーバー側session–matter bindingを唯一のactive sourceとし、表示名や会話履歴だけで案件を推測しない。作成・切替対象への権限を確認する。
3. **管轄:** 案件の法域は `request > matter > practice-profile > tenant-default` で使われる。新規案件で法域が不明なら未指定のまま実質作業を開始しない。
4. **情報源:** 案件事実、当事者名、法域、confidentialityを利用者または権限あるmatter recordから取得する。別案件の値を補完に使わない。
5. **秘匿性・宛先:** confidentiality、clean-team、閲覧者、DLP、保持、legal holdを確認する。cross-matter accessの既定値は`false`。
6. **人のレビュー:** conflicts check、依頼受任、案件終了、保持・廃棄判断は人の責任。作成したworkspaceは受任またはconflict clearanceを意味しない。
7. **不可逆操作:** `close`、共有範囲変更、archive、active binding変更は差分と影響を示し、明示確認後に行う。削除しない。
8. **Create / update:** `new`とfresh-session bindingはcanonical key、
   `expectedAbsent: true`、一意な`idempotencyKey`でcreateし、架空の
   create対象自身の`itemId` / `eTag`を要求しない。fresh-session bindingだけは
   target matterのexact `itemId`、current token、expected active statusを追加し、
   gatewayがbinding absenceとatomically評価する。archive / revokeはexact
   `itemId`、latest `eTag`、一意な`idempotencyKey`でupdateし、
   `expectedAbsent`を含めない。競合、保持ポリシー不明なら停止し、
   ローカルフォルダを代替にしない。
9. **Binding lifecycle:** binding identityとmatterは作成後に変更せず、
   current `active`から完全なrevocation metadata付き`revoked`への一方向遷移
   だけを許可する。同一sessionのmatter差替え、再有効化、第三のstatus追加を行わない。

保存、取得コンテンツ、Cowork DLP制約の詳細は
`references/common/cowork-runtime-contract.md` を必ず読む。

## 会話状態

| 状態 | 動作 |
|---|---|
| `new <slug>` | 短いintake後、SharePoint `matters` に案件レコードを作る |
| `list` | 権限のあるactive/archived案件を一覧表示 |
| `switch <slug>` | current bindingをrevokeし、fresh sessionでnew bindingをcreate |
| `close <slug>` | matterをfenceし、active bindingだけをrevoke（already-revokedはsatisfied）、zero active確認後に`archived`へfinalize |
| `none` | current bindingをrevokeし、fresh sessionをbindingなしで開始 |

意図がない場合は5状態を提示する。旧ランタイムの引数変数やローカルファイルを参照しない。

## `new <slug>`

slugは小文字英数字とhyphenで構成し、例は `acme-ai-review-2026`。同一tenant・practice内のactive/archived両方で重複を確認する。

取得:

- Client / represented party
- Counterparty
- Matter type: `use case | vendor AI review | AIA | regulatory change | policy project | other`
- Confidentiality: `standard | heightened | clean-team`
- Key facts（2～5文）
- Matter-specific overrides
- Related matters
- Jurisdictions
- Retention / legal hold / DLP
- Authorized viewers

作成しても自動切替しない。「この案件へ切り替えるか」を別に確認する。テンプレートは `references/matter-records.md`。

## `list`

権限のある案件だけを表示する。

| Slug | Client | Matter type | Status | Opened | Active | Jurisdictions |
|---|---|---|---|---|---|---|

activeはサーバー側bindingから`*`を付ける。archivedは別表にする。機密案件名を閲覧権限のない利用者へ存在だけでも漏らさない。

## `switch <slug>`

1. 正確なmatter recordとstatusを取得する。
2. 閲覧権限、confidentiality、legal holdを確認する。
3. current bindingを固定複合キー、exact `itemId`、latest `eTag`で再取得する。
4. 旧→新matter、破棄するcontext、fresh session requirementを示す。
5. 人の確認後、current bindingを`revoked`へ条件付きupdateして現在の会話を停止する。
6. 新しいCowork conversationのfresh sessionで、binding不在を確認してからnew
   matter bindingを`expectedAbsent: true`でconditional createする。target
   matterのexact `itemId`、latest `eTag` / `version`または
   `bindingGeneration`、`expectedStatus: active`をmatter preconditionとし、
   gatewayがbinding absenceと同一transactionで評価できなければ停止する。
7. revokeとcreateを別audit eventにし、同じ`correlationId`で関連付ける。
   old/new matter ID、old/new session ID、actor、各idempotency key、結果を残す。

別案件のキャッシュ・引用・資料・draft・cursorを新案件へ持ち込まない。
verified hard context resetが提供・検証されるまで同一session switchを許可しない。
利用者がfresh sessionを開始しなければnew bindingを作らず、旧bindingはrevokedの
ままにする。

## `close <slug>`

「終了」は削除ではない。

1. exact active matter、latest `eTag` / `version`、現在の
   `bindingGeneration`を取得する。
2. 未保存ドラフト、未完了タスク、legal hold、retention、共有リンクを確認する。
3. 終了日・理由・承認者、fence方法、下流影響を提示して明示確認を得る。
4. 最初のatomic conditional operationでmatterを`close-pending`等のnon-active
   stateへtransitionし、必要に応じて`bindingGeneration`も増やしてnew binding
   createをfenceする。fence失敗時は列挙・revocationへ進まない。
5. fence成功後、その`matterId`を参照する全bindingをexact queryし、各
   `itemId` / `eTag`を取得する。列挙が不完全または権限不明ならfenced stateの
   ままfail closedで停止する。
6. 列挙結果をstatusで分ける。`active`だけをrevocation対象とし、
   既に`revoked`のbindingはsatisfiedとして数える。revoked bindingを再更新しない。
7. statusが`active`のbindingだけを、各exact `itemId` / latest `eTag`で
   `revoked`へconditional updateする。revocation reason、actor、各結果を
   同じclose `correlationId`でauditする。
8. 対象matterの全bindingを再度exact queryし、active bindingが0件であることを
   確認する。zero active確認後だけpost-fence matterのexact `itemId` / latest
   `eTag`で`status: archived`へconditional finalizeする。
9. 列挙漏れ、stale write、partial success、revocation failure、finalize failureが
   1件でもあればfenced stateを維持してfail closedとし、block eventを残し、
   close完了を表示せず、matterへの実質アクセスを拒否する。
10. fence前にcommitしたcreateはstep 5のenumerationで捕捉され、fence後のcreateは
    atomic matter preconditionで失敗する。current bindingがactive revocation対象
    なら現在の会話を停止する。

保持期間満了後の削除は本スキルの範囲外。

## `none`

現在のbindingと破棄するcontextを示す。確認後、current bindingを`revoked`へ
条件付きupdateして現在の会話を停止する。practice-levelは新しいCowork
conversationのfresh sessionでbinding不在を確認して開始する。第三のbinding
statusを作らず、verified hard context resetなしに同一sessionでmatterless作業へ
続行しない。

## Cross-matter

`crossMatterAccess: false` が既定。`true`でも、「過去5案件を比較」等の明示依頼がある場合だけ、許可された案件を列挙し、各案件のconfidentialityと目的を確認する。clean-teamまたは依頼者間の共有禁止があれば拒否する。

## 完了

変更したmatter ID、binding、status、itemId/eTag、保存先、audit outcome、
未解決のconflict/retention事項を示す。DRAFTのstate contractまたはflowが
導入済みと推測せず、案件内容の実質レビュー、switch後のbinding create、
close、共有、送信を自動開始しない。

## 本スキルが行わないこと

- conflicts checkまたは受任判断
- retention期限後の削除
- substantive legal review
- cross-matter共有の適切性判断
- 成果物の外部送信
