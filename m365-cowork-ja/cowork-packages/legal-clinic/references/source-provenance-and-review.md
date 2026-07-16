> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 情報源、施行日、レビュー、引用の共通ルール

## Authority taxonomy

| authorityType | 意味 |
|---|---|
| `binding-law` | 施行中の法律 |
| `binding-rule` | 適用ある裁判所規則等 |
| `professional-rule` | 日本の弁護士に適用される職務規程等 |
| `official-guidance` | 裁判所・官庁・公的機関の運用資料 |
| `official-database` | 公式検索database。coverage limitを別途記録 |
| `official-reference` | 公式提供の参考資料。binding原文ではない |
| `case-sensitive` | 事実・裁判例・手続段階に依存 |
| `educational` | pedagogy又はclinic教材 |
| `future-law` | 成立済み又は提案中だが対象規定が未施行 |
| `internal-control` | dual review等の内部統制。法律ではない |

```yaml
authorityType: "[ASCII enum]"
title: "[official title]"
articleOrSection: "[article/rule/section]"
officialUrl: "https://..."
promulgatedAt: "[YYYY-MM-DD or null]"
effectiveFrom: "[YYYY-MM-DD or null]"
revisionCheckedAt: "[YYYY-MM-DD]"
asOf: "[YYYY-MM-DD]"
bindingScope: "[scope]"
humanVerifiedBy: "[object ID or null]"
```

guidanceをlaw、internal controlを法定義務、future lawをcurrent lawとして扱わない。

## 日本法source priority

1. 官報、e-Gov、裁判所、法務省、個人情報保護委員会等の公式日本語原文。
2. 事件固有の命令、送達通知、mints record、行政庁notice、正式な依頼者document。
3. 日弁連のcurrent official会規page、所属弁護士会のcurrent rule、責任弁護士が承認した
   clinic source。public lawyer searchは登録確認のsource candidateであり、search結果
   だけでauthority、specialization、availability又はclinic engagementを証明しない。
4. commercial database又は他のresearch service。
5. 二次資料。一次資料発見と論点整理に限る。

日本法令外国語訳データベースの英訳は参考であり、日本語原文だけが法的効力を持つ。
裁判所裁判例検索は全裁判例を収録せず、negative resultは裁判例不存在を証明しない。
日弁連の弁護士等の業務広告に関する規程・指針を、弁護士職務基本規程又は登録検索と
混同しない。clinic又はAI serviceのpublic description、lawyer title、success claim、
specialization claimはcurrent advertising sourceと責任弁護士reviewを要求する。

法令、規則、施行日、期限、休日、送達、経過措置、professional ruleに依存する場合、
その会話でcurrent official sourceを再確認する。取得できなければ断定せず
`[current source unavailable]`又は`[statute unretrieved — verify]`とする。

## Current vs future law

`asOf`、`effectiveFrom`、経過措置、事件開始日、trigger日を別fieldで保持する。
2026年APPI改正等の未施行規定は`future-law`としてreadinessを示せるが、current duty、
client consent又は期限計算へ自動適用しない。sourceが更新された場合、silentに旧ruleを
使わずcurrency eventを作る。

## 情報不足の3値

1. exact sourceを取得してprovenanceを付けて進む。
2. sourceが得られるまで停止する。
3. 結論には使わないが、結果を変え得る既知の改正・延期・経過措置を
   `[model knowledge — verify]`で示す。

利用者が示した条文、事件名、日付、期限、登録番号、法域も分析前に確認する。

## Approved source-card restricted domains

`criminal | immigration | housing | benefits`はapproved source cardが
`status: approved`、current、matter/forum一致の場合だけsubstantive rule、deadline、
eligibility、formを使う。cardがない又は`pending | in-review | blocked`なら:

1. safety/urgency issue spotting
2. minimum factsとexact document capture
3. responsible lawyer又はapproved specialistへのrouting
4. emergency contact option

に限定する。model knowledge又はforeign-law analogyでgapを埋めない。

## 正規tag

- `[primary source]`
- `[professional rule]`
- `[official guidance]`
- `[user provided]`
- `[model knowledge — verify]`
- `[settled — last confirmed YYYY-MM-DD]`
- `[verify]`
- `[review]`
- `[retrieved but verify support]`
- `[premise flagged — verify]`
- `[statute unretrieved — verify]`
- `[VERIFY: specific fact]`
- `[UNCERTAIN: specific proposition]`
- `[CITE NEEDED: specific source]`

tagは確信度でなく、実際の取得経路を表す。connector declarationだけでconnector tagを
使わない。

## Quote / support / coverage

- exact passageがopenでない限りquotation markを使わない。
- paraphraseには`[verify exact quote — source cite pending]`。
- retrieved passageがholding、rule、guidanceのどれかを確認する。
- citation checkは全文から全citationをextractし`checked N of M`を報告する。
- source本文を取得できなければ`confirmed`と書かない。
- large inputはread coverageと未読範囲を示す。

## レビュー担当者向け注記

成果物直前に1blockだけ置く。

review routing:

- `responsible-lawyer`: legal proposition、deadline、engagement、conflict、scope、
  client/court/agency等のexternal legal content。
- `supervisor`: pedagogy、student feedback、training、pure administrationだけ。
- `both`: legal subjectとpedagogy/adminが同じartifactに混在。
- `competent-language-reviewer`: consequential translation。上記legal/supervisor roleを
  置換せず追加する。

supervisorが弁護士資格を持つ場合も、review recordではどのroleで判断したかを明示する。
`reviewSubjectTypes`と`requiredReviewerRole`はstrict schemaへ記録する。

> **⚠️ レビュー担当者向け注記**
> - **Sources:** [取得source、未接続source]
> - **Read:** [items/pages/records、未読範囲]
> - **Law / rule / guidance / future:** [layer、version、as-of]
> - **Conflict / engagement / scope:** [human-recorded status]
> - **Flagged for judgment:** [`[review]`件数]
> - **Destination / ACL:** [保存先、viewer、external版]
> - **Review subjects / required role:** [subject types、responsible-lawyer / supervisor / both]
> - **Language review:** [not required / competent reviewer、artifact version、status]
> - **Before relying:** [required reviewerが確認する1～2点]
> - **Review status:** DRAFT — qualified Japanese counsel and clinic supervisor review pending

meta-commentaryを本文へ散らさない。

student、AI、cloud、vendor、translator、interpreterは日本の弁護士に適用される
confidentiality/withholding ruleで自動的に保護されるとは表示しない。source tagと
review noteはprotectionを創設しない。

## Recoverable-error bias

不確かな主観判断は見落としよりrecoverableな`[review]`を選ぶ。上流severityは下流の
floorとし、下げる場合は新事実と理由を明示する。AIはdecisionを選ばず、artifact draft、
escalation、追加facts/source、candidate tracker、その他の選択肢を示す。

## Verification audit

```yaml
eventType: legal-source-verified
outcome: succeeded | failed | partial
details:
  citeOrFact: "[cite or fact]"
  source: "[primary source]"
  sourceRevision: "[revision/effective date]"
  verdict: confirmed | corrected | could-not-verify
  correction: "[corrected value or null]"
```

verificationはappend-only auditへ記録し、過去recordをupdate/deleteしない。

## Consequential translation provenance

権利、期限、scope、legal advice、court/agency content等のtranslationには、exact source
language item/version、target-language artifact version/hash、responsible-lawyer legal
review、competent-language reviewを記録する。両reviewが`approved`になるまで外部版を
approvedと表示しない。
