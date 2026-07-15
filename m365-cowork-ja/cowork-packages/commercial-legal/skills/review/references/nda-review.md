> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# NDA review

## Goal

inbound commercial NDAをGREEN / YELLOW / REDへtriageし、lawyer timeを必要なitemへ集中させる。bucket criteriaはattorney-reviewed playbookから取り、skillにdefault thresholdをhardcodeしない。

## Side

mutual NDAでもsideを確認する。誰のpaperか、evaluationの方向、誰が何をdiscloseするか。M&A、employment、investmentはcommercial NDA scope外としてspecialistへrouteする。

## Scope check

NDAに次があればautomatic YELLOW以上:

- standstill
- license grant
- exclusivity
- non-solicit/non-compete
- IP assignment
- ROFR
- MFN
- broad arbitration/forum beyond confidentiality
- services/payment obligation

「NDA」というtitleだけで処理しない。

## GREEN

条件:

- applicable sideの全attorney-reviewed NDA positionsにpass
- playbook silenceなし
- NDA外義務なし
- no RED trigger
- `attorneyReviewed: true`

quick/default profileではGREENを出さない。GREENは「playbook上additional legal review itemなし」であり、AIのsignature approvalではない。signature前gateは残る。

## YELLOW

- playbook deviationだがneverではない
- playbook silence
- NDA外義務
- one-way factsがuncertain
- jurisdiction transferabilityがuncertain

flagged itemを個別に示し、approverをnameする。

## RED

- never/deal-breaker
- structureがteam postureとincompatible
- high-risk extra obligation

相手方へ「signする」と言わず、legalへrouteする。

## One-way questionnaire

1. 自社だけがdiscloseし、相手方は何も返さないか。
2. limited specific disclosureか。
3. M&A、employment、investmentか。
4. receiving/disclosing sideのriskは何か。

playbookにfact patternがなければYELLOW。

## Checks

### Mutuality

directionとremedyが本当にmutualか。

### Definition

marked-only/all disclosed、oral confirmation、affiliates、representatives。

### Carveouts

典型5項目:

1. public other than breach
2. previously known
3. independently developed
4. third-party receipt without restriction
5. compelled disclosure with legally permitted notice

required wordingはplaybookから取る。

### Residuals

unaided memory、notes/copies、patent/copyright license effectを確認。

### Term/survival

initial term、survival、trade secret、return/destruction。

### Restrictive covenant

non-solicit、non-compete、exclusivity、standstill。日本はcompetition/IP module、他法域はcurrent source。

### Fee/remedy

attorneys' fees、injunction、liquidated damages、one-sided remedy。

### Backup

ordinary backup、legal retention、continuing confidentiality。

### Governing law

playbookとactual jurisdiction。

## Output

### GREEN

```markdown
## NDA Triage: [Counterparty]
GREEN — playbook checks passed; signature still requires standard human process

### Executive Summary
No red flags identified under the approved playbook.

| Check | Status | Playbook reference |
|---|---|---|
```

### YELLOW

```markdown
YELLOW — [approver] review required

### Flagged items
**[Issue] — §[X]**
What:
Why:
Legal risk:
Business friction:
Likely resolution:
```

### RED

```markdown
RED — stop and consult Legal

**[Issue] — §[X]**
> "[quote]"
Playbook conflict:
Recommended response:
```

## Complexity

simple strike/word replacementはdraftできる。new substantive provision、clause restructure、novel legal positionが必要なら「§[X] — Legal review」とし、AIだけで完成させない。

## Counterparty context

BigCoが交渉しない可能性はseverityを下げる理由ではなく、accept/use-our-paper/walkのdecision context。startupにはown paperが効率的な場合がある。人が決める。

## Closing action

profileの`ndaTriagePreferences.closingAction`をverbatimで付ける。ただし自動send/sign instructionとして実行しない。未設定なら:

`Route final NDA through your standard approval process.`

## CLM

GREEN/YELLOW/REDに応じたrecord candidateを提案できるが、manifestにconnectorはなく、自動作成しない。REDでもinternal record保持が必要な組織ではprofileに従うため、旧「REDはrecordを作らない」を絶対ruleにしない。
