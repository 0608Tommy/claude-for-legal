> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Stakeholder output

## Internal version

```markdown
[appropriate internal confidentiality marking]

**[Counterparty] [Agreement type]** — [UPSTREAM REVIEW STATUS]

[何のための契約か、business terms、sales/purchasing context。]

[驚く点、main risk、交渉中の点。cleanなら「重大なsurpriseなし」。]

**Escalation status:** [M] of [N] delivered · [D] drafts prepared.
- [unrouted approver — finding]

**What you need to do**
- [ ] [最大3つ]

**Approval:** [approver and expected timing]
```

escalation reconciliation blockはlength目安の外だが、簡潔にする。

## Sanitized version

```markdown
**[Counterparty] [Agreement type]** — [business-facing status]

[内部playbook、privilege、accepted risk、個人名を除いた説明。]

**Next steps**
- [ ] [recipient action]

**Timing:** [realistic timing]
```

external recipientへ`READY TO SIGN`を出す場合、人-reviewed source statusと送信承認を確認する。

## Translation examples

| Legal finding | Business language |
|---|---|
| liability cap at 12 months fees | 問題が起きても、回収できる上限は概ね1年分のfeesです |
| no termination for convenience | 使わなくなってもterm途中で自由に解約できません |
| auto-renewal 60-day notice | 毎年自動更新され、更新60日前までに所定方法で通知が必要です |
| no IP indemnity | 第三者のIP claimがあってもvendorが防御・補償しない範囲があります |
| data export only at termination | 契約終了時までself-service exportできません |
| SLA credits sole remedy | downtime時の主なcontract remedyは限定的なservice creditです |

「indemnification」「notwithstanding」等をそのまま使わず、誰が何を負担するかを書く。
