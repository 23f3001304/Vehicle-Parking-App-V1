// Simple summary page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

// Initialize charts with ApexCharts
function initializeCharts() {
    if (typeof ApexCharts !== 'undefined' && typeof summaryData !== 'undefined') {
        createOccupancyChart();
        createRevenueChart();
    }
}

// Create occupancy rate chart
function createOccupancyChart() {
    const chartElement = document.getElementById('occupancyChart');
    if (!chartElement || !summaryData.occupancyData) return;
    
    const options = {
        series: summaryData.occupancyData.data || [],
        chart: {
            type: 'donut',
            height: 350,
            width: '100%'
        },
        labels: summaryData.occupancyData.labels || [],
        colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
        legend: {
            position: 'bottom',
            fontSize: '12px'
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%'
                }
            }
        },
        dataLabels: {
            formatter: function(val) {
                return Math.round(val) + '%';
            }
        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return val + '%';
                }
            }
        }
    };
    
    const chart = new ApexCharts(chartElement, options);
    chart.render();
}

// Create revenue chart
function createRevenueChart() {
    const chartElement = document.getElementById('revenueChart');
    if (!chartElement || !summaryData.revenueData) return;
    
    const options = {
        series: [{
            name: 'Revenue',
            data: summaryData.revenueData.data || []
        }],
        chart: {
            type: 'bar',
            height: 350,
            width: '100%'
        },
        colors: ['#FF3B30'],
        xaxis: {
            categories: summaryData.revenueData.labels || [],
            labels: {
                rotate: -45,
                style: {
                    fontSize: '11px'
                }
            }
        },
        yaxis: {
            labels: {
                formatter: function(val) {
                    if (val >= 100000) {
                        return '₹' + (val / 100000).toFixed(1) + 'L';
                    } else if (val >= 1000) {
                        return '₹' + (val / 1000).toFixed(1) + 'K';
                    }
                    return '₹' + val;
                }
            }
        },
        plotOptions: {
            bar: {
                columnWidth: '60%',
                borderRadius: 4
            }
        },
        dataLabels: {
            enabled: false
        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return '₹' + val.toLocaleString('en-IN', {minimumFractionDigits: 2});
                }
            }
        }
    };
    
    const chart = new ApexCharts(chartElement, options);
    chart.render();
}

// Simple refresh function
function refreshData() {
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        const icon = refreshBtn.querySelector('i');
        icon.style.animation = 'spin 1s linear infinite';
        refreshBtn.disabled = true;
        
        setTimeout(() => {
            location.reload();
        }, 1000);
    }
}

// Add spin animation
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
