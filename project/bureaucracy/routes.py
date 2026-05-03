from . import bureaucracy_blueprint
from flask import render_template


OT_PHRASES = {
    "safety_constraint": [
        "requires safety impact assessment before any change",
        "not eligible for standard remediation due to safety envelope constraints",
        "operational hazard classification prevents immediate action",
        "requires reassessment under process safety governance",
        "mitigation deferred to maintain safe operating state",
    ],
    "process_dependency": [
        "introduces variability into closed-loop control behaviour",
        "requires validation against physical process constraints",
        "may alter deterministic control timing assumptions",
        "requires recalibration of dependent instrumentation systems",
        "introduces uncertainty into process feedback loop",
    ],
    "vendor_lock": [
        "remediation subject to OEM certification lifecycle",
        "requires alignment with vendor-supported operational envelope",
        "change restricted by proprietary system governance",
        "patching contingent on supplier validation cycle",
        "resolution dependent on external engineering authority",
    ],
    "downtime": [
        "remediation requires scheduled production interruption",
        "cannot be applied outside defined maintenance window",
        "continuous operation constraint prevents immediate intervention",
        "change execution contingent on shutdown approval cycle",
        "availability requirements supersede remediation urgency",
    ],
    "legacy": [
        "remediation constrained by legacy control system dependencies",
        "modification requires full system recertification",
        "legacy process integration prevents isolated patching",
        "change propagation risk across industrial control chain",
        "decommissioning required before secure remediation feasible",
    ],
    "safety_instrumentation": [
        "modification requires validation of safety instrumented functions",
        "interlock integrity must be preserved during remediation",
        "changes subject to emergency shutdown system certification",
        "fail-safe behaviour must remain guaranteed under all conditions",
        "safety layer bypass strictly prohibited without formal waiver",
    ],
    "change_control": [
        "remediation subject to formal Management of Change procedure",
        "requires multi-disciplinary engineering approval cycle",
        "deployment contingent on operational readiness certification",
        "change deferred pending governance alignment across plant stakeholders",
        "requires full revalidation prior to production integration",
    ],
    "monitoring": [
        "visibility constrained by process telemetry limitations",
        "monitoring dependent on historian data fidelity",
        "alarm fatigue affecting signal reliability",
        "sensor calibration drift impacting detection accuracy",
        "observability limited by control system architecture",
    ],
    "incident": [
        "deviation from expected process control behaviour detected",
        "operational state transition outside defined safety envelope",
        "equipment response inconsistent with control logic expectations",
        "loss of process visibility due to telemetry disruption",
        "control system anomaly under investigation",
    ],
    "risk": [
        "risk of deviation from safe operating parameters",
        "risk of uncontrolled process behaviour",
        "risk of cascading operational disruption",
        "risk of failure in safety interlock response",
        "risk of sustained loss of process control integrity",
    ],
}

IT_PHRASES = {
    "intake": [
        "concern logged and assigned to appropriate queue",
        "ticket created and pending triage",
        "issue recorded for review in next sprint cycle",
        "submission acknowledged; SLA clock started",
        "concern captured in risk register for quarterly review",
    ],
    "classify": [
        "classified as informational finding pending severity review",
        "assigned to risk acceptance working group",
        "categorised as out-of-scope for current assessment cycle",
        "reclassified as operational concern rather than security incident",
        "severity downgraded following preliminary assessment",
    ],
    "route": [
        "ownership transferred to application team for remediation",
        "escalated to CAB for next available change window",
        "forwarded to vendor support for root cause analysis",
        "referred to risk management team for formal acceptance",
        "assigned to security architecture for design review",
    ],
    "review": [
        "concern does not meet threshold for immediate action",
        "compensating controls deemed sufficient pending full remediation",
        "risk formally accepted by business owner",
        "finding noted in security backlog for future sprint",
        "issue deferred to next compliance cycle",
    ],
    "close": [
        "closed as accepted risk per enterprise risk framework",
        "resolved via policy exception approval",
        "closed: compensating control documented and approved",
        "marked as tolerated risk, reviewed annually",
        "closed as out of scope for current programme",
    ],
}

HYBRID_PHRASES = {
    "classify": [
        "concern spans IT/OT boundary; ownership determination pending",
        "system type ambiguity requires cross-domain assessment",
        "classified as hybrid risk requiring dual governance track",
        "IT security controls not applicable to OT environment; OT controls not applicable to IT interface",
        "reclassified as integration boundary concern, routed to both domains",
    ],
    "route": [
        "ownership contested between IT security and OT engineering",
        "referred to IT/OT convergence working group for determination",
        "transferred to hybrid systems team, currently being established",
        "neither IT nor OT domain accepts ownership; escalated to programme governance",
        "joint review requested; scheduling pending due to maintenance window conflict",
    ],
    "review": [
        "OT safety constraints prevent IT-standard remediation timeline",
        "IT risk acceptance process does not map to OT change control requirements",
        "cannot be resolved without cross-domain governance framework, currently in draft",
        "hybrid environment lacks unified risk register; concern noted in both",
        "remediation requires coordination that exceeds current programme scope",
    ],
    "close": [
        "closed as organisationally unresolvable at present stage of IT/OT integration",
        "deferred to IT/OT convergence strategy, publication date TBD",
        "formally accepted as residual risk of hybrid architecture",
        "closed: both domains have documented the concern; neither owns the resolution",
        "archived pending establishment of cross-domain governance body",
    ],
}

CLOSE_REASONS = [
    "Accepted risk: concern acknowledged, remediation deferred to next governance cycle.",
    "Out of scope: concern falls outside current programme boundaries.",
    "Duplicate: concern merged with existing registered item.",
    "Resolved via policy: compensating control documented and approved.",
    "Not reproducible: insufficient evidence to substantiate concern as submitted.",
    "Ownership unresolved: concern archived pending governance clarification.",
    "Informational only: no remediation action required at this time.",
]


@bureaucracy_blueprint.route('/bureaucracy/')
def simulator():
    phrase_bank = {
        "ot": OT_PHRASES,
        "it": IT_PHRASES,
        "hybrid": HYBRID_PHRASES,
        "close_reasons": CLOSE_REASONS,
    }
    return render_template('bureaucracy/simulator.html', phrase_bank=phrase_bank)