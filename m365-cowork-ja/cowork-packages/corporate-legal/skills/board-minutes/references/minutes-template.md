> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本の取締役会議事録draft向けに変更した派生ファイルです。

# Minutes draft structure

house precedentを優先するが、mandatory fieldsを削らない。

```markdown
# [会社名] [取締役会 / 委員会]議事録

**開催日時:** [date/time]
**開催場所・方法:** [location / video / hybrid]
**招集:** [authority、notice、waiver]

## 出席

- 出席取締役: [names]
- 特別利害関係等により議決に加わらない者: [name / agenda]
- 出席監査役・委員等: [names/roles]
- その他出席者: [management/adviser]
- 議長: [name]
- 議事録作成者: [name/role]

## 定足数

[eligible count、present count、quorum source、conclusion]

## 議事

### 第1号議案 [title]

**資料:** [exact item/version]
**報告・説明:** [source-based summary]
**審議:** [house depth。source不足はPENDING]
**特別利害関係:** [treatment]
**決議:** [exact approved wording]
**結果:** [for/against/abstain/not participating]

## 報告事項

[mandatory/ordinary reports]

## 閉会

[time / statement]

## 署名・電子署名

[entity/organ/document-specific requirementに従うsigners and method]
```

## Internal checklist

- entity form / organ / articles version
- notice/waiver
- eligible directors / special interest
- quorum / vote
- auditor/committee opinion or objection
- remote method
- mandatory content
- signer/e-signature
- retention
- exhibits
- unresolved placeholders

internal checklistはadopted minutes本文と別に保存する。
