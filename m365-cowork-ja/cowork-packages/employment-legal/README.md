> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 雇用労務法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

採用、雇用契約、労働者性、賃金・労働時間、休暇、解雇・雇止め、社内調査、
就業規則、海外雇用を扱うskills-onlyパッケージです。

> **重要:** すべての分析、checklist、memo、policy、通知案、trackerは、人による
> レビューのためのドラフトです。採用、懲戒、解雇、退職勧奨、給与・保険・福利厚生、
> 休暇・合理的配慮、調査結論、外部送信、届出を自動決定・実行しません。
> 日本法モジュールは **DRAFT / qualified Japanese counsel review pending** です。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表では、Coworkの
> DLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、
> connector等の保存・flow境界へDLPを適用しても、Cowork内prompt/taskがDLPで
> 保護されるとは表示しません。Cowork内DLPが必須なら機密資料を投入せず、本番導入を
> 停止します。
>
> **State prerequisite:** tenant-approved state gateway、SharePoint
> list/library、ACL、監査、Power Platform solutionは本ZIPに含みません。live
> preflight成功まではread-only/manual draft modeに限定し、setup、matter切替、
> leave・investigation・expansion stateの保存やautomation実行を主張しません。

## 登録スキル — exactly 18

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `cold-start-interview` | admin | 日本の事業場・就業規則・36協定・労使・保険・移民を含む初期設定 |
| `customize` | admin | profile/stateを1変更ずつ安全に更新 |
| `expansion-kickoff` | direct | EOR/entity前の適法性gateと海外雇用project開始 |
| `expansion-update` | Power Platform front end | dependency trackerのread/update |
| `handbook-updates` | direct | handbook/就業規則の差分・波及・届出確認 |
| `hiring-review` | direct | 労働条件通知書・雇用契約・採用規制review |
| `investigation-open` | Power Platform front end | restricted investigation matterとsource checklist作成 |
| `investigation-add` | Power Platform front end | evidence、interview note、coverageの追加 |
| `investigation-query` | direct | investigation logへの根拠付きQ&A |
| `investigation-memo` | direct | 内部調査memoのdraft/update |
| `investigation-summary` | direct | HR・leadership・outside counsel向けaudience stripping |
| `leave-tracker` | Power Platform front end | 日本の休業・休暇・配慮のdecision-point review |
| `log-leave` | Power Platform front end | leave caseの最小限登録 |
| `matter-workspace` | Power Platform front end | new、list、switch、close、noneとrestricted isolation |
| `policy-drafting` | direct | 就業規則該当性を確認したpolicy draft |
| `termination-review` | direct | 解雇・懲戒・雇止め・退職・整理解雇review |
| `wage-hour-qa` | direct | 賃金、労働時間、36協定、最低賃金Q&A |
| `worker-classification` | direct | 労働者性、freelancer、派遣・請負・EOR review |

`internal-investigation`と`international-expansion`は登録しません。前者の
five-mode behaviorは5つの`investigation-*` caller、後者のEOR/entity、
dependency、outside-counsel behaviorは`expansion-kickoff`と
`expansion-update`のskill-local referencesへcompileしています。

## Coworkでの使い方

スラッシュコマンドを実行する必要はありません。「東京の固定期間契約をreview」
「調査案件を開く」「育児休業caseを登録」「Germany expansionを開始」のように
依頼します。移行元の`/employment-legal:...`、`--full`、`--redo`、
`--redo <section>`、`--check-integrations`、および
`matter-workspace new | list | switch | close | none`は正規label/flagとして保持し、
Coworkでは会話stateへ変換します。

## 保存・分離・state

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、local
filesystemを保存先にしません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・実務・利用者profile | SharePoint `profiles` document library |
| restricted employment matterとsource documents | SharePoint `matters` document library、item-level ACL |
| review済み共有成果物 | SharePoint `outputs` document library |
| leave、investigation、expansion、cursor、setup、binding | SharePoint `state` list |
| 個人draft | OneDrive |
| verification、approval、write、flow、error | 追記専用SharePoint `audit` list |

state keyは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
binding keyは
`tenantId + practiceId + userObjectId + sessionId`です。practice-levelはfresh
sessionにbindingが存在しない状態で表し、`matterId: null`のactive bindingを
作りません。switch/noneは新しいsessionを要求し、closeは対象matterの全bindingを
revokeします。

一般matter workspaceがoffでも、investigation、whistleblowing、medical/
accommodation、leave、discipline、terminationはrestricted matterとして
分離できます。central indexはpseudonymousにし、identity mappingと実質記録を
restricted matter内へ置きます。

## 日本法レイヤー

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [一次資料台帳](references/jurisdictions/ja-jp/source-register.md)
- [施行日watch](references/currency-watch.md)
- [移行元behavior](references/original-employment-logic.md)

2026-07-16 JST時点の一次資料を基礎に、労働基準法、労働契約法、職業安定法、
男女雇用機会均等・harassment、障害者雇用・合理的配慮、育児介護休業、
派遣・労働者供給、Freelance Act、賃金・労働時間・36協定・最低賃金、労安衛、
APPI/monitoring、公益通報、社会保険、労組・高年齢者、就業規則、解雇/RIF、
EOR・移民を扱います。binding law、statutory guidance、administrative guidance、
internal controlを分け、2026-10-01と2026-12-01の将来施行を早期適用しません。

## Leave automation

[Power Platform互換contract](references/power-platform-automation-contracts.md)は、
別solution `employment-leave-tracker`の`hris-reader`、
`current-law-analyzer`、`leave-state-writer`、`delivery` identityを分離します。
本packageはsolution、connection、recurrence、scheduleを含みません。approved
solution ID/version/owner/scope/last successful runをstateから確認できる場合だけ
scheduled behaviorを表示します。

## Connectorとpackage境界

外部MCP候補は`connectors.draft.json`に隔離し、`manifest.json`へ登録せず、
生成ZIPへ含めません。宣言だけで`connected`と扱わず、管理者同意、per-user
consent、最小権限、保持、保存・flow DLP、live probeが必要です。

## 本番前blocker

strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation test、Power Platform
solution test、移行元法域review、日本法有資格者reviewが必要です。
