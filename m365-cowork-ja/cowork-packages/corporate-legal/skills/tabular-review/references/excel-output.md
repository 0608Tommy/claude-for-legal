> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365の検証可能なspreadsheet draft向けに変更した派生ファイルです。

# Excel / CSV output specification

## Capability

target tenantでfile-generation capabilityとgolden-file testが確認できた場合だけ
`.xlsx`を作成したと表示する。未確認ならCSV/Markdownとimport instructionを
OneDrive draftとして作る。native Excel comment/style fidelity、macro、Office
agent availabilityを推測しない。

## Workbook

### `Review`

- row 1: confidentiality/draft note
- row 2: column labels
- row 3+: one row per document
- column A: document ID/name/source link
- each data columnにsource quote/location/state/Verifiedを隣接またはhidden columnで保持
- filter/sortを壊すdata-region mergeをしない
- `Verified`: blank by default、allowed `✓ | ✗ | ?`

### `Flags`

`unclear` / `needs_review` / quote mismatchを1 rowずつ:
Document、Column、State、Value、Quote、Location、Source Version、Note。

### `_schema`

id、label、type、options、prompt、schema version。

### `_summary`

document/column/batch count、state counts、quote checks、coverage、verification
reminder。

## Color

- answered: default/white
- unclear/needs_review: light yellow
- not_present: light gray
- verified failure: red highlight

confidence scoreを作らない。

## Formula injection

external textが`=`, `+`, `-`, `@`, tab、CR、LFから始まる場合、single quote等で
textとしてneutralizeする。CSVはRFC 4180 quotingを使う。full quoteをtruncate
せずsources file/sheetへ保持する。

## Sharing

初稿はcurrent userのOneDrive、shared by defaultはfalse。SharePoint outputsへの
promotion、external sharing、Teams/Outlook sendは別のhuman confirmation。
