> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Power Platform compatibility contract

本Cowork packageはskills-onlyであり、Power App、cloud flow、Dataverse solution、
connection reference、environment variable、approval、scheduleを含まない。本書は
別solutionが満たすべき互換境界であり、provisionまたは実行の証拠ではない。

## Recommended solution boundary

```text
cflja_LegalBuilderAdminCore
├── request intake / schema validation
├── durable approval state
├── queue state machine
├── append-only audit
└── admin evidence reconciliation

cflja_BuilderRegistrySync
├── registry-reader
├── quarantine-and-qa
├── administrator-approval
└── catalog-writer
```

modern flow sourceは承認済みdevelopment tenantで作成し、unmanaged solutionから
export/cloneしてreviewする。手書きJSON/YAMLをproduction-ready flowと表示しない。

## Dataverse table compatibility

最低限:

- `cflja_BuilderRegistry`
- `cflja_BuilderPublisher`
- `cflja_BuilderLicensePolicy`
- `cflja_BuilderConnectorPolicy`
- `cflja_BuilderCandidate`
- `cflja_BuilderSnapshot`
- `cflja_BuilderScanFinding`
- `cflja_BuilderQAReview`
- `cflja_BuilderQAParameter`
- `cflja_BuilderPackage`
- `cflja_BuilderChangeRequest`
- `cflja_BuilderApproval`
- `cflja_BuilderDeployment`
- `cflja_BuilderProtectedAsset`
- `cflja_BuilderAuditEvent`
- `cflja_BuilderDeadLetter`

alternate key、row version、length/count/enum上限、`additionalProperties: false`相当の
payload validationを実装する。28日を超え得るapprovalはdurable Dataverse stateへ
置き、単一flow runを待機させない。

## SharePoint compatibility

専用site `LegalSkillCatalog`をmatter document siteから分離する。

### `SkillQuarantine`

- path: `{candidateId}/{snapshotId}/{relativePath}`
- versioning on
- external sharing off
- search/indexing off
- item/library ACL
- raw HTML/SVG/script inline rendering off
- retention/security incident policy

### `ApprovedSkillPackages`

- path: `{skillId}/{catalogVersion}/{packageSha256}.zip`
- immutable approved package
- package/source/approval/signature/protection metadata
- overwrite禁止。new versionまたはsuperseding recordを作る

## Identity and connection references

次はbuilder workflowsが使用するshared governanceの7 identitiesである。

| Identity | Minimum scope | 禁止 |
|---|---|---|
| `spn-legal-reader` | approved registry read、restricted ingest create | catalog/queue/deployment write |
| `spn-legal-verifier` | approved official sourceのread、status/effective-date verification record create | catalog/queue/deployment write、approval、package mutation |
| `spn-legal-analyzer` | quarantine read、scan/QA record create | raw source fetch、catalog write |
| `spn-legal-writer` | request/state/audit/draft write | raw source read、deployment |
| `spn-legal-runtime` | parent/child flow ownership、run ledger | raw source、external delivery |
| `spn-legal-delivery` | exact approved notification | state/catalog mutation |
| `spn-legal-deployer` | PAC solution import only | M365 app deploymentへの流用 |

M365 app deployment automation identityは、official API、permission、service-principal
support、least privilegeをtenantで実証するまで作らない。既定はhuman deployment
operator。

connection referenceを分けても同一credentialへbindすれば分離ではない。target
system ACL、actual connection owner、environment admin/co-owner privilegeを確認する。
`spn-legal-verifier`はreader/analyzer/writer/approver/deployerと別credentialにし、
verification結果だけをappendする。catalogまたはdeployment authorityを付与しない。

## Flow stages

1. **Intake:** schema、scope、actor、idempotencyを検証
2. **Preflight:** source/package/evidence/first-party/dependencyを再取得
3. **Review:** bounded structured evidenceだけをreviewerへ渡す
4. **Approval:** exact binding hash、expiry、segregation
5. **Queue:** approved requestを`admin-action-required`へ
6. **Reconcile:** human admin evidenceとread-backを照合
7. **Audit:**各transitionをappend

Power AutomateがCowork conversationまたはMarkdown skillを直接実行するとは扱わない。
Coworkはstructured requestを作り、flowはdeterministic orchestrationを行う。

## DLP、retention、dead-letter

- Business/Non-Business connector groupをtenant policyで検証
- quarantine、Dataverse、SharePoint、notification destinationを同一data policyで評価
- Cowork prompt/task内DLP coverageを主張しない
- retention/legal hold未設定ならproduction queueをblock
- dead-letterはrequest ID、stage、error class、retry countのみ
- raw source、package、secret、client data、privileged analysisをdead-letterへ入れない

## Health evidence

automation availableと表示するには、次をstateから確認する。

- solution unique name、version、environment ID
- approved owner、connection reference、actual credential owner
- DLP policy ID、retention policy
- enabled flow IDとtrigger
- last successful run、last failure、dead-letter count
- schema contract version

本package内の`m365agents.yml`または本書の存在はhealth evidenceではない。

## Tenant acceptance

本番前にapproved tenantで、positive/negative routing、self-approval拒否、
hash change失効、stale eTag、duplicate idempotency、partial failure、dead-letter、
first-party refusal、CoCounsel blocker、admin evidence reconciliationをtestする。
