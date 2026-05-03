from . import recipes_blueprint
from flask import render_template


awareness_recipes_names = []
pentesting_recipes_names = []
teaming_recipes_names = []


CONCEPTS = [
    {
        "name": "Patching is regular",
        "claim": "All systems are patched on schedule",
        "operational_reality": "Patches are staged, delayed, or skipped when they conflict with uptime requirements",
        "failure_mode": "Zero-day exploits target unpatched dependencies that no team claims ownership of",
        "org_incentive": "Patch compliance reports satisfy auditors; actual coverage is never independently verified",
    },
    {
        "name": "Logs arrive on time",
        "claim": "Centralised logging ensures full visibility across all systems",
        "operational_reality": "Log pipelines drop events under load; timestamps drift; some sources never connected",
        "failure_mode": "Incidents are reconstructed from fragments; the relevant logs were never collected",
        "org_incentive": "A SIEM deployment counts as logging regardless of what actually reaches it",
    },
    {
        "name": "Someone owns this decision",
        "claim": "All security decisions have clear ownership and accountability",
        "operational_reality": "Cross-team ownership gaps persist indefinitely through escalation chains that resolve nothing",
        "failure_mode": "The attack surface that nobody owns is exactly what attackers find first",
        "org_incentive": "RACI matrices document who to blame, not who has the authority or capacity to act",
    },
    {
        "name": "Processes are followed",
        "claim": "Documented procedures ensure consistent and compliant operations",
        "operational_reality": "Under pressure, informal workarounds replace formal procedures and are never documented",
        "failure_mode": "The workaround used during the incident was the one nobody trained for",
        "org_incentive": "Process documentation satisfies audits; process adherence is measured by nobody",
    },
    {
        "name": "Backups exist",
        "claim": "All critical data is backed up according to retention policy",
        "operational_reality": "Backup jobs run silently and report success; failure notifications go to a mailbox nobody monitors",
        "failure_mode": "The ransomware encrypted the backups first, before anyone verified they were separate",
        "org_incentive": "Backup existence is a compliance checkbox; backup recoverability is an optional exercise",
    },
    {
        "name": "Staff know the plan",
        "claim": "All staff have been trained on incident response procedures",
        "operational_reality": "Training records are current; the plan itself was last updated before the last two infrastructure migrations",
        "failure_mode": "Staff follow the plan correctly; the plan describes systems that no longer exist",
        "org_incentive": "Training completion rates are reported to the board; plan accuracy is not",
    },
    {
        "name": "Network segmentation is enforced",
        "claim": "Network segmentation limits blast radius across all critical zones",
        "operational_reality": "Segmentation rules exist in policy; firewall configurations diverged from policy two years ago",
        "failure_mode": "Lateral movement succeeded because the segmentation was documented but not deployed",
        "org_incentive": "Network architecture diagrams show clean separation; diagrams are not validated against running config",
    },
    {
        "name": "Credentials are rotated",
        "claim": "Privileged credentials are rotated on schedule according to policy",
        "operational_reality": "Service accounts with hardcoded credentials predate the rotation policy and are excluded from it",
        "failure_mode": "The compromised credential was three years old and exempt from rotation for compatibility reasons",
        "org_incentive": "Rotation metrics track managed accounts; unmanaged accounts are not counted",
    },
    {
        "name": "Monitoring is active",
        "claim": "Continuous monitoring detects threats across the environment in real time",
        "operational_reality": "Monitoring covers the documented environment; shadow IT, legacy systems, and OT are out of scope",
        "failure_mode": "The intrusion dwell time was 47 days because the affected systems were not in scope",
        "org_incentive": "SOC dashboards show green; scope exclusions are not shown on dashboards",
    },
    {
        "name": "Backups are tested",
        "claim": "Backup integrity is verified through regular restore testing",
        "operational_reality": "Restore tests were last completed 14 months ago; the next test is scheduled but not prioritised",
        "failure_mode": "The backup format changed silently; restores from the last six months produce corrupted output",
        "org_incentive": "Backup testing is scheduled annually; the schedule is the compliance artefact, not the result",
    },
    {
        "name": "Vendor access is controlled",
        "claim": "Third-party vendor access is managed through formal access request and review processes",
        "operational_reality": "Vendor accounts persist after contract end because offboarding requires manual cross-team coordination",
        "failure_mode": "The breach originated from a vendor account that had been inactive for eight months",
        "org_incentive": "Vendor access reviews are a procurement requirement; operations teams are not in procurement's chain of command",
    },
    {
        "name": "Change management is followed",
        "claim": "All changes to production systems are approved through the change management process",
        "operational_reality": "Emergency changes bypass the process; emergency is a classification that teams self-assign",
        "failure_mode": "The change that caused the outage was emergency-classified; post-incident review found it was not urgent",
        "org_incentive": "Change management reduces liability; the emergency exception exists because uptime pressure exceeds process adherence",
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

