> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 本人請求 / DSAR相当

**状態:** DRAFT — qualified Japanese counsel review pending

日本の権利はGDPR/CCPAの`DSAR`と完全に同じではない。APPIの`保有個人データ`と第三者提供recordを基礎に、請求種類、要件、例外、手続をcurrent lawで確認する。

## 権利category

- 利用目的の通知
- 保有個人データの開示
- 第三者提供記録の開示
- 内容の訂正、追加、削除
- 利用停止、消去
- 第三者提供の停止

各権利は同じ要件ではない。訂正等（法34条）は内容が事実でない場合。
利用停止・消去（法35条1項）は法18条・19条違反の取扱いまたは法20条違反
取得。第三者提供停止（同条3項）は法27条1項または28条違反。追加的請求
事由（同条5項）は、利用する必要がなくなった場合、法26条1項の報告対象
事態が生じた場合、または本人の権利・正当な利益が害されるおそれがある
場合である。

## Deadline

PPC FAQは開示を`遅滞なく`行うとし、検索・集約に通常必要な期間を考慮した合理的期間を認める。民間APPIにGDPRの1か月、CCPAの45日を自動適用しない。

公式:
https://www.ppc.go.jp/all_faq_index/faq1-q9-12/

internal SLAが法令より短ければinternal SLAを使うが、法定deadlineと書かない。EU/UK、California、他州、sectoral lawが並行適用される場合は別clockを持ち、最短のapplicable deadlineを管理する。

## Workflow

1. receipt date、channel、request text、requested rightを保存する。
2. data subject、authorized representative、法域、entity/roleを確認する。
3. riskに比例して本人確認する。新たな過剰dataを集めない。
4. request scope、identifier、date range、systems listを整理する。
5. exact systemごとにquery結果、not found、unavailableを記録する。
6. third-party data、privilege、trade secret、security、法令保持、legal hold等の制限候補を列挙する。
7. refusal、partial response、redaction、delivery methodを有資格者がreviewする。
8. outward-facing letterと内部分析を分ける。
9. human send approval後だけ送信する。
10. response、production、訂正・停止・削除の実行結果をauditする。

## 本人確認

logged-in session、登録email、challenge、代理権資料等をriskに合わせる。My Number card等を本人確認に使う場合でも、不要な個人番号を収集・保存しない。ID copyのretention、masking、accessを確認する。

## 探索

practice profileのsystems listをfloorとし、production、analytics、support、CRM、marketing、logs、backups、email、collaboration、vendor、paper recordを案件に応じて確認する。

`processor`と呼ばれる事業者がrequestを受けた場合、契約上controllerへ転送すべきか、APPI上誰が保有個人データを持つかを別々に確認する。

## 例外・拒否

blanket exemptionを作らない。各非開示・非対応についてcurrent条文、事実、範囲、代替、本人への理由説明を確認する。訴訟holdや法定保持は全dataの無期限保持を正当化しない。

候補は`proposed — qualified review required`とし、AIが最終的に削除・開示対象を決めない。

## 2通のdraft

移行元のhouse processとして、prompt acknowledgment draftとsubstantive response draftを作れる。ただし日本法一般が常に2通を法定しているとは書かない。

- acknowledgment: receipt、理解したscope、identity gap、target date、contact
- substantive: data / action、withheld scopeと理由、delivery、問い合わせ・complaint route

本人向けdraftに内部work-product header、内部risk、他人のdata、未承認exemption strategyを含めない。

## Log

`requestId`を使い、本人氏名をfilenameやrecord IDに入れない。received、verified、applicable regimes、deadline、systems、decisions、approver、sent date、action completionを記録する。AIはsend、delete、correct、stop processingを自動実行しない。
