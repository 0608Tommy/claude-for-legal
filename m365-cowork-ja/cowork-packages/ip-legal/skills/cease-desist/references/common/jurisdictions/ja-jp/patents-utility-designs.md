> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本特許・実用新案・意匠

## P0 — patent non-disclosure

未公開technical contentをexternal search tool、foreign associate、overseas filing
service、non-isolated AIへ送る前に、2024-05-01運用開始の経済安全保障推進法上の
特許非公開制度をscreenします。未公開かつ日本国内でされた発明のうち
Economic Security Promotion Act Art. 66(1)の対象可能性、Art. 79 clearance、
specified field（2025-01-01 IPC adjustmentを含む）、Japanese filing、foreign filing、
disclosure/implementation/withdrawal restrictionをcurrent Cabinet Office sourceで
確認します。すべての日本発明にblanket first-filing dutyがあるとは書かず、
不明なら送信しません。

## Patentability / invention intake

- **[B]** Patent Act Arts. 2, 29, 29-2, 30, 32, 36, 39。
- software/AIは発明全体が「自然法則を利用した技術的思想の創作」かをJPO guidanceで
  評価。`Alice/Mayo`を使いません。
- Art. 30はqualifying involuntary disclosure（para. 1）とapplicant-caused
  disclosure（para. 2）を分ける。出願と同時の適用書面・30日以内evidenceは
  para. 2 routeで確認する。foreign rightを回復せず、intervening independent
  prior artを消しません。
- conception、disclosure、priority、filingを別dateとして記録。
- inventorはcurrent position上natural person。human contributionを記録。

## Employee inventions — Patent Act Article 35

- human contributor全員、employer/contractor status、invention timeのruleを確認。
- pre-existing agreement/work ruleによりemployee inventionが原始的にemployerへ
  帰属し得る。
- employeeにはreasonable monetary or other economic benefitへの権利。
- consultation、disclosure、opportunity to commentがreasonablenessに影響。
- contractorにはassignmentが必要。Art. 35をgeneric work-for-hireにしない。

## FTO / infringement

1. J-PlatPatでgranted patent、utility model、published application、designを検索。
2. Japanese claim、family、priority、prosecution、correction、opposition/
   invalidation、annuity、term extensionを記録。
3. Patent Act Art. 64の18-month publication blind spotを明示。
4. Arts. 2/68のterritorial acts:
   manufacture、use、assignment/sale、offer、export/import、program transmission。
5. Art. 70でclaims、specification、drawingsを用い、abstractでscopeを決めない。
6. literal scope後に**[C]** *Ball Spline* five requirements。
7. **[C]** *Maxacalcitrol*: filing時に容易想到のalternativeをclaimしなかった
   だけではintentional exclusionとしない。ただしapplicantがalternativeを認識し、
   意図的にclaimから除外したことを客観的・外形的に示した場合は別途検討する。
8. Art. 101のJapanese indirect-infringement categoryを適用。
9. prior use、experiment/research limitation、license、exhaustion、Art. 104-3、
   utility-model technical opinion/enforcement requirementsを確認。
10. importならCustoms branch。

Japanには35 U.S.C. §284 treble-damages regimeがありません。Patent Act Art. 103の
negligence presumptionと、injunction/damages/evidenceを別に扱います。FTO memoを
読んだだけでJapanese treble damagesになるとは警告しません。

## Design

- registration、application/drawings、claimed/unclaimed portion、filing cohort。
- Art. 24のconsumer aesthetic impressionによるsimilarity。
- product、GUI、building、interior、related design、secret design。
- current-law applicationはterm 25 years from filing、annual registration fee。
  older cohortのtransitionを確認。
- related designはcurrent Art. 10の10-year windowをactual basic-design filing dateで
  確認。
- UCPA product configurationをparallel trackとして分離。

`D` number、*Egyptian Goddess*、point-of-novelty、35 U.S.C. §289を日本意匠へ
使いません。

## Claim chart

| Claim element | Product/process mapping | Evidence | Read |
|---|---|---|---|
| exact Japanese claim text | yes / no / possible / construction-dependent | source item/page/version | literal |

全elementを扱い、construction-dependent termを隠しません。equivalents、indirect
infringement、validityは別欄とし、弁理士・弁護士が判断します。

## Portfolio timing floor

- examination request: filingから3年。
- publication: 原則18か月。
- first three patent fees: grant decision service後30日以内にまとめて支払う。
- later annuities: preceding patent year中。6-month late-payment path/surchargeを
  official recordで確認。
- term: 原則filingから20年、delay/regulatory extensionあり。
- opposition: patent gazette publicationから6か月。
- utility model: separate 10-year/annual-fee rules。
- utility-model application ¥14,000、technical opinion ¥42,000 + ¥1,000/claim、
  years 1–3各¥2,100 + ¥100/claim（filing時3年分）、years 4–6各¥6,100 +
  ¥300/claim、years 7–10各¥18,100 + ¥900/claimをruntime再確認。
- design first-year fee: registration decision service後30日以内。

actual office notice、filing cohort、holiday、restoration、representative、
official docketがgeneric tableより優先します。

2026-04-01以降、指定online dispatchは未開封でも法定10日経過でdeemed delivery
となり得てpaper fallbackが廃止されたrouteがあるため、electronic notice statusと
service dateを確認します。2023-04-01以降の一定period restorationは
`not intentional` standardをprocedure別に確認し、自動回復と表示しません。
