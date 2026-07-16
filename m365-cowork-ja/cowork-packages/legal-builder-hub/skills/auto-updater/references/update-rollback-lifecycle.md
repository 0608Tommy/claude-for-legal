> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Update / rollback lifecycle

```text
current approved package
→ new source candidate
→ source-policy-check
→ quarantine
→ scan/raw-review/QA
→ eligible | remediation-required | refused
→ update request
→ approval
→ admin-action-required
→ human admin operation
→ evidence/read-back
→ active new version
```

rollback:

```text
current active package
→ select prior approved snapshot
→ rescan/review/freshness
→ create new managed version candidate
→ fresh approval
→ admin-action-required
→ evidence/read-back
```

## Invariants

- `REFUSE`はapprovalへ進まない
- source revision変更ごとにnew snapshot
- current/prior historyはimmutable
- old packageを上書きしない
- update/rollbackは別request/approval
- target group変更は再承認
- disable状態でもupdateはnew approval
- failureは自動で別versionへ切替えずoperatorへescalate
