> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Full commercial interview

## Pacing

- 1turnに2～3個のanswerable prompt。
- documentにありそうな情報はlink/item指定を先に求める。
- typed answerが必要なら待つ。
- skipは明示選択として記録する。

## Part 0 — User, setting, connection

1. current user roleとattorney contact
2. practice setting
3. Microsoft 365 storageとconnector probe
4. jurisdiction footprint

## Part 1 — Team and work

- organizationが何をsell/buyするか、customer、channel、subscription等
- entity、contracts team、final escalation
- monthly volume、agreement mix
- own paper / their paper / mixed
- negotiation depth、typical cycle
- active side: `sales | purchasing | both`
- the thing that hurts

## Part 2 — Playbook

各sideを別に聞く。

### Limitation of liability

- direct cap amount/multiple
- indirect/consequential treatment
- above-cap carveouts
- acceptable cap base
- fallback、never

### Indemnification

- direction、scope、procedure
- IP infringement
- data/security
- excluded claims
- fallback、never

### Data protection

- own/counterparty DPA
- security evidence
- subprocessors
- transfer/residency
- incident
- audit

### Term and termination

- initial/renewal term
- convenience/cause
- notice
- termination fee
- transition/data exit

### Governing law

- preferred、acceptable、escalate、never
- forum/arbitration

### One thing

sales-sideとpurchasing-sideを別々に記録する。

## NDA positions

- mutual/one-way
- confidential information definition
- oral disclosure
- five carveouts
- residuals
- term/survival/trade secrets
- restrictive covenant
- fee shifting
- return/destruction/backup
- governing law
- NDA外義務
- GREEN / YELLOW / RED criteria
- `attorneyReviewed: true|false`
- `closingAction`

## SaaS positions

- renewal term、cancel window、notice method
- price escalator、overage
- export format、timing、cost
- deletion、derived data
- uptime、measurement、credits、sole remedy
- subprocessor notice/objection
- service change/deprecation

## AI/ML rights

7 dimensions:

1. explicit training grant
2. implicit policy grant/unilateral update
3. anonymization standard
4. competitive contamination
5. opt-out scope/durability
6. output ownership/training examples
7. downstream regulatory chain

## Part 3 — Escalation

- reviewer authority
- value thresholds
- automatic triggers
- named approver
- channel
- turnaround
- business sign-off
- `confirmRouting`

Solo/small firmはapproval chainではなくconsult triggerとして聞く。clinic/governmentはsupervision/agency chainへ適応する。

## Part 4 — Workflow

- review output destination
- internal/external marking
- stakeholder audience/length
- renewal alert destination/cadence
- signed contract repository
- matter workspace enabled
- cross-matter default
- playbook monitor threshold/lookback

scheduled flowは存在をprobeし、なければ「設定済み」と書かない。

## Part 5 — Seed

- playbook
- escalation/delegation matrix
- templates
- 5～10 signed agreements
- past review memo
- renewal register export

extract:

- standard
- actual signed fallback
- one-off
- counterparty-size pattern
- clause category
- review coverage

## Part 6 — Review

profileへwriteする前に、open items、contradictions、limited sample、pending legal reviewを一覧にする。
