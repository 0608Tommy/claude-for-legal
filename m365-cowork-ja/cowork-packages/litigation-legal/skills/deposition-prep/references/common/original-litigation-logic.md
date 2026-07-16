> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元litigation workflowの正規token

本書はsource compatibilityのためのtoken台帳。日本法layerは米国法を移植せず、
ID、flags、keys、enums、placeholder shapeだけを保持する。

## 登録IDとcanonical labels

| ID | canonical label / argument shape |
|---|---|
| `brief-section-drafter` | `/litigation-legal:brief-section-drafter [section — e.g., 'statement of facts', 'argument II']` |
| `chronology` | `/litigation-legal:chronology [slug] [--format=working|sof|witness-[name]]` |
| `claim-chart` | `/litigation-legal:claim-chart [--patent | --civil] [--infringement | --invalidity | --review] [--claim <n>] [--count <name>] [--target <slug>]` |
| `demand-draft` | `/litigation-legal:demand-draft [slug] [--skip-gate] [--version=N]` |
| `demand-intake` | `/litigation-legal:demand-intake [title] [--full]` |
| `demand-received` | `/litigation-legal:demand-received [path-to-incoming] [--slug=custom-slug]` |
| `deposition-prep` | `/litigation-legal:deposition-prep [witness name]` |
| `matter-briefing` | `/litigation-legal:matter-briefing [slug]` |
| `privilege-log-review` | `/litigation-legal:privilege-log-review [log file, or document set]` |
| `subpoena-triage` | `/litigation-legal:subpoena-triage [path-to-subpoena] [--slug=custom-slug]` |
| `legal-hold` | `/litigation-legal:legal-hold [slug] [--issue | --refresh | --release | --status]` |
| `matter-close` | `/litigation-legal:matter-close [slug]` |
| `matter-intake` | `/litigation-legal:matter-intake [optional matter name]` |
| `matter-update` | `/litigation-legal:matter-update [slug] [brief event description]` |
| `matter-workspace` | `/litigation-legal:matter-workspace <new | list | switch | close | none> [slug]` |
| `oc-status` | `/litigation-legal:oc-status [--all | --slug=foo | --no-gmail]` |
| `portfolio-status` | `/litigation-legal:portfolio-status [--all | --risk=high | --stale]` |
| `cold-start-interview` | `/litigation-legal:cold-start-interview [--redo | --check-integrations]` |
| `customize` | `/litigation-legal:customize [section name, or describe what you want to change]` |

Coworkではslash commandを要求せず、会話stateとして解釈する。

## Grammar correction

- `chronology`: `--matter`, `--documents`, `--include-flagged`を公開し、
  `--include-flagged`は明示的な秘密性/privilege acknowledgmentを要求する。
- `claim-chart`: `--include-dependents`を公開し、除外したasserted dependent claimを
  明示する。
- `demand-intake` / `demand-draft`: `--resume-strategic`を実state
  `resume-strategic`として実装し、単なる案内文にしない。
- `legal-hold --status`: writeを要求しないread-only branch。
- 全cold start: `--full`, `--redo <section>`を受け付ける。source proseの
  `--new-matter`もcanonical referenceとして保持する。

## Source enums preserved

### Demand

```yaml
demandType: payment | breach-cure | cease-desist | employment-separation | preservation | other
relationship: customer | vendor | ex-employee | competitor | third-party | other
tone: measured | assertive | aggressive
strategic_block: answered | partial | skipped
status: intake | ready-to-draft | drafted | sent | closed
```

日本案件では`marking`によりinadmissibility/confidentialityを約束しない。

### Matter

```yaml
type: contract | employment | ip | regulatory | investigation | product | other
role: plaintiff | defendant | claimant | respondent | investigated
conflictsStatus: cleared | pending | not-run | waived
conflictsMethod: corporate-legal | outside-counsel | system-check | informal | other
risk: high | medium | low | critical
materiality: reserved | disclosed | monitored | none
engagement: signed | pending | none
source: demand-letter | complaint-served | subpoena | regulator-inquiry | internal-report | pre-suit-threat
initialPosture: fight | settle | investigate | wait
```

日本のprocedure detailは追加fieldへ記録し、上記tokenを翻訳・renameしない。

### Matter workspace

```yaml
state: new | list | switch | close | none
confidentiality: standard | heightened | clean-team
status: active | archived
bindingStatus: active | revoked
```

target packageは`restricted`も追加するが、source tokenを削除しない。

### Update categories

```yaml
eventType: Procedural | Discovery | Substantive | Strategy | Risk re-assessment | Stakeholder | Administrative
```

日本案件のuser-facing labelは日本語化できるが、source import tokenはrawで保持する。

### Claim chart

Patent source mapping:

```yaml
mapping: literal | literal-construction-dependent | doe | anticipation | obviousness-combination | partial | not-found | needs-evidence | construction-dependent
state: mapped | mapped-doe | partial | not-found | needs-evidence | construction-dependent | anticipation | obviousness-combination
confidence: strong | moderate | weak | none
```

Civil source state:

```yaml
state: supported | partial | disputed | gap | needs-discovery
strength: strong | moderate | weak | none
```

日本chartは追加sheet/stateを使えるが、source importをsilent rewriteしない。

### Inbound / request

```yaml
demandRating: substantial | debatable | weak | frivolous
demandResponseOption: A | B | C | D
subpoenaClassification: third-party-docs | third-party-depo | party | CID | grand-jury
burden: small | medium | large | extreme
objectionStrength: strong | reasonable | weak
```

日本の裁判所命令・照会は`instrumentTypeJP`に分類し、
`subpoenaClassification`へRule 45相当として押し込まない。

### Close

```yaml
outcome: settled | dismissed | judgment-for-us | judgment-against-us | withdrawn | consolidated | other
```

日本では`dismissed with/without prejudice`を翻訳適用しない。new JP recordは
`outcomeDetailJP`で実際の終局形態を記録し、source `outcome`は互換fieldとして保持する。

## Source behavior preserved

- every output is draft; consequential actionはfresh human approval。
- exact record quoteとpinpoint。sourceなしのquote/citationを作らない。
- conflicts/access gateをsilent bypassしない。
- history/eventはappend-only。correctionはnew event。
- chartはconclusion/filing/contentionではない。
- demandのdraftとsendを分離。
- hold noticeのdraftとissue/releaseを分離。
- candidate deadlineとcalendar entryを分離。
- connector declarationとlive connectionを分離。
- cross-matter access default`false`。

## 日本で無効化するUS default

FRCP、FRAP、FRE 408、Rule 30、Rule 37(e)、Rule 45、Rule 11、Bluebook、
Markman、Patent Local Rules、米国pattern jury instruction、PACER/CourtListenerを
日本法または日本の裁判所運用として使わない。foreign proceedingが実際に関係する場合
だけ、そのforeign-law branchをcurrent sourceとqualified counsel review付きで使う。
