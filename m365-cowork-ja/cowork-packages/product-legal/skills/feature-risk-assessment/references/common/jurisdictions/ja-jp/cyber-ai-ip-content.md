> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Cybersecurity、AI、disclosure、IP/content

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Cybersecurity

Cybersecurity Basic Act、Economic Security Promotion Act、Cyber Response
Capability Enhancement Actをservice/entity/designationごとに確認する。Cyber
Response Actはstaged commencementであり、全体をcurrentまたはfutureの一色に
しない。2026-07-16時点で一部は施行済みだが、特別社会基盤事業者のreporting/
notification provisionsは将来施行である。

special social-infrastructure operator reportingの8府省庁共同命令は
2026-10-01施行予定。[F]としてlaunch date、designation、system、incident typeを
確認する。

METI Cybersecurity Management Guidelines v3.0、MIC AI security guidance、
JC-STAR等は[G]。JC-STARはIPAのofficial voluntary schemeであり、private
platform policyではない。contract/procurementへincorporateされた場合は、その
別個の契約・調達上のeffectを確認する。

launch check:

- threat model、auth、privilege、logging
- vulnerability handling、patch/update、SBOM
- data/secret、supply chain、cloud/vendor
- incident detection、reporting owner、evidence
- cyber-physical/safety impact
- economic-security designation/procurement

## AI governance

AI Promotion Actはframework/promotion lawであり、EU AI Act型の一律
prohibited/high-risk conformity regimeではない。

分ける:

- `[B]` AI Actとapplicable sector law
- `[G]` AI guideline、AI Business Guidelines、security/evaluation guide
- `[I]` company AIA、registry、tier、human oversight
- `[P]` platform AI/synthetic-content policy
- `[F]` election-specific future rule等
- `[X]` EU AI Act、U.S. state AI law等

2026-07-16時点で全AI outputに一律labelを要求する一般日本法は確認できない。
misleading representation、stealth、impersonation、IP/privacy、election、
sector rule、platform policyが個別に要求するかを確認する。

## AI feature facts

- model/vendor/version、training/fine-tuning/RAG
- input/output data、independent vendor use
- assistive/automated、affected decision
- human review、override、appeal、support
- hallucination、bias、security、monitoring
- generated person/review/content、disclosure
- change management、evaluation evidence

internal AIA completionを日本法上の一律statutory approvalと書かない。

## Copyright / content

development/trainingとgeneration/useを分ける。著作権法30条の4等を
「AI trainingは常に許諾不要」と一般化しない。

training:

- source、licence、technical restriction
- purpose、enjoyment、market impact
- targeted reproduction
- personal/confidential/contract-restricted data

generation/use:

- similarity、dependency、prompt/RAG/fine-tuning
- publication/sale/advertising
- provenance、human search/review
- vendor IP indemnityとexclusion

vendor contract上のoutput allocationを日本法上のcopyright ownershipと同一視
しない。不正競争防止法上のtrade secret、NDA、terms、data licenceも確認する。

著作権法令和8年法律第48号は2026-06-24公布。主要な実演家・レコード製作者報酬規定
は公布後3年以内の政令指定日施行で[F]とする。この改正を著作権法30条の4の
AI training分析を変更するものとして適用しない。

## Future election rule

AI-generated/altered election imagery amendmentの主要部分は2027-03-01予定。[F]で
trackingし、一般AI content labelへ拡張しない。

## Gate

security owner、model/source evidence、human escalation、IP provenance、
applicable disclosure、future dateが不明なら`no issue`としない。AI governance、
security、IP、privacy、product、communications ownerを分ける。
