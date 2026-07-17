> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 行政・公共部門・政府調達

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 1. 公式ガイドライン

デジタル庁は2026年6月12日、「行政の進化と革新のための生成AIの調達・利活用に係るガイドライン（第2.0版）」を公表した。行政機関の利用では、民間一般向けガイドラインだけでなく、この公式資料、各府省の規程、政府情報システムのセキュリティ要件、文書管理、情報公開、調達条件を確認する。

- 公表ページ: https://www.digital.go.jp/news/decb64eb-f26e-41cb-8d37-f3dd173108b8
- 本文PDF: https://www.digital.go.jp/assets/contents/node/information/field_ref_resources/decb64eb-f26e-41cb-8d37-f3dd173108b8/59054b35/20260612_resources_standard_guidelines_guideline_01.pdf
- 概要PDF: https://www.digital.go.jp/assets/contents/node/information/field_ref_resources/decb64eb-f26e-41cb-8d37-f3dd173108b8/f8e1c3b8/20260612_resources_standard_guidelines_guideline_03.pdf

第2.0版は主として政府・各府省庁の調達・利活用ルールであり、地方公共
団体、独立行政法人、公共受託者等へ当然に直接適用されるものとして扱わない。

地方公共団体については、総務省の第4版（2025-12-16）を別に確認する。

- 公表ページ: https://www.soumu.go.jp/menu_news/s-news/01gyosei04_02000155.html
- 第4版PDF: https://www.soumu.go.jp/main_content/000820109.pdf

公文書・情報公開・個人情報の具体的な法的基礎:

- 公文書等の管理に関する法律: https://laws.e-gov.go.jp/law/421AC0000000066
- 行政機関の保有する情報の公開に関する法律: https://laws.e-gov.go.jp/law/411AC0000000042
- 個人情報保護法: https://laws.e-gov.go.jp/law/415AC0000000057

## 2. 公共部門の追加確認

- 対象業務と法的権限
- 国民の権利・義務への影響
- 裁量判断をAIへ委ねていないか
- 人による最終判断、理由提示、異議申立て
- 公文書としてのprompt、output、ログ、意思決定記録
- 情報公開、個人情報、秘密情報、特定秘密等の区分
- 調達時のデータ、モデル、subprocessor、ロックイン
- ベンダー終了時の可搬性、データ返却、継続性
- セキュリティ、監査、事故報告
- アクセシビリティと代替経路

## 3. 調達条件

ベンダーAIレビューには、一般契約項目に加え次を含める。

- 政府・組織固有データを学習に利用しない明示
- 保管・処理場所と再委託
- 公文書・監査ログの保持と取得
- モデル・安全仕様の重大変更通知
- 事故時の即時連絡、証拠保全、当局協力
- 終了・移行支援とvendor lock-in緩和
- アクセシビリティ、説明、human fallback
- 適用される政府標準との適合証跡

## 4. 不可逆判断

給付、許認可、制裁、採用、評価、捜査、教育等の重大な行政判断をAIだけで確定しない。個別法上の根拠、裁量、人による審査、理由提示、救済を有資格者が確認するまで本番承認を停止する。

これは本モジュールの内部停止条件であり、日本法上の全行政判断に共通する
一律の法定禁止を意味しない。個別法、各府省規程、調達条件を特定する。
