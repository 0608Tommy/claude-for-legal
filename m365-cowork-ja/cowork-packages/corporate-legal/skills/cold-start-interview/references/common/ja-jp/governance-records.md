> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本の会社機関・記録・登記workflowを追加した派生ファイルです。

# 日本の会社機関、決議、記録、登記

**Status:** `DRAFT / qualified Japanese counsel review pending`

## 最初に確認するentity facts

- `entity_form`: `KK | GK | other`
- registered head office
- corporate number
- organ design: board、corporate auditor、audit and supervisory committee、
  three statutory committees、accounting auditor等
- articlesとboard/shareholder regulationsのexact item/version
- public-notice method
- share-certificate issuance status
- restricted-share statusとshareholder register
- listed market、EDINET code
- Companies Act Art. 370 authorizationの有無
- electronic minutes/signature policy

entity formまたはorgan designが不明なら、取締役会・株主総会・みなし決議の
formalitiesを確定しない。

## 取締役会meeting

KKの取締役会では、少なくとも次を確認する。

1. convening authority、notice period/method、waiver
2. agenda、meeting method、remote attendanceの相互通信性
3. eligible director count
4. 特別利害関係取締役の議決除外
5. quorumとvote result
6. corporate auditor等の出席・異議・意見・報告
7. mandatory report/opinion
8. conflict disclosure
9. 会社法施行規則101条のminutes content
10. paper minutesの出席取締役・監査役等の署名/記名押印、またはelectronic
    minutesの施行規則225条に従うsignature
11. head officeでの10-year retention

house precedentはmandatory formalityをoverrideしない。移行元の
`motion duly made and seconded`、secretary-only signatureは、その会社が実際に
採用し、かつ日本法上適切と確認できる場合だけ使う。

minutesはcorporate recordであり、内部drafting noteと分ける。実際のdiscussionを
sourceなしに創作しない。quorum failure、special-interest issue、signature
defectがある場合、valid meetingを示すdraftを出さずremediationをJapanese counselへ
routeする。

## 取締役会決議の省略 — Companies Act Art. 370

genericな「unanimous board consent」ではない。次をすべて確認する。

- articlesがArt. 370 mechanismをauthorizeする
- directorがspecific proposalを行う
- 当該proposalについて議決に加わることができる全directorが書面または
  electronic recordでconsentする
- 監査役設置会社では、監査役が当該proposalに異議を述べないこと
- statutory committee action等の別ruleと混同しない
- deemed resolution dateとproposal/consent evidence
- 施行規則101条4項等に従う別のminutes record
- underlying consentsとminutesの10-year retention
- Art. 372による取締役会への報告省略とは別であり、Art. 363(2)の業務執行
  状況報告は省略できない

取締役会を置かない会社、監査等委員会設置会社、指名委員会等設置会社、
statutory committeeでは別ruleを確認する。Art. 370を自動流用しない。

## 株主総会決議・報告の省略

- Companies Act Art. 319: directorまたはshareholderがproposalし、当該議案で
  議決権を行使できる全shareholderの書面/electronic consent等を確認する。
  less-than-unanimous U.S. stockholder consentと同一視しない。consent recordは
  head officeで10年間保存する。
- Companies Act Art. 320: shareholder meetingへのreport省略を扱う。
  resolution省略またはboard report省略と混同しない。
- articles、class share、shareholder agreement、shares subject to transfer
  restriction、special resolution thresholdを別に確認する。
- deemed resolution/reportのminutes、proposal、consent、notice、retentionを
  exact sourceで確認する。

virtual-only shareholder meetingはspecial statutory routeとconfirmationsが
必要であり、ordinary online attendanceと同一視しない。

## Electronic records/signatures

Electronic Signatures Act Art. 3のpresumptionはconditionalであり、すべての
DocuSign/cloud recordがwet inkと同じというruleではない。document-specificな
Companies Act、regulation、registry、authority filing requirementを先に確認する。

確認項目:

- signatory identity、authority、intent
- signature service、certificate、audit trail、timestamp
- counterpart/copy rule
- electronic minutesのprescribed signature
- registry attachmentのaccepted format
- electronic transaction tax record preservation
- retention、legal hold、export format、future readability

AIはsignature requestをsendせず、signせず、signature validityをfinal certifyしない。

## Commercial registration

会社法911条、915条、商業登記法、actual formsに基づき、change eventごとに
registrable particulars、deadline、attachment、signer、submission systemを確認する。
「原則2週間」を機械的に全eventへ適用せず、起算点、head office relocation、
branch/merger/split/dissolution、exceptionをactual ruleで確認する。

track:

-商号、目的、本店、公告方法
- capital/shares、share transfer restriction
- directors、representative director、auditors、committees
- term expiry/reappointment
- merger、company split、share exchange/transfer/delivery
- dissolution、liquidator、continuation
- seal/electronic certificate
- attachment evidence、acceptance/rejection、registered date

filing draft作成とsubmissionは別operation。fresh approval、exact form/version、
signer、evidence、fee、destinationを確認し、AIはfile/payしない。

- registry form primary page:
  https://houmukyoku.moj.go.jp/homu/COMMERCE_11-1.html
- electronic attachment media pageはCD-R/DVD-R等をpaper applicationへ添付する
  手続を中心に扱うため、generic electronic filingと表示しない。
- branch-location registrationは2022-09-01廃止。ただしhead-office registryの
  branch particularsは別途確認する:
  https://www.moj.go.jp/MINJI/minji06_00166.html
- representative-address non-display measureは2024-10-01開始:
  https://www.moj.go.jp/MINJI/minji06_00210.html
- shareholder/class meetingまたはArt. 319 consentに基づく登記ではshareholder
  list attachmentを確認する:
  https://www.moj.go.jp/MINJI/minji06_00095.html

## Beneficial ownership

法務省の実質的支配者list制度はrequest-based制度であり、一般的なannual filingと
表示しない。対象entity、request eligibility、supporting document、current
shareholder/control data、AML/KYC useを確認する。

beneficial owner、foreign investor、FIEA large holder、FEFTA ultimate control、
company shareholder registerは別概念であり、1つのfieldで代用しない。

## Annual accounts/public notice

Companies Act Art. 440のfinancial statement public notice、applicable exemption、
electronic disclosure、articlesの公告方法を確認する。exemptionはFIEA
Art. 24(1)のsecurities report提出義務会社等のexact statutory conditionを確認し、
単にlistedであることだけで適用しない。
annual shareholder meeting、accounts approval/report、tax filing、licence filingは
別calendarにする。

## Evidence

corporate recordの完成前に次を示す。

- entity/organ basis
- articles/regulation exact version
- notice/consent evidence
- eligible voters/signers
- minutes/consent source
- signature/electronic evidence
- retention location
- registry filing/evidence
- unresolved `[review]`

adoption、execution、filing、record promotionはそれぞれfresh confirmationを要求する。
