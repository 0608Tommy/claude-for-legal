> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Parameters 10–13

## 10. Trust Surface

inspect:

- hook
- connector/host/operator/OAuth/tool
- Bash/network
- file/state/catalog write/delete
- credential
- prompt injection
- legal/privilege/security overclaim

undeclared connector、unbounded Bash/network、scope外write、overclaimは🔴。
read-only、no hook/connector/networkはlow surfaceだが安全保証ではない。

## 11. Freshness

reference contentの`last_verified`、window、category、verified sourceをstrict validation。

- author window超過 → material concern候補
- referenceありdateなし/invalid → some concern
- rule/deadlineを`stable` → review
- referenceなし → N/A

commit dateとlegal freshnessを分ける。

## 12. Schema

- discoverable name/description/when-to-use
- workflow/method
- output template
- scope/limitations
- worked example
- legal guardrails
- strict frontmatter/tool metadata

required section欠落はsome concern。legal skillでexampleとguardrail双方なしはmaterial。

## 13. Conflicts

- trigger overlap
- instruction/playbook conflict
- scope duplication
- dependency/version collision
- first-party protected overlap

差異が明確ならrelationshipを記録。defaultが不明なoverlapはsome concern。
first-party instruction conflictを黙って上書きしない。
