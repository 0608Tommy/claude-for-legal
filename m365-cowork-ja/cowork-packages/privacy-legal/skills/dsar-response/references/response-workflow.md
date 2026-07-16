> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# DSAR response workflow and drafts

## Internal cover

```markdown
> **⚠️ レビュー担当者向け注記**
> [sources / read / law-guidance-policy / flags / currency / destination / before relying]

機密 — 内部法務レビュー用ドラフト

# Privacy Request Review: [requestId]

**Received:** [date/time]
**Rights:** [...]
**Regimes / clocks:** [...]
**Identity:** [verified / pending / issue]
**Search coverage:** [...]
**Proposed limits:** [...]
**Human decisions:** [...]
```

## Acknowledgment draft

```markdown
Subject: We received your privacy request — [Company] — [date]

Dear [Name],

We received your [right] request on [date].

Your request, as we understand it: [one sentence].

Our current target date is [date], subject to the applicable legal framework.
[If needed: To verify identity, please complete the following minimal step: ...]

We will contact you if we need clarification or if an applicable extension is required.

[Privacy contact]
```

法域が要求しないextension、fee、clock tollingをtemplateだけで追加しない。

## Substantive access draft

```markdown
Subject: Your privacy request — [Company] — [date]

We received your request on [date].

## What we found

| Category | Source | Purpose | Retention |
|---|---|---|---|

## Delivery

[secure link / protected archive / other reviewed method]

## Information not included

[precise category, reviewed legal basis, redaction]

## Contact / complaint route

[applicable route]
```

## Deletion / cessation draft

```markdown
## Action completed

| Category | System | Action | Completed |
|---|---|---|---|

## Retained

| Category | Reason / authority | Retained until |
|---|---|---|

## Processors / vendors

[instructions issued and verified result; do not claim completion without evidence]
```

## Quality checks

- outward draftにinternal notesなし
- recipientとsecure deliveryをverify
- other-person dataをredact
- withheld basisをattorneyがapprove
- action resultをsystem evidenceで確認
- send approvalとdelete approvalを分離
