import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul Aplikasi
st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

# 2. Link Data Google Sheets (Gunakan link CSV kamu yang sudah benar)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Bersihkan kolom sampah
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.drop(columns=['Tes', 'Tes 2'], errors='ignore')
        return df
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Pencarian ---
    st.sidebar.header("🔍 Pencarian")
    u = st.sidebar.text_input("Cari Unit Number")
    p = st.sidebar.text_input("Cari PS Number")
    w = st.sidebar.text_input("Cari Wo Number")

    # Logika Filter
    f_df = df.copy()
    if u: f_df = f_df[f_df['Unit Number'].astype(str).str.contains(u, case=False, na=False)]
    if p: f_df = f_df[f_df['PS Number'].astype(str).str.contains(p, case=False, na=False)]
    if w: f_df = f_df[f_df['Wo Number'].astype(str).str.contains(w, case=False, na=False)]

    # --- Bagian Grafik ---
    st.subheader("📊 Statistik Status")
    if 'PS Status' in f_df.columns:
        counts = f_df['PS Status'].value_counts()
        
        # Tampilkan Grafik
        fig = px.pie(values=counts.values, names=counts.index, title="Persentase Status Barang")
        st.plotly_chart(fig, use_container_width=True)
        
        # Ringkasan Angka
        c1, c2 = st.columns(2)
        c1.metric("Total Data", len(f_df))
        c2.metric("Sudah Finished", counts.get('Finished', 0))
    
    # --- Tabel Utama ---
    st.subheader("📋 Detail Data")
    st.dataframe(f_df, use_container_width=True)

else:
    st.error("Gagal memuat data. Cek link Google Sheets kamu.")
except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
