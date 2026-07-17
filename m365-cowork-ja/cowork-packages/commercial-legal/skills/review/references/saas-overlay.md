> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# SaaS / subscription overlay

vendor reviewを全部実行した後に追加する。thresholdはprofileの`saasPositions`から取り、hardcodeしない。

## 1. Auto-renewal

- renewal term
- notice-to-cancel window
- notice method
- received/sent/deemed receipt
- renewal price
- current term end
- exact clause

`renewal-tracker`candidateを作るが、保存済みとは書かない。

## 2. Price

- annual escalator
- CPI/fixed/uncapped
- usage overage
- rate card incorporation
- fee definition
- tax/FX
- promotional price reset

条件付きsentenceを短縮して意味を変えない。

## 3. Data exit

- export format
- self-service/on-request/termination-only
- post-termination window
- cost
- deletion certificate
- backup
- anonymized/aggregated derivative
- transition assistance

business frictionがlegal riskより高くなり得る。

## 4. SLA

business criticalityを先に確認する。重要でなければ、skip理由を示してnegotiation capitalを使わない。

- uptime
- measurement period
- exclusions/maintenance
- credit calculation/cap
- claim process
- sole remedy
- chronic failure termination
- cap interaction

## 5. Subprocessors

- current list
- advance change notice
- objection right
- termination fallback
- flow-down
- location
- upstream model/cloud

## 6. Service change/deprecation

- material degradation
- unilateral feature removal
- notice
- version pinning
- replacement parity
- price tier
- termination/refund

## AI/ML rights — 7 dimensions

1. **Explicit grant:** Customer Data/Content/Usage Dataのtraining、improvement、evaluation。
2. **Implicit grant:** privacy policy/TOSのunilateral update、`service improvement`、usage data carveout。
3. **Anonymization:** definition、re-identification、named standard。
4. **Competitive contamination:** competitor service、isolation、output leakage。
5. **Opt-out:** all AI usesか、org/user単位か、renewal/TOS update後も続くか。
6. **Output ownership:** ownership、license、training examples、third-party model。
7. **Regulatory chain:** deployer/provider等のrole、disclosure、records、incident。

silent contractもfinding。「AI/ML rightsが未規定」であり、vendorが使わないとは推測しない。

日本では`common/ja-jp/competition-ip.md`、`common/ja-jp/privacy-data.md`、METI checklistを読む。guidanceをbinding termと混同しない。

## Liability

general vendor reviewの4次元capを繰り返し、SaaS特有のdata breach、IP、confidentiality、service outage、data loss、AI output claimsのcarveoutをmapする。

## Output

```markdown
## SaaS-specific findings

### Auto-renewal
**Current term end:**
**Action/send by:**
**Notice method:**
**Renewal price:**
**Tracker candidate:** yes/no; missing fields

### Price escalation
...

### Data exit
...

### SLA
...

### Subprocessors
...

### Service changes
...

### AI/ML rights
...
```

## Renewal handoff

最低field:

```yaml
counterparty: "[name]"
agreement: "[title]"
sourceItemId: "[exact itemId]"
signed_date: "[ISO date]"
initial_term_end: "[ISO date]"
current_term_end: "[ISO date]"
renewal_mechanism: "[text]"
notice_period_days: "[integer]"
notice_method: "[method]"
cancel_by_effective: "[ISO date candidate]"
send_by_effective: "[ISO date candidate]"
price_on_renewal: "[text]"
annual_value: "[number if known]"
business_owner: "[id if known]"
status: active
```

missing fieldをomitして人に示す。`clm_id`、value、ownerを創作しない。

## Calibration

deal value、switching cost、business criticality、vendor leverageを考慮するが、playbook severityをsilentに下げない。large vendorが交渉しないことはrisk acceptanceの理由であり、AIのdecisionではない。
