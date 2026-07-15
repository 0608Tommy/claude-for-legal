> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 商事契約法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

売り手側・買い手側の実務プレイブックに沿って、vendor agreement、NDA、SaaS subscription、変更契約、更新期限、承認経路、事業部向け要約を扱うskills-onlyパッケージです。

> **重要:** すべての出力は、人によるレビューのためのドラフトです。法的助言、署名可否の最終判断、リスク受諾、契約相手への送信、契約締結、更新・解約の実行を行いません。日本法モジュールは **DRAFT / qualified Japanese counsel review pending** です。
>
> **本番運用上の制約:** Microsoftの2026-06-22付Purview対応表では、CoworkのDLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、接続先等の保存・flow境界にはDLPを適用できますが、Cowork内のprompt/task自体がDLPで保護されるとは表示しません。Cowork内DLPが必須なら、本番導入を停止します。

## 登録スキル

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `amendment-history` | Cowork | 基本契約と変更契約を時系列化し、現行条項を追跡 |
| `cold-start-interview` | admin config | 会社、利用者、両側プレイブック、承認経路、保存先を設定 |
| `customize` | admin config | 実務プロファイルを1変更ずつ安全に更新 |
| `escalation-flagger` | Cowork | 論点を承認matrixへ当て、送信前の依頼文をdraft |
| `matter-workspace` | SharePoint / Power Platform front end | 案件作成、一覧、切替、終了、binding解除 |
| `renewal-tracker` | SharePoint / Power Platform front end | 更新・解約通知期限の登録、検索、missed-window確認 |
| `review` | Cowork | 文書構造を判定し、NDA / vendor / SaaSを単一memoでレビュー |
| `review-proposals` | SharePoint / Power Platform front end | deviation由来のplaybook提案を1件ずつ承認・却下・編集・保留 |
| `stakeholder-summary` | Cowork | 法務レビューを200語以内相当の事業部向け要約へ変換 |

`nda-review`、`vendor-agreement-review`、`saas-msa-review` は登録しません。移行元の判断手順、出力、safety gateは `review` のskill-local referencesへ統合しています。

## Coworkでの使い方

スラッシュコマンドを実行する必要はありません。「契約をレビューしたい」「次の180日を見る」「`--missed` 相当で確認」「案件を切り替えたい」のように依頼します。

旧来の `/commercial-legal:review`、`/commercial-legal:renewal-tracker --days 180`、`--horizon 180`、`/commercial-legal:cold-start-interview --side purchasing` 等は、移行元との対応を示す正規の参照ラベルとして保持します。Coworkでは会話状態へ変換されます。

## 保存と分離

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、ローカルファイルへ保存しません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・実務プロファイル | SharePoint `profiles` document library |
| 案件資料・案件プロファイル | SharePoint `matters` document library |
| 契約レビュー、承認済み共有成果物 | SharePoint `outputs` document library |
| 更新register、deviation、proposal、session–matter binding | SharePoint `state` list |
| 個人用draft | OneDrive |
| 検証、承認、write、flow event | 追記専用SharePoint `audit` list |

読取り・書込みは `tenantId + practiceId + userObjectId + sessionId + matterId` を必要な範囲で組み合わせ、正確な`itemId`、最新`eTag`、一意な`idempotencyKey`を使います。案件が曖昧、権限が不明、bindingが矛盾する場合はfail closedです。

## 法域

管轄は `request > matter > practice-profile > tenant-default` の順に解決します。

- [移行元の米国・global契約ロジック](references/original-commercial-contract-logic.md)
- [日本法モジュール](references/jurisdictions/ja-jp/README.md)
- [日本の公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)

日本法モジュールは民法、電子署名法、電子消費者契約法、個人情報保護法、中小受託取引適正化法（取適法）、フリーランス・事業者間取引適正化等法、消費者契約法、特定商取引法、独占禁止法、不正競争防止法等を整理します。法律、行政guidance、内部playbookを明確に分離し、日本法有資格者レビューが記録されるまで`pending`です。

## ConnectorとPower Platform

外部MCP候補は `connectors.draft.json` に隔離し、`manifest.json`には登録していません。宣言だけで「接続済み」と扱わず、テナント管理者の同意、最小権限、保持、DLP、ライブprobeが必要です。

`matter-workspace`、`renewal-tracker`、`review-proposals` はSharePoint / Power Platform stateの対話front endです。scheduled flowやmanaged solutionは本パッケージに含みません。flowが存在しない場合でも手動対話はできますが、定期監視・通知が動くとは表示しません。

移行元`deal-debrief`、`playbook-monitor`、`renewal-watcher`との互換state・safety behaviorは[Power Platform automation compatibility contracts](references/power-platform-automation-contracts.md)に保持しています。

## Package状態

`manifest.json` はUnified App Manifest 1.28のskills-only構成です。本番投入前に、strict validator、Microsoft公式manifest validation、tenant smoke test、SharePoint concurrency test、Power Platform solution test、移行元法域レビュー、日本法有資格者レビューが必要です。
