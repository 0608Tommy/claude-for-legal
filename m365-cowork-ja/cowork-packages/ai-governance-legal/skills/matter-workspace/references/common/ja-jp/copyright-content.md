> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 著作権・生成コンテンツ・営業秘密

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 1. 開発・学習と生成・利用を分ける

文化庁の「AIと著作権に関する考え方について」は、AI開発・学習段階と生成・利用段階を分けて整理している。著作権法第30条の4等の適用可能性を「AI学習なら常に許諾不要」と一般化しない。目的、享受、既存市場への影響、データ取得方法、技術的制限、生成物の類似性・依拠性等を具体的に確認する。

公式参照:

- 文化庁 AIと著作権: https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html
- 「AIと著作権に関する考え方について」: https://www.bunka.go.jp/seisaku/bunkashingikai/chosakuken/pdf/94037901_01.pdf
- チェックリスト＆ガイダンス（2024-07-31）: https://www.bunka.go.jp/seisaku/chosakuken/pdf/94097701_01.pdf
- 著作権法: https://laws.e-gov.go.jp/law/345AC0000000048

文化庁資料は重要な公式整理だが、法的拘束力のある判決または個別事件の結論として扱わない。

著作権以外の知的財産論点については、内閣府「AI時代の知的財産権検討会
中間とりまとめ」も非拘束的な政策資料として確認する。

- 公式資料一覧: https://www8.cao.go.jp/cstp/ai/ai_guideline/ai_guideline.html
- 検討会資料: https://www.kantei.go.jp/jp/singi/titeki2/ai_kentoukai/

## 2. 開発・fine-tuning確認

- データの出所、ライセンス、robots/technical controls
- 学習目的と、表現の享受を伴う利用の有無
- 特定作家・作品の再現を狙う設計
- 権利者の利益を不当に害する可能性
- 個人情報、秘密情報、契約上利用制限されたデータ
- データ削除、provenance、opt-outへの対応

## 3. 生成・利用確認

- 既存著作物との類似性
- prompt、RAG、fine-tuningからの依拠可能性
- 出典・権利情報の除去
- 公開、販売、広告、社外配布の用途
- 人による検索・比較・修正
- ベンダーのIP indemnityと除外

高価値または公開範囲の広い出力では、類似検索、原資料比較、権利処理を条件にする。

## 4. 営業秘密・契約

著作権だけでなく、不正競争防止法上の営業秘密、秘密保持契約、利用規約、データライセンスを確認する。機密資料を外部モデルへ入力する場合、秘密管理性や契約違反を損なう可能性を検討する。

- 不正競争防止法: https://laws.e-gov.go.jp/law/405AC0000000047

## 5. 出力表現

「著作権侵害なし」「生成物を所有できる」と断定しない。次を分ける。

- ベンダー契約上のoutput allocation
- 日本法上の著作物性・著作者性 `[review]`
- 第三者権利侵害リスク
- 利用目的に必要な追加確認
- indemnityの範囲と除外
