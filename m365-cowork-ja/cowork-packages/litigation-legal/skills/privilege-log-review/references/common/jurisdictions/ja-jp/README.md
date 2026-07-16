> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の訴訟・紛争法務router

checked through: `2026-07-16 JST`
legal review: `pending`

法域は`request > matter > practice-profile > tenant-default`で解決する。日本が
含まれる場合、US defaultを無効化し、必要なmoduleを読む。

- [民事手続・digitalization](civil-procedure-and-digital.md)
- [証拠・秘密性・preservation](evidence-confidentiality-preservation.md)
- [催告・時効・和解](demands-limitation-settlement.md)
- [特許・民事claim chart](patent-and-claim-charts.md)
- [一次資料台帳](source-register.md)
- [currency watch](currency-watch.md)

## False-equivalence blocker

| US concept | 日本での扱い |
|---|---|
| Rule 45 subpoena | 実際の照会、嘱託、文書提出命令、証人呼出し、当局要請を分類 |
| deposition / 30(b)(6) | 裁判所の証人・当事者尋問、内部interview、陳述書準備 |
| FRCP discovery | 一般的な広範discoveryなし。個別の法定証拠手段 |
| legal hold / Rule 37(e) | 内部preservation control + 具体的な日本法・命令・外国法basis |
| attorney-client privilege | 弁護士法23条、民訴法197条・220条等の限定的保護 |
| work product | 一般的なFRCP 26(b)(3)相当なし。自己利用文書はcase-sensitive |
| FRE 408 / without prejudice | labelだけで自動的な証拠排除・秘密性なし |
| Rule 11 | 民訴法2条等を「日本版Rule 11」と呼ばない |
| TRO / preliminary injunction | 民事保全法の仮差押え・仮処分を独自要件で分析 |
| Markman | 特許侵害訴訟内の争点整理・解釈。独立Markman手続なし |
| PACER/CourtListener docket | mints、裁判所文書、OC、手動記録確認。公開裁判例は選択掲載 |
| 21-day answer | 裁判所が指定した答弁期限 |
| dismissal with prejudice | 取下げ、請求放棄・認諾、判決、確定、異議・控訴等を実際に記録 |

foreign proceedingが実際に関係する場合だけ、そのforeign ruleを別branchで使う。
日本法と混ぜず、governing forum、service、protective order、production obligationを
明示する。

## Qualified counsel gate

source mapping、事件固有の手続、期限、秘密性、提出拒絶、特許均等論、時効、
仮差押え・仮処分、執行、労働審判は日本法有資格者が確認するまで`pending`。
AIはlawyer verification fieldを自分で埋めない。
