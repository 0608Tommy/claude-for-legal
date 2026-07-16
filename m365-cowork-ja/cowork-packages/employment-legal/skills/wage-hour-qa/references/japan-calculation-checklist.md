> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Japan wage/hour calculation checklist

1. establishment、prefecture、industry。
2. employee/worker status、work rules、CBA。
3. working-time system、Article 36 agreement、special clause。
4. actual schedule、objective time records、break/holiday/night。
5. wage components、fixed overtime、bonus/allowance、deduction。
6. current prefectural/industry minimum wage。
7. current premium rates/combinations/caps/exceptions。
8. Article 41 or special-system procedure。
9. target period、limitation、interest/penalty、tax/insurance。
10. source/effective date、missing input、qualified review。

formula:

```text
covered wage base = current Japanese rule applied to each wage component
statutory hours = verified actual hours classified by ordinary/overtime/holiday/night
candidate gross by category =
  Σ(category hours × verified hourly base × verified total rate/multiplier)
candidate unpaid =
  candidate gross by category − corresponding amount already paid for those hours
```

overtime、statutory holiday、night workが重なる場合はcurrent ruleのcombinationを
category別に確認し、同じhourを脱落・二重計上しません。rateやthresholdをこの
templateへ固定せず、hours/base/rate/payment inputが不足なら計算を停止します。
