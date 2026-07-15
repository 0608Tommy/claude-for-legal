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
8. **書込み失敗:** 正確な`itemId`、最新`eTag`、一意な`idempotencyKey`がない、binding競合、保持ポリシー不明なら停止する。ローカルフォルダを代替にしない。

保存、取得コンテンツ、Cowork DLP制約の詳細は
`references/common/cowork-runtime-contract.md` を必ず読む。

## 会話状態

| 状態 | 動作 |
|---|---|
| `new <slug>` | 短いintake後、SharePoint `matters` に案件レコードを作る |
| `list` | 権限のあるactive/archived案件を一覧表示 |
| `switch <slug>` | server-side session–matter bindingを変更 |
| `close <slug>` | 保持したまま`archived`へ状態変更 |
| `none` | bindingを解除しpractice-level contextへ戻す |

意図がない場合は5状態を提示する。`$ARGUMENTS` やローカルファイルを参照しない。

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
3. 現在案件→新案件の変更と、読み込まれるプロファイル要約を示す。
4. 人の確認後にserver-side bindingを条件付き更新する。
5. auditへ旧・新matter ID、実行者、時刻を追記する。

別案件のキャッシュ・引用・資料を新案件へ持ち込まない。

## `close <slug>`

「終了」は削除ではない。

1. active matterと一致するか確認する。
2. 未保存ドラフト、未完了タスク、legal hold、retention、共有リンクを確認する。
3. 終了日・理由・承認者を提示する。
4. 明示確認後、`status: archived` とする。
5. activeだった場合はbindingを`none`へ変更する。
6. auditに追記する。

保持期間満了後の削除は本スキルの範囲外。

## `none`

現在のbindingを示し、解除後はpractice-level資料だけを使うことを説明する。確認後にbindingを解除し、案件資料を以後の会話へ引き継がない。

## Cross-matter

`crossMatterAccess: false` が既定。`true`でも、「過去5案件を比較」等の明示依頼がある場合だけ、許可された案件を列挙し、各案件のconfidentialityと目的を確認する。clean-teamまたは依頼者間の共有禁止があれば拒否する。

## 完了

変更したmatter ID、binding、status、保存先、未解決のconflict/retention事項を示す。案件内容の実質レビューを自動開始しない。

## 本スキルが行わないこと

- conflicts checkまたは受任判断
- retention期限後の削除
- substantive legal review
- cross-matter共有の適切性判断
- 成果物の外部送信
