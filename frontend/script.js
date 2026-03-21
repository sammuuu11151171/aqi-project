// 🔮 Prediction
function predict() {
    let data = [
        Number(document.getElementById("pm25").value),
        Number(document.getElementById("pm10").value),
        Number(document.getElementById("no2").value),
        Number(document.getElementById("co").value)
    ];

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            `AQI: ${data.aqi} (${data.category})`;
    });
}

// 📊 Insights
fetch('/insights')
.then(res => res.json())
.then(data => {
    document.getElementById("insights").innerText =
        `Avg AQI: ${data.average_aqi}, Most Polluted: ${data.most_polluted_city}`;
});

// 📈 Trend Chart
fetch('/trend')
.then(res => res.json())
.then(data => {
    let labels = data.map(d => d.Date);
    let values = data.map(d => d.AQI);

    new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'AQI Trend',
                data: values
            }]
        }
    });
});