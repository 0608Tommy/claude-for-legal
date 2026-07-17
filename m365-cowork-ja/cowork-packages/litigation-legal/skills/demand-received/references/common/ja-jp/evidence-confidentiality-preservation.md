> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の証拠、文書提出、秘密性、preservation、証人準備

## No broad US discovery

日本の民事訴訟に一般的なFRCP型discovery、interrogatory、RFA、lawyer-run depositionを
前提にしない。実際のinstrumentを分類する。

| instrumentTypeJP | 主なsource / effect |
|---|---|
| `party-inquiry` | 民訴法163条の当事者照会、法定除外あり |
| `court-commission` | 186条の調査嘱託 |
| `document-production-order` | 220～225条の文書提出命令 |
| `document-transmission-request` | 226条の文書送付嘱託 |
| `pre-action-inquiry` | 132条の2・3のstatutory notice/reply |
| `pre-action-evidence-collection` | 132条の4のseparate order。prior notice/reply、necessity、self-collection difficulty、proportionality、opponent hearing、specified measure、4-month invariable period |
| `formal-evidence-preservation` | 234条の証拠保全 |
| `witness-summons` | current Civil Procedure Rule 106と190～194条のattendance/nonappearance |
| `bar-association-inquiry` | 弁護士法23条の2 |
| `patent-inspection` | 特許法105条の2以下 |
| `execution-information` | 民事執行法上の執行段階手続 |
| `authority-request` | 行政・刑事・sector固有の根拠を特定 |

これらをRule 45 subpoenaと呼ばず、FRCP objection window、geographic limit、
30(b)(6)、motion to quash boilerplateを使わない。

## Document production

民訴法220条は提出義務と除外を定める。221条の申立ては文書の表示、趣旨、所持者、
証明すべき事実、提出義務原因等を特定する。223条のin-camera手続、224条の当事者
不提出・使用妨害、225条の第三者不提出の効果をcurrent textで確認する。

一般的な「関連する全資料」開示義務へ拡張しない。文書category、holder、fact to
prove、legal basis、confidentialityをinstrumentごとに記録する。

CPC 231条の2ではdocumentary-evidence copyの代わりにPDF image等を提出する場合、
231条の3ではnative electronic recordに記録されたinformation自体のevidence
examinationを扱う。231条の3はdocument-production rulesをstatutory substitution
付きで適用する。current court format（PDF/MP4/MP3/JPEG/PNG、media route等）を
確認する。

223条in-cameraはpara. 6の220条4号イ～ニexclusion判断に限定。第三者不提出の
225条effectは20万円以下の過料と即時抗告をcurrent textで確認する。

## Attorney secrecy / withholding

- 弁護士法23条: 職務上知り得た秘密を保持する権利・義務
- 民訴法197条: 職業上の秘密等について証言拒絶
- 民訴法220条4号ハ: 197条関連の黙秘義務が免除されていない事項
- 民訴法220条4号ニ: 専ら所持者利用文書。適用はcase-sensitive
- 特許法105条: 文書提出

民訴法92条はserious private-life secret/trade secretについて第三者のrecord
accessを制限するprocedureで、opponentへのwithholding basisではない。特許法
105条の4はnamed recipientを拘束するtrade-secret orderで、attorney privilege
ではない。

JFTCのconfidential attorney communication determination procedureはqualifying
Antimonopoly Act administrative investigationに限定し、civil litigationへ一般化
しない:
https://www.jftc.go.jp/dk/seido/hanbetsu/hanbetsu.html

これらは一般的なUS attorney-client privilege / FRCP 26(b)(3) work productではない。
in-house counselをCCしただけで保護が生じるとしない。subject-matter waiver、
FRE 502 clawback、fact/opinion work product tierを日本法defaultにしない。

review record:

```yaml
confidentialityClassification: public | internal | confidential | restricted | clean-team
withholdingOrRefusalBasis: "[exact law/order/agreement or null]"
publicRecordAccessBasis: "[basis or null]"
courtConfidentialityOrder: "[order ID or null]"
contractualRestriction: "[basis or null]"
internalDistributionControl: "[control]"
proposedDecision: produce | withhold | redact | seek-direction | unresolved
finalDecision: produce | withhold | redact | seek-direction | unresolved | null
reviewedByQualifiedCounsel: "[object ID or null]"
reviewedAt: "[ISO-8601 or null]"
```

AIは`proposedDecision`だけを設定し、final decisionはqualified counsel review後に
別updateする。

CPC 163 party inquiryとAttorney Act 23-2 bar-association inquiryはcompulsory
Rule 33/45 deviceではない。

内部表示例:

`秘密・社外秘／弁護士確認用 — 表示自体は開示拒絶権を生じさせません`

## Preservation: three separate concepts

1. **Internal preservation instruction**: deletion停止、custody、source integrity、
   collection log等の内部control。
2. **Formal evidence preservation**: 民訴法234条。後に証拠使用が困難となる事情が
   ある場合の裁判所による事前証拠調べ。
3. **Specific legal duty/order**: 文書提出命令、特許inspection、regulator rule、
   contract、foreign proceeding、retention law。

内部noticeの必須表現:

> これはLegalが承認した内部preservation instructionです。

actual basisを特定しない限り「法律が保存を要求する」と書かない。6か月refreshは
configurable internal policyであり、法定intervalではない。

evidence registerはoriginal/copy/electronic、custodian、source system、hash、
collection method、access、auto-delete suspension、translation、chain of custodyを
記録する。民訴法224条をFRCP 37(e) sanctionとして説明しない。

AIはnotice draft、scope proposal、status reportを作れるが、issue、release、
system deletion suspension、device collection、evidence destructionを実行しない。

## Witness / party examination

日本の民事証言は裁判所の証人尋問・当事者尋問であり、米国のout-of-court sworn
depositionではない。民訴法202条の尋問順序は、原則として申出当事者、相手方、
裁判長で、裁判所が変更できる。詳細はcurrent民事訴訟規則とcase directionを確認する。

`deposition-prep` canonical IDは保持するが、日本案件では次へrouteする。

- internal witness interview
- 陳述書support
- 証人尋問outline
- 当事者尋問outline
- remote examination preparation

30(b)(6)相当を発明しない。証人本人の記憶をAIが作らず、witness voiceの完成証言を
代筆しない。質問prompt、document list、矛盾、exact quote/pinpoint、open issueを
整理する。

## Japanese evidence citation

- `甲第1号証3頁`
- `乙第4号証`
- `令和8年7月1日受付`
- `mints通知 [item/version]`
- exact source item/version/hash

日本語原文とtranslationのどちらをreviewしたかを記録する。事実、法的意義、
deadline calculationを別fieldにする。
