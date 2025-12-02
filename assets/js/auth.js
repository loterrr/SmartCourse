// Centralized authentication helpers for login/register pages
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
    
    if (!email || !password) {
        showAlert('Please enter both email and password', 'error');
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}?action=login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        
        if (data && data.success && data.student) {
            // Store student information
            localStorage.setItem('student_id', data.student.student_id);
            localStorage.setItem('student_name', `${data.student.first_name} ${data.student.last_name}`);
            
            showAlert('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1200);
        } else {
            showAlert(data.message || 'Login failed. Please check your credentials.', 'error');
        }
    } catch (err) {
        console.error('Login error:', err);
        showAlert(`An error occurred: ${err.message}`, 'error');
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
    
    // Basic validation
    if (!formData.email || !formData.password || !formData.first_name || !formData.last_name) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}?action=register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        
        if (data && data.success) {
            showAlert('Registration successful! Please login.', 'success');
            setTimeout(() => {
                // Switch to login tab and pre-fill email
                switchAuthTab(null, 'login');
                const emailEl = document.getElementById('loginEmail');
                if (emailEl) emailEl.value = formData.email;
                clearAlert();
            }, 1500);
        } else {
            showAlert(data.message || 'Registration failed. Please try again.', 'error');
        }
    } catch (err) {
        console.error('Registration error:', err);
        showAlert(`An error occurred: ${err.message}`, 'error');
    }
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) {
        console.warn('Alert container not found');
        return;
    }
    
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    container.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
    
    // Auto-clear after 5 seconds
    setTimeout(() => {
        if (container.innerHTML.includes(message)) {
            clearAlert();
        }
    }, 5000);
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
