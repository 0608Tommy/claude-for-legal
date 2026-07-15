> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# AIガバナンス法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

AIユースケースのトリアージ、AIシステム台帳、AI影響評価（AIA）、ベンダーAI条項レビュー、規制ギャップ分析、AIポリシーの作成・更新を支援する日本語版パッケージです。

> **重要:** すべての出力は、人によるレビューのためのドラフトです。法的助言、適法性の保証、導入承認、署名・提出・送信の判断を行いません。日本法モジュールは **DRAFT / qualified Japanese counsel review pending** であり、承認済みとは扱えません。
>
> **本番運用上の制約:** Microsoftの2026-06-22付Purview対応表では、CoworkのDLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform等の保存・flow境界にはDLPを適用しますが、Cowork内のprompt/task自体がDLPで保護されるとは表示しません。Cowork内DLPが必須要件なら、本パッケージを本番導入しません。

## 移行版の特徴

- Microsoft 365 Copilot Cowork の会話から各スキルを選択します。スラッシュコマンドを実行する前提はありません。
- 旧来の `/ai-governance-legal:...` 表記は、移行元との対応を示す正規の参照ラベルとしてのみ保持します。
- ローカルファイルには書き込みません。プロファイル、案件、台帳、監査ログ、成果物は `references/cowork-runtime-contract.md` に従い SharePoint / OneDrive に保存します。リポジトリ全体の正本はビルド時に `../../shared/storage-contract.json` と照合します。
- 管轄は `request > matter > practice-profile > tenant-default` の順で解決し、不一致または曖昧さが残る場合は処理を停止します。
- 元の米国・EU中心の法域ロジックは日本語で保持し、プロファイルで `ja-JP` が選択された場合だけ `references/jurisdictions/ja-jp/` の日本法ドラフトを追加適用します。
- 外部MCPは任意です。利用にはテナント管理者による接続・同意・権限設定が必要です。

## スキル

| ID | 表示名 | 主な用途 |
|---|---|---|
| `ai-inventory` | AIシステム台帳 | システム単位の役割、リスク区分、見直し期限を管理 |
| `aia-generation` | AI影響評価 | インテーク、法規制分類、リスク・対策、承認条件を文書化 |
| `cold-start-interview` | 初期設定インタビュー | 実務プロファイル、規制範囲、レッドライン、保存先を構成 |
| `customize` | プロファイル調整 | 設定全体をやり直さず、1項目ずつ変更 |
| `matter-workspace` | 案件ワークスペース | 複数依頼者・案件の分離、切替、終了 |
| `policy-monitor` | AIポリシー監視 | 実務とポリシーのずれを定期または個別に確認 |
| `policy-starter` | AI利用ポリシー初稿 | 公開された公式資料等を根拠に採用前ドラフトを作成 |
| `reg-gap-analysis` | 規制ギャップ分析 | 新しい法令・指針と現状を比較し、是正計画を作成 |
| `use-case-triage` | ユースケース・トリアージ | `APPROVED / CONDITIONAL / NOT APPROVED` の暫定分類 |
| `vendor-ai-review` | ベンダーAIレビュー | 学習利用、秘密保持、知財、責任、変更通知等を比較 |

## 初回利用

1. Coworkで「`cold-start-interview` を開始したい」と依頼します。
2. クイック設定またはフル設定を選びます。
3. 既存のAIポリシー、過去のAIA、主要ベンダー契約、AI台帳があれば、権限を確認してSharePointの正確なアイテムを指定します。
4. 保存前に、保存先、保持・DLP、アクセス範囲、`itemId`、`eTag`、`idempotencyKey` を確認します。
5. 日本を対象法域に含める場合、プロファイルの管轄モジュールに `ja-JP` を指定します。

## 保存先

| 情報 | Microsoft 365 保存先 |
|---|---|
| 会社・実務プロファイル | SharePoint `profiles` ライブラリ |
| 案件資料・案件テンプレート | SharePoint `matters` ライブラリ |
| AI台帳、レジストリ、トラッカー、セッションと案件の対応 | SharePoint `state` リスト |
| レビュー済み共有成果物 | SharePoint `outputs` ライブラリ |
| 個人用ドラフト | OneDrive |
| 検証・自動処理イベント | 追記専用 SharePoint `audit` リスト |

共有成果物への昇格、外部送信、承認、署名、公開、案件終了などの不可逆操作は、明示的な人の確認後にだけ行います。

## 法域レイヤー

- `references/original-jurisdiction-logic.md`: 移行元の法域認識、EU AI Act、米国法上の privilege / work product、情報源タグ等を忠実に日本語化した基礎レイヤー。
- `references/jurisdictions/ja-jp/`: 日本法の追加モジュール。公式一次資料を記録し、確認日を `2026-07-16` としています。

異なる法域が同時に関係する場合、最も都合のよい法域を選びません。各法域を分けて示し、矛盾する義務または適用関係の曖昧さは `[review]` として有資格者に回します。

## パッケージ状態

`manifest.json` はMicrosoft 365 Unified App Manifest 1.28のskills-only構成です。remote MCPは1.28/1.29のschema・認証差異がテナントで確認できるまで `connectors.draft.json` に隔離し、packageへ登録しません。コンテンツは本番投入前に、厳格なホスト検証、Microsoft公式検証、テナント・スモークテスト、移行元法域レビュー、日本法有資格者レビューを通す必要があります。
