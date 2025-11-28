// Small helper utilities used by scaffold pages

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

// Small convenience: if the project stores student id in localStorage, we can populate fields automatically.
document.addEventListener('DOMContentLoaded', function() {
    var name = localStorage.getItem('student_name');
    if (name) {
        var userNameEls = document.querySelectorAll('#userName, #profileName');
        userNameEls.forEach(function(e) { if (e) e.textContent = name; });
    }
    // Wire nav links to section loader if available
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
    // On load, if there's a hash, show that section
    if (location.hash && typeof window.showSection === 'function') {
        window.showSection(location.hash.replace('#',''));
    }
});

// Global logout helper
function logout() {
    try { localStorage.removeItem('student_id'); localStorage.removeItem('student_name'); } catch (e) {}
    // Redirect to login page (pages folder)
    window.location.href = 'login.html';
}
window.logout = logout;