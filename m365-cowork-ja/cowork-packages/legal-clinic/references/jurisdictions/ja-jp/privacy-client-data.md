> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 依頼者data、安全、APPI、My Number

**状態:** DRAFT — qualified Japanese counsel and clinic supervisor review pending

## Collection gate

real client dataをCoworkへ投入する前に、責任弁護士、学校/host、IT/privacy ownerが
次を承認する。

- 利用目的、必要性、data minimization
- account/tenant terms、training/retention/subprocessor
- approved Microsoft 365 location、foreign transfer、vendor
- APPI上のregime-specific analysis（利用目的、要配慮個人情報、委託、第三者提供、
  外国にある第三者への提供、法令例外等）
- access、incident response、breach escalation
- retention/deletion、internal preservation control、court order、case closure
- Cowork prompt内DLPが必要か

未解決ならsynthetic data又はredacted manual draftだけにする。

## Restricted categories

下表はclinicのoperational access-control categoriesであり、個人情報保護法上の
`要配慮個人情報`の定義と同一ではない。statutory category該当性はdata elementごとに
current lawで判断する。clinicがrestrictedにする情報には、法定要配慮個人情報でない
安全連絡先、case strategy、在留・家族context等も含み得る。逆に、表にないことだけを
理由に法定要配慮個人情報でないと判断しない。

したがって、clinic restricted categoriesは、全ての法定要配慮個人情報と同義でも
完全な一覧でもない。

| category | Control |
|---|---|
| identity/contact | pseudonymous ID、identity mapping別item |
| safe contact | safe channel/time、住所秘匿、voicemail/mail禁止を別ACL |
| health/disability/capacity | minimum necessary、restricted viewer |
| immigration | status、entry、family、riskをrestricted |
| criminal | custody、allegation、recordをrestricted |
| child/family/DV/stalking | child identity、school、address、安全情報をrestricted |
| interpreter/accessibility | language、interpreter、accommodationをneed-to-know |
| My Number | 原則upload/collection/storage拒否 |

My Number cardを通常の本人確認資料又はmatter IDとして扱わない。裁判所のcurrent
mints guidanceを確認し、誤upload時は責任弁護士と裁判所の承認済みincident routeへ
直ちにescalateする。

## APPI

個人情報保護法とPPC guidanceについて、利用目的、適正取得、要配慮個人情報、
安全管理、従業者/委託先監督、第三者提供、外国移転、本人対応、不要時削除を
matter/host-specificに確認する。

最初にclinic hostと対象業務のregimeを選定する。

```text
private-sector-chapter4
public-sector-chapter5
article58-private-treatment
mixed
unresolved
```

国立/公立/私立大学、地方公共団体、独立行政法人、附属病院、法律事務所等で適用関係が
異なり得る。個人情報保護法58条、公的部門guideline/Q&A、hostの設置法・業務を確認し、
`unresolved`ではreal client dataを投入しない。public-sectorだから常にChapter 5、
大学業務だから常にprivate-sectorと決め打ちしない。

`GDPR lawful basis`のような単一fieldへ短縮しない。少なくとも:

- personal informationの利用目的・通知/公表
- 要配慮個人情報の取得と例外
- 委託と委託先監督
- 国内第三者提供
- 外国にある第三者への提供
- 共同利用、法令に基づく例外、緊急例外
- 保有個人データへの本人対応
- My Numberの別regime

を分ける。GDPR等が実際に適用されるcross-border matterは別approved source cardと
qualified counsel reviewを要求し、APPI analysisを置換しない。

2026 APPI amendmentはprovision-specific effective dateまで`future-law`。under-16、
biometric、statistical-use、surcharge等をcurrent ruleとして早期適用しない。

## Safe-contact workflow

intakeで依頼者本人に安全な連絡手段、時間帯、表示名、voicemail、SMS、郵便、
住所、第三者同席を確認する。DV/stalking又は家族conflictがあればgeneral profileへ
複製せず、outbound draftとdelivery approvalがsafe-contact recordに一致することを
確認する。安全でないchannelへ自動通知しない。

## Retention / preservation

`append-only`は永久保存を意味しない。責任弁護士/local bar、大学policy、insurer、
Houterasu契約、matter type、法定保存、client instruction、internal preservation
control、court orderを組み合わせた
documented scheduleを使う。全国一律の弁護士file保存期間を捏造しない。

`legal hold`は原則internal controlであり、FRCP 37(e)又は日本法上の一般的同等制度と
表示しない。法的保全根拠がある場合はexact statute/order/sourceを別記する。

semester endだけでarchive/deleteしない。preservation中又はoriginal handling不明では
deleteしない。approved destructionはidentity mapping、exports、local copies、
backup、audit evidenceを含む別operationである。

## DLP / destination

SharePoint、OneDrive、Power Platform、connectorの保存・flow境界でDLPを確認する。
Cowork prompt自体がDLPで保護されるとは表示しない。destinationがclient、相手方、
public/large group、vendor、個人email等の場合、内部分析をsanitized external artifactへ
変換し、責任弁護士approvalを得る。

student、AI/cloud provider、vendor、translator、interpreterへの開示が日本の弁護士と
同じ守秘又は手続保護を自動的に受けるとは扱わない。必要性、契約、technical control、
foreign transfer、access、retention、disclosure effectを責任弁護士が確認する。

consequential translationはresponsible-lawyer legal reviewとcompetent-language reviewの
両方が同じartifact version/hashへ記録されるまで外部利用しない。

## Incident / urgent safety

誤送信、誤権限、My Number upload、safe-contact違反、暴力・自傷他害、身柄拘束等は
通常workflowを止め、approved incident/emergency routeへ人が連絡する。AI又はclinicが
一定時間内に対応すると約束せず、未確認の外部通報を自動実行しない。

児童虐待が疑われる場合は児童虐待防止法6条等のcurrent official textと守秘との関係を
責任弁護士又はdesignated humanが直ちに確認し、Art.6の`速やかに`を踏まえたprompt
human notificationを判断・実行する。route candidateは`189`。AI/cloudへの入力又は
queue登録を通告と扱わず、AIは通告を実行しない。

DV route candidateは`DV相談ナビ #8008`。189/#8008ともsafe device、call history、
相手方monitoring、利用可能時間を確認し、unsafe contact channelへ自動発信しない。
