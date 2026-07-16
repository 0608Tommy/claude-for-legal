> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Full IP interview guide

practice mixに応じてbranchし、該当しないsectionを聞きません。

## Sections

1. user role、Japanese professional role、practice setting
2. practice areas/sub-focus/volume
3. filing/enforcement/manufacture/import/platform jurisdictions
4. connectors/storage/DLP/retention
5. portfolio/IPMS/owner/audit/alert candidate
6. patent strategy、invention intake、employee invention、patent secrecy
7. trademark clearance/brand watch
8. copyright/platform/takedown
9. trade-secret protection
10. OSS policy/review/release
11. IP clauses/ownership/licensing/recordal
12. enforcement posture/approval/escalation
13. outside counsel/foreign associates
14. matter/clean-team/cross-matter
15. output/reviewer/destination

## Quick minimum

- role/practice setting
- active practice areas
- primary jurisdictions
- attorney/approver route
- Cowork DLP requirement
- portfolio source/owner
- default enforcement posture
- setup status and explicit defaults

## Required Japan prompts

- bengoshi/benrishi/supervision
- Patent Act Art. 35 employee-invention rule/source
- patent non-disclosure screening owner
- JPO/WIPO docket source and human deadline verifier
- trademark kana/kanji/romaji practice
- copyright/Platform Act route
- trade-secret management guideline owner
- Customs/import exposure
- Japanese confidentiality header/review

## Seed extraction

documentからactual position、source item/version、coverage、review statusを記録。
filenameだけでpositionを確定しません。矛盾は人に示し、silent mergeしません。
