> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のdiligence overlayを追加した派生ファイルです。

# 日本のM&A diligence overlay

**Status:** `DRAFT / qualified Japanese counsel review pending`

## 最低category

1. transaction structure / parties / beneficial ownership
2. corporate/registry/articles/shareholder register
3. capitalization/restricted shares/options
4. board/shareholder/class approvalsとcorporate books
5. material contracts / claims / obligations / contractual position
6. financing/security/guarantee
7. real estate/environment
8. labour/employment/pension/social insurance
9. privacy/data/cyber/My Number
10. IP/trade secret/IT/open source
11. litigation/investigation/compliance
12. tax/accounting/public notice
13. FIEA/JPX/public-company
14. JFTC/competition
15. FEFTA/economic security/export control
16. sector licence/permit
17. related-party/intercompany
18. post-close integration dependencies

request list、PA、target businessにないcategoryでも、factsからrelevantなら
checklistのfloorとして追加し、通常checklist外であることを示す。

## Materiality

3つを分ける。

- **PA definition:** disclosure schedule inclusionを支配するcontractual test。
- **Statutory threshold:** FIEA、JFTC、FEFTA、licence等のlaw/rule test。
- **Internal threshold:** VDR review scope、value/headcount/top-N等のplaybook。

internal threshold未満でもstatutory trigger、fraud、bribery、licence、data breach、
title defect、employee transfer、MNPI、clean-team issueは自動除外しない。
境界事例は`[review]`。coverageにはreviewed count、excluded count、reason、
unreadable/missing documentsを示す。

## Contract transfer

「assignment」を1fieldへ潰さない。

- claim assignment
- obligation assumption
- entire contractual position transfer
- change-of-control provision
- notice/consent
- third-party perfection
- governing law
- universal succession
- business transfer
- licence-specific non-transferability

Civil Code 466–467のclaim assignment、470～472-4のdebt assumption、539-2の
contractual position transfer、contract wording、governing lawを分ける。
silent clauseを`auto-assign`としない。
merger/company splitとbusiness transferを同一視しない。

## Corporate / successor liability

verify:

- current registry、articles、shareholder register、share certificates
- issued/authorized shares、options、warrants、pledges
- approval defects、missing minutes/consents
- public notice、financial statements
- intercompany transactions、guarantees、loans
- dormant/inactive entities、unregistered changes

asset/business transferでも「clean」前提にしない。Companies Act Art. 22の
trade-name successor liability、fraudulent act、labour、environment、tax、
product/statutory liability、seller dissolution、assumed/excluded liabilitiesを
Japanese sourceで分析する。U.S. `de facto merger`, `mere continuation`,
`product line`を日本法のholdingとして使わない。

## Labour

structure別に:

- share sale: employer remains、CoC/retention/collective agreementを確認
- business transfer: Civil Code Art. 625等、individual consent、explanation/
  consultation、selective transfer risk
- company split: `会社分割に伴う労働契約の承継等に関する法律`、notice/
  objection、allocation
- merger: statutory successionとguidance

review:

- employment rules/agreements、overtime、wage、leave
- fixed-term/dispatch/contractor classification
- union/collective bargaining
- pensions/benefits/social insurance
- harassment/litigation/whistleblowing
- key employee retention、change-of-control payment
- 2026-05-25 MHLW guidance status

company splitではshareholder approval有無に応じたnotice dateと、少なくとも
13日のobjection periodをcurrent statuteで確認する。business transferは
Civil Code Art. 625のindividual worker consentをguidanceで置き換えない。
Labor Union Act、Worker Dispatching Act、Part-Time/Fixed-Term Workers Act、
social-insurance statutesもfactsに応じてscreenする。

## Privacy / data

APPI、PPC current guidance、diligence FAQ、M&A/reorganization warningを確認する。
PPC FAQのpre-closing safeguard例はreal-estate transaction exampleであり、
universal M&A safe harborではない。旧Art. 23(5)(ii) referenceはcurrent
Art. 27(5)(ii)と照合する。

- due diligence purposeとnecessity
- NDA、clean team、access restriction、data minimization
- personal data / retained personal data / pseudonymized/anonymized treatment
- foreign transfer、subprocessor/data location
- customer/employee notice、purpose of use
- breach/security、retention/deletion
- My Number separation
- post-close system/data migration
- reportable breach、本人通知、My Number separation

2026 amendmentは2026-07-16時点で`PENDING`として、current exception/obligationへ
適用しない。

breach報告は速報目安3～5日、確報30日またはmalicious-purpose類型60日を
current sourceで確認する。domestic outsourcing/business successionでも
foreign transferはArt. 28を別に確認する。My Number dataへordinary APPI
M&A exceptionを自動適用しない。

## IP / IT / trade secret

- patent/trademark/design titleとJPO record
- copyright authorship/assignment、Art. 15、moral rights handling
- Patent Act Art. 35 employee invention policy/remuneration
- contractor/founder assignment
- inbound/outbound licence、CoC/assignment
- open-source licence、source code escrow
- domain/social account
- trade-secret reasonable management measures
- AI/model/data training rights

U.S. work-made-for-hireを代用しない。patent/trademark/design successionと
copyright third-party perfectionを一つの`USPTO recordal` itemへ潰さない。

- patent assignmentはgeneral successionを除きregistrationが効力要件
- trademark/designはPatent Act Art. 98を準用するregistration effectを確認
- copyright assignmentはcontract上成立し得るがthird-party perfectionに
  registrationが必要。Arts. 27/28 rightsは明示なしに譲渡されず、moral rightsは
  non-transferable
- corporate authorship Art. 15はconditionalでU.S. work-made-for-hireではない
- employee inventionはPatent Act Art. 35のownership/reasonable benefit/
  consultation/disclosure/hearingを確認
- Utility Model Act、security interest/licence recordalもfactsに応じて確認

## Competition / FEFTA / public company

初期factsとして:

- Japan turnover、market、competitors
- voting-right before/after
- foreign investor、ultimate control、nationality
- designated/core business、sensitive technology
- listed status、market、EDINET code
- tender offer、large holding、insider/MNPI

threshold、exemption、waiting period、filing formはofficial sourceをそのtaskで
確認する。

## Sector / tax / economic security

target activityからBanking、Insurance、Payment Services、Telecom、Radio、PMD、
Construction、other licenceをscreenする。licence transferability、control change、
prior consent、post notice、fit-and-proper、foreign ownershipをauthority/specialistで
確認する。

tax reorganization、consumption tax、withholding、stamp、loss carryforward等は
tax adviserへrouteし、legal trackerにはdependency/evidenceだけを記録する。
Economic Security Promotion Act、export control、critical infrastructure、
government contracts、classified/sensitive technologyをfactsに応じてscreenする。

## Finding

各findingに:

- transaction structure
- entity/asset/contract
- category
- severity
- exact source item/version/location
- fact
- law/listing/guidance/contract/internal layer
- issueとdeal impact
- recommendation候補
- pre-closing/post-closing action
- evidence required
- owner/deadline
- `[review]` / `[verify]`

document quoteはcharacter-for-characterで、locationを付ける。quoteを再構成しない。
