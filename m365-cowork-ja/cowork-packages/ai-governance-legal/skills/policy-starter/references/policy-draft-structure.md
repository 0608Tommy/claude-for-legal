> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Policy draft構造

```markdown
> **⚠️ レビュー担当者向け注記**
> - **Sources:** [...]
> - **Read:** [...]
> - **Flagged for your judgment:** [...]
> - **Currency:** [...]
> - **Destination:** [...]
> - **Before relying:** [...]

DRAFT FOR INTERNAL LEGAL REVIEW — NOT FOR DISTRIBUTION

# [Organization] AI Usage Policy — Draft

## Sources

| Source | URL | Accessed | Used for |
|---|---|---|---|

## Executive summary

[3 paragraphs maximum]

## 1. [Selected section]

[scope]

[rules with source tags and `[review]`]

### Open questions

1. [decision]
2. [decision]

[repeat selected sections only]

## Adoption checklist

- [ ] [...]

## Version and review

**Status:** DRAFT
**Owner:** [...]
**Next review:** [...]
**Approved by:** pending
```

## 品質確認

- audienceが理解できる平易な表現か。
- section間でapproved / prohibited / exceptionが矛盾しないか。
- 守れない絶対表現がないか。
- named toolsとdata classesが最新か。
- external-facing statementと内部controlを混同していないか。
- すべてのhard callに `[review]` があるか。
