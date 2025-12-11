document.getElementById('solve-button').addEventListener('click', async () => {
    const equation = document.getElementById('equation').value;
    const intervalStr = document.getElementById('interval').value;
    const method = document.getElementById('method').value;
    const resultDiv = document.getElementById('result');

    if (!equation || !intervalStr) {
        resultDiv.innerText = "Please enter both an equation and an interval.";
        resultDiv.style.color = "#f87171"; // Red
        return;
    }

    const interval = intervalStr.split(',').map(Number);
    resultDiv.innerText = "Calculating...";
    resultDiv.style.color = "#e2e8f0";

    try {
        const response = await fetch('/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ equation, interval, method })
        });

        const result = await response.json();

        if (result.error) {
            resultDiv.innerText = `Error: ${result.error}`;
            resultDiv.style.color = "#f87171";
            return;
        }

        if (method === "All") {
            resultDiv.innerText = "Comparison complete. View chart below.";
            const methods = Object.keys(result);
            const maxIterations = Math.max(...methods.map(m => result[m].errors.length));
            const labels = Array.from({ length: maxIterations }, (_, i) => `${i + 1}`);
            
            const colors = ['#818cf8', '#f472b6', '#34d399', '#fbbf24'];

            const datasets = methods.map((m, i) => ({
                label: m,
                data: result[m].errors,
                fill: false,
                backgroundColor: colors[i],
                borderColor: colors[i],
                borderWidth: 2,
                tension: 0.3,
                pointBackgroundColor: '#1e293b',
                pointBorderWidth: 2
            }));

            const ctx = document.getElementById('comparative-chart').getContext('2d');
            if (window.comparativeChart) window.comparativeChart.destroy();
            
            Chart.defaults.color = '#94a3b8';
            Chart.defaults.borderColor = '#334155';

            window.comparativeChart = new Chart(ctx, {
                type: 'line',
                data: { labels, datasets },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: '#e2e8f0' } },
                        title: { display: true, text: 'Convergence Speed (Error vs Iteration)', color: '#f1f5f9' }
                    },
                    scales: {
                        x: { 
                            title: { display: true, text: 'Iterations' },
                            grid: { color: '#1e293b' }
                        },
                        y: { 
                            type: 'logarithmic',
                            title: { display: true, text: 'Error (Log Scale)' },
                            grid: { color: '#334155' }
                        },
                    },
                },
            });
        } else {
            const root = result[method].root;
            resultDiv.innerText = `Root found: ${Number(root).toFixed(6)}`;
            
            if (window.comparativeChart) {
                window.comparativeChart.destroy();
                window.comparativeChart = null;
            }
        }
    } catch (error) {
        console.error(error);
        resultDiv.innerText = "Error connecting to server. Make sure your Python Flask script is running.";
        resultDiv.style.color = "#f87171";
    }
});