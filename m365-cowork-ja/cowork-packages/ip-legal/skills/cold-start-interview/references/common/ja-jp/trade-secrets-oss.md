> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本営業秘密・OSS

## Trade secrets

日本のbinding layerは不正競争防止法です。

- **秘密管理性**
- **有用性**
- **非公知性**
- enumerated acquisition/use/disclosure act

METI Trade Secret Management Guidelinesは**[G]**です。DTSA/UTSAの
`reasonable measures`、state preemption、inevitable disclosureを日本ruleとして
使いません。

2024-04-01施行改正ではimitative product configurationのelectronic provision、
qualifying cross-border trade-secret conductに関するArts. 19-2/19-3のJapanese
jurisdiction/application等をfactsに応じて確認します。

evidence:

- access control、need-to-know、classification/marking
- NDA、employment/contractor agreement
- training、exit、return/destruction
- repository/access log、download、device、version/hash
- source、usefulness、public availability
- lawful reverse engineering/independent development

evidence preservationは**[I]** litigation controlです。U.S. legal-hold doctrineを
日本のbinding representationとして表示しません。

## OSS legal layers

日本に独立した「OSS compliance statute」はありません。binding layerは
copyright、contract、patent、trade secretであり、actual upstream license textが
operative evidenceです。IPA materialは**[G] governance guidance**です。

required inventory:

- package、version、source URL、hash
- actual `LICENSE`、header、NOTICE
- direct/transitive、dual-license choice
- modification、static/dynamic linking、IPC/API relationship
- SaaS、customer-hosted、container、mobile、firmware、source conveyance
- notice、corresponding source/source offer、installation information
- patent clause、trademark、export/crypto
- employee/contractor ownership、CLA/DCO authority
- outbound-license compatibility、confidential/proprietary material

## Avoid categorical shortcuts

- AGPL network interactionを単に「distribution」と言わず、version、modification、
  combined-work scope、AGPL §13を確認。
- pure SaaSだからMIT/BSD UI attributionが必須または不要と決めず、actual clauseと
  copy conveyanceを確認。
- dynamic LGPL linkingをautomatic low riskにしない。source availability、
  relinking/reverse-engineering、notice、modificationを確認。
- microservice/API boundaryはevidenceでありautomatic safe harbor/triggerではない。
- `OSI approved`はpolicy classificationであり、日本法上のenforceability結論ではない。

## Classification enum

`Permissive | Weak copyleft | Strong copyleft | Public domain |
Non-OSI source-available | Other/custom/unknown`

unknownをpermissive defaultにしません。license conflict、recent relicensing、
dual-license ambiguity、strong copyleft、source-available business restrictionは
attorney reviewへrouteします。

AIはsource release、repository publication、license acceptance、commercial licence
purchaseを実行しません。
