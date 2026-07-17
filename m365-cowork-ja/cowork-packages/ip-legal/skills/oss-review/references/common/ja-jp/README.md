> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本法module — Intellectual Property

**Status:** `DRAFT / qualified Japanese counsel review pending`

**Primary sources checked through:** `2026-07-16 JST`

本moduleは移行元のU.S. workflowを単に翻訳せず、日本の特許法、実用新案法、
商標法、意匠法、著作権法、不正競争防止法、Platform Act、Customs、JPO実務へ
forkします。

## 適用順序

1. requestで明示されたjurisdiction
2. authorized matter profile
3. IP practice profile
4. tenant default

複数法域が関係する場合、最も都合のよい1法域へ丸めません。right、registration、
conduct、market、platform、manufacture、import、contract governing lawごとに分けます。
日本がscopeにない場合、本moduleを自動適用しません。

## Authority class

- **[B]** statute、Cabinet Order、ordinance、rule、拘束的judgment
- **[G]** JPO examination guideline、official procedure、agency guidance
- **[C]** case-sensitive doctrine、fact-specific judicial application
- **[I]** internal approval、evidence preservation、watch、isolation、delivery
- **[F]** future/pending、promulgated-not-effective、proposal

class、source、version、effective dateを成果物へ示します。[F]をcurrent lawへ
先行適用しません。

## Module map

- [公式情報源台帳](source-register.md)
- [商標clearance](trademark-clearance.md)
- [特許・実用新案・意匠](patents-utility-designs.md)
- [著作権・Platform Act](copyright-platform.md)
- [営業秘密・OSS](trade-secrets-oss.md)
- [契約・権利帰属・recordal](contracts-ownership.md)
- [権利行使・Customs](enforcement-customs.md)
- [日本の秘密性・matter security](privilege-security.md)

## Mandatory review

次は日本の弁護士、弁理士、税関・platform・prosecution等の適切なspecialistへ
routeします。

- clear、patentable、FTO、infringing/non-infringingの最終結論
- Article 30、patent secrecy、foreign filing、inventorship/employee invention
- claim construction、equivalents、invalidity、Article 104-3
- recordal、standing、co-ownership、moral rights
- C&D、takedown、counter-response、Customs suspension、provisional relief
- JPO deadline、fee、form、restoration、filing cohort
- strong copyleft、license compatibility、source release
- destructive portfolio rebuild、renewal/abandonment decision

本moduleの存在はreview完了、opinion、production approvalを意味しません。

## 絶対に移植しないもの

- `Alice/Mayo`を日本のsoftware/AI eligibility testとして使う
- DMCA §512 form・perjury・counter-notice clockを日本routeへ使う
- `du Pont`, `Polaroid`, `Sleekcraft`またはLanham/TDRAを日本商標testにする
- DTSA/UTSA、state preemption、inevitable disclosureを日本営業秘密ruleにする
- `Egyptian Goddess`, point-of-novelty、35 U.S.C. §289を日本意匠へ使う
- §284 willfulness/treble damages、FRE 408、Rule 11 boilerplateを日本手続へ使う
- U.S. §8/§71、3.5/7.5/11.5-year feeを日本portfolioへ使う

U.S./global案件は`original-ip-logic.md`の別layerを適用します。
