> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cowork実行・保存契約

本packageは学習用です。各skill本文のgateが優先し、本書を読まなかったことを理由に
source authorization、privacy、destination、DLP、concurrency、auditを省略しません。

## 保存モデル

| 種別 | 保存先 | 代表record |
|---|---|---|
| learner・course・exam profile | SharePoint `profiles` | `law-student-user-profile`, `study-profile` |
| authorized study sources | SharePoint `matters`相当のlibrary | syllabus、rubric、AI policy、教材pointer |
| review済み共有artifact | SharePoint `outputs` | study note、approved class handout候補 |
| 状態 | SharePoint `state` | setup、plan、session、deck、feedback tracker、verification |
| 個人draft | OneDrive | outline、case scaffold、答案feedback、過去問分析 |
| 監査 | SharePoint `audit` | read、source verification、confirmation、write、error |

local path、home directory、cache、working directoryを永続保存先にしません。gatewayが
使えない場合、session内のread-only/manual draftとし、利用者が自分で保存します。

## Canonical scopeとkey

- profile: `tenantId + practiceId + userObjectId + profileType`
- state: `tenantId + practiceId + scopeType + scopeId + recordType + recordId`
- authorized source:
  `sourceSystem + sourceItemId + sourceVersion`

`scopeType`はshared state-service schemaの
`tenant | practice | user | matter | session`だけです。保存する個人progressは
`scopeType: user`, `scopeId: [userObjectId]`、setup/session resultは
`scopeType: session`, `scopeId: [sessionId]`を使います。

`studyScopeType: course | exam | general`、`studyScopeId`、`legalSystem`、
`bar_or_exam`等はtop-level keyへ追加せず、create/state envelopeの`payload`、
audit eventの`details`へ入れます。日本の法科大学院・司法試験と米国JD/barを
同じ`studyScopeId`へ混ぜません。別user、別tenant、曖昧なstudy scope、
権限不足ではfail closedです。

## State record ID

| recordType | recordId |
|---|---|
| `setup-session` | `setup:[sessionId]` |
| `study-plan` | `plan:[studyScopeId]:[examYear-or-term]` |
| `session-result` | `session:[sessionId]:[sequence]` |
| `flashcard-deck` | `deck:[subjectId]` |
| `feedback-tracker` | `tracker:[irac-or-writing]:[studyScopeId]` |
| `exam-analysis` | `exam-analysis:[studyScopeId]:[analysisDate]` |
| `verification-entry` | `verification:[sourceType]:[sourceKeyHash]` |

氏名、成績、事件名、依頼者名、診断、答案本文をrecord IDやauditへ入れません。

scope mapping:

| recordType | scopeType | scopeId | study metadata |
|---|---|---|---|
| `setup-session` | `session` | exact `sessionId` | `payload.userObjectId`, `payload.studyScope*` |
| `session-result` | `session` | exact `sessionId` | `payload.userObjectId`, `payload.studyScope*`, exam format |
| `study-plan` | `user` | exact `userObjectId` | `payload.studyScope*`, exam format |
| `flashcard-deck` | `user` | exact `userObjectId` | `payload.studyScope*`, subject/source |
| `feedback-tracker` | `user` | exact `userObjectId` | `payload.studyScope*`, tracker kind |
| `exam-analysis` | `user` | exact `userObjectId` | `payload.studyScope*`, exam/year |
| `verification-entry` | `user` | exact `userObjectId` | `payload.source*`, temporal status |

## Live preflight

初回read/write前にtenant-approved gatewayをlive preflightします。

- current tenant、practice、user、session、study scope
- exact SharePoint site/list/library ID
- current user ACLとsource authorization
- conditional create、ETag update、append-only audit
- retention、legal hold、sensitivity、保存・flow DLP
- Power Platform solution ID/version/owner/connection reference
- destination viewer/channel

失敗、未導入、未検証、Cowork内DLP必須ではread-only/manual draftだけです。
profile、plan、deck、進捗、tracker、verificationを保存したと主張しません。

## Create / update

### Create

1. `tenantId`, `practiceId`, shared `scopeType`, exact `scopeId`,
   `recordType`, `recordId`, unique `idempotencyKey`。
2. `expectedAbsent: true`でconditional create。
3. study metadataは`payload`内だけ。
4. responseのshared state envelopeからexact `itemId`、`eTag`、`version`を記録。
5. timeout/duplicate/partial時は再createせず、同じkey/idempotencyを照合。
6. shared audit-event schemaでappend。

### Update

1. exact `tenantId`, `practiceId`, `scopeType`, `scopeId`, `recordType`,
   `recordId`, `itemId`、latest `eTag`を再取得。
2. current→proposed diff、source、destination、impactを表示。
3. 変更単位のfresh human confirmation。
4. unique `idempotencyKey`とnon-empty `patch`でconditional update。
5. study metadataの変更は`patch.payload`内だけ。
6. stale/duplicate/partialは上書きせず再読取り。
7. success/failureをshared audit-event schemaでappend。

自動save、暗黙save、session終了時の一括saveをしません。

## Shared state envelope

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: "user | session"
scopeId: "[exact userObjectId or sessionId]"
recordType: "[record type]"
recordId: "[record ID]"
itemId: "[SharePoint item ID]"
eTag: "[current eTag]"
version: 1
payload:
  userObjectId: "[Microsoft Entra object ID]"
  studyScopeType: "course | exam | general"
  studyScopeId: "[course/exam/general scope ID]"
  legalSystem: "JP | US | other"
  bar_or_exam: {}
updatedAt: "[ISO-8601]"
```

top-levelに`userObjectId`、`studyScopeType`、`studyScopeId`、`status`等を追加しません。
shared schemaの`additionalProperties: false`に従います。

## Shared audit event

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: null
eventType: "[lowercase kebab-case]"
correlationId: "[16-128 character correlation ID]"
idempotencyKey: "[key or null]"
actorObjectId: "[Microsoft Entra object ID]"
timestamp: "[ISO-8601]"
outcome: "succeeded | failed | rejected | partial"
itemIds:
  - "[SharePoint itemId]"
details:
  scopeType: "user | session"
  scopeId: "[exact userObjectId or sessionId]"
  recordType: "[record type]"
  recordId: "[record ID]"
  userObjectId: "[Microsoft Entra object ID]"
  studyScopeType: "course | exam | general"
  studyScopeId: "[study scope ID]"
  legalSystem: "JP | US | other"
  exam_format_value: "[versioned exam format value or null]"
  sourceItemId: "[source item ID or null]"
  sourceVersion: "[version/eTag/hash or null]"
  eTagBefore: "[eTag or null]"
  eTagAfter: "[eTag or null]"
  approvalId: "[approval record ID or null]"
  notes: "[最小限]"
```

`scopeType`/`scopeId`とstudy metadataは`details`内です。auditはappend-onlyで
update/deleteせず、教材本文、答案本文、個人情報を複製しません。

schema-valid JSON例は[state fixtures](state-fixtures.md)にあります。

## Privacy・destination・DLP

sourceを読む前に、利用者の権限、学校・出版社・予備校の利用条件、course policy、
viewer、保存先を確認します。商用教材を広範囲に複製せず、必要部分だけ処理します。
実在するclient、clinic、externship、司法修習の非公開記録はstudy toolへ入れません。

Teams、email、LMS、公開channel、教員、同級生等への共有は別operationです。本packageは
外部投稿、提出、送信を実行しません。宛先が曖昧なら共有用artifactを作りません。

2026-07-16時点でCowork内prompt/taskのDLPとdata classificationを利用できるとは
扱いません。SharePoint、OneDrive、Power Platform、connector境界のDLPだけを
確認し、Cowork内DLP必須ならproductionをblockします。

## 人のcontrol

AIは法的助言、履修・受験資格判断、採点、合否、提出、登録、LMS更新、外部投稿、
scheduled tutoring、calendar reminderを実行・保証しません。学習内容、答案、保存、
共有、次の演習は常に利用者が選びます。
