import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

# LINK CSV FINAL
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Hapus kolom pengetesan
        cols_to_drop = ['Tes', 'Tes 2']
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter ---
    st.sidebar.header("🔍 Pencarian")
    search_unit = st.sidebar.text_input("Cari Nomor Unit")
    search_ps = st.sidebar.text_input("Cari Nomor PS")
    search_wo = st.sidebar.text_input("Cari Nomor WO")

    # Logika Filter
    filtered_df = df.copy()
    if search_unit:
        filtered_df = filtered_df[filtered_df['Unit Number'].astype(str).str.contains(search_unit, case=False, na=False)]
    if search_ps:
        filtered_df = filtered_df[filtered_df['PS Number'].astype(str).str.contains(search_ps, case=False, na=False)]
    if search_wo:
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False, na=False)]

    # --- BAGIAN GRAFIK & SUMMARY ---
    st.subheader("📊 Ringkasan Status")
    
    # Membuat 3 kolom untuk Metric
    m1, m2, m3 = st.columns(3)
    total_data = len(filtered_df)
    
    # Menghitung jumlah per status (Pastikan nama kolom 'PS Status' sesuai di Sheets kamu)
    if 'PS Status' in filtered_df.columns:
        status_counts = filtered_df['PS Status'].value_counts()
        
        m1.metric("Total Item", total_data)
        m2.metric("Sudah GR", status_counts.get('GR', 0))
        m3.metric("Status NFM", status_counts.get('NFM', 0))

        # Menampilkan Grafik Batang
        fig = px.bar(
            status_counts, 
            x=status_counts.index, 
            y=status_counts.values,
            labels={'x': 'Status Barang', 'y': 'Jumlah'},
            color=status_counts.index,
            color_discrete_map={'GR': '#2ecc71', 'NFM': '#e74c3c', 'Keluar': '#3498db'} # Warna hijau, merah, biru
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom 'PS Status' tidak ditemukan untuk membuat grafik.")

    # --- Tabel Detail ---
    st.subheader("📋 Detail Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu data...")
except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
