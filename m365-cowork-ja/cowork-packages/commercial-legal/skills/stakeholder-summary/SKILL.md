---
name: stakeholder-summary
description: >
  完了した契約reviewを、procurement、budget owner、finance、security、executive向けの短いbusiness summaryへ変換する。署名可否の法的memoではなく、何の契約か、驚く点、必要action、承認状況を平易に伝えたい場合に使用する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Stakeholder summary

旧来の参照labelは`/commercial-legal:stakeholder-summary`。元契約を再reviewせず、完成したreview memoをbusiness languageへ圧縮する。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。local outputを作らない。
2. **Setup/user:** practice profileのhouse styleと、現在利用者の`user-profile`を読む。別利用者のroleを使わない。
3. **Matter:** server-side bindingとsource reviewのmatter IDが一致するか確認する。別matter memoを要約しない。
4. **Side/jurisdiction:** upstreamの`sales | purchasing`、jurisdiction、severityを引き継ぐ。理由なしに変更しない。
5. **Source:** exact review memo item/versionを読む。契約を再解釈してupstream findingをsilentに変えない。
6. **Destination:** recipient、channel、privilege/confidentiality circleを最初に確認する。外部・広範囲ならinternal版とsanitized版を分ける。
7. **Human review:** `READY TO SIGN | NEEDS CHANGES | BLOCKED`等はupstreamの人-reviewed statusだけを使う。AIが新たにsignature verdictを作らない。
8. **Write/send:** draftはOneDrive。共有・送信、SharePoint `outputs`昇格は人の確認後。自動post/emailをしない。

reviewer note、severity、quiet modeは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

`select-source` → `select-audience` → `destination-check` → `choose-version` → `draft` → `reconcile-state` → `confirm-save`

`choose-version`:

- `internal`
- `sanitized`
- `both`

宛先が不明なら先に質問する。internal memoへprivileged labelを付けたままcompany-wideまたはcounterpartyへ出さない。

## Audience

| Audience | 主に知りたいこと |
|---|---|
| Procurement | price、renewal、approval route |
| Budget owner | use、lock-in、cost、failure impact |
| Finance | total cost、escalator、renewal exposure |
| Security / IT | data、subprocessor、SLA、exit |
| Executive sponsor | blocker、decision、timing |

不明なら1問だけ確認する。

## Length

summary bodyは日本語で概ね200 English words相当以内を目安にする。

- 1 paragraph: 何の契約で、現在statusは何か
- 1 paragraph: 後で驚く可能性がある点
- 2～3 action items
- 1 line: approval / timing

section number、defined term、legal jargonを原則除く。ただし誤解を防ぐため必要ならplain-language parentheticalを使う。

quoteする場合は条件文全体を使う。長すぎる場合は条件を残してparaphraseし、例外を落とさない。

## Tracker assertion

「更新trackerへ登録済み」「reminder設定済み」と書く前に、同一`tenantId/practiceId/scopeId`でcounterparty/contractのexact renewal record IDを確認する。

recordがなければ:

- summaryから登録済み表現を削除する、または
- action itemを「renewal trackerへ未登録」にする

存在しないreassuranceを作らない。

## Escalation reconciliation

upstream reviewのunique approver数Nと、scope内のexact escalation recordを
比較する。`status: draft`はapproverへ届いたことを意味しない。

- verified `sent`/`delivered` event数を`M of N delivered`として表示
- draft数を`D drafts prepared`として別表示
- 未routeのapproverとfinding
- no escalationならblockを省略

Power Platform flowの存在を推測しない。verified delivery eventがなければ
M=0であり、draftをrouted/deliveredへ数えない。

## Output

詳細formatは`references/stakeholder-output.md`。external/sanitized版ではinternal reviewer note、playbook quote、approver private notes、accepted riskを除くが、誤解を生む重要conditionは残す。

## 完了

保存先、version、recipient、unrouted escalation、untracked renewalを示す。送信は人が選んだ後も別confirmationを要求する。

## 行わないこと

- source contractをfull re-reviewする
- upstream severityをsilentに下げる
- signatureをapproveする
- tracker/escalationが存在すると推測する
- Slack/emailへ自動送信する
