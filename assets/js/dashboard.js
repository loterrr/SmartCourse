const API_BASE = '/backend/api.php';
let currentStudent = null;
let recommendations = [];

document.addEventListener("DOMContentLoaded", () => {
    // Load initial dashboard
    if (document.getElementById("dashboard-view")) {
        loadStudentData();
    }

    // Activate sidebar view switching
    document.querySelectorAll(".sidebar-icon").forEach(icon => {
        icon.addEventListener("click", async () => {
            const viewId = icon.dataset.view;

            // Highlight selected sidebar icon
            document.querySelectorAll(".sidebar-icon")
                .forEach(i => i.classList.remove("active"));
            icon.classList.add("active");

            // Switch visible view
            document.querySelectorAll(".content-view")
                .forEach(v => v.classList.remove("active"));
            document.getElementById(viewId).classList.add("active");

            // Load content for each view
            if (viewId === "dashboard-view") loadStudentData();
            if (viewId === "recommendations-view") loadRecommendationsTab();
            if (viewId === "courses-view") loadCoursesTab();
            if (viewId === "profile-view") loadProfileForm();
        });
    });

    // Setup profile form if it exists
    setupProfileForm();
});

// ===== STUDENT PROFILE =====
async function loadStudentData() {
    try {
        const studentId = localStorage.getItem('student_id');
        const res = await fetch(`${API_BASE}?action=profile&student_id=${studentId}`);
        const data = await res.json();

        if (!data) {
            showError("Failed to load profile");
            return;
        }

        currentStudent = data;
        updateProfileDisplay(data);
        loadRecommendations(studentId);

    } catch (err) {
        console.error(err);
        showError("Error loading profile");
    }
}

function updateProfileDisplay(student) {
    const fullName = `${student.first_name} ${student.last_name}`;
    const initials = ((student.first_name[0] || '') + (student.last_name[0] || '')).toUpperCase();

    const set = (id, val) => { 
        const el = document.getElementById(id); 
        if (el) el.textContent = val; 
    };
    
    set('userName', fullName);
    set('profileName', fullName);
    set('profileMajor', student.intended_major || 'Undecided');
    set('statGPA', student.high_school_gpa || 'N/A');
    set('userAvatar', initials);
    set('profileAvatar', initials);
}

// ===== RECOMMENDATIONS =====
async function loadRecommendations(studentId) {
    try {
        const res = await fetch(`${API_BASE}?action=recommendations&student_id=${studentId}`);
        const data = await res.json();

        if (!data.success) {
            showError(data.message || "Failed to load recommendations");
            return;
        }

        recommendations = data.recommendations;

        const el = document.getElementById("statCourses");
        if (el) el.textContent = recommendations.length;

        displayRecommendations(recommendations);

    } catch (err) {
        console.error(err);
        showError("Error loading recommendations");
    }
}

function displayRecommendations(list, filter = "all") {
    const container = document.getElementById("recommendationsContainer");
    if (!container) return;

    if (!list || list.length === 0) {
        container.innerHTML = `
        <div style="text-align:center; padding:40px; color:#6b7280;">
            <p>No recommendations yet.</p>
            <button class="btn-primary" onclick="generateRecommendations()">Generate Recommendations</button>
        </div>`;
        return;
    }

    let filtered = list;
    if (filter === "required") filtered = list.filter(r => r.is_major_requirement);
    if (filter === "electives") filtered = list.filter(r => !r.is_major_requirement);

    container.innerHTML = filtered.map(rec => `
        <div class="recommendation-item">
            <div class="rec-header">
                <div>
                    <div class="course-code">${rec.course_code} ${rec.is_major_requirement ? '⭐ Required' : ''}</div>
                    <h3 class="course-name">${rec.course_name}</h3>
                </div>
                <span class="confidence-badge" style="background:${getConfidenceColor(rec.confidence_score)}">
                    ${rec.confidence_score}% Match
                </span>
            </div>

            <p class="reasoning">${rec.reasoning}</p>

            <div class="course-meta">
                <span>${rec.department}</span>
                <span>${rec.credits} Credits</span>
            </div>

            <div class="action-buttons">
                <button class="btn-primary" onclick="enrollCourse(${rec.course_id})">Enroll</button>
                <button class="btn-secondary" onclick="viewCourseDetails(${rec.course_id})">Details</button>
                <button class="btn-secondary" onclick="provideFeedback(${rec.course_id})">Feedback</button>
            </div>
        </div>
    `).join('');
}

function getConfidenceColor(score) {
    if (score >= 80) return "#10b981";
    if (score >= 60) return "#f59e0b";
    return "#ef4444";
}

async function loadRecommendationsTab() {
    // Get the container in the recommendations-view
    const recommendationsView = document.getElementById("recommendations-view");
    if (!recommendationsView) return;
    
    const container = recommendationsView.querySelector(".course-list");
    if (!container) return;
    
    container.innerHTML = "<p style='padding:20px; text-align:center;'>Loading recommendations...</p>";

    const sid = localStorage.getItem('student_id') || 1;
    
    try {
        const res = await fetch(`${API_BASE}?action=recommendations&student_id=${sid}`);
        const data = await res.json();

        if (!data.success) {
            showError(data.message || "Failed to load recommendations");
            return;
        }

        recommendations = data.recommendations;
        
        // Display in the recommendations view container
        displayRecommendationsInView(container, recommendations);

    } catch (err) {
        console.error(err);
        showError("Error loading recommendations");
    }
}

function displayRecommendationsInView(container, list, filter = "all") {
    if (!container) return;

    if (!list || list.length === 0) {
        container.innerHTML = `
        <div style="text-align:center; padding:40px; color:#6b7280;">
            <p>No recommendations yet.</p>
            <button class="btn-primary" onclick="generateRecommendationsForView()">Generate Recommendations</button>
        </div>`;
        return;
    }

    let filtered = list;
    if (filter === "required") filtered = list.filter(r => r.is_major_requirement);
    if (filter === "electives") filtered = list.filter(r => !r.is_major_requirement);

    container.innerHTML = filtered.map(rec => `
        <div class="recommendation-item">
            <div class="rec-header">
                <div>
                    <div class="course-code">${rec.course_code} ${rec.is_major_requirement ? '⭐ Required' : ''}</div>
                    <h3 class="course-name">${rec.course_name}</h3>
                </div>
                <span class="confidence-badge" style="background:${getConfidenceColor(rec.confidence_score)}">
                    ${rec.confidence_score}% Match
                </span>
            </div>

            <p class="reasoning">${rec.reasoning}</p>

            <div class="course-meta">
                <span>${rec.department}</span>
                <span>${rec.credits} Credits</span>
            </div>

            <div class="action-buttons">
                <button class="btn-primary" onclick="enrollCourse(${rec.course_id})">Enroll</button>
                <button class="btn-secondary" onclick="viewCourseDetails(${rec.course_id})">Details</button>
                <button class="btn-secondary" onclick="provideFeedback(${rec.course_id})">Feedback</button>
            </div>
        </div>
    `).join('');
}

async function generateRecommendationsForView() {
    const recommendationsView = document.getElementById("recommendations-view");
    if (!recommendationsView) return;
    
    const container = recommendationsView.querySelector(".course-list");
    if (!container) return;
    
    container.innerHTML = `
        <div class="loading" style="text-align:center; padding:40px;">
            <div class="spinner" style="margin:0 auto 20px;"></div>
            <p>Generating personalized recommendations...</p>
        </div>`;

    try {
        const studentId = localStorage.getItem('student_id');
        const res = await fetch(`${API_BASE}?action=recommendations&student_id=${studentId}&refresh=1`);
        const data = await res.json();

        if (!data.success) {
            showError(data.message || "Failed to generate recommendations");
            return;
        }

        recommendations = data.recommendations;
        displayRecommendationsInView(container, recommendations);
        showSuccess("Recommendations updated successfully!");

    } catch (err) {
        console.error(err);
        showError("Error generating recommendations");
    }
}

async function generateRecommendations() {
    const container = document.getElementById("recommendationsContainer");
    if (!container) return;
    
    container.innerHTML = `
        <div class="loading" style="text-align:center; padding:40px;">
            <div class="spinner" style="margin:0 auto 20px;"></div>
            <p>Generating personalized recommendations...</p>
        </div>`;

    try {
        const studentId = localStorage.getItem('student_id') || 1;
        const res = await fetch(`${API_BASE}?action=recommendations&student_id=${studentId}&refresh=1`);
        const data = await res.json();

        if (!data.success) {
            showError(data.message || "Failed to generate recommendations");
            return;
        }

        recommendations = data.recommendations;
        displayRecommendations(recommendations);
        showSuccess("Recommendations updated successfully!");

    } catch (err) {
        console.error(err);
        showError("Error generating recommendations");
    }
}

function switchTab(e, filter) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    if (e && e.target) e.target.classList.add('active');
    
    // Check which view we're in
    const dashboardView = document.getElementById("dashboard-view");
    const recommendationsView = document.getElementById("recommendations-view");
    
    if (dashboardView && dashboardView.classList.contains('active')) {
        // We're in dashboard view - use the dashboard container
        displayRecommendations(recommendations, filter);
    } else if (recommendationsView && recommendationsView.classList.contains('active')) {
        // We're in recommendations view - use the recommendations view container
        const container = recommendationsView.querySelector(".course-list");
        displayRecommendationsInView(container, recommendations, filter);
    }
}

// ===== COURSES =====
async function loadCoursesTab() {
    // Find the container in the courses view
    const coursesView = document.getElementById("courses-view");
    if (!coursesView) return;
    
    const container = coursesView.querySelector(".recommendations-section") || 
                     document.getElementById("coursesContainer");
    
    if (!container) return;

    container.innerHTML = `
        <div class="loading" style="text-align:center; padding:40px;">
            <div class="spinner" style="margin:0 auto 20px;"></div>
            <p>Loading courses...</p>
        </div>`;

    try {
        const res = await fetch(`${API_BASE}?action=courses`);
        const data = await res.json();
        
        if (!data) throw new Error('No data received');

        container.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h2 style="margin:0">Browse All Courses</h2>
                <input id="courseSearch" placeholder="Search courses..." 
                       style="padding:10px 15px; border-radius:8px; border:1px solid #e5e7eb; width:300px;">
            </div>
            <div id="coursesList"></div>
        `;

        const listEl = document.getElementById("coursesList");

        function renderCourses(filter = "") {
            const term = filter.toLowerCase();
            const filtered = data.filter(c =>
                c.course_name.toLowerCase().includes(term) ||
                c.course_code.toLowerCase().includes(term) ||
                c.department.toLowerCase().includes(term)
            );

            if (!filtered || filtered.length === 0) {
                listEl.innerHTML = '<div style="padding:40px; text-align:center; color:#6b7280">No courses found</div>';
                return;
            }

            listEl.innerHTML = filtered.map(c => `
                <div class="recommendation-item">
                    <div class="rec-header">
                        <div>
                            <div class="course-code">${c.course_code}</div>
                            <h3 class="course-name">${c.course_name}</h3>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:0.9rem; color:#6b7280; margin-bottom:8px">${c.department}</div>
                            <button class="btn-primary" onclick="enrollCourse(${c.id})">Enroll</button>
                        </div>
                    </div>
                    <p class="reasoning">${c.description || 'No description available'}</p>
                    <div class="course-meta">
                        <span>${c.credits} Credits</span>
                    </div>
                </div>
            `).join('');
        }

        const searchInput = document.getElementById("courseSearch");
        if (searchInput) {
            searchInput.addEventListener("input", e => renderCourses(e.target.value));
        }

        renderCourses();

    } catch (err) {
        console.error('Failed to load courses:', err);
        container.innerHTML = '<div style="padding:40px; text-align:center; color:#ef4444">Failed to load courses. Please try again.</div>';
    }
}

// ===== COURSE DETAILS =====
async function viewCourseDetails(courseId) {
    // First try to find in recommendations
    let course = recommendations.find(r => r.course_id === courseId);
    
    if (course) {
        showCourseModal(course);
        return;
    }

    // Otherwise fetch from backend
    try {
        const res = await fetch(`${API_BASE}?action=courses`);
        const data = await res.json();
        
        if (data && Array.isArray(data)) {
            course = data.find(c => parseInt(c.id) === parseInt(courseId));
            if (course) {
                showCourseModal(course);
                return;
            }
        }
        
        showError('Course details not found');
    } catch (err) {
        console.error('Error fetching course details:', err);
        showError('Failed to load course details');
    }
}

function showCourseModal(course) {
    const modalHTML = `
        <div id="courseModal" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        ">
            <div style="
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            ">
                <h2 style="margin-top: 0;">${course.course_name}</h2>
                <p><strong>Code:</strong> ${course.course_code}</p>
                <p><strong>Department:</strong> ${course.department}</p>
                <p><strong>Credits:</strong> ${course.credits}</p>
                ${course.reasoning ? `<p style="margin-top:15px;"><strong>Why this course:</strong> ${course.reasoning}</p>` : ''}
                ${course.description ? `<p style="margin-top:15px;">${course.description}</p>` : ''}
                
                <div style="display:flex; gap:10px; margin-top:20px;">
                    <button class="btn-primary" onclick="closeModal(); enrollCourse(${course.course_id || course.id})">Enroll</button>
                    <button class="btn-secondary" onclick="closeModal()">Close</button>
                </div>
            </div>
        </div>
    `;
    
    const existing = document.getElementById('courseModal');
    if (existing) existing.remove();
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function closeModal() {
    const modal = document.getElementById('courseModal');
    if (modal) modal.remove();
}

// ===== ENROLLMENT =====
async function enrollCourse(courseId) {
    if (!confirm("Are you sure you want to enroll in this course?")) return;

    try {
        const studentId = localStorage.getItem('student_id') || 1;

        const res = await fetch(`${API_BASE}?action=enroll`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: studentId,
                course_id: courseId,
                semester: "Fall 2025"
            })
        });

        const data = await res.json();

        if (data.success) {
            showSuccess("Successfully enrolled in course!");
        } else {
            showError(data.message || "Enrollment failed");
        }

    } catch (err) {
        console.error(err);
        showError("Error processing enrollment");
    }
}

// ===== FEEDBACK =====
async function provideFeedback(courseId) {
    const rating = prompt("Rate this recommendation (1-5):");
    if (!rating || rating < 1 || rating > 5) return;

    const comments = prompt("Additional comments (optional):");

    try {
        const studentId = localStorage.getItem('student_id') || 1;

        const res = await fetch(`${API_BASE}?action=feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student_id: studentId,
                course_id: courseId,
                rating: parseInt(rating),
                comments: comments || ""
            })
        });

        const data = await res.json();
        
        if (data.success) {
            showSuccess("Thank you for your feedback!");
        } else {
            showError("Failed to submit feedback");
        }

    } catch (err) {
        console.error(err);
        showError("Error submitting feedback");
    }
}

// ===== PROFILE FORM =====
function loadProfileForm() {
    const form = document.getElementById('profileForm');
    if (!form) return;

    // Pre-fill student id from localStorage if not set
    const studentIdEl = document.getElementById('studentId');
    if (studentIdEl && (!studentIdEl.value || studentIdEl.value === '1')) {
        const sid = localStorage.getItem('student_id');
        if (sid) studentIdEl.value = sid;
    }

    // Pre-fill with current student data if available
    if (currentStudent) {
        const careerEl = document.getElementById('careerInterests');
        const learningEl = document.getElementById('learningStyle');
        const hoursEl = document.getElementById('studyHours');
        const extraEl = document.getElementById('extracurricular');

        if (careerEl && currentStudent.career_interests) {
            careerEl.value = Array.isArray(currentStudent.career_interests) 
                ? currentStudent.career_interests.join(', ')
                : currentStudent.career_interests;
        }

        if (learningEl && currentStudent.learning_style) {
            learningEl.value = currentStudent.learning_style;
        }

        if (hoursEl && currentStudent.study_hours) {
            hoursEl.value = currentStudent.study_hours;
        }

        if (extraEl && currentStudent.extracurricular) {
            extraEl.value = Array.isArray(currentStudent.extracurricular)
                ? currentStudent.extracurricular.join(', ')
                : currentStudent.extracurricular;
        }
    }
}

function setupProfileForm() {
    const form = document.getElementById('profileForm');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const studentId = document.getElementById('studentId')?.value || 
                         localStorage.getItem('student_id') || 1;
        
        const payload = {
            student_id: studentId,
            career_interests: document.getElementById('careerInterests').value
                .split(',').map(s => s.trim()).filter(Boolean),
            learning_style: document.getElementById('learningStyle').value,
            study_hours: parseInt(document.getElementById('studyHours').value, 10) || 10,
            extracurricular: document.getElementById('extracurricular').value
                .split(',').map(s => s.trim()).filter(Boolean)
        };

        try {
            const resp = await postJSON(`${API_BASE}?action=profile`, payload);
            
            if (resp && resp.success) {
                showInlineAlert('Profile saved successfully. Refreshing recommendations...', 'success', 'profileAlert');
                
                // Reload student data
                await loadStudentData();
                
                // Force refresh recommendations with new profile data
                try {
                    const recRes = await fetch(`${API_BASE}?action=recommendations&student_id=${studentId}&refresh=1`);
                    const recData = await recRes.json();
                    
                    if (recData.success) {
                        recommendations = recData.recommendations;
                        showInlineAlert('Profile and recommendations updated successfully!', 'success', 'profileAlert');
                    }
                } catch (recErr) {
                    console.error('Error refreshing recommendations:', recErr);
                    // Don't show error - profile was saved successfully
                }
                
                setTimeout(() => {
                    // Switch back to dashboard view
                    const dashboardBtn = document.querySelector('[data-view="dashboard-view"]');
                    if (dashboardBtn) dashboardBtn.click();
                }, 1500);
            } else {
                showInlineAlert(
                    (resp && resp.message) ? resp.message : 'Failed to save profile', 
                    'error', 
                    'profileAlert'
                );
            }
        } catch (err) {
            console.error('Error saving profile:', err);
            showInlineAlert(
                'Error saving profile: ' + (err && err.message ? err.message : err), 
                'error', 
                'profileAlert'
            );
        }
    });
}

// Helper function for POST requests
async function postJSON(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Helper function for inline alerts
function showInlineAlert(message, type, containerId) {
    const container = document.getElementById(containerId);
    
    if (!container) {
        // Fallback to toast notification if container not found
        if (type === 'success') {
            showSuccess(message);
        } else {
            showError(message);
        }
        return;
    }

    const alertDiv = document.createElement('div');
    alertDiv.style.cssText = `
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 0.95rem;
        ${type === 'success' 
            ? 'background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7;' 
            : 'background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;'}
    `;
    alertDiv.textContent = message;

    // Clear previous alerts
    container.innerHTML = '';
    container.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// ===== NOTIFICATIONS =====
function showSuccess(msg) {
    const toast = document.createElement("div");
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function showError(msg) {
    const toast = document.createElement("div");
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ===== LOGOUT =====
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('student_id');
        window.location.href = '../index.html';
    }
}

// Expose functions globally
window.switchTab = switchTab;
window.generateRecommendations = generateRecommendations;
window.generateRecommendationsForView = generateRecommendationsForView;
window.enrollCourse = enrollCourse;
window.provideFeedback = provideFeedback;
window.viewCourseDetails = viewCourseDetails;
window.closeModal = closeModal;
window.logout = logout;
