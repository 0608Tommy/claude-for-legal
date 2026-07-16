> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本の決議省略・報告省略draft向けに変更した派生ファイルです。

# Consent / deemed resolution draft

## Mechanism analysis

```yaml
entity: "[entity]"
entityForm: KK | GK | other
organ: "[board/shareholders/committee/other]"
mechanism: board-resolution-omission | shareholder-resolution-omission | shareholder-report-omission | board-report-omission | statutory-committee-action | other
legalBasis: "[article/rule]"
articlesAuthorization: true | false | not-applicable | unknown
proposalBy: "[person]"
eligiblePersons:
  - "[name/role]"
requiredConsent: "[all eligible directors / all entitled shareholders / other]"
auditorCondition: "[no objection / not applicable / unknown]"
reportRecipients:
  - "[director/corporate auditor/shareholder]"
reportNotifiedAt: "[ISO datetime or not applicable]"
effectiveOrDeemedDate: "[date]"
```

## Draft structure

```markdown
# [会社名] — [取締役会決議の省略 / 株主総会決議の省略 / 株主総会への報告省略 / 取締役会への報告省略 / other]

**対象entity/organ:** [value]
**法的・定款上のbasis:** [source]
**proposal date:** [date]
**deemed/effective date:** [date]

## Proposal / matter

[specific action、agreement title/date/parties/exhibit]

## Resolution / consent text

[Art. 319/370等のresolution mechanismだけ。report omissionでは使用しない。]

## Report subject / notification

[Art. 320ではshareholder consent evidence、Art. 372ではreport内容、
recipients、notification evidence。Art. 363(2) reportは省略しない。]

## Implementation authority

[named officer/person、scope、documents]

## Conflict / special interest

[treatment or none confirmed]

## Consent/evidence

[resolution/Art.320ではeligible personごとのconsent evidence。Art.372では
recipientごとのnotification evidence。]
```

## Separate minutes

deemed resolution/reportについて、applicable regulationに従うminutesを別にdraftする。
proposal、consent status、auditor condition、deemed date、legal basis、retention、
sign/e-sign evidenceを記録する。

## Tracker

| Person | Capacity | Eligible/recipient | Consent or notice required | Evidence item/version | Status |
|---|---|---|---|---|---|

statusは`pending | received | invalid-or-unclear | not-required`。AIはsignatureを
request/sendせず、`received`をsource evidenceなしに付けない。
