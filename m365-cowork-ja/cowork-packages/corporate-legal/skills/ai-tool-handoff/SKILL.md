---
name: ai-tool-handoff
description: >
  Luminance、Kira等のbulk-review toolへ渡す候補を判定し、外部transferの法務・security gate、batch指示、source検証、QA sample、deal判断層を会話で管理する。AI toolへの送信、upload、承認は行わず、人の実行前draftと検証記録を作成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# AI tool handoff

旧来の参照labelは`/corporate-legal:ai-tool-handoff`。Coworkでは外部toolを
自動起動せず、handoff stateを会話で進める。

## 目的

Luminance、Kira等はuniformな大量契約からchange-of-control、assignment、
exclusivity、MFN、termination、auto-renewalを抽出する用途に向く。一方、
transaction structureに照らしたtrigger、materiality、consent、waiver、
Japanese lawは人の判断層である。本skillはbulk extractionの準備とQAを行う。

まず`tabular-review`で扱えるscopeか検討する。数百documentとtyped schemaで
足りる場合、外部transferより先にMicrosoft 365内のreviewを提案する。

## 必須gate

1. **Runtime:** `references/common/cowork-runtime-contract.md`を読む。local batch
   folder、local output、agent/subagentを作らない。
2. **Matter:** exact expiring session binding、matter `status: active`、current
   user accessを確認する。practice-levelはfresh sessionでbinding不在を確認する。
3. **Source:** exact source item/version、document count、coverage、category、
   confidentialityを取得する。表示名だけでdocumentを選ばない。
4. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。
   日本なら`references/common/ja-jp/privilege-security.md`と
   `references/common/ja-jp/diligence-overlays.md`を読む。
5. **Mandatory security gate:** 外部transfer前に、VDR/customer/client terms、
   authorization、APPI role/purpose、foreign transfer、subprocessor/data location、
   retention/deletion、no-training、encryption/access log、My Number除外、
   trade secret、MNPI、export-controlled technology、clean-team、legal holdを
   一つずつ確認する。
6. **Privilege/destination:** 日本では米国`ATTORNEY WORK PRODUCT`と同じ保護を
   断定しない。recipient、tool workspace、operator accessを示す。
7. **Human approval:** AIはupload、send、workspace create、external processing
   approvalを行わない。transfer manifestを示し、当該batchへのfresh approvalで
   停止する。
8. **Trust:** `use as-is | spot-check | full re-review`のsource enumを保持する。
   legal conclusionまたはsensitive-data extractionに`use as-is`を使わない。
9. **Evidence:** answered extractionにはexact quote、location、source versionを
   要求する。quoteがない、OCR不良、source truncatedなら`needs_review`。
10. **DLP blocker:** Cowork内DLPが必須ならconfidential contentを投入せず
    production useを停止する。

provenance、reviewer note、severity、next decisionは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | action |
|---|---|
| `assess-fit` | corpus、uniformity、target clause、Microsoft 365内review可否を判定 |
| `prepare-batch` | exact source list、schema、materiality、exclusionを作成 |
| `security-review` | transfer gateとapproved conditionsを確認 |
| `draft-load-request` | 人がtoolへ渡すload instruction/manifestをdraft |
| `qa-result` | returned extractionをtrust levelに応じsample/full review |
| `judgment-layer` | transaction structure、law、PA、materialityへ適用 |
| `handoff-results` | diligence findingとclosing candidateを作成 |

意図不明なら`assess-fit`から始める。state writeは行わず、draft artifactだけを
作る。

## Fit

handoff候補:

- categoryに概ね50超のdocuments
- uniform contract set
- targetがmechanical clause extraction
- teamがapproved tool/license/workspaceを持つ
- provenanceとdeletion evidenceを保持できる

direct review:

- bespoke agreement、side letter、amendment interaction
- transaction structure/legal consequenceが主question
- clean-team/MNPI/My Number/export restriction
- tool terms、data location、no-trainingが未確認
- source quote/locationを返せない

document数は目安であり、internal thresholdであってlawではない。

## Batch manifest

```yaml
batchId: "[stable batch ID]"
matterId: "[matter ID]"
sourceSystem: "[SharePoint/VDR]"
sourceItems:
  - itemId: "[source item ID]"
    sourceVersion: "[version]"
category: "[category]"
transactionStructure: "[share sale | business transfer | merger | company split | share exchange | share transfer | share delivery | other]"
extractionTargets:
  - change_of_control
  - assignment
materiality: "[internal review threshold]"
excludedData:
  - My Number
approvedTool: "[Luminance | Kira | other]"
approvedWorkspace: "[workspace ID]"
retention: "[period]"
deletionEvidenceRequired: true
humanApprover: "[person/role]"
```

target name、tool name、enum、source IDsを翻訳・要約しない。

## QA

- `spot-check`: profileのsample率を使う。random/stratified方法、N、errorを示す。
- 1件でもcomposed/paraphrased quote、wrong location、material false negativeが
  あればsampleを広げる。
- `full re-review`: flagged set全件をsourceへ戻って確認する。
- `use as-is`: 人が承認したnon-sensitive mechanical metadataに限定し、法的結論、
  consent、filing、closing decisionへ使わない。

record:

```yaml
trustLevel: use as-is | spot-check | full re-review
sampleSize: "[N]"
falsePositiveRate: "[value or unknown]"
falseNegativeRate: "[value or unknown]"
quoteMismatchCount: "[N]"
modelAndVersion: "[tool/model version]"
deletionEvidence: "[item ID or pending]"
outcome: accepted-with-human-review | widened-sample | full-re-review | rejected
```

## Judgment layer

各flagを次へ当てる。

- transaction structure
- definition/trigger/carve-out
- governing law
- claim、obligation、contractual positionの区別
- universal succession/business transfer
- PA definition/materiality
- consent/notice/perfection
- statutory/licence overlay

`silent`を`auto-assign`へ変換しない。日本の分析はqualified review pendingを
保持する。

## Output

1. transfer decisionとconditions
2. load request draft
3. QA summary
4. accepted/rejected/needs-review counts
5. diligence candidate
6. closing-checklist candidate
7. source coverage、deletion evidence、unresolved security issue

formatは`references/handoff-workflow.md`を使う。初稿はOneDrive。SharePoint
`outputs`への昇格、external transfer、state ingestはそれぞれ別確認。

## 行わないこと

- Luminance、Kira、VDRへupload/send
- tool workspaceをcreate/configure
- legal conclusionを`use as-is`
- clean-team/MNPI/My Numberを無断transfer
- outputを自動でdiligence/checklist stateへ書く
- schedule、agent、Power Platform solutionが存在すると推測
