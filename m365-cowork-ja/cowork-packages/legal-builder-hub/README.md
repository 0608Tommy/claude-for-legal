> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 法務スキル管理 — Microsoft 365 Copilot Cowork 日本語パッケージ

承認済みの法務スキルを検索し、外部候補を隔離して評価し、テナント管理者向けの
承認要求または配布キュー下書きを作成するskills-onlyパッケージです。移行元の
「app store」を、**テナント管理型スキル カタログの申請・審査フロントエンド**
として再設計しています。

> **最重要境界:** Cowork skillは、テナントアプリ、Unified App package、
> Microsoft 365管理画面、カタログ、assignment、availability、connector、
> Power Platform solutionを直接install、update、rollback、disable、enable、
> uninstall、upload、publish、sign、scan、approveまたは変更しません。
> 依頼はreview draft、またはtenant-approved gatewayへの条件付きadmin queue
> recordになります。実操作と実行証跡の登録は、分離された人の管理者が行います。
>
> **State prerequisite:** 本ZIPはSharePoint site/list/library、Dataverse table、
> state gateway、Power Platform flow、approval、connection reference、管理API、
> scheduleをprovisionしません。live preflight失敗時はread-only/manual draft
> modeに限定します。fallbackはcurrent session内だけに保持し、OneDrive保存は
> ACL、destination、retention、legal hold、storage DLPを独立preflightできた場合だけ
> です。「申請済み」「承認済み」「配布済み」「更新済み」「無効化済み」などと
> 表示しません。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表に基づき、
> SharePoint、OneDrive、Power Platform、connector等の保存・flow境界へDLPを
> 適用しても、Cowork内prompt/task自体がDLPで保護されるとは表示しません。
> Cowork内DLPが必須なら、機密情報を投入せずproduction利用を停止します。
> 確認先: https://learn.microsoft.com/en-us/purview/ai-copilot-cowork
>
> **日本向けレビュー:** tenant governance、privacy、security、license、
> vendor、データ取扱いに関する日本向け注記は
> **DRAFT / qualified review pending**です。本packageの主目的は管理workflowであり、
> 日本法上の結論や承認を代行しません。

## 登録スキル — exactly 9

| ID | logical target | Coworkでの役割 |
|---|---|---|
| `auto-updater` | `ja-jp.admin.legal-builder-hub.auto-updater` | 新snapshot、full diff、freshnessを確認し、update/rollback申請draftを作る |
| `cold-start-interview` | `ja-jp.admin.legal-builder-hub.cold-start-interview` | requester profileとtenant catalog policy候補を初期設定する |
| `customize` | `ja-jp.admin.legal-builder-hub.customize` | user preferenceとtenant policy changeを分離して1件ずつ変更する |
| `disable` | `ja-jp.admin.legal-builder-hub.disable` | community packageのdisable/enable管理者申請を作る |
| `registry-browser` | `ja-jp.admin.legal-builder-hub.registry-browser` | 承認済みcatalogと許可済みregistry metadataをread-only検索する |
| `related-skills-surfacer` | `ja-jp.admin.legal-builder-hub.related-skills-surfacer` | 承認済みcatalogだけから関連skillを推薦する |
| `skill-installer` | `ja-jp.admin.legal-builder-hub.skill-installer` | 隔離、raw review、QA、差分を束ねたテナント配布申請を作る |
| `skills-qa` | `ja-jp.admin.legal-builder-hub.skills-qa` | 隔離snapshotを13 parameters、3 legal failure modes、trust surfaceで評価する |
| `uninstall` | `ja-jp.admin.legal-builder-hub.uninstall` | dependencyとretentionを確認した配布解除申請を作る |

`skill-manager`は登録しません。次のmandatory behaviorを`disable`、`uninstall`、
record contract、管理者automation contractへflattenしています。

- first-party protected asset refusal
- exact deployment/install history check
- operationごとのfresh typed confirmation
- immutable decision/audit history

`registry-sync` agent、hook、`.mcp.json`も本ZIPに含めません。別solution候補
`builder-registry-sync`の互換境界だけを文書化し、既定は無効です。

## Coworkでの使い方

スラッシュコマンドは不要です。「承認済みの契約review skillを探す」
「このpackageを審査する」「v1.2への更新差分を確認する」
「このcommunity appの配布停止申請を作る」のように依頼します。

移行元のcanonical ASCII labelは保持します。

- `/legal-builder-hub:registry-browser [query]`
- `/legal-builder-hub:related-skills-surfacer`
- `/legal-builder-hub:skills-qa [skill path | SKILL.md | pasted content]`
- `/legal-builder-hub:skill-installer [skill name or registry URL]`
- `/legal-builder-hub:auto-updater [--apply | --rollback]`
- `/legal-builder-hub:disable [skill name]`
- `/legal-builder-hub:uninstall [skill name]`
- `/legal-builder-hub:cold-start-interview [--full | --redo | --check-integrations]`
- `/legal-builder-hub:customize [section or change]`

`--apply`はtargetでは「update requestを作るintent」であり、自動適用を意味しません。
`--rollback`もprior approved snapshotから新しい管理versionを作る申請intentです。
backendではrollbackを`operation: update` + `updateMode: rollback`、uninstallを
`operation: remove`へcanonicalizeします。

## 必須の申請前検査

install、update、rollback、disable、enable、uninstall、registry追加、
tenant policy変更の各要求は、次をexact ID/version/hashへ束縛します。

1. package/app/skill IDと対象tenant/group
2. source registry、publisher、canonical URI、commit SHAまたはimmutable revision
3. provenance、全file list、file hash、snapshot hash、package hash
4. SPDX license、metadataとLICENSEの一致、deployment context
5. signature statusと検証者。未署名または未検証をsignedと表示しない
6. deterministic scan、malware/content scan、prompt-injection heuristic
7. privacy、data destination、retention、legal hold、storage/flow DLP
8. hooks、connector、tool scope、network、write path、credential request
9. current versionとtarget versionのfull diff
10. dependencies、conflicts、first-party protected asset
11. requester、reviewer、approver、deployment operatorの分離
12. rollback plan、failure/dead-letter plan、immutable decision history

`REFUSE`はhard denyです。`MATERIAL CONCERNS`はremediation、または明示された
Security/Legal exception routeが必要です。`SOME CONCERN`はrisk acceptanceを
記録します。いずれもcatalog承認や配布の証拠ではありません。

confirmed prompt overrideまたはruntime secret/credential requestは
`SOME CONCERN`としてrisk-acceptできません。除去可能でもmandatory remediation、
guardrail/runtime overrideまたはsecret capture/use/store/transmitは`REFUSE`です。

## 保存、state、分離

[Cowork実行契約](references/common/cowork-runtime-contract.md)に従い、local file、
cache、rename、plugin directoryをcanonical stateまたは操作対象にしません。

| 情報 | 保存先候補 |
|---|---|
| company、practice、current user profile | SharePoint `profiles` library |
| quarantine raw snapshot | 専用SharePoint `SkillQuarantine` library |
| approved immutable package | SharePoint `ApprovedSkillPackages` library |
| user preference、setup、recommendation | SharePoint `state` list |
| registry、publisher、candidate、QA、approval、queue | Dataverse |
| current userの未送信draft | current session。独立control確認後だけOneDrive |
| verification、decision、write、admin evidence | append-only SharePoint/Dataverse audit |

write前にgateway、exact site/list/table/library ID、ACL、conditional create/update、
append-only audit、retention、legal hold、DLP、connection、solution/versionをlive
preflightします。updateはexact `itemId`、latest `eTag`、unique
`idempotencyKey`を要求し、stale writeを上書きしません。

matter固有の資料を評価する場合だけ、
`tenantId + practiceId + userObjectId + sessionId`のactive、non-null、
未期限切れmatter bindingを要求します。practice-level evaluationはfresh
sessionでbindingが存在しない状態です。別user、practice、session、matterの
profile、approval、source、cursorを流用しません。

## Record contracts

- [Catalog records](references/common/catalog-record-contracts.md)
- [Approval records](references/common/approval-record-contracts.md)
- [Deployment queue records](references/common/deployment-queue-record-contracts.md)
- [Machine-readable catalog schema](references/contracts/catalog-record.schema.json)
- [Machine-readable approval schema](references/contracts/approval-record.schema.json)
- [Machine-readable deployment queue schema](references/contracts/deployment-queue-record.schema.json)

decision eventは追記専用です。却下、承認失効、再申請、retry、rollbackも過去recordを
上書きせず、新しいevent/versionとして保存します。

## Power Platformと管理者automation

- [Power Platform compatibility contract](references/common/power-platform-compatibility-contract.md)
- [Administrator automation compatibility contract](references/common/admin-automation-compatibility-contract.md)

本packageはflow source、managed solution、connection、scheduleを含みません。
承認済みdevelopment tenantで作成・exportされたsolution ID/version、owner、
connection、DLP、last successful runを確認できない限り、automationが利用可能、
定期実行中、配布可能とは表示しません。

承認後のqueue statusは`admin-action-required`で停止します。tenantで検証済みの
official admin operationがない限り、人のdeployment operatorが現在サポートされる
Microsoft 365管理画面で実操作し、returned evidenceを登録します。そのevidenceが
exact request/operation/target/audienceへ一致し、distinct
requester/reviewer/approver/operator IDsとsuccessful execution/read-back evidenceが
揃って初めて`succeeded`または`active`にできます。

## Connector、外部publisher、vendor

移行元のSlack、Google Drive、Lawve AIは`connectors.draft.json`に隔離し、
`manifest.json`へ`agentConnectors`を登録しません。connector宣言、README、
publisher claim、badge、signature claim、scan claimはlive検証まで未検証です。

CoCounsel / Thomson Reutersは書面のvendor approval、ブランド・翻訳派生物、
OAuth、entitlement、tenant配布条件が確認できないためblockedです。同じ
`cocounsel-legal` IDでgeneric fallbackを作らず、catalog候補として承認しません。

## 本番前blocker

ローカルpackage validationが成功しても、次は未完了です。

- Microsoft 365 tenant upload、assignment、disable、uninstall smoke test
- SharePoint/Dataverse provisioning、ACL、ETag、idempotency、retention test
- Power Platform managed solution作成、import、owner/connection分離、DLP test
- connector OAuth、tool annotation、read/write scope、live probe
- package signing、malware/security/privacy scan serviceのtenant統合
- original-jurisdiction review、qualified Japanese legal/privacy/security review

AppSource publishing、tenant catalog deployment、package signing、security scan、
scheduled update、rollback、disable、uninstallが実行済みとは主張しません。
