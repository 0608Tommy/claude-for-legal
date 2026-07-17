> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 安全管理・漏えい等

**状態:** DRAFT — qualified Japanese counsel review pending

## 安全管理

APPI、PPC通則guideline、該当sector guidelineに従い、組織的、人的、物理的、技術的安全管理、外的環境の把握、従業者監督、委託先監督を確認する。

DPAの`industry standard security`だけで十分とせず、data category、threat、access、encryption、logging、backup、incident response、subprocessor、deletion、assuranceを具体化する。

## PPC報告対象

PPC公式資料で少なくとも次をcurrent確認する。

- 要配慮個人情報を含む
- 財産的被害のおそれ
- 不正目的による行為のおそれ
- 1,000人を超える本人

`漏えい等`には漏えい、滅失、毀損とそのおそれが含まれ得る。ransomware、misconfiguration、wrong recipient、insider、theft等を事実から分類する。

公式:
https://www.ppc.go.jp/personalinfo/legal/leakAction/

## Timing

- 速報: 速やかに。PPC official explanationは概ね3～5日以内の目安を示す。
- 確報: 当該事態を知った日から30日以内。ただし施行規則7条3号の
  「不正の目的をもって行われたおそれがある行為」による類型は60日以内。
- 本人通知: 法令・guidelineに従い速やかに。代替公表の条件を確認する。

施行規則7条1号は、高度な暗号化その他必要な保護措置を講じたdataを除外
する。他の報告類型への該当性は別途確認する。速報の3～5日はguideline上の
目安であり固定法定期限ではない。

clock、起算点、報告先、delegated reporting、報告内容をcurrent official
formで確認する。GDPR 72時間、HIPAA、state breach law、契約noticeを日本の
法定期限と混ぜない。複数regimeならparallel clockを持つ。

## Response state

1. preserve evidence / legal hold
2. contain and investigate
3. data・本人・件数・jurisdiction・riskを確認
4. APPI、My Number、sector、contract、foreign lawの報告matrix
5. regulator report draft
6. individual notice draft
7. approver、send authority、channel
8. correction、lessons、audit

AIはincidentを軽く分類して報告不要と確定せず、deadlineが近い場合はrecoverable errorとしてescalateする。

## 委託

委託先で発生した場合、委託元への通知、PPC報告主体、本人通知、共同調査を確認する。契約noticeを規制当局報告の代替にしない。委託先から委託元への適切な通知で報告扱いとなる条件はcurrent guidelineを確認する。

## My Number・sector

特定個人情報は番号法・PPC専用手続を確認する。金融、医療・介護、電気通信、公共sector等は追加報告・監督当局・短い契約SLAがあり得る。

## 2025-10-01共通様式

PPCはransomware等のcyber incidentについて政府全体の共通様式を利用できる運用を案内している。利用可能性を確認しても、法定報告先・期限を消さない。

## Human gate

報告、本人通知、public statement、customer noticeはdraft。法務、privacy、security、経営、必要な有資格者が承認し、人が送る。
