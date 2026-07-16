> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# International expansion compiled framework

source `international-expansion`のEOR/entity、cross-functional questions、
outside-counsel briefing、dependency behaviorをkickoff/update callerへcompileします。
expansion decision自体は前提としますが、structure decisionは人が行います。

## Intake

single block:

- country、work locations、roles、headcount 12 months、first-hire target
- existing entity/branch、EOR/vendor、local manager
- strategic testing/long-term
- tax/finance/HR/payroll/security owners
- outside employment counsel、immigration counsel
- sales/signing authority/PE exposure
- employee data/HRIS flows
- visa/status needs
- acquisition/secondment/transfer context

## Legal-feasibility gate before cost

EORをoptionとして比較する前に:

1. providerがgenuine employerか。
2. daily instruction、schedule、evaluation、disciplineを誰が行うか。
3. licensed dispatch、employment placement、genuine outsourcing、worker supplyの
   どれか。
4. work rules、working-time agreement、payroll、insurance、OSH、discipline、
   dismissalのowner。
5. mandatory local protections、choice of law。
6. visa sponsorship/notification。
7. HRIS/privacy/foreign transfer。

unclear/illegal candidateならcost tableを出す前に🔴 Blockingとoutside counselへ
routeします。EORはlow-headcount safe harborではありません。

## EOR/entity framing

| Factor | EOR side | Entity side |
|---|---|---|
| headcount/timeline | fewer/shorter | scale/long-term |
| control | provider genuine control | direct employer control |
| legal feasibility | licensed/permitted structure | local employer registration |
| IP/data | verified assignment/transfer | direct framework |
| cost | current provider/tax model | setup/ongoing compliance |
| transition | conversion risk | stable direct employment |

break-even、markup、setup timeをhardcodeせずfinance/tax/providerへ質問します。

## Cross-functional asks

**Tax**

- PE/nexus、role/signing authority
- entity/EOR/secondment tax
- equity/withholding
- intercompany agreement

**Finance/payroll**

- approved payroll provider
- employer contributions/insurance
- bank/funding、withholding、resident/local tax
- EOR invoice/payroll reconciliation

**HR/total rewards**

- mandatory vs market benefits
- local compensation/equity
- manager/control model
- work rules、leave、working-time operation

**Privacy/security**

- employee data categories、HRIS location
- processor/vendor、foreign transfer、retention
- monitoring/access

**Immigration**

- status/permit、sponsor、role/location
- lead time、notification、renewal

## Outside-counsel briefing

tailor questions:

1. lawful engagement structures and EOR/dispatch/supply limits
2. employment contract/working-condition requirements
3. working time、overtime agreement、minimum wage
4. termination/nonrenewal/RIF
5. benefits、social insurance、payroll
6. leave/accommodation/harassment
7. unions/employee representation/CBA
8. restrictive covenant/IP
9. worker classification/freelance/OSH
10. employee data/monitoring/transfer
11. immigration/foreign-worker notification
12. Day 1 registrations、work rules、filings
13. recent/future changes

JapanではGeneral Rules Act Article 12、dispatch/supply、36 agreement、social
insurance、foreign-worker notification、APPIを必ず追加します。2027 immigration
reformはfutureとして該当時だけ質問します。

## Dependency model

1 item = 1 owner = 1 completable action。status:
`open | in-progress | done | blocked`。

dependency完了でunblocked candidateを示しますが、自動status変更しません。due dateは
human/sourceから取得し、法定deadlineを推測しません。law/source itemがdoneになる前に
authority/effective dateを確認します。

## Completion

structure options、Blocking issue、owners、outside-counsel brief、open dependencies、
source gaps、target dateを示します。AIはentity/EOR契約、hire、payroll、insurance、
visa、filing、external sendを実行しません。
