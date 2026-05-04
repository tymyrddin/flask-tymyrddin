from . import recipes_blueprint
from flask import render_template


awareness_recipes_names = []
pentesting_recipes_names = []
teaming_recipes_names = []


CONCEPTS = [
    {
        "name": "Patching is regular",
        "claim": "All systems are patched on a schedule reviewed quarterly by the Patch Management Committee, subject to operational constraints and Change Advisory Board availability.",
        "operational_reality": "Applying a patch might break the legacy finance system before bonuses are calculated. So the team waits for the Change Advisory Board, then says 'further assessment required' and closes the ticket. The vulnerability remains. The dashboard stays green.",
        "failure_mode": "The March patch was ready on time. The Change Advisory Board met in November. The attackers arrived in October, using the same exploit. Everyone followed the process correctly, including the attacker who read the public CVE.",
        "org_incentive": "The auditor checks whether a patching schedule exists and was reviewed. No auditor has ever asked to see the gap between scheduled and applied patches, because that would mean reading hundreds of deferred tickets. The schedule stays 'compliant' year after year.",
        "impact": "The CEO announced an urgent security transformation. The same consultancy that wrote the schedule was hired to review it. They found the schedule excellent and recommended a new quarterly committee, which met once and then merged into the Change Advisory Board.",
    },
    {
        "name": "Logs arrive on time",
        "claim": "A centralised logging platform provides the Security Operations Centre with comprehensive real-time visibility across the entire estate, including cloud and on-premise.",
        "operational_reality": "Adding a new log source costs money and takes weeks. Engineers have discovered that 'logging locally to a text file' counts as logging if no one reads the definition closely. They set up a cron job and forget about it until the disk fills.",
        "failure_mode": "The attacker moved through an acquired subsidiary added after the logging scope froze in 2021. The SOC dashboard showed a beautiful green line, which meant 'the platform is receiving electricity'. The attacker had been present for 63 days.",
        "org_incentive": "The SIEM renewal form asks for the number of log sources. That number sets the renewal price. No field asks for the percentage of the actual estate that those sources represent. Purchasing approves because the number matches last year's.",
        "impact": "After the breach, the SOC manager said the incident was 'contained' within 3 weeks. An internal memo clarified that 'contained' meant 'we stopped looking because the forensic budget ran out'. A new logging project was descoped to exclude the subsidiary being sold.",
    },
    {
        "name": "Someone owns this decision",
        "claim": "Security ownership is clearly defined through a RACI framework, reviewed annually and endorsed by the Executive Security Steering Committee.",
        "operational_reality": "The RACI was last updated before a reorganisation that split 3 departments into 5 and merged 2 into one that no longer exists. Staff forward any ownership email to 'the person who was here before me' and mark it 'actioned'.",
        "failure_mode": "A critical public exploit waited in the ownership queue for 7 months. The RACI named a position made redundant in April. The auto-reply said 'contact my former manager', whose email bounced. The vulnerability was assigned to a shared mailbox with 14,000 unread messages.",
        "org_incentive": "The RACI is a governance artefact that auditors photograph during compliance reviews. The photograph shows boxes and arrows. Auditors do not interview the named people or check employment records. The photo goes into a binder next to the broken SharePoint link.",
        "impact": "A cross functional working group met quarterly, produced a new RACI, and was restructured before the RACI could be distributed. The new RACI assigned ownership to a steering group that requires quorum from departments that no longer exist.",
    },
    {
        "name": "Processes are followed",
        "claim": "Security operations are governed by a mature suite of documented processes, approved by senior management and embedded in operational culture.",
        "operational_reality": "The process documents live on a SharePoint site migrated twice, decommissioned, then resurrected as a read-only archive. The correct link is in a 2019 email whose attachment was blocked. So they use the old process, pointing to a shut down network drive.",
        "failure_mode": "The on-call engineer followed the Incident Response Process exactly. Step 4 said 'lock out accounts using the Identity Management tool'. The tool had been replaced. He locked out the recovery account instead. Step 5 said 'see Appendix B', which never existed.",
        "org_incentive": "Process documentation is evidence that a security programme exists. Evidence is what you show to enterprise clients. Whether the process describes current infrastructure is an operational matter, and the operational team is too busy following the old process to update it.",
        "impact": "The post-incident review recommended updating all processes. The task was assigned to a disbanded team. It remained open for 8 months, then auto-closed for 'no activity'. A new process was created to manage process updates. It referenced the missing Appendix B.",
    },
    {
        "name": "Backups exist",
        "claim": "Critical data is protected by automated daily backups, retained for 30 days, with offsite replication and end to end encryption.",
        "operational_reality": "Backup completion emails go to a distribution list that includes 3 departed employees and a shared mailbox no one monitors. One team member has a rule moving these emails to a folder labelled 'Do Not Read', which contains 47,000 unread messages.",
        "failure_mode": "Ransomware encrypted the file share at 14:13. The backup ran at 3:00 and produced a perfect encrypted copy, faithfully preserving the ransomware. Offsite replication at 4:00 created a second pristine encrypted copy. Both were retained for 30 days.",
        "org_incentive": "Client questionnaires ask 'Do you perform daily backups?' The answer is yes, supported by a screenshot. The optional follow up 'Do you test restores?' appears in an 'advanced' section. Most clients skip it. Those who ask are told testing is quarterly, which is true if you count the test that failed 11 months ago.",
        "impact": "The ransom was paid using company bitcoin. A post mortem identified 16 improvements, added to the security roadmap where they joined 13 from the previous incident and 9 from the one before that. The roadmap was approved by the committee that had no quorum.",
    },
    {
        "name": "Staff know the plan",
        "claim": "All staff with incident response responsibilities complete annual training and have access to the current Incident Response Plan.",
        "operational_reality": "The Incident Response Plan is a PDF last updated 18 months ago. The infrastructure it describes was decommissioned 14 months ago. Staff complete training by clicking through a web module. The answers 'C, A, D, B, A' are shared in a WhatsApp group called 'Compliance is a Joke'.",
        "failure_mode": "When the alert fired, the team followed Section 7, 'Contact Network Operations Centre'. The NOC had been outsourced in January. The emergency number was in Appendix C, which said 'see attached file', the same missing attachment from Appendix B. They spent 45 minutes searching for a file that never existed.",
        "org_incentive": "Training completion rates are reported to the board each quarter. The board sees 92–96% and says 'excellent'. No one reports the accuracy of the plan, because that would require comparing it to the current environment. That comparison produced 412 discrepancies, filed and forgotten.",
        "impact": "The incident lasted 11 hours, with 3 teams following 3 different plans. The finance team restored from encrypted backups. The infrastructure team called the outsourced NOC. The security team notified a legal contact who had resigned. The post mortem concluded that communication was the main issue.",
    },
    {
        "name": "Network segmentation is enforced",
        "claim": "The network follows a zero trust architecture with strict controls governing lateral movement between production, corporate, and guest zones.",
        "operational_reality": "The network diagram was drawn by a consultant in 2021. The live network has 14 'temporary' firewall rules added since then to fix incidents, unblock vendors, and let a coffee machine reach its config server. No one removes them because breaking something would need a CAB meeting.",
        "failure_mode": "The attacker joined the guest WiFi via a temporary rule from a 2022 vendor demo. The vendor left. The rule did not. From there, he pivoted to the domain controller using a rule added for the coffee machine to authenticate. The coffee machine had been mining cryptocurrency for 6 months.",
        "org_incentive": "The security team shows the consultant's diagram to auditors. The network team maintains the real rules and has never seen the diagram, stored on the decommissioned SharePoint. No process exists to compare them, because that would admit that temporary rules became permanent, triggering a governance review no one wants.",
        "impact": "The attacker had full estate access for 6 days. After the incident, the diagram was updated to reflect reality and marked 'Internal use only. Draft not for external distribution'. The Patch Committee requested a copy but could not receive it because the file exceeded the email attachment size limit.",
    },
    {
        "name": "Credentials are rotated",
        "claim": "Privileged accounts are subject to mandatory 90 day rotation, enforced through the Privileged Access Management platform with audit trails.",
        "operational_reality": "The PAM platform manages 847 human accounts. It does not manage 340 service accounts created before 2020. Rotating them would require locating every service that uses them, which would require nonexistent documentation. So they are marked 'excluded from scope', and no one asks.",
        "failure_mode": "The compromised credential was 4 years old, belonging to a heating contractor's service account. The contract ended 18 months earlier. The account was renewed twice by an automated process responding to a shared mailbox, which generated new passwords stored in a text file on the same system later compromised.",
        "org_incentive": "The PAM dashboard shows 100% compliance for managed accounts. Internal audit sees the dashboard. The auditor used to work on the network team and knows excluded accounts cannot be rotated without breaking production. The audit report says 'satisfactory'.",
        "impact": "A forensic review found 212 accounts with credentials older than 2 years. High priority cases were remediated within 90 days. After the attacker had left. The rest were reviewed at the next annual planning cycle, where resource constraints were noted. The heating contractor's account was not on the list because the review excluded unmanaged accounts.",
    },
    {
        "name": "Monitoring is active",
        "claim": "The Security Operations Centre provides 24/7 monitoring with automated alerting and a mean time to detect of under 4 hours for all critical assets.",
        "operational_reality": "The SOC monitors an 'assets in scope' list last updated in 2021. It excludes cloud workloads after Q2 2022, 3 decommissioning datacentres, and any system ever connected to guest WiFi. Staff mark new systems as 'temporary' to avoid a 30 page onboarding form.",
        "failure_mode": "The attacker operated freely in an acquired subsidiary for 63 days. The subsidiary was never added to monitoring scope because the form needed a signature from a director on gardening leave for 10 months. The SOC dashboard showed no alerts. The dashboard was technically correct.",
        "org_incentive": "The SOC contract measures service level compliance against the defined asset list. Procurement renews annually, unaware the list is outdated. The SOC provider reports 99.99% availability against the list. The gap between list and actual estate is not a service level metric, so it does not exist.",
        "impact": "The board voted to monitor all critical assets. 'Critical' was defined as any system in the 2021 asset list that has a ticket in the CAB queue. The attacker used a different definition, which included the subsidiary's domain controller. The monitoring extension was descoped 6 weeks later due to budget constraints.",
    },
    {
        "name": "Backups are tested",
        "claim": "Backup integrity is validated through quarterly restore tests, with results documented and reviewed by the IT Security Committee.",
        "operational_reality": "The last successful restore test was 11 months ago. Subsequent tests were deferred 'due to operational pressures', which is the standard phrase when the team is too busy but wants to keep the ticket open. The team jokes that the backups are 'probably fine', a phrase in 3 consecutive risk registers.",
        "failure_mode": "When the required test finally ran, the backup agent had been silently failing for 5 months after a routine update. The agent reported success because the update changed logging from 'error' to 'info', and the monitoring script only looked for the word 'success'. Backups were complete, encrypted, and unrestorable: the encryption key had been rotated and the new key never stored.",
        "org_incentive": "The audit requirement is to have a restore test schedule. The team has a schedule. The auditor checks the schedule and marks the control as compliant. The auditor does not attend the test, scheduled for a weekend. The team has learned that the schedule is the compliance artefact, not the test results.",
        "impact": "Recovery took 4 days and cost €2.3 million. A new quarterly backup testing schedule was implemented immediately. It was identical to the previous one, except 'quarterly' was replaced with 'annual' to improve the team's ability to meet it. The IT Security Committee approved by email, not having met in person for 14 months.",
    },
    {
        "name": "Vendor access is controlled",
        "claim": "Third party access is governed by a formal process with time limited credentials, activity logging, and annual reviews by the business owner.",
        "operational_reality": "The annual review is an email to the 'business owner' listed in the vendor system. The owner has usually moved teams or left. Recipients have learned that replying 'still required' is the fastest way to close the email. No one ever replies 'revoke' because that might break something and create work.",
        "failure_mode": "The attacker used credentials from a heating contractor whose engagement ended 18 months earlier. The credentials were renewed twice because a shared mailbox auto-replied 'approved, please send new credentials' to expiry notifications. The original business owner had left. His replacement had also left. The current occupant archived the review email without reading.",
        "org_incentive": "Vendor offboarding requires coordination between procurement, IT security, and the business unit. This coordination is no one's primary job. Procurement says it is security's job. Security says it is procurement's job. The business unit says it is 'someone else's problem'.",
        "impact": "After the breach, all vendor accounts were suspended. 17 belonged to expired contracts. 3 belonged to vendors no one could identify. One belonged to the building's previous tenant that moved out in 2020. The heating contractor's account was not suspended because the list came from the PAM dashboard, which excluded unmanaged accounts.",
    },
    {
        "name": "Change management is followed",
        "claim": "All production changes are subject to formal impact assessment, rollback planning, and Change Advisory Board approval, with emergency changes reviewed retrospectively.",
        "operational_reality": "The emergency change procedure bypasses the CAB when 'waiting would cause unacceptable risk'. Senior managers called at 11pm find most risks unacceptable. The retrospective review is an email to the same managers, who reply 'noted' and close the ticket. The rollback plan is typically 'we will fix it in the morning'.",
        "failure_mode": "A change was raised as emergency at 23:43 because a security tool blocked transactions. The approving manager signed at 23:44 without reading, watching a film. It caused a 9-hour outage. Post incident review called it a 'process compliance success': the form was filed correctly, including a rollback plan from 2019, stored on decommissioned SharePoint drive.",
        "org_incentive": "A correctly filed emergency change form, regardless of outcome, means the process was followed. The process exists to protect the organisation from unauthorised changes. The organisation is not the same as its systems, customers, or the heating contractor's shared mailbox. The change manager is measured on form completion rates, not outage hours. Bonus paid in full.",
        "impact": "The outage cost €400,000 and affected 23,000 customers. The change manager received a commendation. The approving manager was asked to complete additional training. The Understanding Temporary Firewall Rules training, 94% completion rate among staff including 3 employees who left in 2022, was marked 'training complete'.",
    },
]


@recipes_blueprint.route('/')
def recipes():
    return render_template('recipes/recipes.html', concepts=CONCEPTS)


@recipes_blueprint.route('/portfolio/')
def portfolio_recipes():
    return render_template('recipes/portfolio.html')

@recipes_blueprint.route('/services/')
def services_recipes():
    return render_template('recipes/services.html')


@recipes_blueprint.route('/about/')
def about():
    return render_template('recipes/about.html')


@recipes_blueprint.route('/documents/')
def documents():
    return render_template('recipes/documents.html')


@recipes_blueprint.route('/404/')
def fourohfour_recipes():
    return render_template('recipes/404.html')


@recipes_blueprint.route("/contact/")
def contact():
    return render_template("recipes/contact.html")


@recipes_blueprint.route("/thankyou/")
def thankyou():
    return render_template("recipes/thankyou.html")

