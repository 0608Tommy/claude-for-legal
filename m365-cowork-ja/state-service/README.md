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

ordinary createのrequest shapeは変わりません。`session-matter-binding`だけは、
参照matterのexact `itemId`、`expectedStatus: active`、latest `eTag` /
`version`または`bindingGeneration` tokenを`matterPrecondition`として追加します。
gatewayはmatter preconditionとbindingの`expectedAbsent: true`を同一transactionで
評価し、どちらかが失敗すれば何も作成しません。read-check後に別createを行う
sequential実装は契約違反です。

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

session bindingはgeneric state keyへ次の固定値で写像します。

- `scopeType: session`
- `scopeId: [userObjectId]:[sessionId]`
- `recordType: session-matter-binding`
- `recordId: active-matter`

outer `tenantId` / `practiceId` はpayloadと一致し、`scopeId`のuser/sessionも
payloadと一致しなければなりません。createは`expectedAbsent: true`のactive
bindingだけで、atomic active-matter preconditionを必須とします。
`tenantId`、`practiceId`、`userObjectId`、`sessionId`、
`matterId`、`boundAt`、`boundBy`、`expiresAt`は作成後に変更できず、唯一の
更新はcurrent active bindingを完全なrevocation metadata付きで`revoked`へ
移すことです。revoked bindingを再利用・再有効化しません。

共有practice profileへ単一user roleまたはactive matterを保存しません。
practice-levelは`matterId: null`のactive bindingではなく、bindingが存在しない
fresh sessionとして表現します。
`switch` / `none`はcurrent bindingをrevokeして現在の会話を停止します。
別matterのbindingはfresh sessionでconditional createし、practice-levelは
fresh sessionでbindingなしにします。matter closeは最初にmatterを
`close-pending`等のnon-active stateへconditional transitionし、generation方式を
使う実装では同じoperationで`bindingGeneration`も増やして、新規binding createを
atomically fenceします。その後に全bindingを列挙し、activeだけをrevokeし、
zero activeを確認してから`archived`へfinalizeします。
fence前にcommitしたcreateは列挙対象となり、fence後のcreateはmatter
preconditionで失敗します。未確認または失敗が1件でもあればfenced stateを維持し、
matter accessをfail closedで拒否します。

## 実装状態

本directoryはschema、SharePoint layout、ACL、concurrency契約を実装します。
実際のsite/list/library作成、Graph application、MCP gateway、Power Platform
connection、retention/Purview policyはtenant操作が必要であり未実行です。
