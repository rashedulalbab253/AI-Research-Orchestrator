/**
 * MARA Framework - Frontend Application Logic
 * PhD-Level Research Interface
 * Real-time WebSocket Integration
 */

// === Configuration ===
const API_BASE_URL = window.location.origin;
const WS_BASE_URL = API_BASE_URL.replace('http', 'ws');

// === State Management ===
let currentResearchId = null;
let websocket = null;

// === DOM Elements ===
const elements = {
    researchTopic: document.getElementById('researchTopic'),
    startResearchBtn: document.getElementById('startResearchBtn'),
    charCount: document.getElementById('charCount'),
    agentsGrid: document.getElementById('agentsGrid'),
    progressSection: document.getElementById('progressSection'),
    progressBar: document.getElementById('progressBar'),
    progressPercentage: document.getElementById('progressPercentage'),
    progressStatus: document.getElementById('progressStatus'),
    resultsSection: document.getElementById('resultsSection'),
    apiStatusBtn: document.getElementById('apiStatusBtn'),
    apiStatusIndicator: document.getElementById('apiStatusIndicator'),
    viewDocsBtn: document.getElementById('viewDocsBtn'),
    toastContainer: document.getElementById('toastContainer')
};

// === Initialization ===
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkAPIHealth();
});

function initializeApp() {
    console.log('🔬 MARA Framework initialized');
    updateCharCount();
    loadArchive();
}

function setupEventListeners() {
    // Research input character counter
    elements.researchTopic.addEventListener('input', updateCharCount);

    // Start research button
    elements.startResearchBtn.addEventListener('click', startResearch);

    // API status button
    elements.apiStatusBtn.addEventListener('click', checkAPIHealth);

    // View docs button
    elements.viewDocsBtn.addEventListener('click', () => {
        window.open('/api/docs', '_blank');
    });

    // Enter key to submit
    elements.researchTopic.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            startResearch();
        }
    });
}

// === Character Counter ===
function updateCharCount() {
    const length = elements.researchTopic.value.length;
    elements.charCount.textContent = `${length} / 500`;

    if (length > 500) {
        elements.charCount.style.color = 'var(--accent-red)';
    } else if (length > 400) {
        elements.charCount.style.color = 'var(--accent-pink)';
    } else {
        elements.charCount.style.color = 'var(--text-muted)';
    }
}

// === API Health Check ===
async function checkAPIHealth() {
    try {
        showToast('Checking API status...', 'info');

        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();

        if (data.status === 'healthy') {
            elements.apiStatusIndicator.style.background = 'var(--accent-green)';
            showToast('✅ API is healthy and ready', 'success');
        } else {
            elements.apiStatusIndicator.style.background = 'var(--accent-red)';
            showToast(`⚠️ API degraded: ${data.missing_keys.join(', ')} not configured`, 'error');
        }
    } catch (error) {
        elements.apiStatusIndicator.style.background = 'var(--accent-red)';
        showToast('❌ Cannot connect to API', 'error');
        console.error('Health check failed:', error);
    }
}

// === Start Research ===
async function startResearch() {
    const topic = elements.researchTopic.value.trim();

    // Validation
    if (!topic) {
        showToast('⚠️ Please enter a research topic', 'error');
        elements.researchTopic.focus();
        return;
    }

    if (topic.length < 3) {
        showToast('⚠️ Topic must be at least 3 characters', 'error');
        return;
    }

    if (topic.length > 500) {
        showToast('⚠️ Topic must be less than 500 characters', 'error');
        return;
    }

    // Disable button
    elements.startResearchBtn.disabled = true;
    elements.startResearchBtn.innerHTML = `
        <svg class="btn-icon spinning" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
        </svg>
        <span class="btn-text">Initializing...</span>
    `;

    try {
        // Call API to start research
        const response = await fetch(`${API_BASE_URL}/api/research/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to start research');
        }

        const data = await response.json();
        currentResearchId = data.research_id;

        showToast('🚀 Research initiated successfully', 'success');

        // Show agent cards and progress
        showAgentCards();
        showProgressSection();
        hideResultsSection();

        // Connect to WebSocket for real-time updates
        connectWebSocket(currentResearchId);

        // Start polling as fallback
        startPolling(currentResearchId);

    } catch (error) {
        showToast(`❌ Error: ${error.message}`, 'error');
        console.error('Research start failed:', error);
        resetUI();
    }
}

// === WebSocket Connection ===
function connectWebSocket(researchId) {
    try {
        websocket = new WebSocket(`${WS_BASE_URL}/ws/research/${researchId}`);

        websocket.onopen = () => {
            console.log('WebSocket connected');
            showToast('📡 Real-time updates connected', 'info');
        };

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            updateProgress(data);
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = () => {
            console.log('WebSocket disconnected');
        };
    } catch (error) {
        console.error('WebSocket connection failed:', error);
    }
}

// === Polling Fallback ===
let pollingInterval = null;

function startPolling(researchId) {
    pollingInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/research/status/${researchId}`);
            const data = await response.json();

            updateProgress(data);

            if (data.status === 'completed' || data.status === 'failed') {
                stopPolling();
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 3000); // Poll every 3 seconds
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

// === Update Progress ===
function updateProgress(data) {
    const { status, progress, current_agent } = data;

    // Update progress bar
    elements.progressBar.style.width = `${progress}%`;
    elements.progressPercentage.textContent = `${progress}%`;

    // Update status message
    if (current_agent) {
        elements.progressStatus.textContent = `${current_agent} is working...`;
        updateAgentStatus(current_agent, 'active');
    } else {
        elements.progressStatus.textContent = data.message || 'Processing...';
    }

    // Handle completion
    if (status === 'completed') {
        handleResearchComplete();
    } else if (status === 'failed') {
        handleResearchFailed(data.error || 'Unknown error');
    }
}

// === Agent Status Updates ===
function updateAgentStatus(agentName, status) {
    const agentMap = {
        'Research Specialist': 'agent1',
        'Data Analyst': 'agent2',
        'Technical Writer': 'agent3'
    };

    // Reset all agents
    Object.values(agentMap).forEach(id => {
        const badge = document.querySelector(`#${id} .status-badge`);
        if (badge) {
            badge.className = 'status-badge status-idle';
            badge.textContent = 'Idle';
        }
    });

    // Update current agent
    const agentId = agentMap[agentName];
    if (agentId) {
        const badge = document.querySelector(`#${agentId} .status-badge`);
        if (badge) {
            badge.className = `status-badge status-${status}`;
            badge.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }
}

// === Handle Research Complete ===
function handleResearchComplete() {
    showToast('✅ Research completed successfully!', 'success');

    // Mark all agents as completed
    ['agent1', 'agent2', 'agent3'].forEach(id => {
        const badge = document.querySelector(`#${id} .status-badge`);
        if (badge) {
            badge.className = 'status-badge status-completed';
            badge.textContent = 'Completed';
        }
    });

    // Hide progress, show results
    setTimeout(() => {
        hideProgressSection();
        showResultsSection();
        resetUI();
        loadArchive();
    }, 1500);

    // Close WebSocket
    if (websocket) {
        websocket.close();
    }

    stopPolling();
}

// === Handle Research Failed ===
function handleResearchFailed(error) {
    showToast(`❌ Research failed: ${error}`, 'error');

    setTimeout(() => {
        hideProgressSection();
        hideAgentCards();
        resetUI();
    }, 2000);

    if (websocket) {
        websocket.close();
    }

    stopPolling();
}

// === Download File ===
async function downloadFile(filename) {
    try {
        showToast(`📥 Downloading ${filename}...`, 'info');

        const response = await fetch(`${API_BASE_URL}/api/research/results/${filename}`);

        if (!response.ok) {
            throw new Error('File not found');
        }

        const data = await response.json();

        // Create download link
        const blob = new Blob([data.content], { type: 'text/markdown' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showToast(`✅ Downloaded ${filename}`, 'success');
    } catch (error) {
        showToast(`❌ Failed to download: ${error.message}`, 'error');
        console.error('Download error:', error);
    }
}

// === UI Helper Functions ===
function showAgentCards() {
    elements.agentsGrid.style.display = 'grid';
    elements.agentsGrid.classList.add('fade-in');
}

function hideAgentCards() {
    elements.agentsGrid.style.display = 'none';
}

function showProgressSection() {
    elements.progressSection.style.display = 'block';
    elements.progressSection.classList.add('fade-in');
}

function hideProgressSection() {
    elements.progressSection.style.display = 'none';
}

function showResultsSection() {
    elements.resultsSection.style.display = 'block';
    elements.resultsSection.classList.add('fade-in');
}

function hideResultsSection() {
    elements.resultsSection.style.display = 'none';
}

function resetUI() {
    elements.startResearchBtn.disabled = false;
    elements.startResearchBtn.innerHTML = `
        <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span class="btn-text">Initiate Research Protocol</span>
        <div class="btn-shine"></div>
    `;
}

// === Toast Notifications ===
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    elements.toastContainer.appendChild(toast);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            elements.toastContainer.removeChild(toast);
        }, 300);
    }, 5000);
}

// === CSS Animation for Spinning ===
const style = document.createElement('style');
style.textContent = `
    .spinning {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// === Archive Management ===
async function loadArchive() {
    const grid = document.getElementById('archiveGrid');
    if (!grid) return; // Guard clause if element missing

    try {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">Loading manuscripts...</div>';

        const response = await fetch(`${API_BASE_URL}/api/manuscripts`);

        if (!response.ok) throw new Error('Failed to fetch archive');

        const data = await response.json();

        grid.innerHTML = '';

        if (data.manuscripts.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">No past manuscripts found.</div>';
            return;
        }

        data.manuscripts.forEach(file => {
            const item = document.createElement('div');
            item.className = 'result-item'; // Reuse existing class for styling

            // Format size
            const sizeKB = (file.size_bytes / 1024).toFixed(1);

            // Icon based on type
            const icon = file.filename.toLowerCase().includes('report') || file.filename.toLowerCase().includes('manuscript') ? '📝' : '📊';

            item.innerHTML = `
                <div class="result-icon">${icon}</div>
                <div class="result-info">
                    <h4 class="result-title" style="word-break: break-all;">${file.filename}</h4>
                    <p class="result-description">
                        ${new Date(file.created_at).toLocaleString()} • ${sizeKB} KB
                    </p>
                </div>
                <button class="btn-download" onclick="downloadFile('${file.filename}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Download
                </button>
            `;
            grid.appendChild(item);
        });

    } catch (error) {
        console.error('Failed to load archive:', error);
        showToast('⚠️ Could not load archive', 'error');
        if (grid) grid.innerHTML = '<div style="color: var(--accent-red); padding: 1rem;">Failed to load archive.</div>';
    }
}

// === Export for global access ===
window.downloadFile = downloadFile;
window.loadArchive = loadArchive;
