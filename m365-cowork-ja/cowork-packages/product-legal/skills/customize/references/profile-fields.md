> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Customizable profile fields

| Section | Scope | Examples |
|---|---|---|
| Company/product | company | business model、customer、stage、listed status |
| Jurisdiction/sector | company/practice | users、seller/operator、regulator、sector |
| Launch process | practice | intake、lead time、formal/advisory、output |
| Framework | practice | base categories、Japan overlay、auto-skip fact |
| Calibration | practice | blocks、requires work、FYI、owner、timeline |
| Claims | practice | reviewer、comparative、substantiation standard、absolute/sector rule、rejected claims、visual/final screen、stealth、platform owner |
| People | user/practice | current user role、attorney route、default/trigger別escalation owner、fallback、response target |
| Matter | matter/practice | enabled、confidentiality、cross-matter default |
| Integrations | state/practice | live status、source/version、adapter requirement |
| Watcher preference | practice | desired horizon/cadence/destination candidate |

## Scope rules

- user role/attorney contactをshared practice profileへ入れない。
- active matterをpractice profileへ入れない。
- matter secretをcompany/practice profileへ入れない。
- watcher preferenceをautomation status、schedule、last runとして使わない。
- legal source statusはofficial verificationなしに変更しない。
- framework、calibration、escalation、claims、sector ruleはsource item/versionと
  checked-at/byを`configurationSources`へ残す。
