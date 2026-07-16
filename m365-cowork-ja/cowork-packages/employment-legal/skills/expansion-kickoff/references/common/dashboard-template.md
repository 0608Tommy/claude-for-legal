> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Data-heavy output template

10行超のleave register、investigation coverage、expansion tracker、termination
portfolio等ではdashboardを提案できますが、依頼なしに作りません。

## Structure

1. summary stats: total、blocking/high、due、unknown、coverage。
2. sortable table: pseudonymous ID、status、owner、date、source/currency。
3. chartは最大2つ: status distributionまたはtimeline。
4. reviewer note、scope、last refreshed、missing data。

restricted matterの氏名、medical detail、whistleblower identityをsummary/chartへ
出しません。別matterをaggregateするにはexplicit request、permission、purpose、
confidentiality reviewが必要です。

HTMLでは外部由来値をescapeし、DOMへの挿入は`textContent`、URL schemeは
`http:`, `https:`, `mailto:`だけを許可します。CSV/Excelでは`=`, `+`, `-`,
`@`, tab、CR、LFで始まる値をtextとしてneutralizeし、RFC 4180 quotingを使います。
native Office file、chart、email送信を作成・実行したと主張しません。
