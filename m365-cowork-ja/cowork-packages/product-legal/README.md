> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# プロダクト法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

製品リリース、単一機能のrisk assessment、広告表示・通信販売画面、短時間の
「問題になりそうか」triageを扱うskills-onlyパッケージです。

> **重要:** すべての分析、review memo、claims table、ticket comment、risk
> assessmentは、人によるレビューのためのドラフトです。法的助言、launch
> clearance、外部送信、公開、ticket投稿、法的承認、届出、契約変更を自動実行
> しません。日本法moduleは
> **DRAFT / qualified Japanese counsel review pending**です。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表では、Coworkの
> DLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、
> connector等の保存・flow境界へDLPを適用しても、Cowork内prompt/task自体が
> DLPで保護されるとは表示しません。Cowork内DLPが必須なら、機密資料を投入せず
> 本番導入を停止します。
>
> **State prerequisite:** 本ZIPはSharePoint list/library、state gateway、
> Power Platform solutionをprovisionしません。tenant-approved gatewayのlive
> preflightが成功するまでread-only/manual draft modeに限定し、setup完了、
> profile保存、matter mutation、cursor更新、automation実行を主張しません。

## 登録スキル — exactly 7

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `feature-risk-assessment` | direct | 単一機能のscenario、likelihood、impact、法源matrix、optionを整理 |
| `is-this-a-problem` | direct | 1つの決定的質問を使う短時間triage。clearanceではない |
| `launch-review` | direct | 8 categoryと日本固有overlayでlaunch review draftを作成 |
| `marketing-claims-review` | direct | 表示、画像、disclaimer、広告性、最終確認画面をcomplete impressionで確認 |
| `matter-workspace` | SharePoint / Power Platform front end | `new`, `list`, `switch`, `close`, `none`と期限付きserver binding |
| `cold-start-interview` | admin config | risk calibration、review framework、claims posture、法域、保存先を初期設定 |
| `customize` | admin config | company/product/user/matter profileを1変更ずつ安全に更新 |

## Coworkでの使い方

スラッシュコマンドの実行は不要です。「日本向けリリースをレビューしたい」
「この表示は問題になりそうか」「このlanding pageと最終確認画面を確認したい」
のように依頼します。

移行元の次の表記はcanonical labelとして保持し、Coworkでは日本語intentと
conversation stateへ変換します。

- `/product-legal:feature-risk-assessment`
- `/product-legal:is-this-a-problem`
- `/product-legal:launch-review`
- `/product-legal:marketing-claims-review`
- `/product-legal:matter-workspace new | list | switch | close | none`
- `/product-legal:cold-start-interview --full | --redo | --redo <section> | --check-integrations`
- `/product-legal:customize`

## 保存、分離、state

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、local
filesystemをcanonical storageまたはstateにしません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・product legal実務・利用者profile | SharePoint `profiles` document library |
| PRD、spec、marketing asset、案件profile | SharePoint `matters` document library |
| review済み共有成果物 | SharePoint `outputs` document library |
| setup、calibration、cursor、session binding | SharePoint `state` list |
| current userの個人draft | OneDrive |
| verification、human confirmation、write、flow、error | 追記専用SharePoint `audit` list |

state keyは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
binding keyは
`tenantId + practiceId + userObjectId + sessionId`です。matter bindingは非null
`matterId`と`expiresAt`を要求します。practice modeはfresh sessionにbindingが
存在しない状態で表し、`matterId: null`のactive bindingを作りません。
`switch`/`none`は新しいsessionを要求し、`close`は対象matterの全bindingを
revokeします。

## 日本法レイヤー

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [日本の公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)
- [施行・改正watch](references/currency-watch.md)
- [移行元U.S./global product-legal logic](references/original-product-logic.md)

成果物は **[B] binding law**、**[G] official guidance**、
**[P] exchange/platform policy**、**[I] internal control**、
**[F] future/pending**、**[X] foreign law applying in parallel** を分離します。
house calibrationはscrutinyを上げられますが、license、mandatory screen、
required notice、prohibited representation、安全義務等の法的floorを下げません。

日本法moduleはAPPI/PPC、消費者契約法、特定商取引法の最終確認画面、景品表示法、
stealth marketing、製造物責任・製品安全、電気通信・外部送信、platform/
e-commerce、AI/disclosure、未成年、決済・金融・医療、cybersecurity、IP/content、
上場会社開示を扱います。FTC/NAD/COPPA、米国州法、FCC、HIPAA、GLBA/MTL、
DMCA/Section 230、Form 8-Kを日本法の同義語として移植しません。

## Launch watcher境界

移行元`launch-watcher`は本ZIP内のagentまたはscheduleではありません。
[Launch watcher automation compatibility contract](references/launch-watcher-automation-contract.md)
に、別solution `product-launch-watcher`のreader、classifier、writer、
approved-delivery分離を保持します。これはrouting-onlyで、triageはlegal review
またはclearanceではありません。承認済みsolution、connection、version、owner、
scope、last successful runを確認できない限り、定期scanや配信が動くとは表示
しません。

## Connectorとpackage境界

移行元のSlack、Google Drive、Linear、Atlassian、Asana候補は
`connectors.draft.json`に隔離し、`manifest.json`へ`agentConnectors`を登録せず、
生成ZIPにも含めません。Atlassian/Asanaのsource endpointはSSEであり、
Streamable HTTP adapterが必要です。候補宣言だけで`connected`と扱わず、
管理者同意、per-user consent、最小権限、保持、保存・flow DLP、live probeが
必要です。

## 本番前blocker

`manifest.json`はUnified App Manifest 1.28のskills-only構成です。本番投入前に、
strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation test、Power Platform
solution test、移行元法域review、日本法有資格者reviewが必要です。
