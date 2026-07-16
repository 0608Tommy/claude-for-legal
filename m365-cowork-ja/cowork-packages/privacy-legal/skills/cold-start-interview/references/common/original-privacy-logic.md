> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元のglobal / GDPR / USプライバシーロジック

本書は移行元`privacy-legal`の判断枠組みを日本語で保持する基礎layerである。日本法モジュールに置き換えず、関係法域ごとに並行適用する。

## 法域認識

1. request、matter、practice profile、tenant defaultの順で法域を解決する。
2. 当事者、data subjects、処理場所、販売地域、data location、governing lawを確認する。
3. 1つの法域の用語・deadline・例外を別法域へ黙って移植しない。
4. 対応frameworkがなければ、公式基準を取得する、現地有資格者へ回す、または構造だけを使い各結論を`[verify against [jurisdiction] law]`とする。

## Controller / processorとDPA

移行元`dpa-review`は方向を必ず確定する。

- 当社が`processor`でcustomer paperを受ける場合: operational flexibility、subprocessor、audit、incident、location、deletion、liabilityのplaybookを守る。
- 当社が`controller`でvendor paperをreviewする場合: documented instructions、security annex、subprocessor transparency、incident notice、audit evidence、transfer、deletionを要求する。

ただし法域用語は同一ではない。GDPRの`controller` / `processor`、CCPA/CPRAの`business` / `service provider` / `contractor`、日本法の`個人情報取扱事業者` / `委託`は自動的に同じ関係ではない。契約labelではなく、目的・手段・指示・独自利用・再提供・法定義務を事実から分類する。

review対象:

- rolesと実態
- processing scope / documented instructions
- security measures
- subprocessors
- incident triggerとnotice
- audit / assurance
- international transfers
- deletion / return / backup
- assistance with rights and regulator inquiries
- liabilityとMSA整合
- privacy policy / noticeとの整合

修正文案は最小granularityとし、word→phrase→subclause→sentence→clauseの順で検討する。native tracked changesを生成したとは表示しない。

## GDPR / UK GDPR

適用時は最新原文を確認する。

- roles・definitions: GDPR Article 4
- processor terms: Article 28
- data-subject rightsとtransparent response: Articles 12–22
- response: Article 12(3)の原則1か月、条件付き2か月延長
- DPIA: Article 35。高いriskが見込まれる処理についてtriggerを確認
- breach to authority: Article 33の原則72時間
- communication to data subject: Article 34
- international transfers: Chapter V
- EU SCCs: Commission Implementing Decision (EU) 2021/914

公式:

- https://eur-lex.europa.eu/eli/reg/2016/679/oj
- https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj
- https://www.edpb.europa.eu/our-work-tools/our-documents_en
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/

EU supervisory authorityへのDPIA提出・事前consultation、UK IDTA / Addendum、adequacy、SCC module、supplementary measuresはcorridorとcurrent statusを確認する。内部PIAをformal DPIAの代替と扱わない。

## US comprehensive state privacy

米国に単一の一般privacy lawがあると仮定しない。data subject所在地、threshold、entity/data exemption、effective date、regulationsを州ごとに確認する。

CaliforniaではCCPA/CPRAの`business`, `service provider`, `contractor`, `sell`, `share`, sensitive personal information、consumer rights、45-day response framework等をcurrent statute/regulationsで確認する。

- https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CIV&division=3.&title=1.81.5.
- https://cppa.ca.gov/regulations/

Virginia、Colorado、Connecticut、Utah、Texas、Oregonその他の州法は、source `currency-watch.md`の一覧をcurrent mapとして固定せず、各州の公式法令・AG資料で確認する。

## US federal sectoral overlay

state-law exemptionは「無規制」を意味しない。activity-based overlayを先に確認する。

- GLBA / Regulation P / Safeguards Rule: financial institution、NPI、sharing、security
- HIPAA / HITECH: covered entity、business associate、PHI、BAA、breach
- FERPA: education records、school official、consent
- COPPA: child-directed online services、actual knowledge、parental consent
- VPPA: video viewing records
- CPNI / Communications Act: carrier data
- DPPA: motor vehicle records
- TCPA: call/SMS consent
- FTC Act Section 5とHealth Breach Notification Rule

公式:

- https://www.ftc.gov/legal-library/browse/statutes/gramm-leach-bliley-act
- https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314
- https://www.hhs.gov/hipaa/for-professionals/index.html
- https://studentprivacy.ed.gov/ferpa
- https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule
- https://www.fcc.gov/general/customer-proprietary-network-information

2025 COPPA amendmentsは2026-04-22 compliance deadlineを含むため、子どもdata、biometric identifiers、government IDs、targeted advertising、security program、retentionをcurrent ruleで確認する。

## DSAR / rights workflow

移行元の共通順序:

1. request typeと適用regimeを分類する。
2. receipt date、clock、extension、fee、authorized agentを確認する。
3. riskに比例して本人確認する。
4. configured systemsをsystem-by-systemに探索する。
5. third-party data、privilege、trade secret、security、legal obligation、litigation hold、backup等の例外候補を列挙する。
6. acknowledgment draftとsubstantive response draftを分ける。
7. attorneyが例外、redaction、scope、delivery、sendを承認する。
8. response、production/deletion、basisをauditする。

「2通」は移行元のhouse processであり、全法域の一律の法定要件とは書かない。clock start、extension、本人確認によるtollingをregimeごとに確認する。

## PIA / DPIA / triage

移行元のclassificationは次を保持する。

- `PROCEED`
- `PIA REQUIRED`
- `DPIA MANDATORY`
- `STOP`

house PIA triggerと法定assessment triggerを分ける。policy conflict、lawful basis、unexpected processing、children、biometrics、dataset combination、discrimination、automated decisions、ad-tech、sectoral dataは強いrisk indicator。法定triggerがないのに`DPIA MANDATORY`と書かず、internal requirementなら`PIA REQUIRED — internal policy`とする。

PIAはdata fields、purpose、subjects、collection、storage、access、sharing、retention、rights、risks、mitigations、owners、conditions、residual risk、sign-offを記録する。上流severityを理由なく下げない。

## Privacy policy drift

website policyだけでなく、CMP/cookie banner、App Store privacy label、Google Data Safety、in-product consent、GLBA/HIPAA/FERPA/COPPA等のsectoral noticeを確認する。

- policyが列挙しないdata category
- 新目的・二次利用
- vendor独自利用
- retentionの不一致
- rights processが扱えないdata
- cross-border、AI training、ad-tech

`REQUIRED`と`ADVISABLE`は人の判断前の提案であり、skillがpolicyを更新・公開しない。

## Privilege、source、current law

米国の`ATTORNEY WORK PRODUCT`はFRCP 26(b)(3)等の文脈依存であり、EU・UK・日本へ自動移植しない。法令、case、deadline、threshold、adequacy、SCC、state-law map、enforcement postureはcurrent primary sourceで確認する。取得できないauthorityを創作しない。
