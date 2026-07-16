> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Clinic profile and setup-session schema

machine-readable正本は:

- `common/clinic-state-payloads.schema.json#/$defs/clinicPracticeProfile`
- `common/clinic-state-payloads.schema.json#/$defs/setupSession`

fixtureは:

- `common/clinic-state-payload-examples.json`

本書は別schemaを定義しない。

## Canonical profile paths

```text
payload.clinic
payload.authority
payload.conflicts
payload.engagement
payload.studentParticipation
payload.supervision
payload.pedagogy
payload.data
payload.urgentRouting
payload.sourceCards
payload.houterasuPrograms
payload.semester
payload.integrations
payload.legalReview
payload.activationApprovalIds
```

`cold-start-interview`と`customize`は同じnested path、enum、required fieldを使う。
flat alias又は別名fieldへwriteしない。

legal review status:

```text
pending | in-review | approved | blocked
```

`setup-session.payload.status`:

```text
draft | paused | review-pending | interview-complete | superseded
```

`interview-complete`はprofile/legal review approvalではない。`profileStatus: active`は
Japan counselとclinic supervisorの両legal reviewが`approved`で、activation approval
IDsが記録された場合だけschema-validである。本packageのshipped statusはDRAFT/pending。

setupの`profileItemId`、`profileVersion`、`profileETag`は1つのreference tupleであり、
全null又は全populatedだけを許す。partial tupleはschema error。

## Mandatory distinctions

- information barrierはconflict clearance/waiverではない。
- disclaimerはactual conductによるengagement/scope成立可能性を排除しない。
- student participation matrixはinternal policyで、legal authority又はAttorney Act
  72 cureではない。
- Houterasu programはconsultation aid、representation advancement、document
  preparation advancement、appointed criminal counselに分ける。
- `criminal | immigration | housing | benefits`はapproved source cardを別々に持つ。
- data sectionはAPPI regime-specific assessment itemを参照し、generic GDPR
  lawful-basis fieldを持たない。
- `appiHostRegime`、Article 58 assessment、clinic restricted categoriesと法定
  要配慮個人情報が同義でないことをcanonical data sectionへ記録する。
