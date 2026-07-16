> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Currency watch — 日本の訴訟・紛争

checked through: `2026-07-16 JST`

次は毎回current official sourceを再確認する。

## High-risk current items

1. **民事訴訟digitalization:** 2026-05-21全面施行、経過措置、旧mints、covered
   representative、file type、service operation。
2. **別手続rollout:** 民事執行、民事保全、倒産、労働審判、非訟、人事・家事の
   online coverageをordinary civilと同一視しない。
3. **Electronic service:** 民訴法109条の3の通知・閲覧・記録timestamp。
4. **Deadline:** appeal、労働審判異議、court-set answer、holiday、追完。
5. **Limitation:** claim-specific period、2020 transition、accrual、knowledge、
   催告/協議合意。
6. **Court/division operation:** form、file format、hearing、record access、
   case-specific direction。
7. **Patent:** 特許法revision、JPO guidance、均等論・無効抗弁のcurrent precedent。
8. **Confidentiality:** court order、Patent Act order、self-use document doctrine、
   sector inquiry。

## Verification rule

deadlineを使う前に:

```yaml
sourceFetchedThisSession: true
authorityUrl: "https://..."
revisionOrEffectiveDate: "[date]"
triggerSourceItemVersion: "[item/version]"
effectiveServiceAt: "[timestamp or null]"
calculationSteps: []
verifiedByLawyer: null
verifiedByDocketingOwner: null
calendarEntryId: null
```

`sourceFetchedThisSession: false`ならcandidateとしてもdateを断定せず、exact sourceを
取得する。lawyer/docket owner verificationをAIが代入しない。

## Known blocker

qualified Japanese counsel reviewerは記録されていない。tenant production、
external reliance、filing、calendar write、preservation release、settlement executionは
review完了までblock。
