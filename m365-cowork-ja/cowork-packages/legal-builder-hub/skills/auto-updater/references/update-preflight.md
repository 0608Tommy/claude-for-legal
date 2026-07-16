> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Update preflight

## Current

- app/package/skill ID
- catalog version、package SHA-256
- source snapshot/revision/publisher
- current assignment/group
- approval/admin evidence
- license/signature
- security/privacy/tool-scope review
- freshness
- dependencies/conflicts

## Target

- immutable source revision
- complete file inventory、snapshot/package/diff hash
- raw review attestation
- deterministic/malware/content scan status
- QA verdict/parameters
- license metadata/LICENSE/NOTICE consistency
- signer/status/evidence
- connector/hook/network/write scope
- privacy/data destination/retention/DLP
- dependency snapshot
- target group/license entitlement

## Approval invalidators

source、hash、diff、operation、group、destination、dependency、review evidence、
expiryの変化。

## Rollback

- prior approved package ID/hash
- before-state/assignment capture
- failure detection
- operator/owner
- restoration target
- partial group handling
- audit/evidence

preflightはscan、signing、deploymentを実行するものではない。evidenceがなければ
`not-run`または`unverified`。
