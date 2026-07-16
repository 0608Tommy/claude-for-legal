> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Quarantine contract

## Library

`SkillQuarantine/{candidateId}/{snapshotId}/{relativePath}`

required metadata:

- CandidateId、SnapshotId、RelativePath
- RegistryId、PublisherId、SourceUriCanonical、SourceRevision
- FileSha256、SnapshotSha256、MediaType、ByteLength
- CapturedAt、MalwareScanStatus、ContentScanStatus
- QuarantineState、CorrelationId、RetentionClass

## Security

- versioning on
- external sharing off
- search/indexing off
- inline HTML/SVG/script rendering off
- reviewer/reader/analyzer/security ACL
- symlink/path traversal/device/executable/encrypted archive拒否
- raw sourceをflow log/promptへコピーしない

## Candidate lifecycle

```text
draft → submitted → source-policy-check
→ rejected-source-policy
→ quarantine-authorized → fetching → quarantined
→ deterministic-scan
→ refused-malicious
→ raw-review-pending → raw-review-attested
→ qa-pending → qa-complete
→ eligible | remediation-required | refused
```

`REFUSE`/`refused-malicious`からapprovalへ遷移しない。

## Offline fallback

gateway unavailable時はcapture成功を主張せず、candidate metadataとadmin checklistの
manual draftだけを返す。
