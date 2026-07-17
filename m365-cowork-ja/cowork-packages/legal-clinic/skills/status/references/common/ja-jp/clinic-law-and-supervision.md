> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — clinic model、資格、利益相反、受任、守秘

**状態:** DRAFT — qualified Japanese counsel and clinic supervisor review pending

## Responsible lawyer / supervisor / student

- `responsibleLawyer`: 日本で有効な弁護士登録を人が確認し、依頼者・scope・法律判断に
  責任を持つ者。
- `supervisor`: 教育・業務監督者。責任弁護士と同一の場合も別人の場合もある。
- `student`: 法科大学院生又は実習生。弁護士資格、代理権、受任権限を持つと表示しない。

setupでは氏名、所属弁護士会、登録確認日、clinic model、依頼者となる者、
matter-level supervisorを記録する。faculty titleだけで資格を推定しない。

## No nationwide student-practice status

法科大学院の実務教育は全国一律の学生代理資格を生まない。民事訴訟法54条又は
刑事訴訟法31条等の非弁護士代理に関する例外・許可を、再利用可能な
`Certified Legal Intern` statusと扱わない。裁判所、手続、事件ごとの要件を責任弁護士が
確認する。

弁護士法72条について、教育目的又は無償であることだけを包括的safe harborとしない。
大学clinic、法律事務所、弁護士会相談、Houterasu契約、国選事件等の実際のmodelについて
日本の有資格弁護士の書面positionを必要とする。

## Student participation matrix

責任弁護士がactivityごとに`permitted | supervised | prohibited | lawyer-only`を設定する。
matrixはtraining、access、supervisionのinternal policyであり、学生に法的権限を付与せず、
弁護士法72条その他の適法性問題を治癒しない。
既定:

- observe、interview、research、internal draft: supervised
- routine logistics: supervised又はlocked approved template
- legal advice、substantive client communication、negotiate、accept/decline、
  conflict waiver、settle、sign、file、represent、close: lawyer-only

`assist | guide | teach`はpedagogyだけを変え、法的gateを緩和しない。

## Conflict sequence

1. substantive facts前に最小限の氏名pre-screen。
2. prospective client、相手方、alias、旧姓、関連法人・人物・matterを照合。
3. statusは`pending | clear | restricted | blocked`。
4. `pending`/`blocked`ではfacts/document accessを止める。
5. 責任弁護士又はapproved conflicts ownerが結果を記録。
6. conflict clear後もengagementとscopeを別に決める。

「positional conflict」はspecific professional rule又はclinic policyのどちらかを
区別し、AIが法的disqualificationとして断定しない。

information barrier、screening wall、restricted ACLはconfidentiality/risk controlで
あり、conflict clearance、client consent又はwaiverではない。barrierがあっても
`conflictStatus`は別authorityが決定する。

## Engagement / scope

`engagementStatus: pending | active | limited | declined | closed`。client identity、
responsible lawyer、service scope、excluded issues、communication authority、fee/legal
aid status、termination/closure processを記録する。intake summary又はmatter recordは
受任を意味しない。

ただしdisclaimer、unsigned agreement、profile上の`pending/declined`だけで関係不存在を
保証しない。実際にadvice、undertaking、representation、期限管理、相手方communication、
依頼者の合理的reliance等が生じた場合、engagement又はscopeが成立・拡大した可能性を
責任弁護士が直ちに評価し、recordとconductの不一致が解消するまでsubstantive workを
停止する。

AIは`Take/Decline`を出さず、
`受任判断未了 — responsible lawyer decision required`とする。

## Supervision gate

software queueの採否にかかわらず、次はauthenticated responsible lawyer review必須。

- legal advice、case acceptance/decline、scope change
- conflict waiver又はrestricted conflict handling
- limitation/deadline calculation
- settlement、demand、substantive client status
- court/agency document、signature、filing
- capacity/guardian authority determination
- adverse news、withdrawal、case close

reviewはexact artifact version/hash、sources/effective dates、decision、edits、timestamp、
reviewer object ID、release actorを記録する。status clickだけでsubstantive reviewを
証明しない。studentはreleaseしない。

## Japanese confidentiality caveat

弁護士法上の守秘義務、民事訴訟法197条・220条、刑事訴訟法105条・149条等の
提出・押収・証言拒絶は、米国型の一般的attorney-client privilege又はwork productと
同一ではない。依頼関係、情報の性質、所持者、目的、distribution、例外、forumを
責任弁護士が判断する。

`PRIVILEGED & CONFIDENTIAL`又は内部headerは保護を創設しない。外部版へ内部分析、
accepted risk、conflict、守秘評価を流さない。

student、AI system、cloud provider、translator、interpreter、vendorは弁護士と同じ
守秘義務又は手続上の拒絶権で自動的に保護されるとは扱わない。共有の必要性、依頼関係、
契約、technical control、foreign transfer、distribution、forum-specific effectを
責任弁護士が確認する。

## JFBA source / search / advertising

職務基本規程は日弁連のcurrent official会規pageから取得する。public lawyer searchは
登録情報の確認source candidateであり、検索結果だけでauthority、専門性、availability、
clinic engagementを証明しない。弁護士等の業務広告に関する規程・指針は別sourceであり、
public clinic description、lawyer title、success/specialization claimを責任弁護士が
reviewする。

## Professional liability wording

「malpractice defense」を日本へ直訳しない。民法上の委任・債務不履行・不法行為、
弁護士法上のdiscipline等の可能性をmatter-specificに検討する。missed deadlineが
直ちに特定の責任成立を意味すると断定しないが、重大なprofessional-risk eventとして
即時escalateする。
