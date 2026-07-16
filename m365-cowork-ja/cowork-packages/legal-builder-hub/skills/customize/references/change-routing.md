> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Change routing

| Requested change | Scope | Route |
|---|---|---|
| current userの表示/推薦/通知 | `user` | authorized conditional update |
| practice area/team/tooling | `practice` | practice owner権限ならconditional update |
| company shared fact | `tenant/company` | shared-profile owner review |
| registry/publisher/license | `tenant-policy` | policy-change approval |
| connector/tool scope | `tenant-policy` | Security/Privacy/Legal review |
| QA/security gate | `tenant-policy` | guardrail floor + approval |
| target group/deployment owner | `catalog-lifecycle` | admin queue |
| package disable/uninstall | `catalog-lifecycle` | dedicated lifecycle skill |
| first-party protected change | protected | refuse |
| CoCounsel/vendor approval | vendor-blocked | written vendor clearance required |

## Scope conflict

利用者がuser preferenceとしてtenant policyを変更しようとした場合、scopeを上げて
approval routeへ送る。tenant policyをpersonal preferenceとして保存しない。

## Consistency checks

- recommendation `all`だがpractice profileなし
- connector approvedだがlive validationなし
- license allowだがdeployment context/reviewerなし
- QA relaxedだがSecurity/Legal exception processなし
- update preferenceがauto-apply
- Cowork DLP mandatoryだがproduction enabled
- first-party protected assetがcommunity扱い
- vendor-blocked packageがapproved

矛盾を示し、人にどちらを直すか選んでもらう。
