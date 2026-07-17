> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本法公式情報源台帳

**Checked:** `2026-07-16 JST`

**Review:** `qualified Japanese counsel review pending`

URLを記録しただけでpropositionがverifiedになるわけではありません。taskごとに
actual text、supplementary provision、effective date、form、fee、FAQ version、
official recordを読みます。

## Core Acts

| ID | Source | Class / status | 主な用途 |
|---|---|---|---|
| `JP-PATENT` | 特許法 https://laws.e-gov.go.jp/law/334AC0000000121 | `[B]`, current | Arts. 2, 29, 29-2, 30, 32, 35, 36, 39, 64, 65, 68, 70, 98, 99, 101, 103, 104-3 |
| `JP-UTILITY` | 実用新案法 https://laws.e-gov.go.jp/law/334AC0000000123 | `[B]`, current | utility model、technical opinion、term/fee |
| `JP-TM` | 商標法 https://laws.e-gov.go.jp/law/334AC0000000127 | `[B]`, current | Arts. 3, 4, 8, 19–20, 25–26, 32, 37, 50, 53 |
| `JP-DESIGN` | 意匠法 https://laws.e-gov.go.jp/law/334AC0000000125 | `[B]`, current | Arts. 10, 15, 24、GUI/building/interior、related design |
| `JP-COPYRIGHT` | 著作権法 https://laws.e-gov.go.jp/law/345AC0000000048 | `[B]`, current | Arts. 15, 27, 28, 67-3、ownership、moral rights、exceptions |
| `JP-UCPA` | 不正競争防止法 https://laws.e-gov.go.jp/law/405AC0000000047 | `[B]`, current | well-known/famous indication、product configuration、trade secret、false facts |
| `JP-PLATFORM` | 情報流通プラットフォーム対処法 https://laws.e-gov.go.jp/law/413AC0000000137 | `[B]`, current | provider liability、deletion safe harbor、large-platform complaint duties |
| `JP-CUSTOMS` | 関税法 https://laws.e-gov.go.jp/law/329AC0000000061 | `[B]`, current | Art. 69-11、import suspension、identification |
| `JP-CIVIL` | 民法 https://laws.e-gov.go.jp/law/129AC0000000089 | `[B]`, current | assignment、contract、damages、Art. 150 demand effect |
| `JP-CCP` | 民事訴訟法 https://laws.e-gov.go.jp/law/408AC0000000109 | `[B]`, current | evidence、production、digital procedure |
| `JP-ATTORNEY` | 弁護士法 https://laws.e-gov.go.jp/law/324AC1000000205 | `[B]`, current | Arts. 23, 25 |
| `JP-PATENT-ATTORNEY` | 弁理士法 https://laws.e-gov.go.jp/law/412AC0000000049 | `[B]`, current | Art. 30、scope/confidentiality |
| `JP-ECON-SEC` | 経済安全保障推進法 https://laws.e-gov.go.jp/law/504AC0000000043 | `[B]`, current | patent non-disclosure regime |
| `JP-AMA` | 独占禁止法 https://laws.e-gov.go.jp/law/322AC0000000054 | `[B]`, current | IP licensing/competition |

## JPO search、examination、procedure

| ID | Source | Class / status | 主な用途 |
|---|---|---|---|
| `JP-JPLATPAT` | J-PlatPat https://www.j-platpat.inpit.go.jp/web/all/top/BTmTopEnglishPage | `[G] official system` | patent、utility model、design、trademark record/search |
| `JP-PATENT-G` | Patent/Utility Model Examination Guidelines https://www.jpo.go.jp/system/laws/rule/guideline/patent/tukujitu_kijun/index.html | `[G]`, 2026-07-01 revisionを確認 | novelty、inventive step、eligibility、disclosure |
| `JP-PATENT-HB` | Examination Handbook https://www.jpo.go.jp/e/system/laws/rule/guideline/patent/handbook_shinsa/index.html | `[G]` | detailed examination practice |
| `JP-PATENT-HB-2026` | 2026 Handbook revision https://www.jpo.go.jp/system/laws/rule/guideline/patent/handbook_shinsa/kaitei/202606.html | `[G]`, 2026-07-01 | current Japanese versionを優先 |
| `JP-SOFTWARE` | Software chapter https://www.jpo.go.jp/e/system/laws/rule/guideline/patent/handbook_shinsa/document/index/app_b1_e.pdf | `[G]` | software/AI eligibility |
| `JP-AI-EXAMPLES` | AI examination examples https://www.jpo.go.jp/e/system/laws/rule/guideline/patent/ai_jirei_e.html | `[G]`, updated 2024-03 | AI claim examples |
| `JP-ART30` | Article 30 procedure https://www.jpo.go.jp/e/system/laws/rule/other/patent/hatumei_reigai.html | `[G] official procedure` | one-year exception、filing statement、30-day evidence |
| `JP-EMP-INVENT` | Employee-invention guideline https://www.jpo.go.jp/system/patent/shutugan/shokumu/shokumu_guideline.html | `[G]`, 2016-04-22 | Patent Act Art. 35 process/benefit |
| `JP-PATENT-SEC` | Cabinet Office patent regime https://www.cao.go.jp/keizai_anzen_hosho/suishinhou/patent/patent.html | `[G]`, from 2024-05-01 | sensitive invention screen、foreign filing |
| `JP-TM-G` | Trademark Examination Guidelines https://www.jpo.go.jp/e/system/laws/rule/guideline/trademark/kijun/index.html | `[G]`, effective 2026-04-01 | registrability/confusion |
| `JP-TM-G17` | Trademark Guidelines Revised 17th Edition https://www.jpo.go.jp/system/laws/rule/guideline/trademark/kijun-kaitei/17th_kaitei_2026.html | `[G]`, 2026-04-01 | current edition |
| `JP-DESIGN-G` | Design Examination Guidelines https://www.jpo.go.jp/system/laws/rule/guideline/design/shinsa_kijun/index.html | `[G]` | registrability/similarity |
| `JP-TM-SIMCODE` | Similar-group codes https://www.jpo.go.jp/e/system/trademark/gaiyo/bunrui/kokusai/ruijigun_cord_reidai.html | `[G]` | 類似群コード |
| `JP-TM-SIMGS` | Similar goods/services https://www.jpo.go.jp/e/system/laws/rule/guideline/trademark/ruiji-kijun/index.html | `[G]` | goods/services similarity |
| `JP-NICE` | Nice 13-2026 https://www.jpo.go.jp/system/laws/rule/guideline/trademark/kokusai_bunrui/kokusai_bunrui_13-2026.html | `[G]`, effective 2026-01-01 | class mapping |
| `JP-JPO-FEES` | JPO fee table https://www.jpo.go.jp/e/system/process/tesuryo/hyou.html | `[G] official procedure`, live | fee verification |
| `JP-JPO-XFER` | Transfer procedure https://www.jpo.go.jp/system/process/toroku/iten/index.html | `[G] official procedure` | title/recordal |
| `JP-JPO-ONLINE` | online dispatch revision https://www.jpo.go.jp/system/laws/sesaku/tetsuzuki/online-hasso_minaoshi.html | `[G]`, effective 2026-04-01 | deemed delivery/response clock |
| `JP-JPO-RESTORE` | restoration guidance https://www.jpo.go.jp/system/laws/rule/guideline/kyusai_method2.html | `[G]`, in force from 2023-04-01 | not-intentional standard、procedure-specific |

## Principal cases

| ID | Source | Class | Proposition to verify |
|---|---|---|---|
| `JP-HYOZAN` | Supreme Court, 1968-02-27 https://www.courts.go.jp/assets/hanrei/hanrei-pdf-53940.pdf | `[C]` | appearance、sound、concept、trading circumstances |
| `JP-BALL-SPLINE` | Supreme Court, 1998-02-24 https://www.courts.go.jp/assets/hanrei/hanrei-pdf-52790.pdf | `[C]` | doctrine of equivalents five requirements |
| `JP-MAXACALCITROL` | Supreme Court, 2017-03-24 https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86634.pdf | `[C]` | intentional exclusion / filing-time alternative |
| `JP-ESASHI` | Supreme Court, 2001-06-28 https://www.courts.go.jp/assets/hanrei/hanrei-pdf-52267.pdf | `[C]` | copyright expression and direct perceptibility |

anchor caseだけでcurrent citator reviewを完了したと表示しません。

## Copyright、platform、OSS

| ID | Source | Class / status | 主な用途 |
|---|---|---|---|
| `JP-MIC-PLATFORM` | MIC rights-infringement material https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/ihoyugai.html | `[G]` | provider route、ministerial period |
| `JP-UNMANAGED` | Agency for Cultural Affairs unmanaged works https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/chosakukensha_fumei/tyosakubutsu/index.html | `[G]`, effective 2026-04-01 | Art. 67-3 ruling |
| `JP-COPY-2026` | 2026 amendment https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/r08_hokaisei/ | `[F]`, enacted 2026-06-17 / Act No. 48 promulgated 2026-06-24 | secondary remuneration、3年以内の政令施行待ち |
| `JP-COPY-2026-TEXT` | Act No. 48 text https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/r08_hokaisei/pdf/94407301_02.pdf | `[F]` | enacted text |
| `JP-COPY-REG` | Copyright registration https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/toroku_seido/ | `[G] official procedure` | transfer/perfection |
| `JP-IPA-OSS` | IPA OSS governance library https://www.ipa.go.jp/digital/kaihatsu/oss/library.html | `[G]`, updated 2026-05-13 | governance only、license text controls |

## Trade secret、transactions、competition

| ID | Source | Class / status | 主な用途 |
|---|---|---|---|
| `JP-TS-G` | METI Trade Secret Management Guidelines https://www.meti.go.jp/policy/economy/chizai/chiteki/guideline/r7ts.pdf | `[G]`, revised 2025-03-31 | secrecy management |
| `JP-JFTC-IP` | JFTC IP/know-how/data transaction guideline https://www.jftc.go.jp/houdou/pressrelease/2026/jun/260624_chizaitorihiki.html and https://www.jftc.go.jp/dk/guideline/unyoukijun/chizaitorihiki.pdf | `[G]`, published 2026-06-24 | transaction fairness。separate IP-licensing antitrust guidanceを置換しない |
| `JP-JFTC-AMA-IP` | JFTC IP/Antimonopoly guidance https://www.jftc.go.jp/en/legislation_gls/imonopoly_guidelines.html | `[G]` | licensing restrictions |

## Customs、court procedure

| ID | Source | Class / status | 主な用途 |
|---|---|---|---|
| `JP-CUSTOMS-OV` | Japan Customs overview https://www.customs.go.jp/english/c-answer_e/kinseihin/2002_e.htm | `[G]` | prohibited imports |
| `JP-CUSTOMS-ID` | Verification procedure https://www.customs.go.jp/mizugiwa/chiteki/pages/c_001_e.htm | `[G]` | evidence/procedure |
| `JP-CUSTOMS-PORTAL` | Import suspension https://www.customs.go.jp/english/c-answer_e/kinseihin/2003_e.htm | `[G]` | application route |
| `JP-MINTS` | Civil digitalization https://www.courts.go.jp/saiban/minjidejitaruka/index.html | `[G]`, principally actions commenced from 2026-05-21 | online procedure; excluded proceeding types確認 |
| `JP-MINTS-OV` | Civil procedure overview https://www.courts.go.jp/saiban/minjidejitaruka/minso_gaiyou/index.html | `[G]` | electronic service/evidence |

## Principal JPO fee snapshot

**Snapshot checked:** `2026-07-16` against `JP-JPO-FEES`。
**Runtime rule:** feeはrelease/payment前に再取得し、人が確認します。

| Action | Snapshot |
|---|---:|
| Patent application | ¥14,000 |
| Patent examination request | ¥138,000 + ¥4,000/claim |
| Patent years 1–3, each | ¥4,300 + ¥300/claim |
| Patent years 4–6, each | ¥10,300 + ¥800/claim |
| Patent years 7–9, each | ¥24,800 + ¥1,900/claim |
| Patent years 10–25, each | ¥59,400 + ¥4,600/claim |
| Design application | ¥16,000 |
| Design years 1–3, each | ¥8,500 |
| Design years 4–25, each | ¥16,900 |
| Trademark application | ¥3,400 + ¥8,600/class |
| Trademark registration, 10 years | ¥32,900/class |
| Trademark registration, 5-year installment | ¥17,200/class |
| Trademark renewal, 10 years | ¥43,600/class |
| Trademark renewal installment | ¥22,800/class |
| Utility-model application | ¥14,000 |
| Utility-model technical opinion | ¥42,000 + ¥1,000/claim |
| Utility-model years 1–3, each | ¥2,100 + ¥100/claim |
| Utility-model years 4–6, each | ¥6,100 + ¥300/claim |
| Utility-model years 7–10, each | ¥18,100 + ¥900/claim |

## 使用rule

- official URL取得失敗、403、version不明なら取得済みと表示しない。
- e-Gov consolidated textとsupplementary provisionでeffective dateを確認する。
- JPO official record、WIPO route、actual noticeがgeneric tableより優先。
- case anchorをcurrent citator reviewの代替にしない。
- [F]をcurrent obligationへ適用しない。
- source statusをauditし、qualified Japanese counsel reviewは`pending`のまま。
