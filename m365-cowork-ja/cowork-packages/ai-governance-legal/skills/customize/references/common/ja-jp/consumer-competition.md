> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 消費者・表示・競争

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 1. 消費者向けAI

チャットボット、推薦、価格・優先順位、広告生成、レビュー要約、合成人物、AIエージェントが消費者に接する場合、少なくとも次を確認する。

- AIであること、またはAI生成・AI支援であることを説明すべき場面
- 商品・サービスの品質、効果、価格、根拠について誤認を生じさせないか
- 広告・推薦・レビューの主体と利害関係が明確か
- 重要条件、限界、human supportへの移行を隠していないか
- vulnerable users、未成年者、高齢者への設計
- 誤案内、架空の根拠、差別的な価格・推薦の救済

公式参照:

- 景品表示法の概要: https://www.caa.go.jp/policies/policy/representation/fair_labeling/
- 景品表示法: https://laws.e-gov.go.jp/law/337AC0000000134
- 消費者契約法: https://laws.e-gov.go.jp/law/412AC0000000061
- AI技術と消費者問題の専門調査会: https://www.cao.go.jp/consumer/kabusoshiki/ai_technology/index.html

専門調査会資料は審議中・非拘束である。次の政府委託調査は二次資料であり、
外国法そのものとして引用しない。

- 生成AI関連規制の調査報告書: https://www.caa.go.jp/policies/future/national_research/assets/caa_futurer101_250605_01.pdf

## 2. 表示・説明

AIが作った表示でも、事業者の表示として扱われ得る。出力をそのまま公開せず、事実根拠、比較条件、注記、典型的結果、画像・推薦の真正性を人が確認する。

2026年7月16日時点で、AI利用またはAI生成であることを全場面で一律に
表示させる一般法上の義務は確認できない。表示主体、広告性、誤認可能性、
個別法を確認し、それ以外は本モジュールの透明性条件として扱う。

- ステルスマーケティング告示: https://www.caa.go.jp/notice/entry/032672/
- 消費者庁FAQ: https://www.caa.go.jp/policies/policy/representation/fair_labeling/faq/stealth_marketing/

次は🔴または🟠の候補:

- 存在しない認証、性能試験、利用者レビュー
- 根拠のない「最高」「安全」「正確」「公平」
- AI生成の人物・体験談を実在の顧客と誤認させる
- 広告であることを隠した推薦
- 重要な制約を小さく表示し、会話本文で断定する

## 3. 競争・プラットフォーム

生成AI市場、上流モデル、クラウド、データ、流通、排他的条件、bundling、switching cost、ベンダーロックインを確認する。公正取引委員会の公式調査は市場構造の情報源であり、個別契約の違法性を自動判定するものではない。

- 公正取引委員会「生成AIに関する実態調査報告書ver.2.0」公式ページ: https://www.jftc.go.jp/houdou/pressrelease/2026/apr/260416_generativeai.html
- 私的独占の禁止及び公正取引の確保等に関する法律: https://laws.e-gov.go.jp/law/322AC0000000054

プラットフォームまたは取引agentとして使う場合、適用可能性を確認する。

- 情報流通プラットフォーム対処法: https://laws.e-gov.go.jp/law/413AC0000000137
- デジタルプラットフォーム取引透明化法: https://laws.e-gov.go.jp/law/502AC0000000038
- スマホソフトウェア競争促進法: https://laws.e-gov.go.jp/law/506AC0000000058
- 電子消費者契約法: https://laws.e-gov.go.jp/law/413AC0000000095/
- 特定商取引法: https://laws.e-gov.go.jp/law/351AC0000000057

2026年7月13日に国会で成立し、7月14日に公布が閣議決定された選挙AI画像
等に関する法案は、2026年7月16日時点で法律番号・公布情報を確認中で、
主要部分は2027年3月1日施行予定である。現在の一般的表示義務として
適用せず、`成立・公布情報確認中・将来施行` として追跡する。

- 法案要綱: https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/honbun/youkou/g22105026.htm
- 審議経過: https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE2AAA.htm
- 公布の閣議決定: https://www.kantei.go.jp/jp/kakugi/2026/kakugi-2026071401.html

## 4. AIA・契約への追加条件

- 消費者向け文言と法務向け説明を分ける。
- hallucination時に人へ切り替える導線を設ける。
- 誤りの訂正、返金、苦情、アカウント影響の救済を明示する。
- vendor changeで表示・推薦ロジックが変わる場合、再評価する。
- マーケティング、法務、プロダクト、カスタマーサポートの責任者を指定する。

## 5. 未確定事項

審議会資料、調査報告、政策提言を現行の法的義務として引用しない。最新の措置命令、確約手続、ガイドライン、法改正に依存する結論は、消費者庁・公正取引委員会の公式原文をその会話で再確認する。
