(function () {
    'use strict';

    const rules = JSON.parse(document.getElementById('translation-rules').textContent);

    const americanToBritish = [
        [/\bbehavioral\b/gi, 'behavioural'],
        [/\bbehavior\b/gi, 'behaviour'],
        [/\bprogram\b/gi, 'programme'],
        [/\bcategorized\b/gi, 'categorised'],
        [/\bcategorization\b/gi, 'categorisation'],
        [/\brecognized\b/gi, 'recognised'],
        [/\bauthorized\b/gi, 'authorised'],
        [/\bunauthorized\b/gi, 'unauthorised'],
        [/\bauthorization\b/gi, 'authorisation'],
        [/\borganization\b/gi, 'organisation'],
        [/\borganizational\b/gi, 'organisational'],
        [/\borganized\b/gi, 'organised'],
        [/\bprioritized\b/gi, 'prioritised'],
        [/\brealized\b/gi, 'realised'],
        [/\butilized\b/gi, 'utilised'],
        [/\bnormalized\b/gi, 'normalised'],
        [/\bminimized\b/gi, 'minimised'],
        [/\bpublicized\b/gi, 'publicised'],
        [/\banalyzed\b/gi, 'analysed'],
        [/\banalyze\b/gi, 'analyse'],
    ];

    function normalizeSpelling(text) {
        let t = text;
        for (const [pattern, replacement] of americanToBritish) {
            t = t.replace(pattern, replacement);
        }
        return t;
    }

    function isPattern(kw) {
        return kw.includes('.*') || kw.includes('\\b');
    }

    function matchesInput(kw, text) {
        if (isPattern(kw)) {
            return new RegExp(kw, 'i').test(text);
        }
        return text.toLowerCase().includes(kw.toLowerCase());
    }

    function getFragment(text, kw) {
        let index, matchLen;
        if (isPattern(kw)) {
            const m = new RegExp(kw, 'i').exec(text);
            if (!m) return null;
            index = m.index;
            matchLen = m[0].length;
        } else {
            index = text.toLowerCase().indexOf(kw.toLowerCase());
            if (index === -1) return null;
            matchLen = kw.length;
        }
        const start = Math.max(0, index - 35);
        const end = Math.min(text.length, index + matchLen + 65);
        let fragment = text.substring(start, end).trim();
        if (start > 0) fragment = '…' + fragment;
        if (end < text.length) fragment = fragment + '…';
        return fragment;
    }

    function buildTable() {
        const input = document.getElementById('incident-input').value.trim();
        if (!input) {
            document.getElementById('incident-input').focus();
            return;
        }

        const normalizedInput = normalizeSpelling(input);

        const matches = [];
        rules.forEach(function (rule) {
            for (var i = 0; i < rule.keywords.length; i++) {
                if (matchesInput(rule.keywords[i], normalizedInput)) {
                    matches.push({
                        fragment: getFragment(normalizedInput, rule.keywords[i]) || normalizedInput.substring(0, 100),
                        official: rule.official,
                        subtext: rule.subtext
                    });
                    break;
                }
            }
        });

        const tbody = document.getElementById('translation-tbody');
        tbody.innerHTML = '';

        if (matches.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = 3;
            td.className = 'no-matches';
            td.textContent = 'No recognised terminology identified. That language is simply not in the dataset yet, which is a gap rather than a verdict. Review and try again.';
            tr.appendChild(td);
            tbody.appendChild(tr);
        } else {
            matches.forEach(function (m) {
                const tr = document.createElement('tr');

                const tdFrag = document.createElement('td');
                tdFrag.className = 'col-submitted';
                tdFrag.textContent = m.fragment;

                const tdOff = document.createElement('td');
                tdOff.className = 'col-official';
                tdOff.textContent = m.official;

                const tdSub = document.createElement('td');
                tdSub.className = 'col-subtext';
                tdSub.textContent = m.subtext;

                tr.appendChild(tdFrag);
                tr.appendChild(tdOff);
                tr.appendChild(tdSub);
                tbody.appendChild(tr);
            });
        }

        document.getElementById('pir-or-input').textContent = input;
        document.getElementById('incident-form-section').style.display = 'none';
        document.getElementById('translation-output').style.display = 'block';
        window.scrollTo(0, 0);
    }

    function resetForm() {
        document.getElementById('incident-input').value = '';
        document.getElementById('translation-output').style.display = 'none';
        document.getElementById('incident-form-section').style.display = 'block';
        window.scrollTo(0, 0);
    }

    document.getElementById('translate-btn').addEventListener('click', buildTable);
    document.getElementById('translate-again-btn').addEventListener('click', resetForm);

}());