> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# State record・Power Platform compatibility contract

本packageはskills-onlyです。SharePoint schema、Power Platform managed solution、
connection、schedule、LMS integrationを含みません。approved solutionのID、version、
owner、scope、connection reference、last successful runを確認できない場合、
automationがあるとは表示しません。

## Record schema

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: "user | session"
scopeId: "[exact userObjectId or sessionId]"
recordType: "[setup-session | study-plan | session-result | flashcard-deck | feedback-tracker | exam-analysis | verification-entry]"
recordId: "[canonical record ID]"
itemId: "[SharePoint item ID]"
eTag: "[eTag]"
version: 1
payload:
  userObjectId: "[Microsoft Entra object ID]"
  studyScopeType: "course | exam | general"
  studyScopeId: "[stable pseudonymous ID]"
  legalSystem: "JP | US | other"
  status: "[record-specific status]"
  bar_or_exam: {}
updatedAt: "[ISO-8601]"
```

shared `state-envelope.schema.json`のtop-levelだけを使います。`userObjectId`、
study metadata、status、created/updated actor等は`payload`へ置きます。profile、
plan、session、deck、trackerに答案全文や教材全文を埋めず、authorized document
pointerを使います。

scope:

- `setup-session`, `session-result`: `scopeType: session`,
  `scopeId: [sessionId]`
- `study-plan`, `flashcard-deck`, `feedback-tracker`, `exam-analysis`,
  `verification-entry`: `scopeType: user`, `scopeId: [userObjectId]`

## Admin front ends

### `cold-start-interview`

- exact user/profileとsetup sessionをread。
- `initial | resume | quick | full | redo-section | check-integrations`。
- create/updateを分け、profileとsetup recordを別write。
- `[PENDING]`をcompleteにしない。
- gateway failure時はsession内profile draftだけ。

### `customize`

- 一度に1 field。
- current→proposed→source→impact→fresh confirmation。
- shared `scopeType`/`scopeId`、exact itemId/eTag/idempotency。
- guardrail、legal review、DLP blockerを無効化しない。

## Power Platform front ends

### `flashcards`

approved flowは次を分離します。

| identity | 許可 | 禁止 |
|---|---|---|
| `study-source-reader` | authorized sourceのexact item/version/section read | broad drive crawl、write、submission |
| `study-state-writer` | confirmed deck/session patchのconditional create/update | source broad read、LMS、external post |
| `study-audit-writer` | canonical audit append | state overwrite、content copy |

card生成自体はCoworkで行えますが、deck/bucket/next-reviewの永続化はfresh
confirmation後のwriter operationです。review dateは計画値で、notificationや
scheduled tutoringではありません。

### `study-plan`

approved flowはprofileとconfirmed session historyをreadし、human-approved planを
conditional create/updateします。Outlook calendar、Teams reminder、LMS、
prep-course portalへ自動登録しません。plan dateはschedule dataであり、自動実行の
証拠ではありません。

## `session` handoff

`session`はdirect skillですが、結果の永続化は`study-plan` writer contractへ
handoffします。

1. session summaryとsource/versionを表示。
2. learnerがscore/self-assessment、weak topic、保存先を確認。
3. session result create requestを`scopeType: session`, `scopeId: [sessionId]`で構成。
4. separate idempotency keyでsession-resultをconditional create。
5. planは`scopeType: user`, `scopeId: [userObjectId]`でexact record/eTagを取得。
6. plan priority変更は別diff・別confirmation・別update。
7. audit top-levelはshared schemaだけとし、scope/study metadataを`details`へ入れる。

session終了だけで自動更新しません。

## Failure behavior

gateway、ACL、DLP、source version、exact item ID、eTag、idempotency、auditの
いずれかが欠ける場合:

- session内で結果を表示できる。
- manual copy用の最小artifactを作れる。
- 「保存済み」「更新済み」「scheduled」「提出済み」と表示しない。
- local fallback fileを作らない。

## No automation claims

本packageは履修登録、受験申込、提出、採点、LMS update、教員・同級生への連絡、
外部投稿、calendar invite、scheduled tutoring、reminder deliveryを実行しません。

## Valid fixtures

[state fixtures](state-fixtures.md)のcreate、state envelope、update、audit例は、
shared state-serviceの各JSON Schemaに対して検証する前提です。fixtureのstudy metadataは
`payload`または`details`だけに置きます。
