> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Vendor AI term matrix

| Term | 確認点 |
|---|---|
| Training on our data | input/outputをtrain、fine-tune、improve、evaluateに使うか。opt-in/out、既定値、設定証跡 |
| Confidentiality of inputs | prompt、document、RAG、log、人によるquality review |
| Model changes | material change notice、version pinning、再評価権 |
| Output ownership / IP | output allocation、license-back、third-party claim、indemnity |
| Liability for outputs | AI error、harmful output、cap、carve-out |
| Incident notification | AI failure、security、systematic error、期限、協力 |
| Human review rights | review、appeal、dispute、manual fallback |
| Use restrictions | intended useを禁止しないか、曖昧なautomated decision定義 |
| Audit / auditability | SOC 2、third-party audit、bias/accuracy test、customer audit |
| Subprocessors / model providers | 一覧、変更通知、flow-down、責任 |
| Data residency | inference、training、logging、support accessの場所 |
| Term and termination | return/delete、backup、modelへの残存、transition |
| Stacked-vendor accountability | 各層のtraining、retention、liability、免責の隙間 |

## 各finding

```markdown
### [Term]

**Severity:** 🟢 / 🟡 / 🟠 / 🔴
**Vendor says:** "[quote + section]"
**Our position:** [profile]
**Gap:** [specific delta / Aligned]
**Proposed fix:** [smallest redline / escalate]
**Upstream flow-down:** [present / partial / absent / unread]
```

## Flow-down redline例

> Provider shall ensure that any third-party model providers, infrastructure providers, or subprocessors used in delivering the Services are bound by obligations with respect to [Customer Data / AI training / data retention / confidentiality] no less protective than those set forth in this Agreement, and shall be responsible for any breach of this Agreement caused by such third parties.

実際の契約文脈、準拠法、defined termsに合わせてsurgicalに調整し、人が確認する。
