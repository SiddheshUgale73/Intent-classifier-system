document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const intentCardTemplate = document.getElementById('intentCardTemplate');

    analyzeBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        // Reset UI
        resultSection.innerHTML = ''; // Clear previous results
        resultSection.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) throw new Error('API Error');

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error during analysis:', error);
            alert('Could not reach the AI server. Please ensure the backend (main.py) is running.');
        } finally {
            loading.classList.add('hidden');
        }
    });

    function displayResults(data) {
        if (!data.intents || data.intents.length === 0) {
            resultSection.innerHTML = '<p class="alert">⚠️ No intents detected. Try rephrasing.</p>';
            resultSection.classList.remove('hidden');
            return;
        }

        data.intents.forEach((item, index) => {
            const card = intentCardTemplate.content.cloneNode(true);
            
            // 1. Action Number & Intent
            card.querySelector('.action-number').textContent = `Action #${index + 1}`;
            const badge = card.querySelector('.intent-badge');
            badge.textContent = item.intent.replace('_', ' ');

            // 2. Confidence & Color Logic
            const confidencePct = Math.round(item.confidence * 100);
            const fill = card.querySelector('.confidence-fill');
            const text = card.querySelector('.confidence-text');
            text.textContent = `${confidencePct}%`;
            fill.style.width = `${confidencePct}%`;

            if (item.confidence > 0.8) {
                fill.style.background = '#10b981';
                text.style.color = '#10b981';
            } else if (item.confidence > 0.6) {
                fill.style.background = '#f59e0b';
                text.style.color = '#f59e0b';
            } else {
                fill.style.background = '#ef4444';
                text.style.color = '#ef4444';
                badge.style.background = '#fee2e2';
                badge.style.color = '#991b1b';
            }

            // 3. Meaning & Approaches
            card.querySelector('.intent-description').textContent = item.description || "No description available.";
            const approachesList = card.querySelector('.approaches-list');
            if (item.common_approaches && item.common_approaches.length > 0) {
                item.common_approaches.forEach(approach => {
                    const li = document.createElement('li');
                    li.textContent = approach;
                    approachesList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = "No specific approaches defined.";
                approachesList.appendChild(li);
            }

            // 4. Entities (Conditional)
            const entitySection = card.querySelector('.entities');
            const entityGrid = card.querySelector('.entity-grid');
            const entities = item.entities || {};
            const validEntities = Object.entries(entities).filter(([k, v]) => v !== null && v !== undefined && v !== '');

            if (validEntities.length > 0) {
                entitySection.classList.remove('hidden');
                validEntities.forEach(([name, value]) => {
                    const displayValue = name === 'amount' ? `$${value.toLocaleString()}` : value;
                    const entityItem = document.createElement('div');
                    entityItem.className = 'entity-item';
                    entityItem.innerHTML = `
                        <span class="label">${name}</span>
                        <span class="value">${displayValue}</span>
                    `;
                    entityGrid.appendChild(entityItem);
                });
            }

            // 5. Smart Suggestions (New Feature)
            if (item.suggested_action) {
                const suggestionSection = card.querySelector('.suggestion-container');
                suggestionSection.classList.remove('hidden');
                card.querySelector('.suggestion-text').textContent = item.suggested_action;
            }

            resultSection.appendChild(card);
        });

        // Show Section
        resultSection.classList.remove('hidden');
    }
});
