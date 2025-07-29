
    // Sample Data for the charts
    var userGrowthData = [1, 2, 3, 4, 5, 6];
    var benignPredictions = 120;
    var malignantPredictions = 80;
    var noTumorPredictions = 150;
    var pituitaryPredictions = 50;
    var modelAccuracy = 97.8;
    var modelPrecision = 100;
    var modelRecall = 98;
    var modelF1Score = 99;

    // User Growth Chart
    var ctxUserGrowth = document.getElementById('userGrowthChart').getContext('2d');
    var userGrowthChart = new Chart(ctxUserGrowth, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'New Users',
                data: userGrowthData,
                borderColor: '#36A2EB',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'User Growth Trend'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Prediction Analytics Chart
    var ctxPrediction = document.getElementById('predictionChart').getContext('2d');
    var predictionChart = new Chart(ctxPrediction, {
        type: 'doughnut',
        data: {
            labels: ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary'],
            datasets: [{
                data: [benignPredictions, malignantPredictions, noTumorPredictions, pituitaryPredictions],
                backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Tumor Prediction Analytics'
                }
            }
        }
    });

    // Model Performance Chart
    var ctxModelPerformance = document.getElementById('modelPerformanceChart').getContext('2d');
    var modelPerformanceChart = new Chart(ctxModelPerformance, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            datasets: [{
                data: [modelAccuracy, modelPrecision, modelRecall, modelF1Score],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: '#36A2EB',
                pointBackgroundColor: '#36A2EB'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Model Performance'
                }
            },
            scales: {
                r: {
                    ticks: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        }
    });

