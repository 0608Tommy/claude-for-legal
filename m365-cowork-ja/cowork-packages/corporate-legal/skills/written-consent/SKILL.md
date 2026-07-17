---
name: written-consent
description: >
  会社法319条の株主総会決議省略、370条の取締役会決議省略、372条の報告省略、法定委員会等を区別し、定款、eligible voters、監査役条件、precedent、署名・電子記録、保存を確認してreview用draftとsignatory/evidence trackerを作る。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Written consent / deemed resolution

旧来の参照labelは
`/corporate-legal:written-consent [describe the action needing board approval]`。

## 目的

routine corporate actionをhouse precedentに合わせてdraftする。ただし日本では
genericな「unanimous written consent」を使わず、法的mechanismを先に分類する。

## Mandatory consent gate

本gateはreferenceへ移さない。

1. **Runtime/matter:** `references/common/cowork-runtime-contract.md`を読み、
   exact user、binding、matter、source、destinationを確認する。
2. **Entity/organ:** `entity_form: KK | GK | other`、organ design、articles、
   board/shareholder/committee regulation、current membersを確認する。
3. **Mechanism:** 次を混同しない。
   - `board-resolution-omission` — Companies Act Art. 370
   - `shareholder-resolution-omission` — Companies Act Art. 319
   - `shareholder-report-omission` — Companies Act Art. 320
   - `board-report-omission` — Companies Act Art. 372
   - `statutory-committee-action` — committee固有rule
   - `other` — GK/member consent、foreign entity等
4. **Art. 370:** articles authorization、director proposal、当該proposalに議決参加
   できる全directorsのwritten/electronic consent、relevant auditor objection
   conditionを確認する。
5. **Art. 319:** 当該議案で議決権を行使できる全shareholdersのconsent、
   class/restricted share、shareholder agreement、special resolution factsを確認。
6. **Art. 320:** shareholder meetingへのreport省略について、議決権を行使
   できる全shareholdersのconsentとreport対象を確認する。
7. **Art. 372:** boardへのreport省略はconsent/resolutionではない。report内容、
   relevant directors/corporate auditorsへのnotification、notification evidenceを
   確認し、Art. 363(2)の業務執行状況reportを省略しない。
8. **Committee:** audit、nomination、compensationその他statutory committeeに
   Art. 370を自動適用しない。
9. **Minutes/evidence:** deemed resolution/reportの別minutes、proposal、
   consent evidence、date、eligible persons、signature/electronic record、
   10-year retentionを確認する。
10. **Precedent:** house precedentはmandatory lawをoverrideしない。precedentなしは
   hard stop、またはuserがgeneric formalitiesを手作業reviewすると明示した場合だけ
   marked draft。
11. **Conflict:** special interest、related party、fiduciary/process concernを
    `[review]`にし、AIがvalidityを決めない。
12. **Privilege/destination:** executed consent/minutesはcorporate record。内部
    drafting noteと分ける。
13. **Human action:** AIはsign、circulate、DocuSign/envelope send、adopt、
    corporate bookへfinal保存しない。
14. **DLP:** Cowork内DLP必須ならconfidential materialを投入しない。

日本formalitiesは
`references/common/ja-jp/governance-records.md`、
provenanceは
`references/common/source-provenance-and-review.md`を使う。

## Major action + same-day signature hard stop

次の両方がtrueならready-to-sign formを出さない。

1. M&A、financing、new investor equity、capital change、dissolution/winding up、
   material real estate、change-of-control、future data-room exhibit等のmajor
   one-off。
2. 「今日署名」「今夜closing」「すぐDocuSign」「market open前」等のsame-day
   irreversibility signal。

表示:

> ⛔ **Major action + same-day signature — ready-to-signにはしません。**
>
> draftは作成できますが、日本法有資格者または当該取引のoutside counselが
> entity、mechanism、articles、eligible persons、conflict、signature/evidenceを
> reviewする必要があります。reviewerとreview timeを確認するか、
> counsel-review用draftを選んでください。

explicitに`counsel-review draft`または`counsel already reviewed`を選ぶまで
draftingへ進まない。

## No-precedent hard stop

consent/minutes repository、seed consent、actual house formatのいずれもない場合:

> **Precedentがないため、draft前に停止します。**
>
> 1. authorized prior consent/minutesのexact itemを指定する、または
> 2. 「generic marked draftを作り、formalitiesをJapanese counselが全面reviewする」
>    と明示する

どちらかを選ぶまでgeneric house styleを創作しない。

## 会話state

| state | action |
|---|---|
| `identify-action` | action、effective date、supporting document、urgencyを取得 |
| `classify-mechanism` | Art. 319/370/372/committee/otherへ分類 |
| `check-formalities` | entity、articles、eligible persons、auditor/conflictを確認 |
| `select-precedent` | exact repository item/versionを選ぶ |
| `draft` | house wording + mandatory fieldsでmarked draft |
| `review-evidence` | consents、signature/e-signature、minutes、retentionをcheck |
| `prepare-circulation-draft` | counsel review後のclean draft候補 |

## Action classification

### Routine candidate

- officer appointment/removal
- existing plan equity grant
- bank signatory/authorization
- ordinary-course contract approval
- annual authorization
- intercompany agreement
- registered head office、seal、electronic certificate等のadministrative change

### Major one-off

- acquisition、merger、business transfer、company split、investment
- financing/debt facility
- new investor equity
- capital structure/change of control
- dissolution/bankruptcy
- material real estate
- public-company/FIEA/TDnet implication
- future financing/M&A data-room exhibit

routine/majorはinternal routingであり、legal validity testではない。

## Precedent

live probeとpermissionが確認できるauthorized SharePoint repositoryだけを検索する。

search:

1. mechanism
2. action type
3. entity/organ
4. most recent effective version

extract:

- title/intro
- recital depth
- resolution language
- authorization/ratification
- counterpart/electronic language
- signature/evidence block
- deemed-resolution minutes format

similar-looking foreign/Delaware precedentをJapanese mechanismのsourceにしない。

## Draft

`references/consent-template.md`を使う。mandatory:

- entity、organ、mechanism、legal/constitutional basis
- specific proposal/action
- eligible voters/members
- all required consents/objection condition
- effective/deemed date
- exact approved document/exhibit
- authority implementation language
- conflict/special-interest treatment
- signature/electronic record method
- separate minutes/evidence list
- retention

vagueな「transactionを承認する」ではなく、agreement title/date/parties/form/
exhibitとauthorityをspecificにする。

## Consequential execution gate

signatory-ready/circulation-ready候補の前に:

- mechanism/formality check completed
- counsel reviewer
- exact final document version
- required signers/consenters
- conflict treatment
- electronic signature method
- separate minutes/evidence
- destination

を示し、fresh confirmationを得る。ただしAIはsend/signせずdraftで停止する。
Non-lawyerにはattorney briefを先に作る。

## Output

1. reviewer note
2. mechanism/formality analysis
3. marked consent/proposal draft
4. deemed-resolution/report minutes draft
5. eligible person/signatory/evidence tracker
6. review checklist
7. circulation decision tree

corporate record本文にinternal headerを入れない。内部analysisは別artifact。

## 行わないこと

- actionがboard/shareholder approvalを必要とする最終判断
- Art. 370をcommitteeへ自動適用
- precedentなしにhouse wordingを創作
- same-day major actionをready-to-sign化
- DocuSign/envelope送信、signature追跡
- consent/minutesをadopt/finalize
- filing、registry、external circulation
