> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Employee privacy、monitoring、confidentiality、matter isolation

**状態:** DRAFT — qualified Japanese counsel review pending

## APPI・My Number [B/G]

employee/applicant dataについて、利用目的、適正取得、要配慮個人情報、本人同意、
security、委託先監督、第三者提供、外国移転、開示等、retention/deletionを確認します。
My Numberは別の厳格な目的・保管・access controlを適用します。

medical/accommodation、leave、whistleblower identity、investigation evidenceは
必要最小限で取得し、一般HR profileやglobal auditへ複製しません。

## Monitoring [B/G/contract]

日本には単一のemployee-monitoring statuteやforeign doctrineの単純移植はありません。
APPI、労働契約、work rules、CBA、purpose/proportionality guidanceを組み合わせます。

- specific purposeとnecessity
- less intrusive alternative
- data/people/time/system scope
- notice、visibility、employee communication
- performance/discipline use
- access、vendor、foreign transfer
- retention/deletion、security

secret surveillance、continuous emotion inference、purpose外評価、説明不能scoreを
High/`[review]`とします。

## Japanese confidentiality

日本の弁護士の守秘義務と民事手続上の提出拒絶等は、米国のgeneral corporate
attorney-client/work-product shieldと同一ではありません。labelはaccess controlの
代替になりません。attorney-directed purpose、依頼関係、distribution、business/
legal mixed purpose、外部開示を確認します。

## Restricted matter [I]

investigation、whistleblowing、medical/accommodation、leave、discipline、
contested terminationは、一般workspaceがoffでもrestricted matterへ分離できます。

- pseudonymous central index
- identity mappingとsubstantive recordをrestricted ACL内
- whistleblower identityを一般investigation recordから分離
- least privilege、access audit、export control
- legal hold、documented retention/deletion
- close時全binding revoke

`archive forever`をuniversal APPI policyにしません。法定保存、dispute、documented
business needとdeletion scheduleを結びます。
