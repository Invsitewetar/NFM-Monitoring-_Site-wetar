import streamlit as st
import pandas as pd

# 1. Judul Dashboard
st.set_page_config(page_title="NFM Monitoring", layout="wide")
st.title("📦 NFM Monitoring Dashboard")
st.markdown("---")

# Link Google Sheets NFM kamu
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

if df is not None:
    # Sidebar Pencarian
    st.sidebar.header("🔍 Pencarian NFM")
    search_nfm = st.sidebar.text_input("Cari Nomor Form (Contoh: 724)")
    search_unit = st.sidebar.text_input("Cari Unit")

    # Filter Data
    res = df.copy()
    if search_nfm:
        res = res[res['Nomor Form'].astype(str).str.contains(search_nfm, na=False)]
    if search_unit:
        res = res[res['Unit'].astype(str).str.contains(search_unit, case=False, na=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        
        # --- TABEL UTAMA DENGAN OUTSTANDING ---
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # Daftar kolom (Item Code sesuai permintaanmu)
        kolom_tampil = [
            'Nomor Form', 
            'NOMOR PR', 
            'Status PR', 
            'Total Value', 
            'Amount Outstanding', 
            'Item Code', 
            'Description'
        ]
        
        # Filter hanya kolom yang ada di database
        cols_to_show = [c for c in kolom_tampil if c in res.columns]
        
        if cols_to_show:
            st.dataframe(res[cols_to_show], use_container_width=True)
        else:
            st.dataframe(res, use_container_width=True)
            
        # Bagian Daftar Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                # Kita pakai list sederhana agar tidak error spasi lagi
                items = res['Item Code'].unique()
                for i in items:
                    st.write(f"- {i}")
    else:
        st.info("Masukkan Nomor Form di sidebar untuk melihat rincian NFM.")
else:
    st.error("Gagal memuat data.")}`")
