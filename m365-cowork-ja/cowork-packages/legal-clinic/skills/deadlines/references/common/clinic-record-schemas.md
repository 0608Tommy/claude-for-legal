> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Legal clinic canonical record schemas

## Authoritative machine contract

正本は`clinic-state-payloads.schema.json`である。skill-local common copyも同じ
filenameとbyte contentを持つ。Draft 2020-12 JSON
Schema、全object `additionalProperties: false`、top-level `oneOf`で次を検証する。

- `clinic-practice-profile`
- `setup-session`
- `session-matter-binding`
- `binding-revocation-batch`
- `clinic-matter`
- `tracker-record`

検証済みfixtureは`clinic-state-payload-examples.json`。skill-local common copyも
同じfilenameとbyte contentを持つ。本書のprose又はYAML例が
machine schemaと矛盾する場合、JSON Schemaが優先する。

## Canonical nested profile

`clinic-practice-profile.payload`は次のnested sectionだけを持つ。

1. `clinic`
2. `authority`
3. `conflicts`
4. `engagement`
5. `studentParticipation`
6. `supervision`
7. `pedagogy`
8. `data`
9. `urgentRouting`
10. `sourceCards`
11. `houterasuPrograms`
12. `semester`
13. `integrations`
14. `legalReview`
15. `activationApprovalIds`

`data`は`appiHostRegime`、Article 58 assessment item、clinic restricted categoriesが
法定要配慮個人情報と同義でないことを必須fieldとして持つ。

legal review statusは
`pending | in-review | approved | blocked`。`profileStatus: active`はJapan counselと
clinic supervisorの両statusが`approved`の場合だけschema-validである。本packageの
shipped statusはDRAFT/pendingであり、setup interview完了をlegal approvalと呼ばない。

## Conflict / barrier / engagement

- `informationBarrierPolicyItemId`はconflict processの補助control。
- `barrierIsNotClearance: true`を固定し、barrier設置で`conflictStatus`を`clear`へ
  変更しない。
- `disclaimerNotDeterminative: true`と
  `conductMayCreateOrExpandEngagement: true`を固定する。
- disclaimer又はunsigned engagement recordがあっても、実際のadvice、undertaking、
  representation、reliance、communication等が関係を生じさせ又はscopeを拡張し得るため、
  責任弁護士へ即時escalateする。
- `studentParticipation.classification`は`internal-policy`。
  `createsLegalAuthority: false`、`curesAttorneyAct72Risk: false`を固定する。

## Setup session

`setup-session.payload`は次をstrictに記録する。

- mode
- completed section IDs
- pending questions（section、prompt、blocking）
- exact source evidence
- status:
  `draft | paused | review-pending | interview-complete | superseded`
- profile item ID、version、ETag
- Japan counsel / clinic supervisor legal review status
- updated timestamp

`interview-complete`はprofile又はlegal reviewのapprovalではない。
`profileItemId`、`profileVersion`、`profileETag`は参照tupleであり、3つ全てnull又は
3つ全てnon-nullだけを許す。partial linkを保存しない。

## One state wrapper

communication、deadline、review、handoffのcanonical `recordType`はすべて
`tracker-record`。`payload.trackerType`でstrict payload schemaをdiscriminateする。

```text
recordType: tracker-record
scopeType: matter
scopeId: matterId
recordId: stable ASCII ID
itemId / eTag / version / updatedAt
payload:
  trackerType: communication | deadline | review | handoff
  ... strict tracker-specific fields
```

全`tracker-record`はtracker typeにかかわらずsemantic invariantを共有する。

- outer `scopeType`は必ず`matter`
- outer `scopeId == payload.matterId`
- payloadが`tenantId`又は`practiceId`を重複保持する場合、outer値と完全一致

communication、deadline、review、handoffだけでなく、将来追加するmatter-scoped
trackerにも自動適用する。JSON Schemaの`scopeType` constに加え、
package-source build validatorがcross-field equalityを検証する。skill packageには
schemaとpositive/negative fixturesを同梱し、validator executableは重複同梱しない。

`communication-entry`、`deadline-candidate`、`review-item`、
`semester-handoff`をtop-level `recordType`として新規writeしない。旧recordをimportする
場合はsource compatibility fieldとして保持し、canonical write時に`tracker-record`へ
変換する。

portfolio modeはtracker recordを新規作成せず、fresh unbound sessionでauthorized
matter recordsからpseudonymous minimum projectionをreadする。1件を開く又はwriteする
場合はnew bound conversation。

## Workflow evidence

### Communication

artifact item ID、version、hash、destination、reviewer、delivery evidence、correction
linkを必須fieldとして持つ。consequential translationは
`legalAndLanguageReview`で責任弁護士のlegal reviewとcompetent language reviewの両方を
記録する。

### Deadline

trigger item/version、authority/effective date、civil electronic-service events、
time-computation fields、transition regime、completion-postponement/renewal ground、
candidate lifecycle、completion evidence、closure authority、calendar entry lifecycleを
分ける。

criminal deadlineの`governingTimeComputationRegime`は
`criminal-procedure-code-55`。民事訴訟法95条/Civil Codeを刑事へ代用しない。
民事訴訟法55条はlitigation-agent authorityのsourceでありtime-computation enumではない。
このregimeでは`civilElectronicService.mode: not-applicable`、全civil electronic-service
metadata null/empty、`transition.recordRegime: procedure-specific`を強制する。
`post-2026-05-21-new-ordinary-civil` transitionをrejectする。

`closed`はreason/approval/actor/timeに加え、最低1件の`sourceEvidence`を要求する。
各closure sourceはexact item ID、version、authority type、effective date、retrieval、
review statusを持つ。versionなしのorder、email又は口頭説明でcloseしない。

`calendarEntry.status`:
`not-requested | approval-pending | write-pending | created | failed | removed`。
candidate、verification、calendar write、completion、closureを同一operationにしない。

### Review

source item IDs/versions/effective datesは`sourceEvidence[]`、decision理由は
`decisionNotes`。artifact item/version/hash、destination、reviewer role、approval、
release actor、legal/language reviewを必須化する。

`reviewSubjectTypes`により、legal proposition/deadline/engagement/conflict/scope/
external legal contentは`responsible-lawyer`、pedagogy/adminだけは`supervisor`、
mixedは`both`。consequential translationはcompetent-language reviewを追加する。

### Handoff

incoming conflict status、deadline/communication source record IDs、safe contact、
originals、access plan、binding revocation batchを記録する。

## Matter archive / close / reactivate

archive又はcloseは`binding-revocation-batch`を使う。

1. exact active matter item/eTag/versionと`bindingGeneration`を取得する。
2. 最初のatomic conditional operationで`archive-pending`又は`close-pending`へ
   transitionし、generationを1増やしてnew binding createをfenceする。
3. fence後に全bindingをenumerateし、activeとalready-revokedへ分ける。
4. active bindingだけをconditional revokeし、already-revokedはsatisfiedとして
   再更新しない。
5. enumerated IDsはactive IDsとalready-revoked IDsのdisjoint unionに一致し、
   `results[*].bindingItemId`はactive IDsのunique exact setとする。
6. zero activeを再照合後にだけ`archive -> archived`又は`close -> closed`へfinalizeする。
7. fence前にcommitしたcreateはenumerationで捕捉し、fence後のcreateはexact matter
   precondition/generationでrejectする。
8. 1件でも欠落、重複、余分、failure、post active count非zeroならfenced stateを
   維持してfail closedとし、finalizeしない。
9. gatewayがatomic fenceを保証できなければarchive/closeは利用不可。
10. reactivateは`bindingGeneration`を増やし、既存bindingを再利用しない。
11. reactivation後のsubstantive accessは新しいCowork conversationでfresh bindingを
   作成した後だけ。

`blockTransitionOnAnyFailure: true`と
`reactivationRequiresFreshBinding: true`はschemaで固定する。

## Validation

package validationでは:

1. JSON parse
2. `Draft202012Validator.check_schema`
3. `FormatChecker`付きで全fixtureをtop-level schemaへvalidateし、全
   `tracker-record`をshared state-envelope schemaへもvalidate
4. package-source build validatorでcross-array/cross-field semantic invariantをvalidate
5. `clinic-state-payload-negative-examples.json`のbypassを全件reject
6. root schema/examples/validatorと全skill-local common copyのbyte parity

を実行する。
