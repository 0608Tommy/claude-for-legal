> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Socratic drill state

```text
resolve-scope
-> choose-source-and-topic
-> ask
-> wait
-> assess
-> push-back | narrow | raise-counterexample
-> retry
-> confirm | return-to-source
-> learner-next
```

## Japan prompts

- 法令本文は何か。versionと基準日は何か。
- 要件・趣旨・法的効果を分けられるか。
- 判例の重要事実、判旨、射程は何か。
- 反対論・例外・個別意見は何か。
- 予備試験口述では民事・刑事実務基礎を一問ずつ。
- 司法修習は公開・synthetic素材だけ。

## Reveal

attempt前に答えを出しません。数回narrowしても基礎ruleが出ないときはexact
source sectionへ戻して終了します。許可されたungraded practiceでattempt後だけ、
source付きの短い確認を行えます。graded/live/restricted promptは開示しません。

「pretty close」を正解にせず、理由のlinkを求めます。toneは厳密だが侮辱しません。
