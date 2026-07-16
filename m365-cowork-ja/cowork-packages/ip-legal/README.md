> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 知的財産法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

商標、特許・実用新案・意匠、著作権、営業秘密、OSS、知財条項、権利行使、
知財portfolioを扱うskills-onlyパッケージです。

> **重要:** すべての分析、clearance、FTO、invention screen、侵害評価、
> C&D・takedown文案、修正文案、portfolio reportは、人によるレビューのための
> ドラフトです。法的意見、送信、platform submission、出願、登録、支払、
> 更新判断、notice、takedown、案件終了を自動実行しません。日本法moduleは
> **DRAFT / qualified Japanese counsel review pending** です。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表では、
> CoworkのDLPとdata classificationは未対応です。SharePoint、OneDrive、
> Power Platform、connector等の保存・flow境界へDLPを適用しても、Cowork内の
> prompt/task自体がDLPで保護されるとは表示しません。Cowork内DLPが必須なら、
> invention、trade secret、未公開出願、係争資料等を投入せず、本番導入を停止します。
>
> **State prerequisite:** 本ZIPはSharePoint list/library、state gateway、
> Power Platform solutionをprovisionしません。tenant-approved gatewayのlive
> preflightが成功するまでread-only/manual draft modeに限定し、setup完了、
> matter切替、portfolio保存、deadline更新、automation実行を主張しません。

## 登録スキル — exactly 12

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `cease-desist` | direct | C&Dの送付案または受領triage。日本の権利・手続・第三者警告riskを確認 |
| `clearance` | direct | J-PlatPat、称呼・外観・観念、類似群コードを含む商標first pass |
| `fto-triage` | direct | 日本特許・実用新案・意匠のFTO first passとclaim chart |
| `infringement-triage` | direct | 商標、特許、意匠、著作権、営業秘密を権利別にtriage |
| `invention-intake` | direct | 発明開示、Article 30、従業者発明、経済安全保障、意匠・秘密化screen |
| `ip-clause-review` | direct | assignment、license、recordal、著作権27/28条、moral rights、OSS/AI条項 |
| `oss-review` | direct | 実license本文、配布形態、copyleft、compatibility、notice/source義務 |
| `takedown` | direct | 日本のprovider routeとPlatform Act、または別法域のDMCA routeを分離したdraft |
| `matter-workspace` | Power Platform front end | `new`, `list`, `switch`, `close`, `none`とserver binding |
| `portfolio` | Power Platform front end | 権利・deadline・fee sourceのreport/add/update/audit/rebuild |
| `cold-start-interview` | admin | quick/full/resume/redo/check-integrationsでprofileを初期設定 |
| `customize` | admin | profile/stateを1変更ずつ安全に更新 |

## Coworkでの使い方

スラッシュコマンドの実行は不要です。「日本で新しいmarkを調べたい」「受領した
C&Dをtriage」「JPOの期限を90日で確認」のように依頼します。次の移行元label、
flag、subcommandは互換参照として保持し、Coworkでは会話stateへ変換します。

- `/ip-legal:cease-desist --send | --receive`
- `/ip-legal:takedown --send | --respond | --counter`
- `/ip-legal:portfolio --report [--days N] | --add | --update | --audit | --rebuild`
- `/ip-legal:matter-workspace new | list | switch | close | none`
- `/ip-legal:cold-start-interview --full | --redo | --redo <section> | --check-integrations`

## 保存、分離、state

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、local
filesystemを保存先・canonical sourceにしません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・知財実務・利用者profile | SharePoint `profiles` document library |
| 案件資料、発明開示、権利証憑、template | SharePoint `matters` document library、item-level ACL |
| review済み共有成果物 | SharePoint `outputs` document library |
| portfolio、setup、cursor、session binding | SharePoint `state` list |
| current userの個人draft | OneDrive |
| verification、approval、write、flow、error | 追記専用SharePoint `audit` list |

state keyは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
binding keyは
`tenantId + practiceId + userObjectId + sessionId`です。matter bindingは
非null `matterId`と`expiresAt`を要求します。practice modeはfresh sessionに
bindingが存在しない状態で表し、`matterId: null`のactive bindingを作りません。
`switch`/`none`は新しいsessionを要求し、`close`は対象matterの全bindingを
revokeします。

## 日本法レイヤー

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [日本法公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)
- [施行・改正watch](references/currency-watch.md)
- [移行元U.S./global logic](references/original-ip-logic.md)

2026-07-16 JST時点の一次資料を基礎に、特許法、実用新案法、商標法、意匠法、
著作権法、不正競争防止法、従業者発明、JPO手続・fee・deadline、権利移転・
登録対抗要件、商標clearance、patentability/FTO/infringement、design、
trade secret、OSS、Platform Act、provider liability、online takedown、
Customs水際措置を扱います。

成果物は **[B] binding law**, **[G] official guidance**, **[C] case-sensitive
doctrine**, **[I] internal control**, **[F] future/pending** を分離します。
`Alice/Mayo`、DMCA、Lanham Act、DTSA/UTSA、U.S. design-patent testを日本法へ
移植しません。U.S./global案件では移行元layerを別に適用します。

## Portfolioとrenewal automation

portfolio deadline、fee、form、grace、holiday、filing cohortは、実行時にJPO等の
current official recordを取得し、人が確認した場合だけ確定します。generic memory
または保存済み計算だけで「期限なし」「提出済み」「支払済み」と表示しません。

[Power Platform automation contract](references/power-platform-automation-contracts.md)
は、別solution `ip-renewal-watcher`の`portfolio-reader`、
`deadline-verification-analyzer`、`portfolio-alert-writer`、
`approved-alert-delivery`を別identityとして分離します。本packageはsolution、
connection、recurrence、scheduleを含みません。approved solution ID/version/owner/
scope/last successful runをstateから確認できない限りscheduled behaviorを
表示しません。

## Connectorとpackage境界

移行元の候補connector名・URLは互換資料に保持しますが、`connectors.draft.json`
は本packageから**除外**し、`manifest.json`へ`agentConnectors`を登録しません。
宣言だけで`connected`と扱わず、管理者同意、per-user consent、最小権限、保持、
保存・flow DLP、live probeが必要です。

## 本番前blocker

strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation test、Power Platform
solution test、移行元法域review、日本法有資格者reviewが必要です。Cowork prompt
DLPが必須のtenantではproduction deploymentをblockします。
