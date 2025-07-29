// charts.js

document.addEventListener('DOMContentLoaded', function() {
    // Prediction Statistics Chart
    var ctxPrediction = document.getElementById('predictionChart').getContext('2d');
    var predictionChart = new Chart(ctxPrediction, {
        type: 'doughnut',
        data: {
            labels: ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary'],
            datasets: [{
                data: [30, 25, 35, 10],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { size: 12 }
                    }
                }
            }
        }
    });

    // Accuracy Trend Chart
    var ctxAccuracy = document.getElementById('accuracyChart').getContext('2d');
    var accuracyChart = new Chart(ctxAccuracy, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Accuracy',
                data: [0.92, 0.94, 0.93, 0.95, 0.96, 0.97],
                borderColor: '#4BC0C0',
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0.9,
                    max: 1,
                    ticks: {
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        }
                    }
                }
            }
        }
    });
});
