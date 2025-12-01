// Centralized authentication helpers for login/register pages
// Depends on postJSON and showInlineAlert from assets/js/app.js

// Use a path that works when this script is loaded from pages/*.html
// pages/* are one level down, so backend API lives at ../backend/api.php
const API_BASE = '/backend/api.php';

function switchAuthTab(e, tab) {
	document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
	document.querySelectorAll('.form-content').forEach(f => f.classList.remove('active'));

	if (e && e.target) e.target.classList.add('active');

	if (tab === 'login') document.getElementById('loginForm').classList.add('active');
	else document.getElementById('registerForm').classList.add('active');

	clearAlert();
}

async function handleLogin(e) {
	if (e && e.preventDefault) e.preventDefault();

	const email = document.getElementById('loginEmail').value;
	const password = document.getElementById('loginPassword').value;

	try {
		// Use postJSON util if available
		let data;
		if (typeof postJSON === 'function') {
			data = await postJSON(`${API_BASE}?action=login`, { email, password });
		} else {
			const res = await fetch(`${API_BASE}?action=login`, {
				method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password })
			});
			data = await res.json();
		}

		if (data && data.success) {
			localStorage.setItem('student_id', data.student.id);
			localStorage.setItem('student_name', data.student.first_name + ' ' + data.student.last_name);
			showAlert('Login successful! Redirecting...', 'success');
			setTimeout(() => { window.location.href = 'dashboard.html'; }, 1200);
		} else {
			showAlert((data && data.message) ? data.message : 'Login failed. Please check your credentials.', 'error');
		}
	} catch (err) {
		console.error('Login error:', err);
		showAlert('An error occurred. Please try again.', 'error');
	}
}

async function handleRegister(e) {
	if (e && e.preventDefault) e.preventDefault();

	const formData = {
		first_name: document.getElementById('regFirstName').value,
		last_name: document.getElementById('regLastName').value,
		student_id: document.getElementById('regStudentId').value,
		email: document.getElementById('regEmail').value,
		password: document.getElementById('regPassword').value,
		gpa: document.getElementById('regGPA').value,
		major: document.getElementById('regMajor').value
	};

	try {
		let data;
		if (typeof postJSON === 'function') {
			data = await postJSON(`${API_BASE}?action=register`, formData);
		} else {
			const res = await fetch(`${API_BASE}?action=register`, {
				method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData)
			});
			data = await res.json();
		}

		if (data && data.success) {
			showAlert('Registration successful! Please login.', 'success');
			setTimeout(() => {
				// switch to login tab
				switchAuthTab(null, 'login');
				const el = document.getElementById('loginEmail'); if (el) el.value = formData.email;
			}, 1000);
		} else {
			showAlert((data && data.message) ? data.message : 'Registration failed. Please try again.', 'error');
		}
	} catch (err) {
		console.error('Registration error:', err);
		showAlert('An error occurred. Please try again.', 'error');
	}
}

function showAlert(message, type) {
	const container = document.getElementById('alertContainer');
	if (!container) return;
	container.innerHTML = `<div class="alert ${type === 'success' ? 'alert-success' : 'alert-error'}">${message}</div>`;
}

function clearAlert() {
	const container = document.getElementById('alertContainer');
	if (container) container.innerHTML = '';
}

// Expose to global scope for inline HTML to call
window.switchAuthTab = switchAuthTab;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.showAlert = showAlert;
window.clearAlert = clearAlert;

