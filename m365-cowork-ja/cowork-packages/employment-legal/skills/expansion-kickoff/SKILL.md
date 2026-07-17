---
name: expansion-kickoff
description: >
  new-country employment expansionを開始し、cost比較より先にEOR・dispatch・worker-supplyの法的feasibilityを確認し、entity/EOR framing、tax・finance・HR・privacy・immigration questions、outside-counsel brief、dependency trackerを作る。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# International expansion — kickoff

旧来のlabel:
`/employment-legal:expansion-kickoff [country]`。

hidden `international-expansion`は登録せず、
`references/international-expansion-framework.md`へcompileしています。

## Mandatory structure / counsel / state gate

1. `references/common/cowork-runtime-contract.md`を読み、exact user/practiceと
   source/destinationを確認します。authorized `country-expansion` matterが
   ある場合はmatter scope、fresh sessionで明示的にpractice-levelを選んだ場合は
   `scopeType: practice`のproject stateを使います。別matter contextをcarryしません。
2. gateway preflight失敗時はplan/tracker draftだけで、project/state作成済みと
   表示しません。
3. jurisdictionはtarget country/work location/entityで解決し、current local primary
   sourceとqualified local counselへrouteします。
4. EOR/entity cost比較前にgenuine employer、daily direction、dispatch/placement/
   outsourcing/worker supply、licence、work rules、payroll、insurance、OSH、
   discipline/dismissal ownerを確認します。
5. sales/signing roleはPE/tax counselへrouteします。
6. employee data/HRIS foreign transfer、visa/status、social insuranceを別track。
7. tracker create、matter create/switch、outside-counsel sendは別operation。
8. AIはEOR/entity、hire、payroll、insurance、visa、filing、external sendを決定・実行
   しません。
9. Cowork内DLP必須ならsensitive expansion materialを投入せずproduction停止です。

Japan target/structureには
`references/common/ja-jp/international-insurance.md`を使います。

## 会話state

`intake` → `legal-feasibility` → `eor-entity-framing` →
`cross-functional-asks` → `outside-counsel-brief` →
`tracker-candidate` → `confirm-create` → `audit`

## Intake

frameworkのsingle blockでcountry、roles、headcount、first-hire target、entity/EOR、
manager/control、strategic commitment、tax/finance/HR/privacy/immigration owners、
sales authority、HRIS flow、outside counselを確認します。

## Legal feasibility

EOR/vendor candidateが🔴ならcost tableより先にblockし、specific counsel questionを
示します。日本ではGeneral Rules Act Article 12、Employment Security Act
Article 44、Worker Dispatch Act、36 agreement、social insurance、foreign-worker
notification、APPIを確認します。

## Framing / questions

`references/international-expansion-framework.md`のEOR/entity tableと、
tax、finance/payroll、HR/total rewards、privacy/security、immigration、
outside counselへの具体的questionsを作ります。headcount break-even、contribution
rate、visa timelineをhardcodeしません。

## Tracker create

`references/expansion-records.md`のproject/itemsをseparate conditional createsに
します。project `recordId`は
`expansion:[countryCode]:[projectId]`。

existing active projectがあればoverwriteせず`expansion-update`を案内します。
matter create/switchは`matter-workspace`の別confirmationです。

## Output

- structure legality status
- EOR/entity factors
- PE/privacy/immigration flags
- named owner questions
- tailored outside-counsel brief
- open dependency items
- tracker create status/source gaps

next itemを人に選んでもらい、自動送信・更新しません。
