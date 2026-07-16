> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Verdict policy

## `READY`

13 parameters、3 legal failure modes、dependency mapにmaterial gapなし。配布審査へ
進めるが、security/privacy/legal/catalog/deployment approvalではない。

## `SOME CONCERN`

limited partial gap、legal failure modes addressed、high-stakes scope/escalation failureなし。
named risk owner/acceptanceを要求。

confirmed prompt overrideまたはruntime secret/credential requestはこのbandに置かない。

## `MATERIAL CONCERNS`

- legal failure mode unaddressed
- scope boundary absent
- escalation absent
- insufficient inputをsilent処理
- delegation overreach
- stale author-declared reference
- schema/guardrailの重大欠落
- 除去可能だがconfirmedなprompt override
- runtime secret/credential request（capture/use/store/transmit未確認）

remediation前のtenant-wide deploymentを勧めない。

## `REFUSE`

guardrail/runtime override、secret capture/use/store/transmit、credential theft、
exfiltrationその他concrete malicious behavior。hard deny、queue/overrideなし。

## Severity floor

upstream blocking/high findingを理由なく下げない。loweringにはold/new severityと理由、
human reviewerを記録する。

## Update comparison

new finding、expanded permission、changed purpose、dropped freshness、license/signature
regressionを明示する。old verdictを自動継承しない。
