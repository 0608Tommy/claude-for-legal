> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — ベンダー契約・AIセキュリティ

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 1. 契約スタック

AIサービスを1社の契約だけで評価しない。

1. エンドユーザー向けSaaS
2. API gateway / orchestration
3. cloud AI service
4. model provider
5. RAG、vector database、外部データ
6. logging、評価、fine-tuning等のsubprocessor

各層について、入力・出力の学習利用、保持、処理場所、秘密保持、セキュリティ、モデル変更、知財、責任、インシデント、終了時削除を確認する。上位ベンダーの約束が下位にflow-downされているか、顧客が執行できるかを確認する。

## 2. 日本向け契約チェック

| 項目 | 最低確認 |
|---|---|
| データ利用 | 学習、改善、評価、人による閲覧、opt-out、設定証跡 |
| 秘密保持 | prompt、RAG、output、ログ、上流提供者 |
| 個人情報 | 委託・第三者提供等の整理、国外、subprocessor、事故対応 |
| セキュリティ | 認証、権限、暗号化、ログ、脆弱性、prompt injection、red teaming |
| モデル変更 | 事前通知、version pinning、重大変更後の再評価 |
| 知財 | output allocation、第三者請求、indemnity、除外 |
| 責任 | AI固有損害、データ損失、上流免責、責任上限 |
| インシデント | 定義、通知期限、調査協力、証拠保全、再発防止 |
| 監査 | 第三者報告、テスト結果、規制対応資料、監査権 |
| 終了 | データ返却・削除、backup、モデルへの残存、移行支援 |

## 3. 公式セキュリティ資料

- AI事業者ガイドライン第1.2版:
  https://www.soumu.go.jp/main_content/001064279.pdf
- 総務省「AIのセキュリティ確保のための技術的対策に係るガイドライン」公表ページ:
  https://www.soumu.go.jp/menu_news/s-news/01cyber01_02000001_00282.html
- 本文PDF（2026-03-27）:
  https://www.soumu.go.jp/main_content/001064122.pdf
- AIセーフティ評価観点ガイドv1.20（2026-07-07）:
  https://aisi.go.jp/output/output_information/260707/
- 国家サイバー統括室・政府統一基準改定:
  https://www.cyber.go.jp/pdf/policy/general/rev_pointr8_6.pdf

これらのガイドラインは、それ自体として一律の法定最低基準ではない。
契約、調達条件または個別業法に組み込まれる場合を除き、非拘束的な技術
参照資料として扱う。AISIはIPA内に設置されたAI安全性評価機関であり、
独立規制当局ではない。実装、設定、脅威モデル、テスト結果を別途確認する。

契約・個別法の適用可能性:

- METI「AIの利用・開発に関する契約チェックリスト」:
  https://www.meti.go.jp/press/2024/02/20250218003/20250218003.html
- サイバーセキュリティ基本法: https://laws.e-gov.go.jp/law/426AC1000000104
- 経済安全保障推進法: https://laws.e-gov.go.jp/law/504AC0000000043
- 重要電子計算機に対する不正行為による被害の防止に関する法律:
  https://laws.e-gov.go.jp/law/507AC0000000042

これらは条件付きの適用確認であり、全AIベンダーに一律に課される義務では
ない。

## 4. セキュリティAIA追加項目

- prompt injectionとretrieved-content injection
- model extraction、data exfiltration、membership inference
- excessive agency、tool misuse、権限昇格
- unsafe output handling
- poisoning、RAG source改ざん
- denial of service、resource exhaustion
- secrets in prompts/logs
- 監視、kill switch、rollback、incident playbook

## 5. 失敗ゲート

上流モデル、保存場所、学習利用、subprocessor、重大インシデント通知のいずれかが不明で、ElevatedまたはHigh用途なら契約承認を推奨しない。必要な資料と修正文案を提示し、人の判断へ回す。
