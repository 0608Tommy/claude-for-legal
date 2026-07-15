# Power Platform automation source boundary

Cowork app ZIPとは別に、10個のscheduled/event workflowをPower Platform
managed solutionとして配布するための契約です。

## 現在の状態

このrepositoryには、agent catalog、identity/DLP/approval contract、
deployment settings template、schema fixtureを保存します。**実際のmodern
cloud flow sourceは未生成です。**

PAC 2.9.3の`solution init`はlegacy XML / `.cdsproj`を作りますが、modern
flowのYAML source-control layout、GUID、`workflow.yml`、connection reference
wiringを安全に作成しません。次の手順が必要です。

1. 承認済みdevelopment tenantでunmanaged solutionを作る。
2. parent/child flow、connection reference、environment variable、Dataverse
   tableを作る。
3. owner、identity、DLP、approval、licensingを設定する。
4. `pac solution clone`でtenant生成sourceを取得する。
5. 本directoryの契約と比較し、review後にcommitする。
6. `pac solution pack --packagetype Managed`でoffline buildする。

tenant export前に手書きしたJSON/YAMLをproduction-ready solutionと表示しません。

## Solution分割

```text
connectors/legal-agent-connectors/
core/legal-automation-core/
agents/commercial-deal-debrief/
agents/commercial-renewal-watcher/
agents/commercial-playbook-monitor/
agents/corporate-dataroom-watcher/
agents/employment-leave-tracker/
agents/ip-renewal-watcher/
agents/builder-registry-sync/
agents/litigation-docket-watcher/
agents/product-launch-watcher/
agents/regulatory-reg-change-monitor/
```

各agent solutionにparentとchild flowを同居させます。connector solutionを
先にimportし、core、agentの順にimportします。

## 実行境界

- readerはsource readとrestricted staging writeだけ。
- analyzerはstaging readとanalysis writeだけ。
- writerはapproved analysisからdraft/output/auditを作り、raw sourceを読まない。
- deliveryはexact artifact hash、destination、approvalを受けて送信する。
- flow間payloadは`additionalProperties: false`、length/enum/count上限を持つ。
- retry後のfailureはdead-letterへ保存し、raw document/secretを入れない。
- consequential actionはfresh approvalとhash再確認後だけ実行する。

connection referenceを分けても、同じmaker connectionへbindすればidentity
分離になりません。target service側のACLと実際のconnection ownerを確認します。

## Coworkとの関係

Power AutomateがMarkdown agentまたはCowork conversationを直接実行するとは
扱いません。deterministic orchestration、SharePoint/Dataverse state、
approved custom connector経由の別agent runtime、成果物配布を担当します。

Cowork licenseとPower Automate/premium connector/process capacityは別です。
