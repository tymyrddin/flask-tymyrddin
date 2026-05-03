from . import recipes_blueprint
from flask import render_template


awareness_recipes_names = []
pentesting_recipes_names = []
teaming_recipes_names = []


CONCEPTS = [
    {
        "name": "Patching is regular",
        "claim": "All systems are patched on a schedule reviewed quarterly by the Patch Management Committee, subject to operational constraints and Change Advisory Board availability.",
        "operational_reality": "Patches are applied promptly, where 'promptly' is defined in a governance appendix as 'within eighteen months, barring documented exceptions.'",
        "failure_mode": "The patch was available in March. The Change Advisory Board met in November. The attackers were not on the Committee.",
        "org_incentive": "The schedule satisfies the auditor, who checks whether a schedule exists, not whether it is followed. This has suited everyone.",
        "impact": "The CEO announced the company took security extremely seriously and had commissioned an urgent review. The review was conducted by the same consultancy that had certified the patch management process four months earlier. They found areas for improvement.",
    },
    {
        "name": "Logs arrive on time",
        "claim": "A centralised logging platform provides the Security Operations Centre with comprehensive, real-time visibility across the estate.",
        "operational_reality": "Systems configured before 2021 send logs. Everything acquired, migrated, or stood up since then logs locally, into files that are not read.",
        "failure_mode": "The forensic team found the attacker had been present for eleven weeks. The relevant logs did not exist. The dashboard had shown green throughout.",
        "org_incentive": "The SIEM licence is renewed annually. The renewal form asks how many sources are connected. It does not ask what percentage of the estate this represents.",
        "impact": "The incident was declared contained after three weeks. It was subsequently established that 'contained' had been used in the sense of 'we have stopped actively looking.'",
    },
    {
        "name": "Someone owns this decision",
        "claim": "Security ownership is clearly defined through a RACI framework, reviewed annually and endorsed by the Executive Security Steering Committee.",
        "operational_reality": "The RACI assigns ownership to a team restructured in 2021 and dissolved in 2022, whose responsibilities were distributed across four departments, none of which received the RACI.",
        "failure_mode": "The vulnerability waited in the queue for seven months. The owner was identified during the post-incident review. He had left the company in April.",
        "org_incentive": "The RACI demonstrates governance. Governance is what auditors photograph. Whether anyone named in it is still employed is an operational detail.",
        "impact": "A cross-functional working group was formed to establish ownership going forward. It met four times, produced a revised RACI, and was restructured as part of a broader organisational realignment before the RACI could be distributed.",
    },
    {
        "name": "Processes are followed",
        "claim": "Security operations are governed by a mature suite of documented processes, approved by senior management and embedded in operational culture.",
        "operational_reality": "The processes live in a SharePoint migrated twice, accessible via a link in a document titled 'OLD - DO NOT USE - SECURITY PROCS FINAL v3.'",
        "failure_mode": "The on-call engineer followed the process exactly. The process had not been updated to reflect the new authentication system. Step 4 locked out the recovery account.",
        "org_incentive": "Process documentation is evidence of a security programme. The security programme is what is presented to enterprise clients. Adherence is an operational matter.",
        "impact": "The post-incident report recommended updating processes to reflect current infrastructure. This was assigned to the team responsible for the infrastructure that no longer existed, where it awaited resource allocation.",
    },
    {
        "name": "Backups exist",
        "claim": "Critical data is protected by automated daily backups, retained for thirty days, with offsite replication and end-to-end encryption.",
        "operational_reality": "Backup jobs complete and send confirmation emails to a list that includes three departed employees and one who routes these to a folder called 'Automated - Do Not Read.'",
        "failure_mode": "The ransomware encrypted the primary data at 2am. The backup job ran at 3am, as scheduled, and produced a meticulous encrypted copy, retained for thirty days, with offsite replication.",
        "org_incentive": "Backup existence is a line item in client questionnaires. Whether backups are tested appears in the optional section, which is optional.",
        "impact": "The ransom was paid. A lessons-learned exercise identified fourteen improvements to backup procedures. These were added to the security roadmap for the following financial year, where they joined eleven improvements from the previous incident.",
    },
    {
        "name": "Staff know the plan",
        "claim": "All staff with incident response responsibilities complete annual training and have access to the current Incident Response Plan.",
        "operational_reality": "The plan is version 4.2, updated eighteen months ago. The infrastructure it describes was decommissioned fourteen months ago. Training completion is 94%, which is considered excellent.",
        "failure_mode": "The team followed the plan precisely. It directed them to call the Network Operations Centre. The NOC had been outsourced in January. The emergency number was in an appendix referencing an attachment that was not attached.",
        "org_incentive": "Training completion rates are reported to the board. Version currency and operational accuracy are reported to nobody, which keeps the percentages satisfactory.",
        "impact": "The incident took eleven hours to resolve, during which three separate teams followed three separate plans, none describing the same systems. Afterwards, everyone agreed that communication had been the main issue.",
    },
    {
        "name": "Network segmentation is enforced",
        "claim": "The network is segmented according to a zero-trust architecture, with strict controls governing lateral movement between zones.",
        "operational_reality": "The architecture diagram is accurate. Fourteen temporary firewall rules added since 2021 to resolve production incidents are also accurate, and have not been removed in case removing them causes incidents.",
        "failure_mode": "The attacker moved from guest WiFi to the domain controller via a rule created for a vendor demonstration in 2022. The vendor had left. The rule had not.",
        "org_incentive": "The architecture diagram is shown to clients and regulators. Configuration is maintained by a different team and has not been compared to the diagram since the consultant departed.",
        "impact": "The attacker had access to the entire estate for six days before detection. The network architecture diagram was updated to reflect actual configuration. It was classified as internal use only.",
    },
    {
        "name": "Credentials are rotated",
        "claim": "Privileged accounts are subject to mandatory ninety-day rotation, enforced through the Privileged Access Management platform.",
        "operational_reality": "The PAM platform manages 847 accounts. A further 340 service accounts predating the platform are excluded from rotation, as rotating them would require a Change Advisory Board window.",
        "failure_mode": "The compromised credential was four years old, predating the PAM platform, the rotation policy, and two of the three security team members who were unaware it existed.",
        "org_incentive": "The PAM dashboard reports 100% rotation compliance. Unmanaged accounts are not in the dashboard. The dashboard is what is shown during audits. This distinction has not been raised.",
        "impact": "Two hundred and twelve accounts were found to hold credentials older than two years. The highest-priority cases were remediated within ninety days. The remainder were reviewed at the next annual planning cycle, where resourcing constraints were noted.",
    },
    {
        "name": "Monitoring is active",
        "claim": "The Security Operations Centre provides 24/7 monitoring with automated alerting and a mean time to detect of under four hours.",
        "operational_reality": "The SOC monitors systems in scope. Scope was defined in 2021 and excludes cloud workloads post-Q2 2022, the OT network, three legacy datacentres under decommission, and last year's acquisition.",
        "failure_mode": "The attacker operated in the acquired subsidiary for sixty-three days. The SOC showed no alerts. There were no alerts because there was no monitoring. The dashboard was, technically, correct.",
        "org_incentive": "The SOC contract measures SLA compliance against defined assets. Assets are defined at contract renewal. The gap between defined and actual estate is not an SLA metric.",
        "impact": "The board was informed that monitoring had been extended to cover all critical assets. 'Critical' was defined during the same meeting. The definition was somewhat narrower than the one the attacker had been using.",
    },
    {
        "name": "Backups are tested",
        "claim": "Backup integrity is validated through quarterly restore tests, with results documented and reviewed by the IT Security Committee.",
        "operational_reality": "The last restore test was eleven months ago. Subsequent tests were deferred due to conflicting projects, extended leave, and a general consensus that the backups were probably fine.",
        "failure_mode": "The restore test revealed the backup agent had been silently failing for five months following a routine update. The backups were complete, encrypted, and entirely unrestorable.",
        "org_incentive": "The testing schedule is documented and approved. The schedule is the compliance artefact, not the outcome. Auditors are shown the schedule. They are not present for the test.",
        "impact": "Recovery took four days at an estimated cost of €2.3 million. A new quarterly backup testing schedule was implemented. It was identical to the previous quarterly backup testing schedule.",
    },
    {
        "name": "Vendor access is controlled",
        "claim": "Third-party access is governed by a formal process with time-limited credentials, activity logging, and annual access reviews.",
        "operational_reality": "Annual reviews ask the original business owner whether access is still required. The original business owner has typically moved teams and is unaware the vendor relationship still exists.",
        "failure_mode": "The attacker used credentials from a heating contractor whose engagement ended eighteen months prior, renewed twice by a shared mailbox nobody monitored, on behalf of someone who had left.",
        "org_incentive": "Vendor offboarding requires coordination between procurement, IT, and the business unit. This coordination is nobody's primary responsibility and therefore occurs, on average, never.",
        "impact": "All vendor accounts were suspended pending review. Seventeen belonged to vendors whose contracts had expired. Three belonged to vendors nobody could identify. One, on further investigation, appeared to belong to the building's previous tenant.",
    },
    {
        "name": "Change management is followed",
        "claim": "All production changes are subject to formal impact assessment, rollback planning, and Change Advisory Board approval.",
        "operational_reality": "The emergency change procedure allows CAB to be bypassed when waiting would cause unacceptable risk. Senior managers called at 11pm tend to find most risk unacceptable.",
        "failure_mode": "The change was raised as emergency at 11:43pm, approved at 11:44pm, and caused a nine-hour outage. The post-incident review classified it as a process compliance success. The form had been filed correctly.",
        "org_incentive": "A correctly filed emergency change form means the process was followed, regardless of outcome. The process protects the organisation. The organisation is not the same as the systems it operates.",
        "impact": "The outage cost €400,000 and affected 23,000 customers. The change manager received a commendation for ensuring the emergency change form was filed within the required timeframe. The approving manager was asked to complete additional training.",
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

