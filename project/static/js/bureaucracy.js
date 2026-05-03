(function () {
    'use strict';

    const PHRASE_BANK = JSON.parse(document.getElementById('phrase-bank-data').textContent);

    const state = {
        stage: 'submit',
        systemType: 'it',
        severity: 'medium',
        urgency: 'routine',
        description: '',
        seed: 0,
        refNumber: '',
        auditLog: [],
        submissionCount: 0,
    };

    // --- Seeded RNG (djb2 hash + LCG) ---

    function hashStr(s) {
        let h = 0;
        for (let i = 0; i < s.length; i++) {
            h = (Math.imul(31, h) + s.charCodeAt(i)) | 0;
        }
        return Math.abs(h);
    }

    function seededRand(seed, n) {
        let s = (seed + n * 2654435761) >>> 0;
        s = Math.imul(s ^ (s >>> 16), 0x45d9f3b);
        s = Math.imul(s ^ (s >>> 16), 0x45d9f3b);
        return (s >>> 0) / 0xFFFFFFFF;
    }

    let pickCounter = 0;

    function pick(arr) {
        if (!arr || arr.length === 0) return '';
        return arr[Math.floor(seededRand(state.seed, pickCounter++) * arr.length)];
    }

    function getBank(domain, category) {
        const d = PHRASE_BANK[domain];
        if (d && d[category] && d[category].length) return d[category];
        if (domain === 'hybrid' && PHRASE_BANK.ot && PHRASE_BANK.ot[category]) {
            return PHRASE_BANK.ot[category];
        }
        return [];
    }

    function genRefNumber() {
        const year = new Date().getFullYear();
        const num = String(Math.floor(seededRand(state.seed, 97) * 9999)).padStart(4, '0');
        return 'SEC-' + year + '-' + num;
    }

    // --- Audit trail ---

    const REWRITES = [
        [/\bsecurity concern\b/gi, 'process-adjacent observational input'],
        [/\breported\b/gi, 'received and logged per intake protocol'],
        [/\burgent\b/gi, 'time-sensitive (routing subject to standard governance timeline)'],
        [/\bhigh severity\b/gi, 'elevated concern classification (tier pending formal taxonomy)'],
        [/\bcritical\b/gi, 'tier-1 classified (formal priority assignment pending)'],
        [/\baffected system\b/gi, 'system under assessment'],
        [/\bno immediate action\b/gi, 'no action required at this governance cycle'],
    ];

    function bureaucratise(text) {
        return REWRITES.reduce((t, [re, rep]) => t.replace(re, rep), text);
    }

    function addAuditEntry(text) {
        const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
        state.auditLog.push({ ts, text });
    }

    function renderAuditTrail() {
        const list = document.getElementById('audit-list');
        list.innerHTML = '';
        state.auditLog.forEach(entry => {
            const li = document.createElement('li');
            const stamp = document.createElement('span');
            stamp.className = 'audit-timestamp';
            stamp.textContent = entry.ts + ' ';
            li.appendChild(stamp);
            li.appendChild(document.createTextNode(bureaucratise(entry.text)));
            list.appendChild(li);
        });
    }

    // --- Stage navigation ---

    const STAGE_ORDER = ['submit', 'classify', 'route', 'review', 'close'];

    function renderStage(stageName) {
        state.stage = stageName;
        document.querySelectorAll('.stage-panel').forEach(p => p.classList.remove('stage-active'));
        const panel = document.getElementById('stage-' + stageName);
        if (panel) {
            panel.classList.add('stage-active');
            panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        const stageIdx = STAGE_ORDER.indexOf(stageName);
        STAGE_ORDER.forEach((s, i) => {
            const dot = document.getElementById('progress-' + s);
            if (!dot) return;
            dot.classList.remove('active', 'complete');
            if (i === stageIdx) dot.classList.add('active');
            else if (i < stageIdx) dot.classList.add('complete');
        });
        renderAuditTrail();
    }

    // --- DOM helpers (textContent only — no innerHTML with user data) ---

    function addField(container, label, value, extraClass) {
        const div = document.createElement('div');
        div.className = 'generated-field';
        const lbl = document.createElement('span');
        lbl.className = 'field-label';
        lbl.textContent = label;
        const val = document.createElement('span');
        val.className = 'field-value' + (extraClass ? ' ' + extraClass : '');
        val.textContent = value;
        div.appendChild(lbl);
        div.appendChild(val);
        container.appendChild(div);
    }

    function makeButton(text, className, handler) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = className;
        btn.textContent = text;
        btn.addEventListener('click', handler);
        return btn;
    }

    function clearBody(stageId) {
        const body = document.querySelector('#' + stageId + ' .stage-body');
        body.innerHTML = '';
        return body;
    }

    // --- Stage: Submit ---

    function submitConcern() {
        const desc = document.getElementById('concern-description').value.trim();
        if (!desc) {
            document.getElementById('concern-description').focus();
            return;
        }
        state.description = desc;
        state.systemType = document.getElementById('system-type').value;
        state.severity = document.getElementById('severity').value;
        state.urgency = document.getElementById('urgency').value;
        state.seed = hashStr(desc + state.systemType);
        pickCounter = 0;

        addAuditEntry(
            'Security concern submitted. Severity: ' + state.severity +
            '. Urgency: ' + state.urgency + '.'
        );
        buildClassifyPanel();
        renderStage('classify');
    }

    // --- Stage: Classify ---

    function buildClassifyPanel() {
        const domain = state.systemType;
        const refNum = genRefNumber();
        state.refNumber = refNum;

        const severityMap = {
            low: 'Tier 4 — Low-Confidence Signal',
            medium: 'Tier 3 — Pending Formal Assessment',
            high: 'Tier 2 — Elevated Concern (Unverified)',
            critical: 'Tier 1 — Priority Classification (Review Pending)',
        };
        const urgencyMap = {
            routine: 'Standard Governance Timeline',
            elevated: 'Elevated (Subject to Scheduling Availability)',
            immediate: 'Immediate (Routed via Standard Process)',
        };

        let phrase1, phrase2;
        if (domain === 'ot') {
            phrase1 = pick(getBank('ot', 'safety_constraint'));
            phrase2 = pick(getBank('ot', 'change_control'));
        } else if (domain === 'hybrid') {
            phrase1 = pick(getBank('hybrid', 'classify'));
            phrase2 = pick(getBank('ot', 'vendor_lock'));
        } else {
            phrase1 = pick(getBank('it', 'classify'));
            phrase2 = pick(getBank('it', 'intake'));
        }

        const body = clearBody('stage-classify');
        addField(body, 'Reference Number', refNum, 'ref-number');
        addField(body, 'Concern Classification', severityMap[state.severity] || state.severity);
        addField(body, 'Operational Impact Category', urgencyMap[state.urgency] || state.urgency);
        addField(body, 'Domain Assessment', phrase1);
        addField(body, 'Governance Constraint', phrase2);
        body.appendChild(makeButton('Acknowledge Classification', 'proc-btn proc-btn-primary', function () {
            addAuditEntry('Concern classified. Reference: ' + refNum + '. Acknowledged by submitter.');
            buildRoutePanel();
            renderStage('route');
        }));
    }

    // --- Stage: Route ---

    function buildRoutePanel() {
        const domain = state.systemType;

        const otTeams = [
            ['Process Safety Engineering', 'safety validation review'],
            ['OT/ICS Integration Group', 'control system impact assessment'],
            ['Vendor Liaison Authority', 'OEM certification requirement'],
        ];
        const itTeams = [
            ['Application Security Team', 'technical remediation scoping'],
            ['Risk Management Committee', 'formal risk acceptance process'],
            ['Change Advisory Board', 'scheduling within next change window'],
        ];
        const hybridTeams = [
            ['IT Security Operations', 'IT-side assessment'],
            ['OT Engineering Authority', 'OT-side assessment'],
            ['IT/OT Convergence Working Group', 'boundary determination (formation pending)'],
        ];

        const teams = domain === 'ot' ? otTeams : domain === 'hybrid' ? hybridTeams : itTeams;

        let routeNote;
        if (domain === 'ot') routeNote = pick(getBank('ot', 'downtime'));
        else if (domain === 'hybrid') routeNote = pick(getBank('hybrid', 'route'));
        else routeNote = pick(getBank('it', 'route'));

        const body = clearBody('stage-route');

        const note = document.createElement('p');
        note.className = 'routing-note';
        note.textContent = routeNote;
        body.appendChild(note);

        const ul = document.createElement('ul');
        ul.className = 'routing-log';

        teams.forEach(([team, reason]) => {
            const li = document.createElement('li');
            const teamSpan = document.createElement('span');
            teamSpan.className = 'routing-team';
            teamSpan.textContent = team;
            const reasonSpan = document.createElement('span');
            reasonSpan.className = 'routing-reason';
            reasonSpan.textContent = reason;
            li.appendChild(teamSpan);
            li.appendChild(reasonSpan);
            ul.appendChild(li);
        });

        const unassigned = document.createElement('li');
        unassigned.className = 'routing-unassigned';
        const ownerLabel = document.createElement('span');
        ownerLabel.textContent = 'Current Owner';
        const ownerValue = document.createElement('span');
        ownerValue.className = 'routing-owner-unassigned';
        ownerValue.textContent = 'Unassigned — routing determination in progress';
        unassigned.appendChild(ownerLabel);
        unassigned.appendChild(ownerValue);
        ul.appendChild(unassigned);

        body.appendChild(ul);
        body.appendChild(makeButton('Proceed to Assessment', 'proc-btn proc-btn-primary', function () {
            addAuditEntry('Concern routed to ' + teams.length + ' stakeholders. Owner unassigned.');
            buildReviewPanel();
            renderStage('review');
        }));
    }

    // --- Stage: Review ---

    function buildReviewPanel() {
        const domain = state.systemType;

        const doubtHeaders = [
            'Based on available evidence, the concern as submitted cannot be independently verified.',
            'The described behaviour falls within documented operational parameters.',
            'Insufficient telemetry to confirm the reported deviation.',
        ];
        const headerIdx = Math.floor(seededRand(state.seed, 50) * doubtHeaders.length);

        let phrase1, phrase2;
        if (domain === 'ot') {
            phrase1 = pick(getBank('ot', 'monitoring'));
            phrase2 = pick(getBank('ot', 'risk'));
        } else if (domain === 'hybrid') {
            phrase1 = pick(getBank('hybrid', 'review'));
            phrase2 = pick(getBank('ot', 'monitoring'));
        } else {
            phrase1 = pick(getBank('it', 'review'));
            phrase2 = pick(getBank('it', 'classify'));
        }

        const rsi = (1.0 + seededRand(state.seed, 51) * 8.0).toFixed(1);

        const body = clearBody('stage-review');

        const header = document.createElement('p');
        header.className = 'review-doubt-header';
        header.textContent = doubtHeaders[headerIdx];
        body.appendChild(header);

        addField(body, 'Assessment Finding', phrase1);
        addField(body, 'Risk Characterisation', phrase2);

        const scoreBlock = document.createElement('div');
        scoreBlock.className = 'risk-score-block';
        scoreBlock.textContent = 'RSI: ' + rsi + ' (methodology: SEC-RM-7, Annex B)';
        body.appendChild(scoreBlock);

        body.appendChild(makeButton('Confirm Assessment', 'proc-btn proc-btn-primary', function () {
            addAuditEntry('Preliminary assessment complete. RSI: ' + rsi + '. No immediate action recommended.');
            buildClosePanel();
            renderStage('close');
        }));
    }

    // --- Stage: Close ---

    function buildClosePanel() {
        const domain = state.systemType;

        let closeReason;
        if (state.submissionCount > 0) {
            closeReason = 'Duplicate: concern merged with previous submission ' + state.refNumber + '.';
        } else {
            let pool;
            if (domain === 'hybrid') pool = getBank('hybrid', 'close');
            else if (domain === 'ot') pool = PHRASE_BANK.close_reasons || [];
            else pool = getBank('it', 'close');
            if (!pool.length) pool = PHRASE_BANK.close_reasons || [];
            closeReason = pick(pool);
        }

        const body = clearBody('stage-close');

        const notice = document.createElement('div');
        notice.className = 'closure-notice';
        const reason = document.createElement('p');
        reason.className = 'close-reason';
        reason.textContent = closeReason;
        const footer = document.createElement('p');
        footer.className = 'close-footer';
        footer.textContent = 'This matter is now closed. If conditions change, a new submission may be initiated via the standard intake process.';
        notice.appendChild(reason);
        notice.appendChild(footer);
        body.appendChild(notice);

        addField(body, 'Closure Reference', state.refNumber, 'ref-number');
        addField(body, 'Closed By', 'Automated Process Governance System v2.4');

        const btnRow = document.createElement('div');
        btnRow.className = 'close-btn-row';

        const inversionBtn = makeToggleButton('View Operational Record', 'Hide Operational Record', function (panel) {
            buildInversionContent(panel);
        });
        const reconstructBtn = makeToggleButton('Generate Compliance Narrative', 'Hide Compliance Narrative', function (panel) {
            buildReconstructionContent(panel);
        });
        const resubmitBtn = makeButton('Submit New Concern', 'proc-btn proc-btn-secondary', resubmit);

        btnRow.appendChild(inversionBtn);
        btnRow.appendChild(reconstructBtn);
        btnRow.appendChild(resubmitBtn);
        body.appendChild(btnRow);

        addAuditEntry('Concern closed. Reason: ' + closeReason);
    }

    // --- Incident inversion mode ---

    const INSTITUTIONAL_TRANSFORMS = [
        [/\bfound\b/gi, 'identified'],
        [/\bnoticed\b|\bsaw\b/gi, 'observed'],
        [/\bproblem\b/gi, 'deviation'],
        [/\bbug\b/gi, 'defect'],
        [/\bhacked\b/gi, 'subject to unauthorised access'],
        [/\bcompromised\b/gi, 'subject to unauthorised access'],
        [/\bvulnerability\b/gi, 'exploitable condition'],
        [/\bvulnerable\b/gi, 'presenting an exploitable condition'],
        [/\bpassword\b/gi, 'credential'],
        [/\bopen port\b/gi, 'unrestricted network service'],
        [/\bopen\b/gi, 'unrestricted'],
        [/\bbroken\b/gi, 'non-compliant'],
        [/\bold\b/gi, 'legacy'],
        [/\battacker\b/gi, 'threat actor'],
        [/\bhacker\b/gi, 'unauthorised party'],
        [/\bexposed\b/gi, 'accessible without adequate controls'],
        [/\bno (auth|authentication)\b/gi, 'absence of authentication controls'],
        [/\bclear(text)?\b/gi, 'unencrypted'],
    ];

    function institutionalise(text) {
        let result = bureaucratise(text);
        INSTITUTIONAL_TRANSFORMS.forEach(([re, rep]) => { result = result.replace(re, rep); });
        return '“' + result + '” No further operational context was retained in the governance record.';
    }

    function buildInversionContent(container) {
        const grid = document.createElement('div');
        grid.className = 'inversion-grid';

        const opBlock = document.createElement('div');
        opBlock.className = 'inversion-block inversion-operational';
        const opLabel = document.createElement('div');
        opLabel.className = 'inversion-label';
        opLabel.textContent = 'Operational reality';
        const opText = document.createElement('p');
        opText.className = 'inversion-text';
        opText.textContent = state.description;
        opBlock.appendChild(opLabel);
        opBlock.appendChild(opText);

        const recBlock = document.createElement('div');
        recBlock.className = 'inversion-block inversion-record';
        const recLabel = document.createElement('div');
        recLabel.className = 'inversion-label';
        recLabel.textContent = 'Official record';
        const recText = document.createElement('p');
        recText.className = 'inversion-text';
        recText.textContent = institutionalise(state.description);
        recBlock.appendChild(recLabel);
        recBlock.appendChild(recText);

        grid.appendChild(opBlock);
        grid.appendChild(recBlock);
        container.appendChild(grid);
    }

    // --- Audit reconstruction mode ---

    function generateComplianceNarrative() {
        const domainLabel = state.systemType === 'ot' ? 'operational technology'
            : state.systemType === 'hybrid' ? 'hybrid IT/OT'
            : 'information technology';
        return [
            'A security-related submission was received and processed in accordance with the established governance framework. The submission was assigned reference ' + state.refNumber + ' and subjected to formal intake procedures applicable to ' + domainLabel + ' environments.',
            'Classification was conducted in accordance with Ref. SEC-PROC-4.2. The submission was assessed against the applicable taxonomy and assigned an appropriate tier designation. All classification activities were completed within the standard governance timeline.',
            'Routing and ownership determination was completed in accordance with Ref. SEC-PROC-7.1. Relevant stakeholders were notified and invited to contribute to the assessment process. Responsibilities were allocated in accordance with the current accountability matrix.',
            'A preliminary assessment was conducted in accordance with Ref. SEC-PROC-9.3. The assessment considered all available evidence and applied the standard risk methodology (SEC-RM-7, Annex B). Findings were documented and communicated to relevant parties in a timely manner.',
            'The matter was resolved in accordance with Ref. SEC-PROC-12.0. The outcome was determined to be consistent with the organisation’s risk appetite and applicable governance requirements. The case was formally closed with full documentation retained for audit purposes.',
            'This record confirms that all activities were conducted in compliance with applicable policies and procedures. No deviations from the standard governance process were recorded.',
        ];
    }

    function buildReconstructionContent(container) {
        const doc = document.createElement('div');
        doc.className = 'compliance-doc';

        const head = document.createElement('div');
        head.className = 'compliance-header';
        const title = document.createElement('h4');
        title.textContent = 'Security Governance Record';
        const subtitle = document.createElement('p');
        subtitle.textContent = 'Ref: ' + state.refNumber + ' | Classification: INTERNAL | Status: CLOSED';
        head.appendChild(title);
        head.appendChild(subtitle);

        const docBody = document.createElement('div');
        docBody.className = 'compliance-body';
        generateComplianceNarrative().forEach(para => {
            const p = document.createElement('p');
            p.textContent = para;
            docBody.appendChild(p);
        });

        doc.appendChild(head);
        doc.appendChild(docBody);
        container.appendChild(doc);
    }

    // --- Toggle helper ---

    function makeToggleButton(labelShow, labelHide, buildContent) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'proc-btn proc-btn-secondary';
        btn.textContent = labelShow;

        const panel = document.createElement('div');
        panel.className = 'toggle-panel';
        panel.style.display = 'none';

        let built = false;
        btn.addEventListener('click', function () {
            if (panel.style.display === 'none') {
                if (!built) { buildContent(panel); built = true; }
                panel.style.display = 'block';
                btn.textContent = labelHide;
            } else {
                panel.style.display = 'none';
                btn.textContent = labelShow;
            }
        });

        const wrapper = document.createElement('span');
        wrapper.appendChild(btn);
        wrapper.appendChild(panel);
        return wrapper;
    }

    // --- Resubmit ---

    function resubmit() {
        state.submissionCount++;
        state.auditLog = [];
        document.getElementById('concern-description').value = '';
        renderStage('submit');
    }

    // --- Event wiring ---

    document.getElementById('btn-submit').addEventListener('click', submitConcern);
    document.getElementById('concern-description').addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) submitConcern();
    });

})();