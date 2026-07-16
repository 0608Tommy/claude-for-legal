---
name: policy-monitor
description: >
  privacy policyと実際の運用のずれを確認するSharePoint / Power Platform front end。scope別cursorでreview済みPIA、DPA、triage、DSARを前回acknowledgment以降にsweepするmodeと、提案中の実務を個別比較するmodeを会話で実行する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Privacy policy monitor

旧来の参照label:

- `/privacy-legal:policy-monitor`
- `/privacy-legal:policy-monitor --sweep`
- `/privacy-legal:policy-monitor "[proposed practice]"`

agent、hook、subagent、schedulerを使わない。会話または別途承認されたtenant automationから明示的に開始する。

## 目的

PIAで新data categoryが条件付き承認され、DPAでvendorが追加され、DSARで未記載systemが見つかっても、policy/CMP/labelが更新されなければ表示と実態がずれる。本skillはgapと修正文案をdraftする。外部法改正は`reg-gap-analysis`。

## 必須gate

1. `references/common/cowork-runtime-contract.md`を読む。local crawl/saveへ切り替えない。
2. exact practice profileのpolicy commitments、outputs scope、actual policy`itemId`、commitment surfaces、現在利用者の`user-profile`を読む。
3. server bindingとscopeを確認する。matter sweepはmatter `status: active`だけ。archived/revoked/expiredでは停止する。
4. exact scopeの`policy-sweep-cursor`をstateから読む。global cursorを共有しない。
5. actual policy/noticeとreview済みoutputsをexact item/versionで読む。summaryだけで確定diffを出さない。
6. jurisdictionを`request > matter > practice-profile > tenant-default`で解決する。
7. reportはsource artifactsの最も厳しいconfidentialityを引き継ぐ。
8. REQUIRED/ADVISABLE、suggested language、registry/state changeはhuman review。
9. cursor、policy、registerをresult提示直後に更新しない。acknowledgment後に別updateする。
10. automationは存在・version・connection・last runを確認できる場合だけ表示する。

## Commitment surfaces

- website privacy policy
- CMP / cookie banner
- App Store privacy label
- Google Data Safety
- in-product consent / settings
- GLBA、HIPAA、FERPA、COPPA、telecom等のsector notice
- employee / applicant notice
- subprocessor / transfer notice

日本のCookie・external transmission:
`references/common/jurisdictions/ja-jp/tracking-telecom.md`。

## 会話state

| state | trigger | target |
|---|---|---|
| `sweep` | no description、`--sweep`、前回以降 | SharePoint outputs |
| `direct-query` | proposed practice | exact practice vs surfaces |
| `acknowledge-sweep` | report review済みの明示 | cursor/state only |
| `draft-policy-change` | selected gap | suggested language only |

不明なら`sweep`か`direct-query`を選んでもらう。

## Sweep scope

cursor key:

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordType: policy-sweep-cursor
recordId: "policy-sweep:[scopeType]:[scopeId]:[sourceSystem]:[queryFingerprint]"
sourceSystem: SharePoint
queryFingerprint: "[filters/order hash]"
```

timestamp + itemIdで順序を確定する。cursorなしはfirst sweep。大量なら期間、type、件数を示してbatch化する。

対象:

- PIA: data、purpose、vendor、country、retention、rights、conditions
- DPA review / approved deviation: subprocessor、location、purpose、obligation
- triage: approved/conditional activity、disclosure condition
- DSAR internal log: new data category/system。本人情報をreportへ出さない
- policy / CMP / label update

draft、未review、別matterを確定practiceとして扱わない。

## Gap

- **REQUIRED:** current practiceが明示的commitmentと矛盾、またはmaterial practiceが無記載で表示が実態を誤らせる。
- **ADVISABLE:** conflictはないが重要practiceの説明が不足。
- **UNKNOWN:** source/policy version/technical evidenceが不足。noneへ丸めない。

各gap:

- source exact item/version
- actual practice
- current exact statement
- layer: law / guidance / internal
- gap
- suggested language
- owner、timing、evidence
- affected surface

templateは`references/policy-output.md`。

## Acknowledgment and Update protocol

report提示時はcursorを更新しない。

1. userがreport ID/hashと「reviewした」と明示。
2. exact cursor itemとlatest`eTag`を再取得。
3. old/new cursor、gaps count、scopeを示す。
4. fresh confirmation。
5. unique`idempotencyKey`でconditional update。
6. conflict/partial successでは再読取りし、推測継続しない。
7. auditへ追記。

policy本文更新、CMP変更、label更新はcursor updateと別operation。

## Direct query

proposed practiceからdata、purpose、subjects、vendor、country、retention、automated decision、notice/consent、rightsを抽出する。最も重要なunknownを1つずつ質問する。

| Check | Current surface | Proposed practice | Verdict |
|---|---|---|---|
| Data categories | | | 🟢 / 🟡 / 🔴 / ? |
| Purpose | | | |
| Recipients / vendor use | | | |
| Cross-border | | | |
| Retention | | | |
| Rights | | | |
| Cookie / external send | | | |
| Sector notice | | | |

結論は`POLICY UPDATE REQUIRED / ADVISABLE / NO UPDATE NEEDED / UNKNOWN`のproposal。

## Suggested language

- actual policy voiceを使う
-守れないabsolute promiseを作らない
- durable categoryを優先
- position changeとclarificationを分ける
- section/surfaceを特定
- law requirementとinternal transparency choiceを分ける

## Automation

`references/automation-contract.md`を読む。weekly sweepが必要でも、本skillはscheduleを作成しない。approved Power Automate等がなければon-demandのみ。

## Save

report初稿はOneDrive。review済みreportのoutputs昇格、cursor acknowledgment、policy edit/publicationは別確認。

## 完了

REQUIRED/ADVISABLE/UNKNOWN件数、coverage、missing sources、next decisionを示す。policy draft、technical check、owner escalation、next sweepから人に選んでもらう。
