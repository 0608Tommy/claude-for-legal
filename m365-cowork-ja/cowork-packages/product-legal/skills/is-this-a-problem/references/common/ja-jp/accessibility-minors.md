> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Accessibility、未成年、child users

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Accessibility

障害者差別解消法上、private businessのreasonable accommodationは2024-04-01から
mandatoryとなった。具体的request、burden、alternative、interactive process、
critical flowを確認する。

JIS X 8341-3:2016、WCAG、Digital Agency guidebookは、contract/procurement、
internal acceptance criteria、reasonable processのevidenceになり得るが、
private productすべてに一律のstatutory WCAG/JIS conformance mandateがあるとは
書かない。

launch check:

- account creation、authentication、purchase/cancel、support、safety notice
- screen reader、keyboard、caption、contrast、error recovery
- accommodation request routeとowner
- public-sector/procurement/sector contract

## Minors

Civil Code上の成年年齢は2022-04-01から18歳。18歳未満のcontractは法定代理人同意
等を含む取消可能性を検討するが、exceptionとactual transactionを確認する。

PPC FAQは、APPI上本人同意が必要な場面で、本人が同意の結果を判断できる能力を
有するかをdata、business context等から個別に判断し、能力がない場合に法定代理人等
から同意を得る考え方を示す。年齢は一要素であり、すべての収集・処理へ一律の
parental consentを課すruleでも、COPPAのfixed under-13 ruleでもない。

確認:

- age range、actual knowledge、age assurance
- contract/paid feature、representative consent
- personal data、sensitive inference、profiling
- harmful/addictive design、contact、location
- UGC、marketing、influencer、school/family context
- support、refund、account recovery
- Youth Internet Environment Act、sector/platform rule

## Future APPI

2026 amendmentのunder-16 provisionは、notice、consent、rights等を法定代理人へ
routeする将来規定であり[F]。official promulgation、law number、effective date、
PPC ruleを確認するまでcurrent dutyまたは全processingへのblanket opt-inとして
適用しない。future readiness taskとcurrent rule findingを分ける。

## Foreign law

COPPA、UK AADC、U.S. state AADC/social-media/minor laws、EU DSA等は対象user/entityの
nexusがある場合だけ[X]で並行適用する。日本のcapacity/contract/privacy analysisを
置き換えない。

## Gate

age、purchase authority、affected users、consent flow、accessibility-critical
journey、accommodation routeが不明なら、child/accessibility riskを`FYI`へ落とさない。
product、privacy、support、accessibility、日本法有資格者のownerを指定する。
