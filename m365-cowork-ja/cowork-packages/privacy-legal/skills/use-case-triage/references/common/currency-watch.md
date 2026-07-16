> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Privacy currency watch

**Last verified: 2026-07-16**

90日を超えた場合、本書を最新statusの根拠ではなく、検索すべき論点のchecklistとして使う。法案、施行日、threshold、deadline、transfer mechanism、enforcement postureは案件ごとに公式資料を再取得する。

## 日本

### 2026年個人情報保護法改正

- 2026-04-07: 内閣提出。PPC法案資料:
  https://www.ppc.go.jp/news/press/2026/260407/
- 2026-07-10: 参議院可決により国会成立。参議院議案:
  https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/meisai/m221080221054.htm
- 2026-07-14: 内閣が法律の公布を決定:
  https://www.kantei.go.jp/jp/kakugi/2026/kakugi-2026071401.html
- 2026-07-16確認: 参議院議案ページの`公布年月日`と`法律番号`は空欄。e-Gov上の施行を確認できない。

扱いは **成立済み・公布確認待ち・未施行**。16歳未満、特定生体個人情報、連絡可能個人関連情報、統計等の同意不要措置、課徴金を現行義務・現行例外として使わない。官報、法律番号、施行日、政令、PPC規則・guidelineを再確認する。

### PPC guideline

- 通則編: 令和8年6月一部改正
  https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/
- 外国にある第三者への提供編: 令和7年12月一部改正
  https://www.ppc.go.jp/personalinfo/legal/guidelines_offshore/
- 漏えい等:
  https://www.ppc.go.jp/personalinfo/legal/leakAction/

更新日だけで改正法施行済みと推測しない。

### PIA

民間一般のPIAは一律の法定義務ではなく、PPCが促進する自主的risk-management手法。

- https://www.ppc.go.jp/files/pdf/pia_promotion.pdf
- https://www.ppc.go.jp/files/pdf/pia_overview.pdf

特定個人情報保護評価は公的機関等と一部対象者の個別制度で、一般民間PIAと同一ではない。

## COPPA

2025 amendmentsのcompliance deadlineは2026-04-22。biometric identifiers、government-issued identifiers、targeted advertisingに伴う第三者開示、written information security program、retention等をcurrent ruleで確認する。

https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa

## US state privacy

移行元は2026-05時点の州law mapを示していたが、州数・effective date・amendment・rulemakingは固定しない。各州のofficial code / AG / regulatorを再確認する。CCPA/CPRA:

- https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CIV&division=3.&title=1.81.5.
- https://cppa.ca.gov/regulations/

## Cross-border

- EU–US Data Privacy Framework、UK Extension、Swiss–US DPFのstatusと参加者を公式listで確認する。
- EU adequacy、SCC Decision (EU) 2021/914、EDPB supplementary measuresをcurrent sourceで確認する。
- 日本から外国への提供はAPPI Article 28とPPC外国提供guidelineを確認する。
- EUから日本はEU adequacy decisionと日本のSupplementary Rulesを確認する。

公式:

- https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en
- https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj
- https://www.dataprivacyframework.gov/
- https://www.ppc.go.jp/enforcement/cooperation/cooperation/sougoninshou/

## Incident / breach

日本のPPC報告対象、速報・確報、本人通知、2025-10-01以降の共通様式を確認する。GDPR 72-hour、HIPAA、GLBA、state breach law等を日本の期限と混ぜない。

## FTC / health / ad-tech

Health Breach Notification Rule、FTC Act Section 5、dark patterns、AI trainingへのdata sharing等はcurrent ruleとofficial enforcement sourceを確認する。

- https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule
- https://www.ftc.gov/legal-library/browse/statutes/federal-trade-commission-act

## 更新

変更を確認したら、日付、確認者、primary source、旧status、新statusをSharePoint `audit`へ追記する。二次資料で変更を知った場合、一次資料を取得するまで結論を変えないが、変更可能性は`[verify]`として示す。
