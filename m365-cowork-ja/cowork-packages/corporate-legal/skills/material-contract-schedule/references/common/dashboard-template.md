> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) のdashboard templateを日本語化し、Microsoft 365成果物向けに変更した派生ファイルです。

# ダッシュボード標準

価値は装飾ではなく、短時間で全体像を理解できることにある。

## 構造

1. **Title / metadata:** 対象、作成日時、scope、source versionを1行で示す。
2. **Summary stats:** 重要な件数を先頭に置く。
   `40件: 🔴 3 blocking · 🟠 8 high · 🟡 15 medium · 🟢 14 low`
3. **レビュー担当者向け注記:** source、coverage、law layer、currency、destination、
   before relyingを1blockにする。
4. **Chart:** 1～2個まで。risk distribution、category、timelineから選ぶ。
5. **Table:** sort/filter可能にし、item、owner、due、source、statusを保持する。
6. **Decision tree:** draft、escalate、追加事実、watch、その他を示す。

## Microsoft 365成果物

- **HTML:** 単一file、inline CSS、外部CDN/font/frameworkなし。SharePointまたは
  OneDriveへ保存し、Coworkでlinkを返す。inline JavaScriptが許可されると仮定せず、
  static tableでも読めるようにする。
- **Excel:** meeting、sharing、filter用途。formula injectionを防止し、source、
  state、owner、date、verification列を保持する。
- **PowerPoint:** management向けにsummary statsと1～2 chartだけを使う。
- **Markdown/PDF:** HTMLを開けない利用者向けに同じsummaryを保持する。

Word native tracked changes、specific Office style fidelity、macro、interactive
HTML動作は、target tenantでgolden-file testを通った範囲だけを対応済みと表示する。

## 未信頼input

- `&`, `<`, `>`, `"`, `'`をHTML entityへescapeする。
- DOMへ入れる文字列は`textContent`を使い、未信頼値を`innerHTML`へ渡さない。
- 未信頼値をscriptへ補間しない。
- URL schemeは`http:`, `https:`, `mailto:`だけを許可する。
- Excel/CSVで`=`, `+`, `-`, `@`, tab、CR、LFから始まる外部値を式として
  実行させない。

## 表示rule

- severityはred / orange / yellow / green、neutralはgray、statusはblue。
- animation、外部依存、複雑なlayoutを使わない。
- summary、reviewer note、chart、table、decision treeの順序を揃える。
- dashboardは依頼または提案への同意後だけ作り、自動生成しない。
