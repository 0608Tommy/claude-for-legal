> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Recommendation policy

## Record

```yaml
recordType: builder-recommendation
scopeType: user
scopeId: "[userObjectId]"
recordId: "[packageId]:[catalogVersion]:[contextHash]"
payload:
  packageId: "[package ID]"
  catalogVersion: "[version]"
  contextHash: "[non-reversible task category hash]"
  status: surfaced | dismissed | requested
  surfacedAt: "[ISO-8601]"
  reasonCodes:
    - "[canonical reason]"
```

matter名、client名、文書本文、secretをcontextHashまたはreasonへ入れない。

## Exclusions

- first-party protected
- vendor-blocked
- unapproved candidate
- `REFUSE`
- unavailable mandatory connector
- direct trigger conflict
- current assignment
- prior dismissal
- stale/expired approval

## Risk display

recommendationはpurpose fitだけを示し、legal accuracy、安全性、品質を保証しない。
QA verdict、review status、unknown fieldをcardへ残す。
