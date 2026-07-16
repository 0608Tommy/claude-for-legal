> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のpost-close integration・entity complianceを追加した派生ファイルです。

# 日本のpost-close integrationとentity compliance

**Status:** `DRAFT / qualified Japanese counsel review pending`

## structure別post-close

### Share sale

target entity、contract party、employerは通常同一。次を重点追跡する。

- shareholder register / share certificate / restricted-share approval evidence
- board/representative/signatory change
- commercial registration
- FEFTA/JFTC/FIEA/TDnet post action
- control-change licence/contract notification
- bank/insurance/authority KYC
- data purpose/notice/system access alignment
- integration governance、clean-team解除

### Business transfer

asset、claim、obligation、contractual position、employee、personal data、IP、
licenceを個別に追跡する。

- assignment/assumption/novation/consent/perfection
- employee consent/consultation/onboarding
- customer/vendor notice
- receivable/movable/real-estate registration
- APPI purpose/public notice/foreign transfer
- licence reapplication/consent
- tax/social insurance dependencies

### Merger / company split

universal successionのscope、special exception、creditor objection、employee
succession、licence、registration、effective dateを追跡する。自動承継と表示する
前にasset/right/licenceごとのspecial ruleを確認する。

### Share exchange / transfer / delivery

shareholder/register/capital/approval/appraisal/disclosure/registrationと、
target subsidiaryのpost-control notificationを追跡する。

## Day 1 / 30 / 90 / 180

phaseは内部project controlであり法定期限ではない。各itemの
`deadline_basis`を`pa-obligation | law/rule | listing | guidance |
internal`で分ける。

主なworkstream:

- corporate records、representative/officer、seal/electronic certificate
- two-week commercial registrations（actual event/start dateを確認）
- JFTC/FEFTA/FIEA/TDnet/sector post action
- tax office、local tax、social insurance、labour notices
- contract consent/assignment/novation/CoC
- employee transfer/harmonization
- data migration/APPI purpose/public notice/security
- patent/trademark/design recordal、copyright perfection
- domain/social/account control
- entity rationalization、merger/dissolution
- rep survival、escrow、earnout dates（finance ownershipを明示）

U.S. `Secretary of State ownership notification`、`USPTO recordal`、
`certificate of good standing`を日本defaultとして使わない。

## Entity compliance model

state × annual reportではなく、event obligationとperiodic obligationを分ける。

### event obligation

- registered particulars changeとactual filing deadline
- officer appointment/reappointment/term expiry
- representative、head office、purpose、capital/share change
- articles/organ design change
- merger/split/exchange/transfer/delivery
- dissolution/liquidator/continuation
- seal/electronic certificate
- beneficial-owner list request/update evidence
- licence/control change
- tax/social-insurance/labour change notification

### periodic obligation

- annual shareholder meeting、accounts/report
- Companies Act Art. 440 public noticeまたはexemption
- corporate/local tax filing
- social/labour insurance periodic filing
- licence renewal/report
- listed-company EDINET/TDnet/governance calendar
- officer term review
- dormant-company review
- electronic-record retention health

## Evidence type

日本法人に一般的なsingle `good standing` certificateがあると表示しない。
必要目的ごとに分ける。

- certificate of registered matters
- seal certificate
- articles/certified copy
- shareholder register
- tax payment/tax filing certificate
- social-insurance evidence
- licence certificate/authority confirmation
- beneficial-owner list
- filing receipt/acceptance

## Entity state record

```yaml
recordType: entity-obligation
entityId: "[immutable entity ID]"
entity_form: KK | GK | other
corporateNumber13: "[13-digit 法人番号]"
companyCorporateNumber12: "[12-digit 会社法人等番号]"
registered_head_office: "[address]"
organ_design: "[design]"
obligationType: event | periodic
obligationId: "[stable ID]"
legal_basis: "[law/rule/guidance/internal]"
source_version: "[version]"
effective_date: "[date]"
trigger_date: "[date or null]"
due_date: "[date or null]"
filing_system: "[registry/authority/system/N/A]"
evidence_required: "[evidence]"
status: not_started | in_progress | filed_pending | complete | blocked | unknown
itemId: "[SharePoint itemId]"
eTag: "[eTag]"
```

status `complete`はactual acceptance/evidenceに基づく。draft作成、submission、
fee payment、certificate orderは別operation。

法人番号と会社法人等番号を同一fieldへ格納しない。実質的支配者listは
request-based制度で、対象KK等・supporting documentsを確認し、annual filing
または法定periodic updateとして扱わない。

## Rebuild

entity/integration trackerの`rebuild`はdestructiveに見えるoperationである。

1. exact current record/version/ETagとdependent outputを読む。
2. rebuild reason、source set、dropped/changed records、history impactを示す。
3. export candidateを用意する。
4. explicit typed/fresh confirmationを得る。
5. old recordをdeleteせず`superseded`として保持し、new versionをconditional
   createする。
6. itemごとのmapping、unmatched、partial failureをauditする。

confirmationなし、gatewayなし、source coverage不足ではread-only rebuild planだけを
出し、stateを変えない。

## Post-close report

reportは次を分ける。

- statutory/contract deadlines
- internal phase targets
- evidence obtained/pending
- refused/blocked
- missing source
- owner/approver
- next human decision

10行超ならdashboardを提案するが、自動生成・送信しない。
