---
name: privilege-log-review
description: >
  canonical IDを保持しつつ、日本案件では一般的なUS privilege logを前提にせず、秘密性、提出拒絶、閲覧制限、秘密保持命令、契約・内部distribution controlをentry別にreviewする。close callはdesignationを外さず有資格者へflagする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Confidentiality and withholding review

canonical label:
`/litigation-legal:privilege-log-review [log file, or document set]`

日本matterではuser-facing outputを「秘密性・提出拒絶review」とし、actual court
protocolが要求する場合だけprivilege log形式を使う。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、active matter binding、attorney-limited/evidence/clean-team ACLを
   確認。
3. exact instrument、court order、production protocol、document set/versionを確認。
4. Japanなら
   `references/common/jurisdictions/ja-jp/evidence-confidentiality-preservation.md`と
   `source-register.md`を読む。
5. 民訴法197、220、92条、弁護士法23条、特許法105条等のactual basisをcurrent
   official sourceで確認。
6. source use restriction、destination、external/internal version、DLPを確認。
7. quote/citation coverageをexhaustiveに行う。
8. AIはproduce/withhold/redact/designate/serveを実行しない。

## Review fields

```yaml
confidentialityClassification: public | internal | confidential | restricted | clean-team
withholdingOrRefusalBasis: "[exact law/order/agreement or null]"
publicRecordAccessBasis: "[basis or null]"
courtConfidentialityOrder: "[order ID or null]"
contractualRestriction: "[basis or null]"
internalDistributionControl: "[control]"
proposedDecision: produce | withhold | redact | seek-direction | unresolved
finalDecision: produce | withhold | redact | seek-direction | unresolved | null
reviewedByQualifiedCounsel: "[object ID or null]"
reviewedAt: "[ISO-8601 or null]"
```

AI outputは`proposedDecision`だけを設定する。`finalDecision`はqualified counselの
identity/timeとexact source reviewが記録された場合だけ更新する。

表示例:
`秘密・社外秘／弁護士確認用 — 表示自体は開示拒絶権を生じさせません`

## Three-state review

- **clear basis**: exact law/order/protocolとfactsが一致。なおhuman final review。
- **keep + flag**: mixed legal/business、third party、self-use document、waiver/
  confidentiality、in-house counsel、attachment、foreign proceeding等のclose call。
- **no identified basis**: basisが見当たらないというassessmentを記録するが、
  designationをAIがremoveしない。

under-markingは回復困難。uncertain itemはkeep + `[review]`。

日本defaultにしないもの:

- FRCP 26(b)(5)(A) mandatory fields
- subject-matter waiver
- fact/opinion work-product tier
- FRE 502 clawback
- in-house counsel copyによるautomatic privilege

foreign/U.S. protocolが実際に適用される場合だけ別branch。

## Workflow

1. actual required fields/protocolを確認。
2. document metadata、author/recipient、purpose、attachment、distribution、sourceを読む。
3. entryごとにpossible basisとcounterpointを記録。
4. repeated patternをgroupするが、individual source linkを失わない。
5. citationを全抽出し、checked N of Mを報告。
6. external log候補とinternal reasoningを別artifactにする。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# 秘密性・提出拒絶review — [matter]

**Instrument / protocol:** [...]
**Entries reviewed:** [N]
**Results:** clear basis [N] / keep+flag [N] / no identified basis [N]

## Keep + flag
| Entry | Source/version | Claimed basis | Evidence for | Evidence against | Counsel question |
|---|---|---|---|---|---|

## No identified basis — designation unchanged
| Entry | Reason | Missing source/fact |
|---|---|---|

## Clear basis
[count/list on request]

## Pattern observations
[repeat issue、description quality、ACL]

## External protocol output candidate
[必要fieldだけ。内部reasoningを除く]
```

## Completion

counts、actual rule/order、citation coverage、pattern、ACL、unresolved calls、save stateを
示し、次から選んでもらう。

1. flagged entries review packet
2. court/protocol direction request draft
3. missing metadata/source取得
4. sanitized external log candidate
5. other

## 行わないこと

- close callの最終判断
- designation removal
- produce/withhold/redact/serve
- US privilege/work-productの日本への移植
- local filesystem、agent、hook、subagent
