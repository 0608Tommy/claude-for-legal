> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本法corporate/M&A moduleを追加した派生ファイルです。

# 日本法module — Corporate / M&A

**Status:** `DRAFT / qualified Japanese counsel review pending`

**Primary sources checked through:** `2026-07-16`

本moduleは移行元の米国中心workflowを単に翻訳せず、日本の会社法、金融商品取引法、
上場規則、独占禁止法、外為法、商業登記、労働、個人情報、知財、許認可、
電子記録・署名、post-close integrationへforkする。

## 適用順序

1. requestで明示されたjurisdiction
2. authorized matter profile
3. corporate practice profile
4. tenant default

複数法域が関係する場合、最も都合のよい1法域へ丸めない。entity、asset、
employee、data、licence、security、listing、governing lawごとに分ける。
日本がscopeにない場合、本moduleを自動適用しない。

## layer

- `LAW/RULE`: statute、Cabinet Order、ordinance、regulation
- `LISTING`: JPX等のlisting relationshipを通じたrule
- `GUIDANCE`: official administrative/enforcement guidance
- `SOFT LAW`: Corporate Governance Code、METI M&A guide等
- `CONTRACT`: PA、articles、company regulation、shareholder agreement
- `INTERNAL`: materiality、sample、approval、clean-team、house style
- `PENDING`: proposal、enacted/promulgation pending、not effective

成果物はlayer、version、effective dateを示す。`PENDING`をcurrent lawとして
適用しない。内部thresholdを法定materialityと表示しない。

## module map

- **Official source register:** Companies Act、FIEA、JPX、JFTC、FEFTA、registry、
  e-sign、labor、APPI、IP、sector、professional rules
- **Governance and records:** entity form、organ design、board/shareholder action、
  minutes、written/electronic consent、retention、registry、beneficial-owner list
- **M&A and regulatory:** transaction structure、corporate action、FIEA/TDnet、
  merger control、foreign investment、closing
- **Diligence overlays:** contract transfer、labor、privacy、IP、licence、tax、
  economic security、successor liability
- **Integration and entity:** structure-specific succession、two-week registrations、
  tax/social/labor notices、licence、IP recordal、periodic/event obligations
- **Privilege and security:** Japanese confidentiality/production differences、
  JFTC limited procedure、AI/VDR transfer gate、Cowork DLP blocker

## mandatory review

次は日本法有資格者または該当specialistへrouteする。

- organ design、articles、board/shareholder validityに不明点がある
- tender offer、large holding、insider、EDINET/TDnet trigger
- JFTC thresholdまたはhigh-value below-threshold review
- FEFTA investor/control/designated/core business/exemption
- labour succession、collective agreement、employee objection/consent
- regulated-sector ownership、licence succession、economic security
- privilege、authority production、clean-team、MNPI
- destructive rebuild、closing certification、filing、signature、external send

本moduleの存在はreview完了またはproduction approvalを意味しない。
