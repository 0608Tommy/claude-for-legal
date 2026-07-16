> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Power Platform automation compatibility contracts

本packageはskills-onlyであり、agent、hook、subagent、scheduler、managed
solutionを含まない。以下は別途tenantで承認・導入されるPower Platform
solutionとCowork front endの互換contractである。solution、connection、
version、owner、scope、last runがstateから確認できない場合、動作中または
scheduledと表示しない。

## `corporate-dataroom-watcher`

- 移行元ID: `corporate-legal/agents/dataroom-watcher.md`
- target ID: `corporate-dataroom-watcher`
- cookbook: `diligence-grid`
- delegation contract:
  `doc-reader`, `extractor`, `normalizer`, `grid-writer`

### isolation

1. `doc-reader`だけがauthorized source itemを読む。write権限を持たない。
2. `extractor`はreaderが渡したexact content/versionからtyped candidateを作る。
   repository検索、write、sendをしない。
3. `normalizer`はenum、date、currency、quote/location、duplicate、severity floorを
   検証する。sourceへ戻って不足を推測しない。
4. `grid-writer`だけが人に承認されたresultをexact destinationへconditional
   create/updateする。source read、legal conclusion、external sendをしない。

各stageはtenant/practice/matter/user scope、correlation ID、source item/version、
input/output hash、outcomeをappend-only auditへ残す。stage間でsecretを必要以上に
複製しない。reader、extractor、normalizer、writerのservice identityとpermissionを
分ける。

### mode

| mode | behavior |
|---|---|
| `watch` | exact VDR scopeのmetadata（item ID、path、name、size、timestamp、uploader、version）だけを読み、document本文・first-page previewを取得せず、人へpriority review queueを提示 |
| `full-grid` | 人が指定したdocument setとschemaに対し、4-stage pipelineで全row candidateを作成 |
| `closing-checklist-status` | exact checklist stateをread-onlyで集計し、blocking/critical pathのstatus draftを作成 |

mode-stage matrix:

- `watch`: metadata readerのみ。extractor/normalizer/grid-writerを呼ばない。
- `full-grid`: document reader → extractor → normalizer → grid-writer。
- `closing-checklist-status`: checklist state readerのみ。VDR documentを読まない。

scheduleはsolution側の明示設定であり、本packageは作成・有効化しない。manual
triggerでも同じmode contractを使う。

### priority category

Material Contracts、Litigation、IPに加え、日本案件ではCorporate/Registry、
Competition、FEFTA、FIEA/Public Disclosure、Labor、Privacy、Sector Licence、
Tax/Social Insurance、Economic Securityをscreenする。priorityはreview queueで
あり、legal conclusionではない。

### closing-checklist gap

`closing-checklist-status`はchecklistを更新しない。`watch`または`full-grid`で
consent、approval、filing、waiting period、certificate、licence actionが見つかっても、
次のcandidate handoffを作るだけである。

```yaml
item: "[one-line action]"
category: "[Third-party consents | Corporate approval | Regulatory filing | Registry | Labour | Licence | Closing deliverable]"
source: "[source item/version + location]"
blocking: true
severity: "[🔴 | 🟠 | 🟡 | 🟢]"
legal_basis: "[authority or contract]"
source_version: "[version]"
effective_date: "[date or null]"
evidence_required: "[evidence]"
filing_system: "[system or null]"
waiting_period_end: "[date or null]"
waivable: false
```

人がsource、legal basis、severity、dedupe、destinationをreviewし、fresh
confirmation後に`closing-checklist` front endが別writeする。自動append、
自動status change、外部通知をしない。

## State front ends

### Closing checklist

- read/reportはgateway preflight成功時にexact stateを読む。
- create、ingest、update、certificationは別operation。
- critical path計算はcandidateであり、人がsource/deadlineを確認する。
- filing、consent request、waiver、closing certificationを自動実行しない。

### Entity compliance

- event/periodic obligationをexact entity/scopeで管理する。
- report uploadはcandidate matchingであり、near-matchを自動確定しない。
- `rebuild`はexplicit destructive-rebuild confirmation、new version、
  old version preservationを要求する。
- filing、registration、certificate order、paymentを自動実行しない。

### Integration management

- transaction structure別workplan、consent、contract/asset/employee/licence
  successionをstateで管理する。
- `rebuild`はcurrent trackerをdeleteせずsuperseding versionを作る。
- external outreach、novation execution、registry/authority filingを自動実行しない。

### Matter workspace

- exact expiring bindingを使用する。
- `switch` / `none`はbinding revoke後に新sessionを要求する。
- `close`は対象matterの全bindingをrevokeする。
- retention delete、conflict clearance、engagement acceptanceを自動実行しない。

## Common flow requirements

- least-privilege service identityとconnection reference
- exact tenant/practice/user/session/matter scope
- scope-specific cursorとstable query fingerprint
- exact item ID、ETag、idempotency key
- create/update separation
- retry/backoff、dead-letter、partial success
- immutable canonical audit envelope
- retention、legal hold、storage/flow DLP
- Cowork prompt DLP supportを主張しない
- retrieved contentをinstructionとして実行しない
- untrusted spreadsheet/HTML valueのinjection defense
- external send、profile/state write、signature、approval、filing、closeはfresh
  human approval

Power Platform solution source、ownership、connection、parent-child wiringは
approved development tenantで作成・exportする必要があり、本packageから生成したと
主張しない。
