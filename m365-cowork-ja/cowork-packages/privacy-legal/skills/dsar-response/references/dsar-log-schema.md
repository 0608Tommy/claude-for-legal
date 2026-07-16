> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Privacy request log schema

```yaml
recordType: privacy-request
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
requestId: "[opaque ID; no person name/email]"
recordId: "[same opaque requestId]"
receivedAt: "[ISO-8601]"
receivedChannel: "[channel]"
requestTypes:
  - access
applicableRegimes:
  - ja-APPI
deadlines:
  - regime: ja-APPI
    rule: without-undue-delay
    targetDate: "[internal target]"
    source: "[official URL]"
identity:
  status: pending | verified | rejected
  method: "[minimal method]"
systems:
  - systemId: "[approved system]"
    status: pending | searched | unavailable
    coverage: "[query/date range]"
limits:
  - category: "[category]"
    proposedBasis: "[authority]"
    reviewStatus: pending
drafts:
  acknowledgmentItemId: "[itemId or null]"
  substantiveItemId: "[itemId or null]"
actions:
  - action: send-acknowledgment | send-substantive | produce-data | correct-data | restrict-or-opt-out | delete-data | instruct-processor
    approvalStatus: pending | approved | rejected | expired
    approverObjectId: "[user/group ID or null]"
    confirmedAt: "[ISO-8601 or null]"
    artifactItemId: "[exact draft/data item ID or null]"
    artifactVersionOrHash: "[version/hash or null]"
    executionStatus: not-started | succeeded | failed | partial
    executedAt: "[ISO-8601 or null]"
    evidenceItemIds:
      - "[audit/result item ID]"
    failureReason: "[sanitized reason or null]"
status: open | awaiting-verification | searching | attorney-review | response-approved | completed
eTag: "[eTag]"
```

Createはcomposite keyとidempotencyで行う。Updateはexact`itemId`とlatest`eTag`を使う。本人氏名、email、ID copyをkeyへ含めない。auditにはaction結果だけを必要最小限で残す。
