> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# QA and role routing

| Verdict | Route |
|---|---|
| `READY` | approval packet作成可 |
| `SOME CONCERN` | named risk acceptance |
| `MATERIAL CONCERNS` | remediationまたはSecurity/Legal exception |
| `REFUSE` | hard deny、queueなし |

confirmed prompt override/runtime secret or credential requestは
`SOME CONCERN`のrisk acceptance対象外。mandatory remediationまたは`REFUSE`。

## Non-lawyer requester

concern以上では、plain-language attorney/security briefを先にする。requesterに
final risk acceptance/self-approvalを求めない。attorney/security contact不明なら
setup/profile correctionへ戻す。

## Lawyer requester

lawyerでもtenant Security/Privacy/Policy approvalを代行しない。

## Separation

- requester ≠ required approver
- reviewer ≠ deployment operator
- security/license exceptionはSecurity + Legal
- deployment operatorはpacket内容を変更しない

role/groupはexact Entra IDとcurrent membership evidenceで確認する。
