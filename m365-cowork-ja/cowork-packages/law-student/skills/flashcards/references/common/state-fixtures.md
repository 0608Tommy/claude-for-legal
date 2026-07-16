> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Shared state-service schema fixtures

次のJSONはpackage-local test fixtureです。

- [session result create](fixtures/session-result.create.json)
- [session result state envelope](fixtures/session-result.state-envelope.json)
- [study plan update](fixtures/study-plan.update.json)
- [progress audit event](fixtures/progress.audit-event.json)

対応するshared schema:

| fixture | schema |
|---|---|
| `session-result.create.json` | `create-request.schema.json` |
| `session-result.state-envelope.json` | `state-envelope.schema.json` |
| `study-plan.update.json` | `update-request.schema.json` |
| `progress.audit-event.json` | `audit-event.schema.json` |

fixtureはshared schemaのtop-levelを変更しません。`userObjectId`、`studyScopeType`、
`studyScopeId`、`legalSystem`、versioned `bar_or_exam.exam_format`等の追加情報は
create/state envelopeの`payload`、auditの`details`だけに入れます。
`bar_or_exam.attempt_cap`はstatus必須で、`numeric`の場合だけcountを持ちます。temporal metadataは
exam cutoff後に施行済みの法を`currently-effective`かつ
`excluded-post-cutoff`として表せます。

実運用値ではなく、secretや個人情報を含まないsynthetic IDです。
