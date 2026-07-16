> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Employment matter records

## Matter profile

SharePoint `matters` library:

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: "[opaque matter ID]"
slug: "[lowercase-hyphen]"
pseudonymousCode: "[EMP-0001]"
matterType: "[hire | termination | contested-termination | investigation | whistleblowing | leave | medical-accommodation | discipline | classification | country-expansion | policy-project | other]"
status: active | archived
confidentiality: standard | heightened | restricted | clean-team
restricted: true
jurisdictions: []
authorizedViewerObjectIds: []
retentionClass: "[class]"
legalHold: false
openedAt: "[ISO-8601]"
```

氏名・allegation・diagnosisをslug、record ID、central indexへ入れません。

## Matter state key

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: matter
scopeId: "[matterId]"
recordType: matter-state
recordId: "matter:[matterId]"
```

newは`expectedAbsent: true`、updateはexact`itemId`/`eTag`です。

## Binding

canonical binding schemaはcommon runtime contractのfieldをそのまま使います。
active bindingの`matterId`はnon-null。switch/noneはnew session、closeは全binding
revokeです。

## Restricted identity

identity mappingはmatter libraryのrestricted itemとして保存し、一般state/auditへ
複製しません。whistleblower identityは別item/ACLです。
