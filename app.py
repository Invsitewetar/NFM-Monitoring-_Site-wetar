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
        # Bersihkan kolom percobaan jika ada
        cols_to_drop = ['Tes', 'Tes 2']
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
        return df
    except Exception as e:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter ---
    st.sidebar.header("🔍 Pencarian")
    search_unit = st.sidebar.text_input("Cari Nomor Unit (Contoh: GR004)")
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

    # --- BAGIAN VISUALISASI ---
    st.subheader("📊 Ringkasan Status Barang")
    
    if 'PS Status' in filtered_df.columns:
        status_counts = filtered_df['PS Status'].value_counts()
        
        # Metric Box (Angka Utama)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Item", len(filtered_df))
        m2.metric("Selesai (Finished)", status_counts.get('Finished', 0))
        m3.metric("Status Lainnya", len(filtered_df) - status_counts.get('Finished', 0))

        # Grafik Batang Interaktif
        fig = px.bar(
            x=status_counts.index, 
            y=status_counts.values,
            labels={'x': 'Status', 'y': 'Jumlah Barang'},
            title="Distribusi Status PS",
            color=status_counts.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Tip: Pastikan ada kolom 'PS Status' di Sheets untuk melihat grafik.")

    # --- Tabel Data ---
    st.subheader("📋 Detail Data Monitoring")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu data. Pastikan link Google Sheets sudah benar.")
except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
