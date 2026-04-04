document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    
    // Result elements
    const intentBadge = document.getElementById('intentBadge');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceText = document.getElementById('confidenceText');
    const uncertainAlert = document.getElementById('uncertainAlert');
    const amountValue = document.getElementById('amountValue');
    const receiverValue = document.getElementById('receiverValue');

    analyzeBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        // Reset UI
        resultSection.classList.add('hidden');
        loading.classList.remove('hidden');
        uncertainAlert.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) {
                throw new Error('API Error');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error during analysis:', error);
            alert('Could not reach the AI server. Please ensure the backend is running.');
        } finally {
            loading.classList.add('hidden');
        }
    });

    function displayResults(data) {
        // 1. Intent & Confidence
        intentBadge.textContent = data.intent;
        const confidencePct = Math.round(data.confidence * 100);
        confidenceText.textContent = `${confidencePct}%`;
        confidenceFill.style.width = `${confidencePct}%`;

        // 2. Handle Uncertainty
        if (data.intent === 'UNCERTAIN' || data.confidence < 0.6) {
            uncertainAlert.classList.remove('hidden');
            intentBadge.style.background = '#ffd8d8';
            intentBadge.style.color = '#c62828';
        } else {
            intentBadge.style.background = '#e1f5fe';
            intentBadge.style.color = '#01579b';
        }

        // 3. Entities
        if (data.entities) {
            amountValue.textContent = data.entities.amount ? `$${data.entities.amount.toLocaleString()}` : 'N/A';
            receiverValue.textContent = data.entities.receiver ? data.entities.receiver : 'N/A';
        } else {
            amountValue.textContent = 'N/A';
            receiverValue.textContent = 'N/A';
        }

        // Show Section
        resultSection.classList.remove('hidden');
        resultSection.style.animation = 'fadeIn 0.5s ease-in-out';
    }
});

// Simple fade-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);
