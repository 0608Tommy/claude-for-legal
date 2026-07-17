---
name: board-minutes
description: >
  取締役会・法定委員会等の議事録を、entity form、機関設計、定款、招集、定足数、特別利害関係、遠隔出席、署名・電子署名、保存義務を確認してhouse precedentに合わせてdraftする。会議検出、採択、配布は自動実行しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Board minutes

旧来の参照labelは`/corporate-legal:board-minutes`。

## 目的

agenda、pre-read、attendance、actual discussion/resultから、会社のhouse formatと
mandatory formalitiesを満たすreview用draftを作る。議事録はcorporate recordで
あり、内部drafting noteと分ける。

## Mandatory board gate

本gateはreferenceへ移さず、毎回実行する。

1. **Runtime/matter:** `references/common/cowork-runtime-contract.md`を読み、
   exact binding、matter、source、viewerを確認する。local fileへ保存しない。
2. **Entity:** `entity_form: KK | GK | other`、registered head office、
   organ design、articles、board regulation、committee basisを確認する。
3. **Meeting:** meeting type、date/time、location/remote method、convening
   authority、notice/waiver、agendaを確認する。
4. **Eligible voters:** directors、special-interest exclusions、quorum、
   vote、abstention/dissent、conflictをactual governing ruleで確認する。
5. **Auditor/committee:** corporate auditor、audit and supervisory committee、
   three statutory committees等のattendance、objection、opinion、report、
   signature ruleを分ける。
6. **Content:** 会社法施行規則101条等のmandatory minutes contentを確認する。
   house precedentはmandatory lawをoverrideしない。
7. **Signature:** paper minutesは該当するattending directors/corporate auditors等の
   signature/seal、electronic minutesは施行規則225条等のprescribed electronic
   signatureを確認する。secretary-only signatureをdefaultにしない。
8. **Retention:** head officeでの10-year retentionとelectronic readability、
   legal holdを確認する。
9. **Evidence:** sourceなしにdiscussion、question、vote、timeを創作しない。
   missingは`[PENDING — confirm]`。
10. **Privilege/destination:** minutes本文に内部work-product headerを入れない。
    drafting noteを別artifactにし、recipientを確認する。
11. **Adoption:** AIはminutesをadopt/finalize/sendしない。adoption-ready版は
    exact changes、reviewer、approverへのfresh confirmation後もdraftで停止する。
12. **DLP:** Cowork内DLP必須ならconfidential materialsを投入しない。

日本のformalitiesは
`references/common/ja-jp/governance-records.md`、
provenanceは`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | action |
|---|---|
| `identify-meeting` | exact meeting、entity、organ、date、sourceを選ぶ |
| `confirm-attendance` | eligible voters、special interest、auditor、quorumを確認 |
| `collect-materials` | agenda、slides、reports、resolution、exhibitsを読む |
| `draft-minutes` | house precedentとmandatory fieldsでdraft |
| `review-formalities` | vote、signature、electronic record、retentionをcheck |
| `prepare-adoption-draft` | placeholdersを解消し、review packageを作る |

calendar connectorをlive probeでき、userが明示した場合だけmeeting candidateを
検索する。自動検出、30-day watch、scheduleが常時動くとは表示しない。

## Source

exact items:

- articles / board regulation / committee charter
- current director/auditor list
- notice/waiver
- attendance
- agenda
- pre-read/slides/reports
- draft resolution
- prior minutes precedent
- electronic signature policy

precedentがない場合、generic formatを使う前にその事実を示し、mandatory fieldsを
優先する。precedentがlawと衝突する場合、lawを優先し差を`[review]`にする。

## Draft rule

- actual company languageとJapanese corporate terminologyを使う。
- discussion depthは`long-form narrative | action minutes | hybrid`のprofile値。
- exact speaker attributionは必要な場合だけ。
- resolution wording、vote、special-interest exclusionを明記。
- remote attendance methodと相互通信性をsourceに基づき記録。
- mandatory report/opinion、audit/corporate auditor objectionを落とさない。
- exhibitはexact item/versionとlabelで参照。
- `motion duly made and seconded`はhouse practiceかつ適切と確認した場合だけ。

templateは`references/minutes-template.md`。

## Failure

次はvalid meetingを示すdraftを出さず停止する。

- entity/organ/meeting basis不明
- quorum不足またはeligible voter count不明
- special-interest director処理不明
- vote/resultがsourceと矛盾
- signature/electronic signature rule不明
- agenda/materialが不完全でdiscussionを再構成する必要がある

Japanese counselへ、欠けているfact、possible remediation、必要sourceを示す。

## Output

1. **レビュー担当者向け注記**
2. **Minutes draft** — corporate record、内部headerなし
3. **Internal drafting notes** — source、placeholder、law/precedent delta
4. **Formality checklist**
5. **Exhibit/signature checklist**
6. **Adoption decision tree**

初稿はOneDrive。review済み共有成果物への昇格、circulation、adoption、signatureは
別operation。

## 行わないこと

- meetingへattend/record
- calendar eventを自動scan
- discussion、quorum、voteを推測
- minutesをadopt/finalize
- signature requestまたは配布
- statutory committeeへArt. 370を自動流用
- Office fidelity/native tracked changesを保証
