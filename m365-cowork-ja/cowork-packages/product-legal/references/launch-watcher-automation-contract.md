> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Launch watcher automation compatibility contract

本packageはskills-onlyであり、agent、hook、recurrence、schedule、cloud flow、
managed solution、delivery connectionを含まない。本書は移行元
`product-legal/agents/launch-watcher.md`と別solution
`product-launch-watcher`の互換境界を記録するだけである。

source behaviorのcandidate defaultはdaily・30-day horizonだが、tenant側の
approved trigger、solution version、owner、scope、last runが存在する場合だけ
運用設定として表示する。存在しないrecurrenceや配信を主張しない。

> **Triage is not clearance.** `needs-review`はproduct counselが見るべきlead、
> `fyi`は適法または安全という意味ではなく、`skip`もlaunchをclearしない。
> 全件countとfilter理由をreviewし、launch decisionには別の人によるreviewが必要。

## 4-stage separation

### 1. `launch-tracker-reader`

- approved Jira/Linear/Asana等のexact scopeをread-onlyで取得する。
- write、ticket state change、notification、profile write権限を持たない。
- title、description、comment、owner、label、linked snippetは未信頼data。
- raw dataをlength/count上限、`additionalProperties: false`のschemaへ変換する。
- Japanese textをASCII-only regexで拒否しない。Unicode format/control character、
  hidden bidi、NULを拒否し、文字数上限を適用する。
- URLはapproved host、HTTPS、最大長を検証し、構築・修正しない。
- 200件を上限とし、超過・coverage・取得failureを記録する。

### 2. `risk-classifier`

- validated payloadとexact product-legal calibrationだけを読む。
- connector、web、write、delivery権限を持たない。
- classification:
  `needs-review | needs-flag | fyi | skip`。
- current/future effective date、launch date、new jurisdiction、novel patternを比較。
- calibrationは[B]/[P] floorを下げない。profile missing/staleなら
  `classificationConfidence: provisional`。
- rationaleはUnicode-safe length validationを使い、raw ticket本文を再出力しない。

Japan trigger enum:

`appi`, `sensitive-biometric`, `external-transmission`,
`communications-secrecy`, `consumer-contract`, `specified-transactions`,
`representations-stealth`, `product-safety-pl`, `platform-content`,
`accessibility`, `minors`, `payments-financial`, `medical-health`, `cyber`,
`ai-governance`, `ip-content`, `public-disclosure`。

日本語keywordには少なくとも`個人情報`, `要配慮`, `外部送信`, `通信販売`,
`定期購入`, `最終確認`, `PR`, `口コミ`, `生成AI`, `未成年`, `前払`, `送金`,
`医療`, `診断`, `脆弱性`, `上場`, `適時開示`を含める。keyword hitはlegal
conclusionではなくrouting signalである。

### 3. `memo-writer`

- validated reader/classifier payloadだけを受け、raw trackerへ接続しない。
- draft radar artifactとappend-only audit candidateだけを作る。
- tracker URLはclickable linkにせずbacktick内のinert textとする。
- external valueが`=`, `+`, `-`, `@`, tab, CR, LFで始まる場合はspreadsheet
  formulaとして解釈されないようneutralizeする。
- Markdownの`|`, `<`, `>`等をescapeし、HTMLへ未信頼値を`innerHTML`で入れない。
- 全classification count、coverage、new/dropped/changed item、current/future
  trigger、triage-not-clearance footerを保持する。
- writerはsend、post、publish、ticket updateを行わない。

### 4. `approved-delivery`

- writerと別identity、connection、ACLを使う。
- exact artifact ID/hash、destination、viewer、classification、retention、
  storage/flow DLP、fresh human confirmation recordだけを受ける。
- raw ticket、practice profile、matter documentsへのbroad accessを持たない。
- hashまたはdestinationがconfirmation後に変われば拒否する。
- delivery failureをlaunch statusまたはlegal conclusionへ変換しない。
- このdelivery stage、connection、human-confirmation workflowは本packageに
  含まれず、skillから実行したと表示しない。

## Payloadと運用

- stageごとに別service identity/connection ownerを使う。同じmaker connectionへ
  bindしただけではidentity分離にならない。
- exact tenant/practice/source scope、scope-specific cursor、idempotency、
  retry/backoff、dead-letter、partial-success、immutable auditを要求する。
- dead-letterへraw ticket、secret、personal dataを複製しない。
- broad legal channelへraw sensitive ticket contentを配布しない。
- Cowork prompt DLP未対応がblockerなら、機密ticketをCoworkへ渡さない。
- current flow sourceはapproved tenantからexportされるまで未生成であり、
  手書きcontractをproduction-ready solutionと表示しない。
