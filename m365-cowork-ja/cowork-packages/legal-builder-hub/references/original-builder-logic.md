> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元Legal Builder Hub behavior

本packageは移行元のdiscovery、raw review、trust evaluation、profile customization、
freshness、update diff、disable/uninstall safetyを保持し、local/plugin-management
operationだけをtenant-governed admin workflowへ置換する。

| Source skill | Preserved substance | Cowork redesign |
|---|---|---|
| `registry-browser` | watched registry search、name/description/category、full preview | approved catalog/metadata read。registry追加はpolicy request |
| `related-skills-surfacer` | practice fit、not already installed、strong-match、frequency limit | approved catalogのみ。hookなし。dismissalはgateway state |
| `skills-qa` | dependency map、13 parameters、3 legal failure modes、injection scan、verdict | quarantine snapshot read-only review。catalog権限なし |
| `skill-installer` | allowlist、raw source、trust check、QA、fresh approval、license/freshness | 「テナント配布申請」。install/copyしない |
| `auto-updater` | immutable revision、full diff、re-scan、freshness、rollback | update/rollback queue request。auto-applyなし |
| `disable` | first-party refusal、history check、confirmation、audit | assignment/availability停止申請。file renameなし |
| `uninstall` | first-party refusal、file/config/dependency確認、confirmation、audit | tenant配布解除申請。deleteなし |
| `cold-start-interview` | role、practice、sources、deployment context、license/freshness/update preference | user profileとtenant policy候補を分離。starter packはrequest |
| `customize` | 1変更、current→new→impact→confirm、guardrail degradation拒否 | user preference conditional write、tenant policy change request |

## Flattened helper

`skill-manager`はdeployable skillにしない。次を`disable`、`uninstall`、record/automation
contractへcompileする。

- first-party protected asset refusal
- latest install/deployment history check
- fresh typed operation confirmation
- exact target/file相当のpackage/assignment list
- config/retention preservation
- immutable audit
- disabled stateからuninstallまたはenableを許可

sourceに存在したbuilt-in path listの重複・欠落に依存せず、solution-managed
`builder-protected-asset` recordで判定する。

## Corrected contradictions

- permissive defaultとrestrictive defaultの矛盾:
  tenant targetはrestrictive/fail-closed。例外はpolicy approvalのみ
- pre-fetch license:
  registry/source policyはfetch前、actual license一致はpost-fetch
- installer step numbering:
  review/approval/queueを明確に分離
- QA advisory contradiction:
  `REFUSE`はhard deny。その他のverdictもdeployment approvalではない
- auto-update claim:
  targetはauto-applyなし。すべてupdate request
- local cache/rename/backup:
  SharePoint/Dataverse recordとapproved managed versionへ置換
- agent digestの“Applied N updates”:
  candidate/diff digestへ置換

## Ancillary artifact disposition

- source `.mcp.json`: connector draft/policyへ
- source `registry-sync` agent: separate admin automation contractへ
- empty hooks: omitted。behavior lossなし
- `.gitignore`: omitted
- source practice template: SharePoint profile/policy recordへ
- source allowlist/freshness reference: target policy/referenceへ

## Scope

移行元と同様、hubはcommunity skillの実体法上の正確性を保証しない。targetではさらに、
package signing、security scan、privacy approval、tenant deploymentを実行したと
主張しない。
