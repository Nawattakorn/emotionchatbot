let emotionChart = null;

function addMessage(text, isUser) {
    const chatContainer = document.getElementById('chat-container');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`;
    bubble.textContent = text;
    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateChart(data) {
    const ctx = document.getElementById('emotionChart').getContext('2d');
    const colors = {
        anger: '#dc3545',
        fear: '#17a2b8',
        joy: '#ffc107',
        sadness: '#28a745'
    };

    if (emotionChart) emotionChart.destroy();

    emotionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Probability',
                data: Object.values(data),
                backgroundColor: Object.keys(data).map(e => colors[e]),
                borderWidth: 0,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        callback: (value) => `${(value * 100).toFixed(0)}%`
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => 
                            `${ctx.dataset.label}: ${(ctx.raw * 100).toFixed(1)}%`
                    }
                }
            }
        }
    });
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    
    if (!text) return;

    // แสดงข้อความของผู้ใช้
    addMessage(text, true);
    input.value = '';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        // แสดงข้อความของบอท
        addMessage(data.response, false);
        // อัปเดทกราฟตามค่า probabilities ที่ส่งกลับมา
        updateChart(data.probabilities);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, something went wrong. Please try again.', false);
    }
}

// Initialize empty chart เมื่อหน้าเว็บโหลด
window.onload = () => updateChart({ anger: 0, fear: 0, joy: 0, sadness: 0 });
