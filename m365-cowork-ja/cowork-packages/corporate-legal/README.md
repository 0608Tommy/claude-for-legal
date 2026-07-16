> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# コーポレート法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

M&Aデューデリジェンス、取締役会・株主総会、開示、クロージング、
ポストクロージング統合、法人管理を扱うskills-onlyパッケージです。

> **重要:** すべての分析、議事録、同意書、開示schedule、checklist、
> tracker、filing packageは、人によるレビューのためのドラフトです。法的助言、
> 送信、署名、承認、提出、登記、届出、決済、案件終了を自動実行しません。
> 日本法モジュールは **DRAFT / qualified Japanese counsel review pending**
> です。
>
> **本番運用上のblocker:** Microsoftの2026-06-22付Purview対応表では、
> CoworkのDLPとdata classificationは未対応です。SharePoint、OneDrive、
> Power Platform、connector等の保存・flow境界にはDLPを適用できますが、
> Cowork内のprompt/task自体がDLPで保護されるとは表示しません。Cowork内DLPが
> 必須なら、機密資料を投入せず本番導入を停止します。
>
> **State prerequisite:** 本ZIPはSharePoint list/library、state gateway、
> Power Platform solutionをprovisionしません。tenant-approved gatewayの
> live preflightが成功するまで、read-only/manual draft modeだけを使用し、
> setup完了、matter切替、checklist・entity・integration state更新を主張しません。

## 登録スキル

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `ai-tool-handoff` | direct | Luminance / Kira等への外部transfer gate、QA、判断層 |
| `board-minutes` | direct | 取締役会・委員会議事録のprecedent準拠draft |
| `deal-team-summary` | direct | board / deal lead / working team向けdiligence brief |
| `diligence-issue-extraction` | direct | VDRから日本法overlayを含む論点を抽出 |
| `material-contract-schedule` | direct | PA定義に基づくMaterial Contracts schedule |
| `tabular-review` | direct | typed schema、verbatim source付きbatch review |
| `written-consent` | direct | 会社法319条・370条・372条等を分けた同意・みなし決議draft |
| `closing-checklist` | SharePoint / Power Platform front end | 取引構造別のCP、届出、証憑、critical path |
| `entity-compliance` | SharePoint / Power Platform front end | 登記事項変更、機関運営、公告、税・社会保険・許認可 |
| `integration-management` | SharePoint / Power Platform front end | 構造別post-close workplan、consent、承継、届出 |
| `matter-workspace` | SharePoint / Power Platform front end | new、list、switch、close、noneとserver binding |
| `cold-start-interview` | admin config | 会社・利用者・実務・案件profileの初期設定 |
| `customize` | admin config | profileを1変更ずつ安全に更新 |

## Coworkでの使い方

スラッシュコマンドを実行する必要はありません。「VDRをレビューしたい」
「取締役会議事録をdraftしたい」「`--report --days 60`相当で法人期限を見たい」
のように依頼します。

移行元の `/corporate-legal:...`、`--new-deal`、`--module`、`--schema`、
`--template`、`--docs`、`--output`、`--sample`、`--init`、`--report`、
`--update`、`--from-report`、`--sweep`、`--audit`、`--export`、
`--format`、`--section`、`--deal`、`--rebuild` は正規の対応label・flagとして
保持し、Coworkでは会話stateへ変換します。

## 保存と分離

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、
ローカルファイルへ保存しません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・実務・利用者profile | SharePoint `profiles` document library |
| 案件資料、VDR、precedent、案件profile | SharePoint `matters` document library |
| review済み共有成果物 | SharePoint `outputs` document library |
| checklist、entity、integration、cursor、setup、session binding | SharePoint `state` list |
| 個人用draft | OneDrive |
| verification、approval、write、flow、error event | 追記専用SharePoint `audit` list |

stateは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
bindingは
`tenantId + practiceId + userObjectId + sessionId`
を正規keyとします。practice-levelはfresh sessionにbindingが存在しない状態で
表し、`matterId: null`のactive bindingは作りません。switchとnoneは新しい
Cowork sessionを要求し、closeは対象matterの全bindingをrevokeします。

## 法域レイヤー

- [移行元のoriginal-jurisdiction logic](references/original-corporate-logic.md)
- [日本法モジュール](references/jurisdictions/ja-jp/README.md)
- [日本の公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)
- [施行・改正watch](references/currency-watch.md)

日本法モジュールは会社法、金融商品取引法、JPX規則、独占禁止法、外為法、
商業登記、電子署名・電子帳簿、M&Aの承認・開示・closing、労働、個人情報、
知財、許認可、post-close integration、日本のlegal privilege差異を扱います。
法律、exchange rule、official guidance、soft law、契約、内部controlを分け、
将来施行・未施行の変更を現行義務として適用しません。

## Dataroom automation

移行元`dataroom-watcher`は本package内のagentやscheduleではありません。
[Power Platform automation compatibility contract](references/power-platform-automation-contracts.md)
に、別solution `corporate-dataroom-watcher`の`watch`、`full-grid`、
`closing-checklist-status`、および`doc-reader` / `extractor` /
`normalizer` / `grid-writer`分離を保持します。承認済みsolution、connection、
version、last runが確認できない限りscheduled behaviorを表示しません。

## Connectorとpackage境界

外部MCP候補は`connectors.draft.json`に隔離していますが、
`manifest.json`へ登録せず、生成ZIPにも含めません。宣言だけで
`connected`と扱わず、管理者同意、per-user consent、最小権限、保持、
保存・flow DLP、live probeが必要です。

## Package状態

`manifest.json`はUnified App Manifest 1.28のskills-only構成です。本番投入前に、
strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation test、Power Platform
solution test、移行元法域レビュー、日本法有資格者レビューが必要です。
