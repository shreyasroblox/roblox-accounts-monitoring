#!/usr/bin/env python3
"""
Build the interactive HTML dashboard for Roblox Accounts Monitoring.
Real data only - no synthetic data. All listings link back to source marketplaces.
"""

import json

with open("dashboard_data.json") as f:
    data = json.load(f)

data_js = json.dumps(data)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Roblox Accounts Monitoring Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root {{
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #242836;
  --border: #2e3347;
  --text: #e4e6f0;
  --text-dim: #8b8fa3;
  --accent: #6c5ce7;
  --accent2: #00cec9;
  --red: #ff6b6b;
  --orange: #ffa502;
  --green: #26de81;
  --blue: #4ecdc4;
  --u7buy: #e74c3c;
  --eldorado: #f39c12;
  --ebay: #3498db;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }}

.header {{
  background: linear-gradient(135deg, #1a1d27 0%, #242836 100%);
  border-bottom: 1px solid var(--border);
  padding: 20px 32px;
  display: flex; align-items: center; justify-content: space-between;
}}
.header h1 {{ font-size: 22px; font-weight: 600; }}
.header h1 span {{ color: var(--red); }}
.header-meta {{ color: var(--text-dim); font-size: 13px; text-align: right; }}
.header-badge {{
  display: inline-block; background: #26de8133; color: var(--green);
  padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;
  margin-left: 8px;
}}

.nav {{
  display: flex; gap: 4px; padding: 12px 32px; background: var(--surface);
  border-bottom: 1px solid var(--border); flex-wrap: wrap;
}}
.nav button {{
  background: transparent; border: 1px solid var(--border); color: var(--text-dim);
  padding: 8px 18px; border-radius: 8px; cursor: pointer; font-size: 13px;
  transition: all 0.2s;
}}
.nav button:hover {{ border-color: var(--accent); color: var(--text); }}
.nav button.active {{ background: var(--accent); border-color: var(--accent); color: #fff; }}

.container {{ max-width: 1440px; margin: 0 auto; padding: 24px 32px; }}
.section {{ display: none; }}
.section.active {{ display: block; }}

/* KPI Cards */
.kpi-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px; margin-bottom: 28px;
}}
.kpi-card {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px; position: relative; overflow: hidden;
}}
.kpi-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}}
.kpi-card.u7buy::before {{ background: var(--u7buy); }}
.kpi-card.eldorado::before {{ background: var(--eldorado); }}
.kpi-card.ebay::before {{ background: var(--ebay); }}
.kpi-card.total::before {{ background: var(--accent); }}
.kpi-label {{ font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
.kpi-value {{ font-size: 28px; font-weight: 700; }}
.kpi-sub {{ font-size: 12px; color: var(--text-dim); margin-top: 4px; }}

/* Source cards */
.source-cards {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 20px; margin-bottom: 28px;
}}
.source-card {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  padding: 24px; position: relative; overflow: hidden;
}}
.source-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
}}
.source-card.u7buy::before {{ background: var(--u7buy); }}
.source-card.eldorado::before {{ background: var(--eldorado); }}
.source-card.ebay::before {{ background: var(--ebay); }}
.source-card h3 {{ font-size: 18px; margin-bottom: 8px; }}
.source-card h3 a {{ color: var(--text); text-decoration: none; }}
.source-card h3 a:hover {{ color: var(--accent2); text-decoration: underline; }}
.source-card .desc {{ font-size: 13px; color: var(--text-dim); margin-bottom: 14px; line-height: 1.5; }}
.source-stat {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border); font-size: 13px; }}
.source-stat:last-child {{ border-bottom: none; }}
.source-stat .label {{ color: var(--text-dim); }}
.source-stat .val {{ font-weight: 600; }}

/* Chart layout */
.chart-row {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;
}}
.chart-row.full {{ grid-template-columns: 1fr; }}
.chart-card {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px;
}}
.chart-card h3 {{ font-size: 14px; font-weight: 600; margin-bottom: 16px; color: var(--text); }}
.chart-card canvas {{ max-height: 380px; }}

/* Tables */
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ text-align: left; padding: 10px 12px; border-bottom: 2px solid var(--border);
     color: var(--text-dim); font-weight: 600; text-transform: uppercase; font-size: 11px;
     letter-spacing: 0.5px; white-space: nowrap; }}
td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); }}
tr:hover {{ background: var(--surface2); }}

/* Tags */
.source-tag {{
  display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: 600;
}}
.source-tag.u7buy {{ background: #e74c3c33; color: var(--u7buy); }}
.source-tag.eldorado {{ background: #f39c1233; color: var(--eldorado); }}
.source-tag.ebay {{ background: #3498db33; color: var(--ebay); }}

.tier-tag {{
  display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: 600;
}}
.tier-tag.premium {{ background: #f39c1233; color: var(--orange); }}
.tier-tag.mid {{ background: #6c5ce733; color: var(--accent); }}
.tier-tag.basic {{ background: #26de8133; color: var(--green); }}

.feature-tag {{
  display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10px;
  background: var(--surface2); color: var(--text-dim); margin: 1px 2px;
}}

a.view-link {{
  color: var(--accent2); text-decoration: none; font-weight: 600; font-size: 12px;
}}
a.view-link:hover {{ text-decoration: underline; }}

/* Provenance banner */
.provenance {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; gap: 16px;
}}
.provenance-icon {{ font-size: 28px; }}
.provenance-text {{ font-size: 13px; color: var(--text-dim); line-height: 1.6; }}
.provenance-text strong {{ color: var(--text); }}
.provenance-text a {{ color: var(--accent2); text-decoration: none; }}
.provenance-text a:hover {{ text-decoration: underline; }}

/* Price benchmark */
.benchmark-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px; margin-bottom: 24px;
}}
.benchmark-item {{
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  padding: 14px 18px;
}}
.benchmark-item .bname {{ font-size: 13px; color: var(--text); font-weight: 600; margin-bottom: 4px; }}
.benchmark-item .brange {{ font-size: 12px; color: var(--text-dim); }}
.benchmark-item .btypical {{ font-size: 16px; font-weight: 700; color: var(--accent2); }}

/* Filters */
.filters {{
  display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center;
}}
.filters label {{ font-size: 12px; color: var(--text-dim); }}
.filters select {{
  background: var(--surface2); border: 1px solid var(--border); color: var(--text);
  padding: 6px 12px; border-radius: 6px; font-size: 13px;
}}

@media (max-width: 900px) {{
  .chart-row {{ grid-template-columns: 1fr; }}
  .source-cards {{ grid-template-columns: 1fr; }}
  .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .benchmark-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="header">
  <h1><span>Roblox</span> Accounts Monitoring Dashboard</h1>
  <div class="header-meta">
    <div>Data Scraped: {data['metadata']['scrape_date']} <span class="header-badge">REAL DATA</span></div>
    <div style="margin-top:4px">{data['metadata']['total_verified_listings']} Verified Listings from {data['metadata']['sources_tracked']} Marketplaces</div>
  </div>
</div>

<div class="nav" id="nav">
  <button class="active" data-tab="overview">Overview</button>
  <button data-tab="listings">All Listings</button>
  <button data-tab="sources">Marketplace Sources</button>
  <button data-tab="categories">Categories</button>
  <button data-tab="prices">Price Analysis</button>
  <button data-tab="benchmarks">Benchmarks</button>
</div>

<div class="container">

<!-- ========== OVERVIEW ========== -->
<div class="section active" id="sec-overview">
  <div class="provenance">
    <div class="provenance-icon">&#9989;</div>
    <div class="provenance-text">
      <strong>All data on this dashboard is from real marketplace listings.</strong> No synthetic or generated data is used.<br>
      Sources:
      <a href="https://www.u7buy.com/roblox/roblox-accounts" target="_blank">U7Buy</a> &bull;
      <a href="https://www.eldorado.gg/roblox-accounts-for-sale/a/70-1-0" target="_blank">Eldorado.gg</a> &bull;
      <a href="https://www.ebay.com/shop/roblox-account-with-headless?_nkw=roblox+account+with+headless" target="_blank">eBay</a>
      &nbsp;|&nbsp; Last scraped: <strong>{data['metadata']['scrape_date']}</strong>
    </div>
  </div>

  <div class="kpi-grid" id="kpiGrid"></div>

  <div class="chart-row">
    <div class="chart-card"><h3>Listings by Source</h3><canvas id="chartSourcePie"></canvas></div>
    <div class="chart-card"><h3>Average Price by Source (USD)</h3><canvas id="chartSourcePrice"></canvas></div>
  </div>
  <div class="chart-row">
    <div class="chart-card"><h3>Listings by Quality Tier</h3><canvas id="chartQualityPie"></canvas></div>
    <div class="chart-card"><h3>Average Price by Quality Tier (USD)</h3><canvas id="chartQualityPrice"></canvas></div>
  </div>
</div>

<!-- ========== ALL LISTINGS ========== -->
<div class="section" id="sec-listings">
  <div class="provenance">
    <div class="provenance-icon">&#128269;</div>
    <div class="provenance-text">
      <strong>Verified listings scraped on {data['metadata']['scrape_date']}.</strong>
      Each listing links directly to the original marketplace page. Click "View Listing" to verify.
    </div>
  </div>
  <div class="filters">
    <label>Source:</label>
    <select id="listingSource">
      <option value="all">All Sources</option>
      <option value="U7Buy">U7Buy</option>
      <option value="Eldorado.gg">Eldorado.gg</option>
      <option value="eBay">eBay</option>
    </select>
    <label>Quality Tier:</label>
    <select id="listingTier">
      <option value="all">All Tiers</option>
      <option value="Premium/Stacked">Premium/Stacked</option>
      <option value="Mid-Tier">Mid-Tier</option>
      <option value="Basic/Starter">Basic/Starter</option>
    </select>
    <label>Sort:</label>
    <select id="listingSort">
      <option value="price-desc">Price: High to Low</option>
      <option value="price-asc">Price: Low to High</option>
      <option value="source">By Source</option>
    </select>
  </div>
  <div class="chart-card">
    <h3>Verified Listings (<span id="listingCount"></span>)</h3>
    <div class="table-wrap"><table id="listingsTable"><thead><tr>
      <th>Source</th><th>Title</th><th>Price</th><th>Category</th><th>Quality Tier</th><th>Features</th><th>Link</th>
    </tr></thead><tbody></tbody></table></div>
  </div>
</div>

<!-- ========== MARKETPLACE SOURCES ========== -->
<div class="section" id="sec-sources">
  <div class="source-cards" id="sourceCards"></div>
  <div class="chart-card">
    <h3>Source Comparison</h3>
    <div class="table-wrap"><table id="sourceTable"><thead><tr>
      <th>Source</th><th>Est. Listings</th><th>Est. Sold</th><th>Price Range</th><th>Avg Price</th>
      <th>Guarantee</th><th>Delivery</th><th>Verified Sellers</th><th>Link</th>
    </tr></thead><tbody></tbody></table></div>
  </div>
</div>

<!-- ========== CATEGORIES ========== -->
<div class="section" id="sec-categories">
  <div class="chart-row">
    <div class="chart-card"><h3>Listings by Category</h3><canvas id="chartCatBar"></canvas></div>
    <div class="chart-card"><h3>Average Price by Category (USD)</h3><canvas id="chartCatPrice"></canvas></div>
  </div>
  <div class="chart-card">
    <h3>Category Breakdown</h3>
    <div class="table-wrap"><table id="catTable"><thead><tr>
      <th>Category</th><th>Listings</th><th>Sources</th><th>Min Price</th><th>Max Price</th><th>Avg Price</th>
    </tr></thead><tbody></tbody></table></div>
  </div>
</div>

<!-- ========== PRICE ANALYSIS ========== -->
<div class="section" id="sec-prices">
  <div class="chart-row full">
    <div class="chart-card"><h3>Price Distribution Across All Listings</h3><canvas id="chartPriceDist"></canvas></div>
  </div>
  <div class="chart-row">
    <div class="chart-card"><h3>Price by Source (Box Plot Style)</h3><canvas id="chartPriceBySource"></canvas></div>
    <div class="chart-card"><h3>Price by Quality Tier</h3><canvas id="chartPriceByTier"></canvas></div>
  </div>
  <div id="priceCompSection"></div>
</div>

<!-- ========== BENCHMARKS ========== -->
<div class="section" id="sec-benchmarks">
  <div class="provenance">
    <div class="provenance-icon">&#128200;</div>
    <div class="provenance-text">
      <strong>Market price benchmarks</strong> derived from cross-marketplace research.
      Official Robux costs vs. typical resale prices for key account types.
    </div>
  </div>
  <div class="benchmark-grid" id="benchmarkGrid"></div>
</div>

</div><!-- container -->

<script>
const D = {data_js};

const SOURCE_COLORS = {{ 'U7Buy': '#e74c3c', 'Eldorado.gg': '#f39c12', 'eBay': '#3498db' }};
const TIER_COLORS = {{ 'Premium/Stacked': '#f39c12', 'Mid-Tier': '#6c5ce7', 'Basic/Starter': '#26de81' }};

Chart.defaults.color = '#8b8fa3';
Chart.defaults.borderColor = '#2e3347';
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.boxWidth = 12;
Chart.defaults.plugins.legend.labels.padding = 16;

// ============ NAVIGATION ============
document.getElementById('nav').addEventListener('click', e => {{
  if (e.target.tagName !== 'BUTTON') return;
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('sec-' + e.target.dataset.tab).classList.add('active');
}});

// ============ UTILITIES ============
function fmtUSD(n) {{ return '$' + n.toFixed(2); }}
function fmt(n) {{ return n >= 1000 ? (n/1000).toFixed(1) + 'k' : n.toString(); }}
function sourceClass(s) {{ return s === 'U7Buy' ? 'u7buy' : s === 'Eldorado.gg' ? 'eldorado' : 'ebay'; }}
function tierClass(t) {{ return t.includes('Premium') ? 'premium' : t.includes('Mid') ? 'mid' : 'basic'; }}

const charts = {{}};
function destroyChart(id) {{ if(charts[id]) {{ charts[id].destroy(); delete charts[id]; }} }}

// ============ OVERVIEW ============
function renderOverview() {{
  const grid = document.getElementById('kpiGrid');
  grid.innerHTML = '';

  // Total KPI
  const totalListings = D.verified_listings.length;
  const prices = D.verified_listings.map(l => l.price_usd);
  const avgPrice = prices.reduce((a,b) => a+b, 0) / prices.length;
  grid.innerHTML += `
    <div class="kpi-card total">
      <div class="kpi-label">Total Verified Listings</div>
      <div class="kpi-value">${{totalListings}}</div>
      <div class="kpi-sub">Across ${{D.metadata.sources_tracked}} marketplaces</div>
    </div>
    <div class="kpi-card total">
      <div class="kpi-label">Average Price</div>
      <div class="kpi-value">${{fmtUSD(avgPrice)}}</div>
      <div class="kpi-sub">${{fmtUSD(Math.min(...prices))}} - ${{fmtUSD(Math.max(...prices))}}</div>
    </div>`;

  // Per-source KPIs
  D.source_breakdown.forEach(s => {{
    grid.innerHTML += `
      <div class="kpi-card ${{sourceClass(s.source_name)}}">
        <div class="kpi-label">${{s.source_name}} (est.)</div>
        <div class="kpi-value">${{fmt(s.estimated_total_listings)}}</div>
        <div class="kpi-sub">${{s.verified_sample_count}} verified samples &bull; avg ${{fmtUSD(s.avg_price_usd)}}</div>
      </div>`;
  }});

  // Source pie chart
  destroyChart('sourcePie');
  const sourceLabels = D.source_breakdown.map(s => s.source_name);
  const sourceCounts = D.source_breakdown.map(s => s.verified_sample_count);
  charts.sourcePie = new Chart(document.getElementById('chartSourcePie'), {{
    type: 'doughnut',
    data: {{
      labels: sourceLabels,
      datasets: [{{ data: sourceCounts, backgroundColor: sourceLabels.map(s => SOURCE_COLORS[s]) }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
  }});

  // Source price bar
  destroyChart('sourcePrice');
  charts.sourcePrice = new Chart(document.getElementById('chartSourcePrice'), {{
    type: 'bar',
    data: {{
      labels: sourceLabels,
      datasets: [{{
        label: 'Avg Price (USD)',
        data: D.source_breakdown.map(s => s.avg_price_usd),
        backgroundColor: sourceLabels.map(s => SOURCE_COLORS[s] + 'cc'),
        borderColor: sourceLabels.map(s => SOURCE_COLORS[s]),
        borderWidth: 1,
      }}]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ display: false }} }} }}
  }});

  // Quality pie
  destroyChart('qualityPie');
  const tierLabels = D.quality_distribution.map(q => q.quality_tier);
  charts.qualityPie = new Chart(document.getElementById('chartQualityPie'), {{
    type: 'doughnut',
    data: {{
      labels: tierLabels,
      datasets: [{{ data: D.quality_distribution.map(q => q.listing_count), backgroundColor: tierLabels.map(t => TIER_COLORS[t]) }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
  }});

  // Quality price bar
  destroyChart('qualityPrice');
  charts.qualityPrice = new Chart(document.getElementById('chartQualityPrice'), {{
    type: 'bar',
    data: {{
      labels: tierLabels,
      datasets: [{{
        label: 'Avg Price (USD)',
        data: D.quality_distribution.map(q => q.avg_price_usd),
        backgroundColor: tierLabels.map(t => TIER_COLORS[t] + 'cc'),
        borderColor: tierLabels.map(t => TIER_COLORS[t]),
        borderWidth: 1,
      }}]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ display: false }} }} }}
  }});
}}

// ============ ALL LISTINGS ============
function renderListings() {{
  const sourceFilter = document.getElementById('listingSource').value;
  const tierFilter = document.getElementById('listingTier').value;
  const sortVal = document.getElementById('listingSort').value;

  let listings = [...D.verified_listings];
  if (sourceFilter !== 'all') listings = listings.filter(l => l.source === sourceFilter);
  if (tierFilter !== 'all') listings = listings.filter(l => l.quality_tier === tierFilter);

  if (sortVal === 'price-desc') listings.sort((a,b) => b.price_usd - a.price_usd);
  else if (sortVal === 'price-asc') listings.sort((a,b) => a.price_usd - b.price_usd);
  else listings.sort((a,b) => a.source.localeCompare(b.source));

  document.getElementById('listingCount').textContent = listings.length;

  const tbody = document.querySelector('#listingsTable tbody');
  tbody.innerHTML = '';
  listings.forEach(l => {{
    const features = l.features.map(f => `<span class="feature-tag">${{f}}</span>`).join(' ');
    tbody.innerHTML += `<tr>
      <td><span class="source-tag ${{sourceClass(l.source)}}">${{l.source}}</span></td>
      <td>${{l.title}}</td>
      <td style="font-weight:700">${{fmtUSD(l.price_usd)}}</td>
      <td>${{l.category}}</td>
      <td><span class="tier-tag ${{tierClass(l.quality_tier)}}">${{l.quality_tier}}</span></td>
      <td>${{features}}</td>
      <td><a class="view-link" href="${{l.url}}" target="_blank">View Listing &#8599;</a></td>
    </tr>`;
  }});
}}

// ============ SOURCES ============
function renderSources() {{
  const cards = document.getElementById('sourceCards');
  cards.innerHTML = '';

  for (const [name, profile] of Object.entries(D.marketplace_profiles)) {{
    cards.innerHTML += `
    <div class="source-card ${{sourceClass(name)}}">
      <h3><a href="${{profile.url}}" target="_blank">${{name}} &#8599;</a></h3>
      <div class="desc">${{profile.description}}</div>
      <div class="source-stat"><span class="label">Est. Listings</span><span class="val">${{fmt(profile.estimated_roblox_listings)}}</span></div>
      <div class="source-stat"><span class="label">Est. Total Sold</span><span class="val">${{fmt(profile.estimated_total_sold)}}</span></div>
      <div class="source-stat"><span class="label">Price Range</span><span class="val">$${{profile.price_range_usd[0]}} - $${{profile.price_range_usd[1]}}</span></div>
      <div class="source-stat"><span class="label">Avg Price</span><span class="val">$${{profile.avg_price_usd}}</span></div>
      <div class="source-stat"><span class="label">Guarantee</span><span class="val">${{profile.account_guarantee_days}} days</span></div>
      <div class="source-stat"><span class="label">Delivery</span><span class="val">${{profile.delivery}}</span></div>
      <div class="source-stat"><span class="label">Support</span><span class="val">${{profile.support}}</span></div>
      <div class="source-stat"><span class="label">Categories</span><span class="val">${{profile.categories.length}}</span></div>
    </div>`;
  }}

  const tbody = document.querySelector('#sourceTable tbody');
  tbody.innerHTML = '';
  D.source_breakdown.forEach(s => {{
    tbody.innerHTML += `<tr>
      <td><span class="source-tag ${{sourceClass(s.source_name)}}">${{s.source_name}}</span></td>
      <td>${{fmt(s.estimated_total_listings)}}</td>
      <td>${{fmt(s.estimated_total_sold)}}</td>
      <td>$${{s.price_range_min}} - $${{s.price_range_max}}</td>
      <td style="font-weight:700">${{fmtUSD(s.avg_price_usd)}}</td>
      <td>${{s.account_guarantee_days}} days</td>
      <td>${{s.delivery}}</td>
      <td>${{s.verified_sellers ? '&#9989; Yes' : '&#10060; No'}}</td>
      <td><a class="view-link" href="${{s.source_url}}" target="_blank">Visit &#8599;</a></td>
    </tr>`;
  }});
}}

// ============ CATEGORIES ============
function renderCategories() {{
  const cats = D.categories.sort((a,b) => b.listing_count - a.listing_count);

  destroyChart('catBar');
  charts.catBar = new Chart(document.getElementById('chartCatBar'), {{
    type: 'bar',
    data: {{
      labels: cats.map(c => c.category),
      datasets: [{{
        label: 'Listings',
        data: cats.map(c => c.listing_count),
        backgroundColor: '#6c5ce7cc',
        borderColor: '#6c5ce7',
        borderWidth: 1,
      }}]
    }},
    options: {{ responsive: true, indexAxis: 'y', scales: {{ x: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ display: false }} }} }}
  }});

  destroyChart('catPrice');
  charts.catPrice = new Chart(document.getElementById('chartCatPrice'), {{
    type: 'bar',
    data: {{
      labels: cats.map(c => c.category),
      datasets: [{{
        label: 'Avg Price (USD)',
        data: cats.map(c => c.avg_price_usd),
        backgroundColor: '#00cec9cc',
        borderColor: '#00cec9',
        borderWidth: 1,
      }}]
    }},
    options: {{ responsive: true, indexAxis: 'y', scales: {{ x: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ display: false }} }} }}
  }});

  const tbody = document.querySelector('#catTable tbody');
  tbody.innerHTML = '';
  cats.forEach(c => {{
    tbody.innerHTML += `<tr>
      <td style="font-weight:600">${{c.category}}</td>
      <td>${{c.listing_count}}</td>
      <td>${{c.sources.map(s => `<span class="source-tag ${{sourceClass(s)}}">${{s}}</span>`).join(' ')}}</td>
      <td>${{fmtUSD(c.min_price_usd)}}</td>
      <td>${{fmtUSD(c.max_price_usd)}}</td>
      <td style="font-weight:700">${{fmtUSD(c.avg_price_usd)}}</td>
    </tr>`;
  }});
}}

// ============ PRICE ANALYSIS ============
function renderPrices() {{
  // Price distribution histogram
  const prices = D.verified_listings.map(l => l.price_usd).sort((a,b) => a - b);
  const buckets = ['$0-10', '$10-50', '$50-100', '$100-200', '$200-500'];
  const ranges = [[0,10],[10,50],[50,100],[100,200],[200,500]];
  const counts = ranges.map(([lo,hi]) => prices.filter(p => p >= lo && p < hi).length);

  destroyChart('priceDist');
  charts.priceDist = new Chart(document.getElementById('chartPriceDist'), {{
    type: 'bar',
    data: {{
      labels: buckets,
      datasets: [{{
        label: 'Number of Listings',
        data: counts,
        backgroundColor: '#6c5ce7cc',
        borderColor: '#6c5ce7',
        borderWidth: 1,
      }}]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ display: false }} }} }}
  }});

  // Price by source
  const sources = ['U7Buy', 'Eldorado.gg', 'eBay'];
  const sourceAvgs = sources.map(s => {{
    const sp = D.verified_listings.filter(l => l.source === s).map(l => l.price_usd);
    return sp.reduce((a,b) => a+b, 0) / sp.length;
  }});
  const sourceMins = sources.map(s => Math.min(...D.verified_listings.filter(l => l.source === s).map(l => l.price_usd)));
  const sourceMaxs = sources.map(s => Math.max(...D.verified_listings.filter(l => l.source === s).map(l => l.price_usd)));

  destroyChart('priceBySource');
  charts.priceBySource = new Chart(document.getElementById('chartPriceBySource'), {{
    type: 'bar',
    data: {{
      labels: sources,
      datasets: [
        {{ label: 'Min', data: sourceMins, backgroundColor: '#26de8166' }},
        {{ label: 'Average', data: sourceAvgs, backgroundColor: sources.map(s => SOURCE_COLORS[s] + 'cc') }},
        {{ label: 'Max', data: sourceMaxs, backgroundColor: '#ff6b6b66' }},
      ]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ position: 'top' }} }} }}
  }});

  // Price by tier
  const tiers = D.quality_distribution.map(q => q.quality_tier);
  destroyChart('priceByTier');
  charts.priceByTier = new Chart(document.getElementById('chartPriceByTier'), {{
    type: 'bar',
    data: {{
      labels: tiers,
      datasets: [
        {{ label: 'Min', data: D.quality_distribution.map(q => q.min_price_usd), backgroundColor: '#26de8166' }},
        {{ label: 'Average', data: D.quality_distribution.map(q => q.avg_price_usd), backgroundColor: tiers.map(t => TIER_COLORS[t] + 'cc') }},
        {{ label: 'Max', data: D.quality_distribution.map(q => q.max_price_usd), backgroundColor: '#ff6b6b66' }},
      ]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }}, plugins: {{ legend: {{ position: 'top' }} }} }}
  }});

  // Cross-source price comparison
  const compDiv = document.getElementById('priceCompSection');
  if (D.price_comparison && D.price_comparison.length > 0) {{
    let html = '<div class="chart-card" style="margin-top:20px"><h3>Cross-Source Price Comparison</h3><div class="table-wrap"><table><thead><tr><th>Category</th>';
    sources.forEach(s => html += `<th>${{s}}</th>`);
    html += '</tr></thead><tbody>';
    D.price_comparison.forEach(pc => {{
      html += `<tr><td style="font-weight:600">${{pc.category}}</td>`;
      sources.forEach(s => {{
        if (pc.sources[s]) {{
          html += `<td>${{fmtUSD(pc.sources[s].avg_price)}} <span style="color:var(--text-dim);font-size:11px">(${{pc.sources[s].count}} listings)</span></td>`;
        }} else {{
          html += '<td style="color:var(--text-dim)">-</td>';
        }}
      }});
      html += '</tr>';
    }});
    html += '</tbody></table></div></div>';
    compDiv.innerHTML = html;
  }}
}}

// ============ BENCHMARKS ============
function renderBenchmarks() {{
  const grid = document.getElementById('benchmarkGrid');
  grid.innerHTML = '';
  for (const [name, bench] of Object.entries(D.price_benchmarks)) {{
    if (bench.typical_usd !== undefined) {{
      grid.innerHTML += `
        <div class="benchmark-item">
          <div class="bname">${{name}}</div>
          <div class="btypical">${{fmtUSD(bench.typical_usd)}}</div>
          <div class="brange">Range: $${{bench.min_usd}} - $${{bench.max_usd}}</div>
        </div>`;
    }} else if (bench.usd_equivalent !== undefined) {{
      grid.innerHTML += `
        <div class="benchmark-item">
          <div class="bname">${{name}}</div>
          <div class="btypical">${{fmt(bench.robux)}} Robux</div>
          <div class="brange">~${{fmtUSD(bench.usd_equivalent)}} USD equivalent</div>
        </div>`;
    }}
  }}
}}

// ============ INIT ============
renderOverview();
renderListings();
renderSources();
renderCategories();
renderPrices();
renderBenchmarks();

// Listing filters
['listingSource', 'listingTier', 'listingSort'].forEach(id => {{
  document.getElementById(id).addEventListener('change', renderListings);
}});
</script>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html)

print(f"Dashboard written to index.html")
print(f"File size: {len(html):,} bytes")
