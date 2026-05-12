import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Pharmasix Historical Dashboard",
    layout="wide"
)

# =====================================
# LOAD LOGO
# =====================================
logo = Image.open("pharmasix_logo.png")

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

/* =========================
MAIN BACKGROUND
========================= */
.stApp {
    background: linear-gradient(to bottom right, #081028, #0E1B3D);
    color: white;
}

/* =========================
SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background: #081C4B;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* =========================
MULTISELECT
========================= */

/* BOX SELECT */
.stMultiSelect div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 4px;
}

/* TAG SELECTED */
[data-baseweb="tag"] {
    background-color: #2F6BFF !important;
    border-radius: 8px !important;
    border: none !important;
}

/* TAG TEXT */
[data-baseweb="tag"] span {
    color: white !important;
}

/* X BUTTON */
[data-baseweb="tag"] svg {
    fill: white !important;
}

/* INPUT TEXT */
.stMultiSelect input {
    color: black !important;
}

/* DROPDOWN */
div[data-baseweb="popover"] {
    color: black !important;
}

/* =========================
TITLE
========================= */
.dashboard-title {
    font-size: 38px;
    font-weight: bold;
    color: white;
}

.dashboard-subtitle {
    color: #AAB6D3;
    margin-bottom: 25px;
    font-size: 16px;
}

/* =========================
KPI CARD
========================= */
.kpi-card {
    background: linear-gradient(145deg, #111C44, #0B1739);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* KPI TITLE */
.kpi-title {
    color: #AEB9D6;
    font-size: 15px;
    margin-bottom: 10px;
}

/* KPI VALUE */
.kpi-value {
    color: white;
    font-size: 34px;
    font-weight: bold;
}

/* =========================
CHART BOX
========================= */
.chart-box {
    background: linear-gradient(145deg, #111C44, #0B1739);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* =========================
TEXT
========================= */
h1, h2, h3, h4, p {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================
df = pd.read_csv("pharmasix_dataset.csv")

# =====================================
# PREPROCESSING
# =====================================
df['date'] = pd.to_datetime(df['date'])

# =====================================
# SIDEBAR HEADER
# =====================================
st.sidebar.image(logo, width=110)

st.sidebar.markdown("""
<h1 style='
color:white;
font-size:34px;
margin-top:-10px;
margin-bottom:0px;
'>
PharmaSix
</h1>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.title("📌 FILTER")

# =====================================
# SIDEBAR FILTER
# =====================================
selected_years = st.sidebar.multiselect(
    "Periode Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df['region'].unique()),
    default=df['region'].unique()
)

selected_category = st.sidebar.multiselect(
    "Kategori Obat",
    options=sorted(df['category'].unique()),
    default=df['category'].unique()
)

# =====================================
# FILTER DATAFRAME
# =====================================
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['category'].isin(selected_category))
]

# =====================================
# TITLE
# =====================================
col_logo, col_title = st.columns([1, 8])

with col_logo:
    st.image(logo, width=80)

with col_title:
    st.markdown("""
    <div class='dashboard-title'>
    Pharmasix Historical Dashboard
    </div>

    <div class='dashboard-subtitle'>
    Analisis penjualan dan permintaan obat tahun 2020-2025
    </div>
    """, unsafe_allow_html=True)

# =====================================
# KPI SECTION
# =====================================
total_obat = filtered_df['medicine'].nunique()
unit_sold = filtered_df['units_sold'].sum()
total_transaksi = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

# KPI 1
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💊 Total Obat</div>
        <div class="kpi-value">{total_obat}</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 2
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📦 Unit Sold</div>
        <div class="kpi-value">{unit_sold:,}</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 3
with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🧾 Total Transaksi</div>
        <div class="kpi-value">{total_transaksi:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# ROW 1
# =====================================
col4, col5 = st.columns(2)

# =====================================
# 1. OBAT TERTINGGI & TERENDAH
# =====================================
with col4:

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    st.subheader("💊 Volume Penjualan Obat Tertinggi & Terendah")

    medicine_sales = (
        filtered_df.groupby('medicine')['units_sold']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    top_bottom = pd.concat([
        medicine_sales.head(5),
        medicine_sales.tail(5)
    ])

    fig = px.bar(
        top_bottom,
        x='units_sold',
        y='medicine',
        orientation='h',
        color='units_sold',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        paper_bgcolor="#111C44",
        plot_bgcolor="#111C44",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
    top_med = medicine_sales.iloc[0]
    low_med = medicine_sales.iloc[-1]

    st.markdown(f"""
    <div style='color:#D6E2FF; margin-top:10px;'>

    <b>Insight:</b><br>

    Obat dengan volume penjualan tertinggi adalah 
    <b>{top_med['medicine']}</b> sebanyak 
    <b>{top_med['units_sold']:,.0f}</b> unit.

    Sedangkan obat dengan volume penjualan terendah adalah 
    <b>{low_med['medicine']}</b> sebanyak 
    <b>{low_med['units_sold']:,.0f}</b> unit.

    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# 2. TREN PENJUALAN
# =====================================
with col5:

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    st.subheader("📈 Tren Penjualan Obat 2020-2025")

    trend = (
        filtered_df.groupby('year')['units_sold']
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x='year',
        y='units_sold',
        markers=True
    )

    fig.update_traces(
        line_width=4
    )

    fig.update_layout(
        paper_bgcolor="#111C44",
        plot_bgcolor="#111C44",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
    max_year = trend.loc[trend['units_sold'].idxmax()]

    st.markdown(f"""
    <div style='color:#D6E2FF; margin-top:10px;'>

    <b>Insight:</b><br>

    Tren penjualan obat dari tahun 2020 hingga 2025 menunjukkan
    perubahan jumlah unit sold setiap tahunnya.

    Penjualan tertinggi terjadi pada tahun 
    <b>{max_year['year']}</b> dengan total penjualan 
    <b>{max_year['units_sold']:,.0f}</b> unit.

    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# ROW 2
# =====================================
col6, col7 = st.columns(2)

# =====================================
# 3. POLA MUSIMAN
# =====================================
with col6:

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    st.subheader("📅 Pola Musiman Permintaan Obat")

    seasonal = (
        filtered_df.groupby('month')['units_sold']
        .mean()
        .reset_index()
    )

    fig = px.line(
        seasonal,
        x='month',
        y='units_sold',
        markers=True
    )

    fig.update_traces(
        line_width=4
    )

    fig.update_layout(
        paper_bgcolor="#111C44",
        plot_bgcolor="#111C44",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
    peak_month = seasonal.loc[seasonal['units_sold'].idxmax()]

    st.markdown(f"""
    <div style='color:#D6E2FF; margin-top:10px;'>

    <b>Insight:</b><br>

    Grafik menunjukkan adanya pola musiman pada permintaan obat.

    Permintaan tertinggi terjadi pada bulan 
    <b>{peak_month['month']}</b> dengan rata-rata penjualan sebesar 
    <b>{peak_month['units_sold']:,.2f}</b> unit.

    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# 4. DISTRIBUSI BERDASARKAN KATEGORI
# =====================================
with col7:

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    st.subheader("📊 Distribusi Permintaan Berdasarkan Kategori Obat")

    category_dist = (
        filtered_df.groupby('category')['units_sold']
        .sum()
        .reset_index()
        .sort_values(by='units_sold', ascending=False)
    )

    fig = px.bar(
        category_dist,
        x='category',
        y='units_sold',
        color='units_sold',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        paper_bgcolor="#111C44",
        plot_bgcolor="#111C44",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
    top_category = category_dist.iloc[0]

    st.markdown(f"""
    <div style='color:#D6E2FF; margin-top:10px;'>

    <b>Insight:</b><br>

    Kategori obat dengan permintaan tertinggi adalah 
    <b>{top_category['category']}</b> dengan total penjualan sebesar 
    <b>{top_category['units_sold']:,.0f}</b> unit.

    Hal ini menunjukkan bahwa kategori tersebut memiliki
    permintaan pasar yang paling dominan.

    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# 5. DISTRIBUSI REGION
# =====================================
st.markdown('<div class="chart-box">', unsafe_allow_html=True)

st.subheader("🌍 Distribusi Permintaan Obat di Setiap Region")

region_sales = (
    filtered_df.groupby('region')['units_sold']
    .sum()
    .reset_index()
)

fig = go.Figure(
    data=[go.Pie(
        labels=region_sales['region'],
        values=region_sales['units_sold'],
        hole=0.4,
        textinfo='percent+label',
        texttemplate='%{label}<br>%{percent:.2%}'
    )]
)

fig.update_layout(
    paper_bgcolor="#111C44",
    plot_bgcolor="#111C44",
    font_color="white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)
top_region = region_sales.sort_values(
    by='units_sold',
    ascending=False
).iloc[0]

st.markdown(f"""
<div style='color:#D6E2FF; margin-top:10px;'>

<b>Insight:</b><br>

Region dengan distribusi permintaan obat tertinggi adalah 
<b>{top_region['region']}</b> dengan total penjualan sebesar 
<b>{top_region['units_sold']:,.0f}</b> unit.

Hal ini menunjukkan bahwa region tersebut memiliki
tingkat permintaan obat paling tinggi dibanding region lainnya.

</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)