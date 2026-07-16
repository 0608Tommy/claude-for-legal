> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# プライバシー法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

PIA、DPA、DSAR相当の本人請求、処理トリアージ、規制ギャップ、ポリシーと実務のずれを扱うskills-onlyパッケージです。

> **重要:** すべての分析、DPA修正文案、通知文、本人向け回答、PIA、是正計画は、人によるレビューのためのドラフトです。法的助言、適法性認定、署名、外部送信、本人への回答、削除実行、規制当局への提出を行いません。日本法モジュールは **DRAFT / qualified Japanese counsel review pending** です。
>
> **本番運用上のblocker:** Microsoftの2026-06-22付Purview対応表では、CoworkのDLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、connector等の保存・flow境界にはDLPを適用できますが、Cowork内のprompt/task自体がDLPで保護されるとは表示しません。Cowork内DLPが必須なら、機密データを投入せず本番導入を停止します。
>
> **State prerequisite:** 本ZIPはskills-onlyで、SharePoint list/libraryまたは
> state gatewayをprovisionしません。tenant-approved gatewayのlive preflight
> が成功するまで、read-only/manual draft modeだけを使用し、setup完了、
> matter mutation、cursor更新、DSAR action実行を主張しません。

## 登録スキル

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `dpa-review` | direct | controller / processorの方向を確認し、DPAをplaybookと現行法に照らしてreview |
| `dsar-response` | direct | 本人請求を分類し、本人確認、探索、例外、確認通知・本回答をdraft |
| `pia-generation` | direct | house style、法定評価trigger、データフロー、リスク、条件をPIAへ整理 |
| `reg-gap-analysis` | direct | 新法・改正・guidanceと現状を分離して比較し、是正計画をdraft |
| `use-case-triage` | direct | `PROCEED / PIA REQUIRED / DPIA MANDATORY / STOP` を暫定分類 |
| `matter-workspace` | SharePoint / Power Platform front end | 案件作成、一覧、切替、終了、binding解除 |
| `policy-monitor` | SharePoint / Power Platform front end | scope別cursorでpolicy driftをsweepまたは個別確認 |
| `cold-start-interview` | admin config | 会社、利用者、DPA、PIA、DSAR、法域、保存先を設定 |
| `customize` | admin config | 実務プロファイルを1変更ずつ安全に更新 |

## Coworkでの使い方

スラッシュコマンドを実行する必要はありません。「DPAをレビューしたい」「本人請求の回答をdraftしたい」「`--sweep` 相当で前回以降を確認したい」のように依頼します。

移行元の `/privacy-legal:dpa-review`、`/privacy-legal:dsar-response`、`/privacy-legal:pia-generation`、`/privacy-legal:reg-gap-analysis`、`/privacy-legal:use-case-triage`、`/privacy-legal:matter-workspace new | list | switch | close | none`、`/privacy-legal:policy-monitor --sweep`、`/privacy-legal:cold-start-interview --redo | --check-integrations` は、正規の対応ラベル・flagとして保持し、Coworkでは会話状態へ変換します。

## 保存と分離

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、ローカルファイルへ保存しません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・実務・利用者プロファイル | SharePoint `profiles` document library |
| 案件資料・案件プロファイル | SharePoint `matters` document library |
| レビュー済み共有成果物 | SharePoint `outputs` document library |
| DSAR log、policy cursor、setup session、session–matter binding | SharePoint `state` list |
| 個人用draft | OneDrive |
| 検証、承認、write、flow、error event | 追記専用SharePoint `audit` list |

読取り・書込みは `tenantId + practiceId + userObjectId + sessionId + matterId` を必要な範囲で組み合わせます。createとupdateを分け、正確な`itemId`、最新`eTag`、一意な`idempotencyKey`を使います。matterが`archived`、bindingが`revoked`、期限切れ、矛盾、権限不明のいずれかならfail closedです。

## 法域と2026年改正

管轄は `request > matter > practice-profile > tenant-default` の順で解決します。

- [移行元のglobal / GDPR / USロジック](references/original-privacy-logic.md)
- [日本法モジュール](references/jurisdictions/ja-jp/README.md)
- [日本の公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)

2026年改正法案は2026-07-10に国会で成立し、2026-07-14に内閣が公布を決定しました。ただし2026-07-16確認時点で参議院議案ページの公布年月日・法律番号は空欄で、e-Gov上の施行も確認できません。したがって **成立済み・公布確認待ち・未施行** と扱い、16歳未満、特定生体個人情報、統計等の新例外、課徴金等を現行義務・現行例外として適用しません。

日本法モジュールは、個人情報保護法とPPCガイドライン、本人請求、漏えい等報告、越境、委託、Cookie・外部送信、通信の秘密、従業員・応募者、子ども、生体情報、マイナンバー、金融・医療・電気通信等のsectoral overlay、PIAの法的位置付けを分けて整理します。法律、official guidance、internal policyを混同しません。

## ConnectorとPower Platform

外部MCP候補は `connectors.draft.json` に隔離し、`manifest.json`には登録していません。宣言だけで「接続済み」と扱わず、管理者同意、per-user consent、最小権限、保持、保存・flow DLP、live probeが必要です。

`matter-workspace`と`policy-monitor`はSharePoint / Power Platform stateの対話front endです。scheduled flow、agent、hook、subagent、managed solutionは本パッケージに含みません。flowが存在しない場合、定期監視や通知が動くとは表示しません。

## Package状態

`manifest.json` はUnified App Manifest 1.28のskills-only構成です。本番投入前に、strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、tenant smoke test、SharePoint concurrency/isolation test、移行元法域レビュー、日本法有資格者レビューが必要です。
