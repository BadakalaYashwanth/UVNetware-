/**
 * UV Netware Analytics Dashboard - Main Logic
 * Version: 2.0 (Premium)
 */

// Global state for charts
let charts = {};

async function fetchData(url) {
    try {
        const response = await fetch(url + '?t=' + Date.now()); // Anti-cache
        if (!response.ok) throw new Error('Failed to fetch data');
        return await response.json();
    } catch (error) {
        console.error('Error fetching data from ' + url + ':', error);
        return null;
    }
}

async function refreshData() {
    const insights = await fetchData('../output_insights.json');
    const rawInput = await fetchData('../data/raw/real_world_input.json');
    
    if (!insights || !rawInput) return;

    updateSummaries(insights, rawInput);
    updateCharts(insights);
    updateAnomalies(insights);
    updateBudgetActions(insights);
    updateGeo(insights);
    
    lucide.createIcons();
    console.log('Dashboard refreshed at ' + new Date().toLocaleTimeString());
}

function updateSummaries(data, raw) {
    // Weekly
    document.getElementById('weekly-revenue').innerText = '$' + (data.weekly_summary.total_revenue).toLocaleString();
    document.getElementById('weekly-growth').innerText = data.weekly_summary.growth_rate;
    document.getElementById('weekly-sub').innerHTML = `<i data-lucide="mouse-pointer" class="w-3 h-3"></i> ${data.weekly_summary.total_clicks} Clicks`;

    // Monthly
    document.getElementById('monthly-clicks').innerText = (data.monthly_summary.total_clicks).toLocaleString();
    document.getElementById('monthly-growth').innerText = data.monthly_summary.growth_rate;
    document.getElementById('monthly-sub').innerHTML = `<i data-lucide="dollar-sign" class="w-3 h-3"></i> $${data.monthly_summary.total_revenue.toLocaleString()} Revenue`;

    // Yearly
    document.getElementById('yearly-revenue').innerText = '$' + (data.yearly_summary.total_revenue).toLocaleString();
    document.getElementById('yearly-growth').innerText = data.yearly_summary.growth_rate;
    document.getElementById('yearly-sub').innerHTML = `<i data-lucide="bar-chart-2" class="w-3 h-3"></i> Predicted Growth`;

    // Loyalty (Inject raw input data here)
    const userHistory = raw.userHistory || { totalSessions: 0, lastActiveDays: 0 };
    document.getElementById('loyalty-engagement').innerText = data.user_history_metrics.loyalty_engagement_score + '%';
    document.getElementById('loyalty-score').innerText = 'System Health';
    document.getElementById('loyalty-sub').innerHTML = `<i data-lucide="database" class="w-3 h-3"></i> ${userHistory.totalSessions} sessions | ${userHistory.lastActiveDays}d active`;
}

function updateAnomalies(data) {
    const list = document.getElementById('anomaly-list');
    list.innerHTML = '';
    data.anomalies.forEach(anomaly => {
        const div = document.createElement('div');
        div.className = 'p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl flex items-start gap-3';
        div.innerHTML = `
            <div class="mt-1 flex-shrink-0 w-2 h-2 rounded-full bg-rose-400"></div>
            <p class="text-xs text-rose-200">${anomaly}</p>
        `;
        list.appendChild(div);
    });
}

function updateBudgetActions(data) {
    const increase = document.getElementById('budget-increase');
    const decrease = document.getElementById('budget-decrease');
    
    increase.innerHTML = '';
    data.budget_recommendations.increase.forEach(channel => {
        increase.innerHTML += `
            <span class="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-1">
                <i data-lucide="trending-up" class="w-3 h-3"></i>${channel}
            </span>`;
    });

    decrease.innerHTML = '';
    data.budget_recommendations.decrease.forEach(channel => {
        decrease.innerHTML += `
            <span class="px-3 py-1 bg-slate-800 text-slate-400 border border-slate-700 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center gap-1">
                <i data-lucide="trending-down" class="w-3 h-3"></i>${channel}
            </span>`;
    });
}

function updateGeo(data) {
    const list = document.getElementById('geo-list');
    list.innerHTML = '';
    const entries = Object.entries(data.geo_insights).sort((a,b) => b[1] - a[1]);
    
    entries.forEach(([country, value], index) => {
        const percentage = Math.round((value / entries.reduce((acc, curr) => acc + curr[1], 0)) * 100);
        list.innerHTML += `
            <div class="space-y-1">
                <div class="flex justify-between text-xs font-medium">
                    <span class="text-slate-300 font-bold">${country}</span>
                    <span class="text-slate-500">${value} users</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div class="bg-indigo-500 h-full rounded-full transition-all duration-1000" style="width: ${percentage}%"></div>
                </div>
            </div>`;
    });
}

function updateCharts(data) {
    // 1. Channel ROI (Horizontal Bar Chart)
    initChart('channelChart', 'bar', {
        labels: data.channel_performance.map(c => c.channel.toUpperCase()),
        datasets: [{
            label: 'ROI Score',
            data: data.channel_performance.map(c => c.ROI),
            backgroundColor: ['rgba(99, 102, 241, 0.4)', 'rgba(167, 139, 250, 0.4)', 'rgba(34, 211, 238, 0.4)'],
            borderColor: ['rgb(99, 102, 241)', 'rgb(167, 139, 250)', 'rgb(34, 211, 238)'],
            borderWidth: 2,
            borderRadius: 12,
            borderSkipped: false
        }]
    }, { 
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
            y: { grid: { display: false }, ticks: { color: '#f8fafc', font: { weight: 'bold' } } }
        }
    });

    // 2. Device Distribution (Doughnut)
    const deviceData = data.user_behavior_insights.top_devices;
    initChart('deviceChart', 'doughnut', {
        labels: Object.keys(deviceData),
        datasets: [{
            data: Object.values(deviceData),
            backgroundColor: ['rgba(99, 102, 241, 0.6)', 'rgba(34, 211, 238, 0.6)'],
            borderColor: ['#0f172a', '#0f172a'],
            borderWidth: 4,
            hoverOffset: 15
        }]
    }, {
        cutout: '75%',
        plugins: { 
            legend: { position: 'bottom', labels: { color: '#94a3b8', usePointStyle: true, pointStyle: 'circle', padding: 20 } }
        }
    });

    // 3. User Type (Pie)
    const userData = data.user_behavior_insights.user_types;
    initChart('userTypeChart', 'pie', {
        labels: Object.keys(userData),
        datasets: [{
            data: Object.values(userData),
            backgroundColor: ['rgba(167, 139, 250, 0.6)', 'rgba(232, 121, 249, 0.6)'],
            borderColor: ['#0f172a', '#0f172a'],
            borderWidth: 4
        }]
    }, {
        plugins: { 
            legend: { position: 'bottom', labels: { color: '#94a3b8', usePointStyle: true, padding: 20 } }
        }
    });

    // 4. Conversion Funnel (Line / Area)
    initChart('funnelChart', 'line', {
        labels: ['Homepage', 'Pricing', 'Checkout', 'Thank You'],
        datasets: [
            {
                label: 'Conversion Rate',
                data: data.funnel_analytics.avg_conversion_rates,
                fill: true,
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderColor: 'rgb(99, 102, 241)',
                pointBackgroundColor: 'rgb(99, 102, 241)',
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 8
            },
            {
                label: 'Drop-off Rate',
                data: data.funnel_analytics.avg_drop_off_rates,
                fill: false,
                borderColor: 'rgba(244, 63, 94, 0.5)',
                borderDash: [5, 5],
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 4
            }
        ]
    }, {
        scales: {
            y: { beginAtZero: true, max: 1.2, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
            x: { grid: { display: false }, ticks: { color: '#cbd5e1' } }
        },
        plugins: { legend: { labels: { color: '#94a3b8' } } }
    });

    // 5. Geo Spread (Bar)
    const geoData = data.geo_insights;
    initChart('geoChart', 'bar', {
        labels: Object.keys(geoData),
        datasets: [{
            label: 'Users',
            data: Object.values(geoData),
            backgroundColor: 'rgba(56, 189, 248, 0.2)',
            borderColor: 'rgb(56, 189, 248)',
            borderWidth: 2,
            borderRadius: 8
        }]
    }, {
        plugins: { legend: { display: false } },
        scales: {
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
            x: { grid: { display: false }, ticks: { color: '#cbd5e1' } }
        }
    });

    // Bottleneck logic
    document.getElementById('bottleneck-tag').querySelector('span').innerText = 'Bottleneck: ' + data.funnel_analytics.bottleneck_step;
}

function initChart(id, type, data, options) {
    if (charts[id]) {
        charts[id].destroy();
    }
    const ctx = document.getElementById(id).getContext('2d');
    charts[id] = new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            ...options,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    refreshData();
    // Auto-refresh every 10 seconds for real-time reflection
    setInterval(refreshData, 10000);
});
