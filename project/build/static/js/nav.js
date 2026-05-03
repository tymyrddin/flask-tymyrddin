(function() {
    var btn = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!btn || !nav) return;
    btn.addEventListener('click', function() {
        var open = nav.style.display !== 'block';
        nav.style.display = open ? 'block' : '';
        btn.setAttribute('aria-expanded', String(open));
    });
})();
