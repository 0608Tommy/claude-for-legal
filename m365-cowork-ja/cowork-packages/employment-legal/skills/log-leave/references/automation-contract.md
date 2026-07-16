> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Leave automation contract

別Power Platform solution `employment-leave-tracker`だけがautomationを提供します。
package内にsolution、schedule、agentはありません。

## Identities

- `hris-reader`: approved HRIS scopeのread-only、medical narrativeなし。
- `current-law-analyzer`: minimized data + current official authority、writeなし。
- `leave-state-writer`: human-approved state candidateだけconditional write。
- `delivery`: approved alertだけ配信、state/HRIS broad accessなし。

identity、connection、credentialを分離します。exact source/version、scope cursor、
input/output hash、correlation ID、resultをauditします。

## Required proof before schedule claim

- solution ID/version/owner
- enabled recurrence definition
- connection references and service identities
- tenant/practice/matter scope
- last successful run and result
- approved destination

不足時はscheduledと表示せず、人による再実行が必要と明示します。

## Hard limits

automationはleave eligibility/approval/denial、medical sufficiency、reasonable
accommodation、return-to-work、payroll、insurance benefit、discipline、terminationを
決めません。delivery failureでも法的deadlineやstateを自動変更しません。
