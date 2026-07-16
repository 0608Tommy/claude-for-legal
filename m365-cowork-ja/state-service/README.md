# SharePoint / OneDrive state-service contract

Cowork skillsが直接任意のpathを読み書きするのではなく、tenant-approved
Graph/MCP/Power Platform gatewayを介して、型付きrecordを扱うための契約です。

## 保存先

- SharePoint `profiles`: company、practice、user profile
- SharePoint `matters`: matter profile、source documents、templates
- SharePoint `outputs`: reviewed shared deliverables
- SharePoint `state`: registry、tracker、cursor、session binding、setup session
- SharePoint `audit`: append-only event
- OneDrive: current userの未共有draft

## Create

新規recordは既存`itemId`/`eTag`を要求しません。完全なcomposite key、
`recordId`、unique `idempotencyKey`を送り、同一keyが存在しない条件付きcreate
を行います。成功後に返された`itemId`と`eTag`を保存します。

## Update

更新はexact `itemId`、current `eTag`、unique `idempotencyKey`、変更差分を
要求します。stale writeは上書きせず`412`相当で拒否し、current recordを
再読取りして人へ差分を示します。

## Matter isolation

- user profile key: `tenantId + practiceId + userObjectId`
- binding key: 上記 + `sessionId`
- matter key: `tenantId + practiceId + matterId`
- generic state key:
  `tenantId + practiceId + scopeType + scopeId + recordType + recordId`

共有practice profileへ単一user roleまたはactive matterを保存しません。
practice-levelは`matterId: null`のactive bindingではなく、bindingが存在しない
fresh sessionとして表現します。
matter close時は、その`matterId`を参照する全bindingをrevokedへ更新します。

## 実装状態

本directoryはschema、SharePoint layout、ACL、concurrency契約を実装します。
実際のsite/list/library作成、Graph application、MCP gateway、Power Platform
connection、retention/Purview policyはtenant操作が必要であり未実行です。
