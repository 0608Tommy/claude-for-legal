> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Escalation draft

## Output

```markdown
**Escalating to:** [name/role]
**Via:** [channel]
**Urgency:** [deadline or none]
**Playbook side:** [sales | purchasing]

---

[Name] —

[Counterparty]の[agreement type]について判断をお願いします。[deal context]

**Issue:** [plain language]

**Contract says**
> "[full relevant conditional text]" (§[X], [item/version])

**Playbook says**
> "[exact current position]" ([profile item/version])

**Why this is escalated:** [threshold / fallback / automatic trigger / ambiguity]

**Options**
1. **Accept** — [effect and conditions]
2. **Push back** — [surgical replacement language and likely response]
3. **Alternative** — [commercial or structural option]

**Draft recommendation:** [option and reason; approver decides]

**Decision needed by:** [date/time/time zone]
**Full review:** [SharePoint/OneDrive link]
```

## Multi-approver

findingsごとにapproverをde-duplicateし、各人のdecisionを分ける。CISO、Privacy、CFO、GC、business ownerの全員を1つの曖昧なapprovalへまとめない。

| Approver | Finding IDs | Decision requested | Routed record |
|---|---|---|---|

upstream reviewがN approverを指定した場合、verified `sent`/`delivered` event
だけを`M of N delivered`へ数える。draft recordは`D drafts prepared`として
別表示し、recordまたはdelivery eventがなければそれぞれ0とする。

## Destination

external recipient、company-wide channel、counterpartyを宛先にした場合、internal analysisをそのまま使わない。sanitized external draftを別に作り、内部playbook、accepted risk、privilege analysisを除く。
