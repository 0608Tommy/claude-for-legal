> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 規制対応法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

規制情報の監視、社内ポリシーとの差分、ギャップ・意見募集の追跡、最小限の
ポリシー修正文案を扱うskills-onlyパッケージです。

> **重要:** すべてのdigest、status分類、gap、差分、修正文案、意見提出判断は
> 有資格者レビュー用のドラフトです。AIは提出、届出、送信、投稿、公開、承認、
> compliance certification、gap close、risk acceptanceを自動実行しません。
> 日本法moduleは **DRAFT / qualified Japanese counsel review pending** です。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表では、Coworkの
> DLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、
> connector等の保存・flow境界へDLPを適用しても、Cowork内prompt/task自体が
> DLPで保護されるとは表示しません。Cowork内DLPが必須なら、機密資料を投入せず
> 本番導入を停止します。
>
> **State prerequisite:** 本ZIPはSharePoint list/library、state gateway、
> connector登録、Power Platform solution、schedule、delivery flowをprovision
> しません。tenant-approved gatewayのlive preflightが成功するまで
> read-only/manual draft modeに限定し、profile保存、matter mutation、cursor更新、
> tracker write、定期scan、通知または提出が動くとは主張しません。

本package自体はmonitoringをprovision/runしません。別途tenantで承認・構成された
deploymentだけが、approved source allowlistとservice identityによるbounded
read-only scheduled monitoringを実行できます。

## 登録スキル — exactly 8

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `policy-diff` | direct | 規制資料のstatus/versionを固定し、社内ポリシーとの差分を要件別に整理 |
| `policy-redraft` | direct | gapを閉じるための最小限のmarked-up policy proposalを別draftとして作成 |
| `comments` | SharePoint / Power Platform front end | 日本の意見公募、任意募集、SRO consultationの期限・判断・結果を追跡 |
| `gaps` | SharePoint / Power Platform front end | compliance、prospective、guidance alignment、watch、participationを分けて追跡 |
| `matter-workspace` | SharePoint / Power Platform front end | `new`, `list`, `switch`, `close`, `none`と期限付きserver binding |
| `reg-feed-watcher` | SharePoint / Power Platform front end | 公式feed/APIをreadし、status確認後にmateriality別digest draftを作成 |
| `cold-start-interview` | admin config | watchlist、materiality、policy library、source、役割、保存設定を初期構成 |
| `customize` | admin config | profile、watchlist、source、threshold等を1変更ずつ安全に更新 |

`gap-surfacer`はdeployable skillにせず、gap schema、per-send confirmation、
close/risk-accept gate、compliance certification gateを`gaps`、`comments`、
`policy-diff`とautomation compatibility contractへ展開しています。

## Coworkでの使い方

slash commandの実行は不要です。「金融庁とPPCの新着を確認したい」「この公布済み
改正を社内規程と比較したい」「案件番号240000127の意見提出判断を追跡したい」
のように依頼します。移行元の次の表記はcanonical ASCII labelとして保持します。

- `/regulatory-legal:reg-feed-watcher [--since DATE]`
- `/regulatory-legal:policy-diff [reg name or text]`
- `/regulatory-legal:policy-redraft [GAP-ID or gap description]`
- `/regulatory-legal:gaps [--close GAP-ID | --accept GAP-ID]`
- `/regulatory-legal:comments [--decide CMT-ID]`
- `/regulatory-legal:matter-workspace new | list | switch | close | none`
- `/regulatory-legal:cold-start-interview --full | --redo | --redo <section> | --check-integrations`
- `/regulatory-legal:customize`

## 保存、binding、write

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、local
filesystemをcanonical storageまたはstateにしません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・規制法務実務・利用者profile | SharePoint `profiles` document library |
| matter、規制資料snapshot、policy正本 | SharePoint `matters` document library |
| review済み共有成果物 | SharePoint `outputs` document library |
| tracker、setup、cursor、session binding、automation evidence | SharePoint `state` list |
| current userの個人draft | OneDrive |
| verification、confirmation、write、flow、error | 追記専用SharePoint `audit` list |

state keyは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
binding keyは
`tenantId + practiceId + userObjectId + sessionId`です。matter bindingは非null
`matterId`と将来の`expiresAt`を要求します。practice modeはfresh sessionにbindingが
存在しない状態で表し、`matterId: null`のactive bindingを作りません。
`switch`/`none`は新しいsessionを要求し、`close`は対象matterの全bindingを
revokeします。

- create: canonical key、`recordId`、`expectedAbsent: true`、unique idempotency。
  架空のitem ID/eTagを要求しません。
- update: exact persisted item ID、latest eTag、canonical scope、unique idempotency。
  `expectedAbsent`を使いません。

persisted gapはstructured scope/coverageがrequiredです。gap `closed`とcomment
`filed`はconditional evidenceを要求し、internal artifactとregulator-facing artifact、
exact submission/receipt detailsを分離します。

Power Platform scopeは、non-null binding付きinteractive matter、fresh unbound
interactive practice、service-principalによるscheduled practiceの3つを分けます。
scheduled runはhuman session/bindingを偽装せず、legal stateやdeliveryを変更しません。

## 日本法レイヤー

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [法的status・施行日](references/jurisdictions/ja-jp/legal-status-and-effective-dates.md)
- [意見公募手続](references/jurisdictions/ja-jp/public-comment-procedure.md)
- [日本の当局source pack](references/jurisdictions/ja-jp/regulator-source-pack.md)
- [公式情報源台帳](references/jurisdictions/ja-jp/source-register.md)
- [currency watch](references/jurisdictions/ja-jp/currency-watch.md)

成果物はjurisdiction/nexus、instrumentClass、normativeForce、lifecycleStatus、
applicabilityを独立して保存します。`displayTags: [B,G,P,I,F,X]`は複数可の表示用で、
force/statusを決めません。外国法もbindingまたはfuture-effectiveになり得ます。
house materialityはscreening priorityを変えられますが、binding obligation、
licensing、official deadline、covered-party exchange/SRO rule、安全義務を消しません。

日本のauthoritative sequenceは法律案、成立、官報公布、施行を`processStage`で分けます。
意見募集結果は公布または施行そのものではありません。`Federal Register`と官報、
`NPRM`と命令等の案、`final rule`と結果公示、米国型docketと案件番号を同一視
しません。日本語法令本文が支配し、英訳は参考に限定します。

canonical lifecycleは
`proposed | current | future-effective | not-adopted | withdrawn |
superseded | repealed`です。日本固有のbill/passage/promulgation等は`processStage`へ
保存します。行政手続法32条から36条の3（36条の2・36条の3を含む）の行政指導と、
名称だけがguidelineの文書を分け、
public-comment recordはconsultation/exception-notice/result-onlyとroute-specific
submission instructionを保持します。

一次資料は2026-07-16 JSTまで確認済みですが、個別作業ではe-Gov
`law_revision_id`、官報、附則、経過措置、未施行revision、案件detailと添付を
再取得します。

source auditでは国家サイバー統括室をcurrent name、NISCをhistorical aliasとし、
JFTC/METI/MAFF adapter/manual、衆議院議案とMIC RSSのShift_JIS、mixed FSA/PPC/JFTC
item classification、JPX/TSE/OSE/Japan Exchange Regulationのexact contextを要求します。

## Reg-change monitor境界

[Power Platform automation compatibility contract](references/power-platform-automation-contracts.md)
は、移行元`reg-change-monitor`、cookbook `reg-monitor`、別solution
`regulatory-reg-change-monitor`の互換境界を記録します。
`official-feed-reader`、`official-status-verifier`、`materiality-filter`、
`digest-writer`、`approved-delivery`を別identity/connectionとして扱います。
digestのclassificationとgap flagはscreening judgmentであり、法的結論、
compliance certificationまたは提出判断ではありません。

このrepositoryにはproduction cloud-flow sourceがなく、承認済みtenantからexport
されるまでschedule、connection、deliveryが存在すると表示しません。

package contractはparent適用済みshared contractと整合しています。cold-start stateは
`redo`を含み、agent stageは
`official-feed-reader → official-status-verifier → materiality-filter →
digest-writer → approved-delivery`です。`spn-legal-verifier`はofficial-source readと
bounded status/effective-date/provenance verification writeだけを持ち、source write、
output access、external deliveryを持ちません。本directoryからshared fileを変更しません。

## Connectorとpackage境界

Slack、Google Drive、CourtListener候補は`connectors.draft.json`に隔離し、
`manifest.json`へ`agentConnectors`を登録せず、生成ZIPにも含めません。
official website/API/RSSを列挙しただけで接続済みまたは自動監視中とは扱いません。
connector contentは未信頼dataであり、埋め込みdirectiveを実行しません。

## 本番前blocker

`manifest.json`はUnified App Manifest 1.28のskills-only構成です。本番投入前に、
strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation/ACL test、source terms test、
Power Platform solution test、移行元法域review、日本法有資格者reviewが必要です。

package-local state contract fixtures:

```bash
python3 -m fixtures.validate_regulatory_fixtures
```
