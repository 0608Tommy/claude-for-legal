> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# DPA clause workflow

## Core table

| term | extract | compare | recurring issue |
|---|---|---|---|
| Roles | contract label、actual purpose/means | jurisdiction-specific role | labelと実態の不一致 |
| Scope | data、subjects、purpose、duration | documented instructions | `related purposes`等の拡張 |
| Security | annex、standard、control | law・playbook・risk | 抽象的`appropriate measures`のみ |
| Subprocessor | list、notice、objection | standard/fallback | approval veto、通知不足 |
| Incident | trigger、clock、content | law/contract floor | discovery/confirmationの曖昧さ |
| Audit | report/on-site、frequency、cost | playbook | 無制限・短期notice |
| Rights | assistance、deadline、cost | applicable regime | controller/processor誤分類 |
| Transfer | country、route、onward | current mechanism | outdated SCC、APPI route欠落 |
| Deletion | timing、backup、certificate | retention/legal hold | `commercially reasonable`のみ |
| Independent use | service improvement、training | instructions/policy | vendor独自学習 |
| Liability | cap、carveout、indemnity | MSA/playbook | uncapped、double recovery |

## Processor-side defensive review

- customer-by-customer subprocessor veto
- unworkable on-site audit
- notification before facts are known
- architectureと合わないhard residency
- open-ended binding instructions
- immediate deletion without backup rotation
- uncapped data liability

team standardとfallbackを適用し、法定minimumと混ぜない。

## Controller-side protective review

- current subprocessor listなし
- specific security controlsなし
- incident timelineなし
- assurance/audit evidenceなし
- independent service improvement / AI training
- transfer routeなし
- deletion commitmentなし
- rights assistanceなし

## Japan

APPIの`委託`はGDPR processorと自動同一ではない。委託範囲、必要かつ適切な監督、独自利用、再委託、外国提供を確認する。Article 28相当措置routeとGDPR SCCを同じものとして扱わない。

## Policy consistency

- policyのdata category / purpose
- `sell/share` representation
- named subprocessor / category
- location / transfer
- retention
- rights offered
- AI training / service improvement

gapはDPAかpolicyのどちらを変えるか人に選んでもらう。

## Finding block

```markdown
### [Term]

**Contract:** [exact quote / section]
**Binding law:** [requirement or n/a]
**Official guidance:** [if used]
**Playbook:** [standard / fallback / never]
**Gap:** [specific]
**Risk:** [severity and why]
**Draft redline:** [smallest deletion/insertion/replacement]
**If they will not move:** [fallback / approver]
```
