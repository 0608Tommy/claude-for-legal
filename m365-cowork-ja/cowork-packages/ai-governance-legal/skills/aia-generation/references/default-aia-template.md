> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 標準AIAテンプレート

```markdown
> **⚠️ レビュー担当者向け注記**
> - **Sources:** [...]
> - **Read:** [...]
> - **Flagged for your judgment:** [...]
> - **Currency:** [...]
> - **Destination:** [...]
> - **Before relying:** [...]

機密 — 内部法務レビュー用ドラフト — 法的助言ではなく、有資格者の確認前に依拠・配布しないこと

# AI Impact Assessment: [System/Feature Name]

**Prepared by:** [name] | **Date:** [date] | **Status:** DRAFT
**System owner:** [name] | **AI governance reviewer:** [name]
**Governance tier:** [Standard / Elevated / High]
**Track:** [Fast track / Full assessment]

## Executive summary

[何をするシステムか、導入可否の提案、必要条件]

**Overall risk:** 🟢 Low / 🟡 Medium / 🟠 High / 🔴 Blocking

## 1. System description

**What it does:** [...]
**Model / vendor:** [...]
**Deployment mode:** [Assistive / Augmentative / Automated]
**Output type:** [...]
**Stage:** [Proposed / Pilot / Production / Scaled]

## 2. Affected parties

**Who:** [...]
**Scale:** [...]
**Harm if wrong:** [...]
**Vulnerable groups:** [...]

## 3. Data

**Inputs:** [...]
**Personal/confidential data:** [...]
**Data leaves perimeter:** [...]
**Training / RAG / logging:** [...]

## 4. Decision-making and oversight

**Human review:** [Effective / Nominal / None]
**Override:** [...]
**Appeal / correction:** [...]
**Owner / kill switch:** [...]

## 5. Accuracy, bias, and security

**Testing:** [...]
**Failure handling:** [...]
**Bias:** [...]
**Security:** [...]

## 6. Regulatory classification

[法域ごとに適用、role、tier、義務、別評価、日付、未確定点]

## 7. AI policy consistency

| Commitment | Consistent? | Notes |
|---|---|---|
| [...] | 🟢 / 🟡 / 🟠 / 🔴 | [...] |

## 8. Risks and mitigations

| # | Risk | Likelihood | Impact | Mitigation | Status | Owner |
|---|---|---|---|---|---|---|
| 1 | [...] | L/M/H | L/M/H | [...] | Done / Planned / Gap | [...] |

**Residual risk:** [...]

## 9. Recommendation

**Proposed outcome:** [APPROVED / APPROVED WITH CONDITIONS / CHANGES REQUIRED / NOT APPROVED]

**Conditions:**
- [ ] [action — owner — deadline]

**Separate reviews:** [PIA / FRIA / vendor / sector / none]
**Human sign-off required:** [name/role]

## 10. Unverified items

[citation, date, threshold, open legal judgment]
```

`APPROVED` はテンプレート上の候補値であり、AIが設定しない。人の承認前は `DRAFT` とする。
