// Small utilities used across the frontend

async function postJSON(url, data) {
	const res = await fetch(url, {
		method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
	});
	try { return await res.json(); } catch (e) { return null; }
}

function showInlineAlert(message, type = 'success', containerId = 'alertContainer') {
	const el = document.getElementById(containerId);
	if (!el) return;
	el.innerHTML = `<div class="alert ${type === 'success' ? 'alert-success' : 'alert-error'}">${message}</div>`;
}

// Export for pages
window.postJSON = postJSON;
window.showInlineAlert = showInlineAlert;

