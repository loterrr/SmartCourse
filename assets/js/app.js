async function postJSON(url, data) {
    var res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    try { return await res.json(); } catch (e) { return null; }
}

function showInlineAlert(message, type, containerId) {
    type = type || 'success';
    var el = containerId ? document.getElementById(containerId) : document.getElementById('alertContainer');
    if (!el) return;
    el.innerHTML = '<div class="alert ' + (type === 'success' ? 'alert-success' : 'alert-error') + '">' + message + '</div>';
}

document.addEventListener('DOMContentLoaded', function() {
    var name = localStorage.getItem('student_name');
    if (name) {
        var userNameEls = document.querySelectorAll('#userName, #profileName');
        userNameEls.forEach(function(e) { if (e) e.textContent = name; });
    }

    document.querySelectorAll('.nav-menu a').forEach(function(a) {
        a.addEventListener('click', function(e) {
            var href = a.getAttribute('href') || '';
            if (href.startsWith('#')) {
                var section = href.substring(1);
                if (typeof window.showSection === 'function') window.showSection(section);
                e.preventDefault();
            }
        });
    });

    if (location.hash && typeof window.showSection === 'function') {
        window.showSection(location.hash.replace('#',''));
    }
});

function logout() {
    try { localStorage.removeItem('student_id'); localStorage.removeItem('student_name'); } catch (e) {}

    window.location.href = 'login.html';
}
window.logout = logout;
