> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Parameters 01–09

## 1. Audience

role、seniority、AI fluency、supervisionを定義し、output/delegationを合わせる。
undefinedなら🔴。

## 2. Work Shape

- `Accretive Judgment`: context stewardship、conservative delegation
- `Bounded Transactional`: deviations/options、explicit resolution
- `Pattern-Matched Review`: higher execution autonomy、outlier escalation

work shape未定義、またはbehaviorと矛盾なら🔴。

## 3. Delegation Threshold

AIとhumanの境界がoutput構造に現れるか。high-stakes outputがfinal conclusionとして
見えるなら🔴。disclaimerだけでhuman judgment surfaceがなければ⚠️。

## 4. Input Requirements

minimum input、不足時のask/halt/labeled assumption、out-of-scope trigger。
不足をsilentに補完するなら🔴。

## 5. Versioning and Ownership

owner/review mechanism、material change notice、cadence/trigger。community skillは
source/version欠落を⚠️。team-wide first-partyでownerなしは🔴。

## 6. Confidence Bands

- high: propose
- medium: rationale + ask
- low: suppressせずuncertaintyをhandoff

accretive/bounded workにbandなしは🔴。

## 7. Failure Modes

hallucination、novel input、jurisdiction、insufficient context等をdesignで扱う。
legal advice/support、privilege/confidentiality、accountability gapの3つは必須。

## 8. Scope Boundaries

in-scope document/workflow/work shape、explicit not-do、out-of-scope deflection。
boundaryなしは🔴、failure path不足は⚠️。

## 9. Escalation Logic

novel input、outside jurisdiction、conflicting signal、complexity超過、low confidence。
stop、human route、reasonを構造化する。non-trivial bounded/accretive workでlogicなしは🔴。
