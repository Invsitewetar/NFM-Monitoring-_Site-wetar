import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="NFM Monitoring", layout="wide")
st.title("📦 NFM & Backlog Monitoring Dashboard")
st.markdown("---")

# LINK GOOGLE SHEETS TERBARU KAMU
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        return data
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter ---
    st.sidebar.header("🔍 Filter NFM")
    u = st.sidebar.text_input("Cari Unit")
    p = st.sidebar.text_input("Cari PS Number")
    w = st.sidebar.text_input("Cari WO")
    
    # Logika Filter
    df_f = df.copy()
    if u: df_f = df_f[df_f['Unit'].astype(str).str.contains(u, case=False, na=False)]
    if p: df_f = df_f[df_f['PS Number'].astype(str).str.contains(p, case=False, na=False)]
    if w: df_f = df_f[df_f['WO'].astype(str).str.contains(w, case=False, na=False)]

    # --- BAGIAN DASHBOARD KHUSUS NFM ---
    if 'Status' in df_f.columns:
        st.subheader("📊 Statistik Status NFM")
        counts = df_f['Status'].value_counts()
        
        # Metric Utama
        m1, m2, m3 = st.columns(3)
        total = len(df_f)
        nfm_count = counts.get('NFM', 0)
        gr_count = counts.get('GR', 0)
        
        m1.metric("Total Item", total)
        m2.metric("Status NFM (🔴)", nfm_count, delta=f"{nfm_count/total*100:.1f}% dari total", delta_color="inverse")
        m3.metric("Status GR (🟢)", gr_count)

        # Grafik Batang Khusus Status
        fig = px.bar(
            x=counts.index, 
            y=counts.values,
            labels={'x': 'Status', 'y': 'Jumlah'},
            color=counts.index,
            # Merah untuk NFM, Hijau untuk GR, Biru untuk lainnya
            color_discrete_map={'NFM': '#ef5350', 'GR': '#66bb6a'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Tabel Detail ---
    st.subheader("📋 Daftar Rincian Barang")
    st.dataframe(df_f, use_container_width=True)

else:
    st.error("⚠️ Data tidak terbaca. Pastikan link Google Sheets benar.")
