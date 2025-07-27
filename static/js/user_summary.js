// User Summary page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeAnimations();
});

// Initialize charts with ApexCharts
function initializeCharts() {
    if (typeof ApexCharts !== 'undefined' && typeof summaryData !== 'undefined') {
        createUsageChart();
    }
}

// Create usage chart
function createUsageChart() {
    const chartElement = document.getElementById('usageChart');
    if (!chartElement || !summaryData.usageData || summaryData.usageData.labels.length === 0) return;
    
    const options = {
        series: summaryData.usageData.data || [],
        chart: {
            type: 'donut',
            height: 280,
            width: '100%'
        },
        labels: summaryData.usageData.labels || [],
        colors: ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', '#1abc9c'],
        legend: {
            position: 'bottom',
            fontSize: '12px'
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Total Visits',
                            fontSize: '14px',
                            fontWeight: 600,
                            color: '#333'
                        }
                    }
                }
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function(val, opts) {
                return opts.w.config.series[opts.seriesIndex];
            },
            style: {
                fontSize: '12px',
                fontWeight: 'bold'
            }
        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return val + ' visits';
                }
            }
        },
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    height: 250
                },
                legend: {
                    position: 'bottom',
                    fontSize: '10px'
                }
            }
        }]
    };
    
    const chart = new ApexCharts(chartElement, options);
    chart.render();
}

// Initialize animations
function initializeAnimations() {
    // Animate overview cards on load
    const overviewCards = document.querySelectorAll('.overview-card');
    overviewCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // Animate favorite bars
    const favoriteBars = document.querySelectorAll('.favorite-fill');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.transition = 'width 1s ease';
                    bar.style.width = width;
                }, 200);
            }
        });
    }, { threshold: 0.5 });
    
    favoriteBars.forEach(bar => observer.observe(bar));
    
    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 300 + (index * 100));
    });
}

// Refresh costs function
function refreshCosts() {
    const btn = event.target.closest('.quick-action-btn');
    const originalContent = btn.innerHTML;
    
    // Show loading state
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Refreshing...</span>';
    btn.disabled = true;
    
    // Simulate refresh (in real app, this would make an API call)
    setTimeout(() => {
        // Restore button
        btn.innerHTML = originalContent;
        btn.disabled = false;
        
        // Show success message
        showNotification('Costs refreshed successfully!', 'success');
        
        // Optionally reload the page to get updated data
        // window.location.reload();
    }, 2000);
}

// Show notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : '#0c5460'};
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Auto-refresh active reservations every 30 seconds
if (document.querySelector('.active-card')) {
    setInterval(() => {
        // In a real application, this would fetch updated data
        console.log('Auto-refreshing active reservations...');
    }, 30000);
}

// Add hover effects to cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.overview-card, .stat-card, .active-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
