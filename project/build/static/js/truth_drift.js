const CONCEPTS = JSON.parse(document.getElementById('concepts-data').textContent);

const LENSES = [
    { key: 'claim',               label: 'The Organisational Narrative' },
    { key: 'operational_reality', label: 'The Operational Reality'       },
    { key: 'failure_mode',        label: 'How It Fails'                  },
    { key: 'org_incentive',       label: 'Why It Persists'               },
];

let current = 0;

function render(index) {
    const lens = LENSES[index];

    document.querySelectorAll('.drift-step').forEach(function(el, i) {
        el.classList.toggle('active', i === index);
    });

    const grid = document.getElementById('drift-grid');
    grid.innerHTML = '';
    CONCEPTS.forEach(function(concept) {
        const card = document.createElement('div');
        card.className = 'drift-card';
        const name = document.createElement('h3');
        name.className = 'drift-card-name';
        name.textContent = concept.name;
        const text = document.createElement('p');
        text.className = 'drift-card-text';
        text.textContent = concept[lens.key];
        card.appendChild(name);
        card.appendChild(text);
        grid.appendChild(card);
    });

    const prev = document.getElementById('drift-prev');
    const next = document.getElementById('drift-next');
    prev.disabled = (index === 0);
    if (index < LENSES.length - 1) {
        next.textContent = LENSES[index + 1].label + ' →';
        next.disabled = false;
    } else {
        next.textContent = '← Start over';
        next.disabled = false;
    }
}

document.getElementById('drift-next').addEventListener('click', function() {
    current = (current + 1) % LENSES.length;
    render(current);
});

document.getElementById('drift-prev').addEventListener('click', function() {
    if (current > 0) { current--; render(current); }
});

document.querySelectorAll('.drift-step').forEach(function(el) {
    el.addEventListener('click', function() {
        current = parseInt(el.dataset.index, 10);
        render(current);
    });
});

render(0);