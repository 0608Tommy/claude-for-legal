> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — PIA / DPIA / risk assessment

**状態:** DRAFT — qualified Japanese counsel review pending

## 民間一般

2026-07-16時点、日本の民間事業者一般に対し、すべてのpersonal-data processingへ一律のPIAを義務付けるAPPI ruleがあるとは扱わない。PPCはPIAをrisk-managementの自主的取組として促進している。

- https://www.ppc.go.jp/files/pdf/pia_promotion.pdf
- https://www.ppc.go.jp/files/pdf/pia_overview.pdf

したがって成果物は次を分ける。

- `Binding law trigger`
- `Official guidance / recommended`
- `Internal house trigger`
- `Foreign-law trigger`

internal policyで全件PIAを要求することはできるが、「日本法上mandatory」と書かない。

## 特定個人情報保護評価

My Numberの`特定個人情報保護評価`は固有の法定制度で、対象主体・file・threshold・公表手続を確認する。一般企業の通常PIAに自動拡張しない。

https://www.ppc.go.jp/legal/assessment/

## 外国法

EU/UK GDPR Article 35、US state data protection assessment、sectoral risk assessmentが適用される場合、日本のPIAと並行してformal requirementを満たす。内部PIAがforeign statutory DPIAを代替すると主張しない。

## PIA triggerとして強く扱う事項

- children
- biometric identification / categorization
- health、financial、precise location、communications
- employee/applicant scoring・monitoring
- large-scale or systematic tracking
- dataset combination / inference
- automated consequential decision
- ad-tech / cross-context behavioral advertising
- vendor independent training
- new cross-border route
- data subjectsが予期しないreuse
- policy / notice conflict

これらはrisk indicatorであり、単独で日本法上のmandatory PIAと断定しない。

## Minimum content

1. activity、purpose、necessity、proportionality
2. exact data fields、subjects、source
3. data flow、systems、vendors、countries
4. role / legal route by jurisdiction
5. notice、consent、rights、complaint
6. retention、deletion、backup
7. security、access、monitoring
8. risk to people、likelihood、impact
9. mitigation、owner、deadline
10. residual risk、conditions、approver、review date

## Recommendation

`APPROVED / APPROVED WITH CONDITIONS / CHANGES REQUIRED / NOT APPROVED`はhuman decision。skillは`proposed recommendation`としてdraftし、承認stateを変更しない。

## 2026改正

children・specific biometric等の改正内容はfuture-readiness欄に分け、公布・施行・PPC rule確認前にcurrent mandatory triggerへ加えない。
