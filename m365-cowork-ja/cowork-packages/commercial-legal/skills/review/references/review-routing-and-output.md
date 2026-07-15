> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Review routing and integrated output

## Title-first routing

| Main/attachment title | Workflow |
|---|---|
| `Non-Disclosure`, `NDA`, `Confidentiality Agreement` as main agreement | NDA |
| `Master Services Agreement`, `Professional Services`, `Statement of Work`, `Consulting Agreement` | Vendor/services |
| `Subscription`, `SaaS`, `Cloud Services`, auto-renew `Order Form`, recurring-fee `Software License` | Vendor + SaaS overlay |
| `Data Processing Addendum`, `DPA`, `Data Processing Agreement` | Vendor data section + separate privacy handoff candidate |
| `Service Level Agreement`, `SLA` | SaaS SLA section |

document title、TOC、attachment listを先に読む。confidentialityというbody wordだけでNDAへrouteしない。

## Structure record

```yaml
routing:
  main:
    title: "[title]"
    itemId: "[exact itemId]"
    workflow: nda | vendor | vendor-plus-saas
  attachments:
    - title: "[title]"
      itemId: "[itemId or URL/version]"
      workflow: "[workflow]"
  confirmedByUser: true | false
  confirmedAt: "[ISO datetime or null]"
```

## Integrated memo

```markdown
[appropriate internal confidentiality marking]

> **⚠️ レビュー担当者向け注記**
> - Sources:
> - Read:
> - Playbook:
> - Flagged for your judgment:
> - Currency:
> - Destination:
> - Before relying:

# Contract Review: [Counterparty] — [Agreement type]

**Reviewed:** [date]
**Documents/version:** [items]
**Our role:** Customer | Vendor
**Playbook side:** purchasing | sales
**Contract value:** [value or unresolved]
**Routing:** [workflows]

## Bottom line

[Two sentences: current draft status and what must happen next. Not a signature approval.]

**Legal risk:** [N]🔴 [N]🟠 [N]🟡 [N]🟢
**Business friction:** [N]🔴 [N]🟠 [N]🟡 [N]🟢
**Approval candidates:** [names/roles]

## Deal-breaker

[Clear | Present]

## Findings

[Grouped by higher of the two axes, while preserving both]

## SaaS overlay

[if applicable]

## NDA triage

[if applicable]

## Better than standard

[trade-bait terms]

## Missing / unread

[missing provisions, DPA/URL/SLA, read coverage]

## Approval routing

[all approvers, findings, route status]

## Draft redline package

[only if requested; no native tracked-change claim]

## Renewal candidate

[candidate fields; not "registered" until exact record exists]
```

## Severity

NDA GREEN/YELLOW/REDはtriage outcomeであり、legal risk scaleとは別。YELLOW/RED findingにもdual severityを付ける。

## Quiet output

counterparty、business、board向けartifactはinternal memoと別に作る。internal playbook、accepted risk、privilege analysis、private approver namesをexternal版へ移さない。

## Quality

- correct side
- full relevant quote
- deal-breaker first
- each deviation has specific smallest redline
- named approver
- DPA/URL terms status
- read coverage
- renewal assertion verified
- no send/sign/update without confirmation
