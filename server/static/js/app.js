const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const tabs = document.querySelectorAll('.nav-item');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Run Cycle Button
    const runBtn = document.getElementById('run-cycle-btn');
    if (runBtn) runBtn.addEventListener('click', runDesignCycle);

    // Modal Close
    const closeBtn = document.querySelector('.close-modal');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            document.getElementById('video-modal').style.display = 'none';
            document.getElementById('video-player-container').innerHTML = '';
        });
    }

    // Close modal on outside click
    window.onclick = function (event) {
        const modal = document.getElementById('video-modal');
        if (event.target == modal) {
            modal.style.display = "none";
            document.getElementById('video-player-container').innerHTML = '';
        }
    }
});

function switchTab(tabId) {
    // Update Nav
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

    // Update View
    document.querySelectorAll('.view').forEach(el => el.style.display = 'none');

    // Mapping tabs to view IDs
    const viewMap = {
        'dashboard': 'dashboard-view',
        'trends': 'trends-view',
        'hunter': 'hunter-view',
        'gallery': 'gallery-view'
    };

    const viewId = viewMap[tabId];
    if (viewId) document.getElementById(viewId).style.display = 'block';

    // Auto-load seeds if hunter tab
    if (tabId === 'hunter') {
        loadSeeds();
    }
}

// Global scope for onclick handlers
window.generateVideo = generateVideo;
window.switchTab = switchTab;
window.runHarvest = runHarvest;

// --- Trend Hunter Logic ---

async function loadSeeds() {
    const list = document.getElementById('seed-categories-list');
    list.innerHTML = 'Loading categories...';

    try {
        const res = await fetch(`${API_BASE}/seeds/categories`);
        const data = await res.json();

        let html = '';
        for (const [cat, items] of Object.entries(data)) {
            html += `
                <div style="margin-bottom:1rem;">
                    <div style="color:var(--primary); font-weight:600; text-transform:capitalize; margin-bottom:0.4rem;">
                        ${cat.replace('_', ' ')} <span style="font-size:0.8em; opacity:0.7">(${items.length})</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
                        ${items.slice(0, 5).map(i =>
                `<span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:0.8em;">${i}</span>`
            ).join('')}
                        ${items.length > 5 ? `<span style="opacity:0.5; font-size:0.8em;">+${items.length - 5} more</span>` : ''}
                    </div>
                </div>
            `;
        }
        list.innerHTML = html;

    } catch (e) {
        list.innerHTML = 'Error loading seeds.';
    }
}

async function runHarvest() {
    const btn = document.getElementById('run-harvest-btn');
    const container = document.getElementById('harvest-results');

    btn.disabled = true;
    btn.innerText = 'Harvesting...';
    container.innerHTML = '<div class="loading-spinner"></div>';

    try {
        const res = await fetch(`${API_BASE}/seeds/harvest`, { method: 'POST' });
        const data = await res.json();

        let html = '<div class="pipeline-steps" style="display:flex; flex-direction:column; gap:1rem;">';

        data.tasks.forEach(task => {
            const scoreColor = task.trend_score > 0.9 ? '#4ade80' :
                task.trend_score > 0.8 ? '#facc15' : '#94a3b8';

            html += `
                <div class="step-card" style="min-height:auto; display:flex; flex-direction:row; justify-content:space-between; align-items:center; padding:1rem;">
                    <div>
                        <div style="font-size:1.1rem; font-weight:bold; color:#e2e8f0;">${task.query}</div>
                        <div style="font-size:0.85rem; color:#64748b; margin-top:0.2rem;">
                            Source: ${task.source} | Category: ${task.category}
                        </div>
                    </div>
                    <div style="text-align:right; display:flex; gap:1rem; align-items:center;">
                        <button class="primary-btn" style="padding:0.3rem 0.6rem; font-size:0.8rem;" onclick="runVisualHunt('${task.query}')">
                           📸 Hunt Visuals
                        </button>
                        <div>
                            <div style="font-size:1.5rem; font-weight:bold; color:${scoreColor}">${task.trend_score}</div>
                            <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;">Trend Score</div>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';

        // Add Screenshot Gallery Section
        html += `
            <div style="margin-top:2rem;">
                <h3>Visual Evidence Captured</h3>
                <div id="visual-evidence-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:1rem; margin-top:1rem;">
                    <p class="placeholder">Loading captured visuals...</p>
                </div>
            </div>
        `;

        container.innerHTML = html;
        loadScreenshots(); // Load existing screenshots


    } catch (e) {
        console.error(e);
        container.innerHTML = 'Error running harvest.';
    } finally {
        btn.disabled = false;
        btn.innerText = 'Run Daily Harvest';
    }
}

async function runVisualHunt(keyword) {
    const btn = event.target;
    const originalText = btn.innerText;
    btn.disabled = true;
    btn.innerText = 'Hunting...';
    btn.style.opacity = '0.7';

    try {
        const res = await fetch(`${API_BASE}/hunter/explore`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword: keyword })
        });
        const data = await res.json();

        // Refresh grid
        loadScreenshots();
        alert(`Captured ${data.urls.length} screenshots for "${keyword}"`);

    } catch (e) {
        alert('Error hunting visuals: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerText = originalText;
        btn.style.opacity = '1';
    }
}

async function loadScreenshots() {
    const grid = document.getElementById('visual-evidence-grid');
    if (!grid) return;

    try {
        const res = await fetch(`${API_BASE}/hunter/screenshots`);
        const data = await res.json();

        if (data.screenshots.length === 0) {
            grid.innerHTML = '<p class="placeholder">No visuals captured yet.</p>';
            return;
        }

        grid.innerHTML = data.screenshots.map(url => `
            <div style="border:1px solid var(--border); border-radius:8px; overflow:hidden;">
                <a href="${url}" target="_blank">
                    <img src="${url}" style="width:100%; height:150px; object-fit:cover; display:block;">
                </a>
                 <div style="padding:0.5rem; font-size:0.75rem; background:rgba(0,0,0,0.5); color:#94a3b8; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    ${url.split('/').pop()}
                </div>
            </div>
        `).join('');

    } catch (e) {
        console.error('Error loading screenshots', e);
    }
}

// Global scope
window.runVisualHunt = runVisualHunt;
window.loadScreenshots = loadScreenshots;

async function runDesignCycle() {
    const runBtn = document.getElementById('run-cycle-btn');
    runBtn.disabled = true;
    runBtn.textContent = 'Running...';

    try {
        // Step 1: Fetch Trends (V2: Grouped)
        updateStatus('step-trends', 'Fetching multi-source trends...');
        const trendsRes = await fetch(`${API_BASE}/trends`);
        const trendsData = await trendsRes.json(); // { trends: { google: [], ... } }

        // Render Trend Board
        renderTrendBoard(trendsData.trends);

        // Pick top Google trend for analysis demo
        const demoTrend = trendsData.trends.google_search[0];
        renderTrendCard(demoTrend, 'trend-content');

        const totalTrends = Object.values(trendsData.trends).flat().length;
        document.getElementById('stats-trends').textContent = totalTrends;

        // Step 2: Analyze
        updateStatus('step-analysis', 'Analyzing trend attributes...');
        const analyzeRes = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trend: [demoTrend] }) // Fix: Wrap in array
        });
        const analysisData = await analyzeRes.json();

        renderAnalysis(analysisData);
        document.getElementById('stats-ideas').textContent = '1';

        // Step 3: Generate Images (Batch of 10)
        updateStatus('step-result', 'Generating 10 Asset Variations...');
        const imgRes = await fetch(`${API_BASE}/generate-images`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: analysisData.prompt,
                count: 10
            })
        });
        const imgData = await imgRes.json();

        // Render Gallery
        renderGallery(imgData.images, analysisData.attributes);
        document.getElementById('stats-assets').textContent = imgData.images.length;

        // Update Dashboard Summary
        document.getElementById('result-content').innerHTML = `
            <div style="text-align:center;">
                <p style="color:#4ade80; margin-bottom:10px;">✅ Generated ${imgData.images.length} assets.</p>
                <button class="primary-btn" onclick="switchTab('gallery')" style="font-size:0.9rem;">View Gallery</button>
            </div>
        `;

    } catch (err) {
        console.error(err);
        alert('Error in design cycle: ' + err.message);
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = 'Run Design Cycle';
    }
}

function updateStatus(stepId, status) {
    const container = document.getElementById(stepId.replace('step-', '') + '-content');
    if (container) container.innerHTML = `<p class="placeholder">${status}</p>`;
}

function renderTrendCard(trend, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="trend-item">
            <img src="${trend.image_url}" alt="Trend">
            <h4>${trend.title || 'Trend Found'}</h4>
            <p>${trend.description}</p>
            <small>Source: ${trend.source}</small>
        </div>
    `;
}

function renderAnalysis(data) {
    const container = document.getElementById('analysis-content');

    // Check if data is structured (V4) or legacy
    if (!data.dimensions) {
        // Fallback for compatibility or error
        container.innerHTML = `<p class="placeholder">Analysis format error.</p>`;
        return;
    }

    const { meta, rationale, dimensions, composition, prompt } = data;

    container.innerHTML = `
        <div class="idea-card">
            <div class="idea-header">
                <div>
                    <strong>${meta.trend_source}</strong>
                    <div style="font-size:0.8rem; color:var(--text-muted);">${rationale.headline}</div>
                </div>
                <span class="idea-persona-badge">${meta.persona}</span>
            </div>
            
            <div class="idea-body">
                <!-- Left Col: Dimensions -->
                <div class="idea-dimensions">
                    <h4>Analysis Dimensions</h4>
                    
                    <div class="dimension-row">
                        <span class="dim-label">Target Audience</span>
                        <div class="dim-value">${dimensions.target_audience}</div>
                    </div>
                    <div class="dimension-row">
                        <span class="dim-label">Commercial Potential</span>
                        <div class="dim-value">${dimensions.commercial_viability}</div>
                    </div>
                    
                    <h4>Visual Structure</h4>
                    <div class="dimension-row">
                        <span class="dim-label">Layout Strategy</span>
                        <div class="dim-value">${composition.layout}</div>
                    </div>
                     <div class="dimension-row">
                        <span class="dim-label">Color Psychology</span>
                        <div class="dim-value" style="font-size:0.85rem">${dimensions.color_psychology}</div>
                    </div>
                </div>

                <!-- Right Col: Rationale -->
                <div class="idea-rationale">
                    <h4>Design Conclusion</h4>
                    <p>${rationale.content}</p>
                    
                    <h4>Key Elements</h4>
                    <p>${composition.foreground}</p>
                </div>
                
                <!-- Prompt Footer -->
                <div class="idea-prompt-section">
                    <h4>Generative Prompt</h4>
                    <div class="prompt-box">${prompt}</div>
                </div>
            </div>
        </div>
    `;
}

function renderTrendBoard(trendsGrouped) {
    const container = document.getElementById('trend-board-grid');
    container.innerHTML = '';

    for (const [source, items] of Object.entries(trendsGrouped)) {
        if (items.length === 0) continue;

        // Source Header
        const header = document.createElement('h3');
        header.className = 'trend-section-title';
        header.textContent = source.replace('_', ' ').toUpperCase();
        container.appendChild(header);

        // Grid for this source
        const sectionGrid = document.createElement('div');
        sectionGrid.className = 'trend-board-grid';

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'trend-card';
            card.innerHTML = `
                <img src="${item.image_url}" loading="lazy">
                <div class="trend-card-body">
                    <h4>${item.title}</h4>
                    <p>${item.description}</p>
                </div>
            `;
            sectionGrid.appendChild(card);
        });

        container.appendChild(sectionGrid);
    }
}

function renderGallery(images, attributes) {
    const container = document.getElementById('gallery-grid');
    container.innerHTML = '';

    images.forEach((url, index) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.innerHTML = `
            <img src="${url}" loading="lazy">
            <div class="gallery-overlay">
                <button class="gen-video-btn" onclick="generateVideo('${url}')">Make Video</button>
            </div>
        `;
        container.appendChild(item);
    });
}

async function generateVideo(imageUrl) {
    const modal = document.getElementById('video-modal');
    const playerContainer = document.getElementById('video-player-container');
    const modelImage = 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=500&q=80'; // T-shirt model

    modal.style.display = 'flex';

    // 1. Initial State: Show Inputs
    playerContainer.innerHTML = `
        <h3 style="text-align:center; margin-bottom:1rem;">Production Workflow</h3>
        <div class="video-process-container">
            <div class="process-step">
                <img src="${imageUrl}" class="process-img active">
                <span class="process-label">Design Pattern</span>
            </div>
            <div class="process-step">
                <span class="process-operator">+</span>
            </div>
            <div class="process-step">
                <img src="${modelImage}" class="process-img">
                <span class="process-label">Model Mockup</span>
            </div>
            <div class="process-step">
                <span class="process-operator">→</span>
            </div>
            <div class="process-step">
                <div id="process-result-placeholder" style="width:120px; height:160px; background:rgba(0,0,0,0.3); border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <div class="loading-spinner"></div>
                </div>
                <span class="process-label" id="process-status">Generating...</span>
            </div>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/generate-video`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image_url: imageUrl,
                attributes: { theme: 'Dynamic', mood: 'Cinematic' }
            })
        });
        const data = await res.json();

        // 2. Success State: Show Video
        const resultPlaceholder = document.getElementById('process-result-placeholder');
        const statusLabel = document.getElementById('process-status');

        if (resultPlaceholder) {
            // Replace placeholder with video result
            document.querySelector('.video-process-container').innerHTML = `
                <div class="process-step">
                    <img src="${imageUrl}" class="process-img" style="opacity:0.5; width:80px; height:100px;">
                </div>
                <div class="process-step">
                    <span class="process-operator" style="font-size:1.5rem;">+</span>
                </div>
                 <div class="process-step">
                    <img src="${modelImage}" class="process-img" style="opacity:0.5; width:80px; height:100px;">
                </div>
                <div class="process-step">
                    <span class="process-operator" style="font-size:1.5rem;">→</span>
                </div>
                <div class="process-step" style="flex:1;">
                     <video controls autoplay loop class="video-player" style="max-height:60vh; border: 2px solid var(--primary);">
                        <source src="${data.video_url}" type="video/mp4">
                        Your browser does not support video.
                    </video>
                    <span class="process-label" style="color:#4ade80;">COMPLETE</span>
                </div>
            `;

            playerContainer.insertAdjacentHTML('beforeend', `
                <p style="text-align:center; margin-top:1rem;">
                    <a href="${data.video_url}" target="_blank" class="primary-btn" style="text-decoration:none; font-size:0.9rem;">Download Final Asset</a>
                </p>
            `);
        }

    } catch (err) {
        console.error(err);
        playerContainer.innerHTML = '<p style="color:#ef4444; text-align:center;">Error generating video.</p>';
    }
}

// Global scope for onclick handlers
window.generateVideo = generateVideo;
window.switchTab = switchTab;
