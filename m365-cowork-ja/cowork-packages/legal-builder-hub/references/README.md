> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Package-local reference index

本directoryは法務スキル管理packageの実行境界、record contract、移行元behavior、
日本向けreview項目を保持します。各skillは必要な共通契約をskill自身の
`references/common/`へ同梱し、skill rootの外へ依存しません。

## Common contracts

- `common/cowork-runtime-contract.md`
- `common/catalog-record-contracts.md`
- `common/approval-record-contracts.md`
- `common/deployment-queue-record-contracts.md`
- `common/source-provenance-and-review.md`
- `common/power-platform-compatibility-contract.md`
- `common/admin-automation-compatibility-contract.md`
- `common/connectors-and-vendors.md`

## Machine-readable contracts

- `contracts/catalog-record.schema.json`
- `contracts/approval-record.schema.json`
- `contracts/deployment-queue-record.schema.json`

## Migration and Japan review

- `original-builder-logic.md`
- `japan-tenant-governance-review.md`

これらはSharePoint、Dataverse、Power Platform、管理API、connector、scan serviceを
provisionしません。実装証拠ではなく、tenant実装が満たすべき互換契約です。
