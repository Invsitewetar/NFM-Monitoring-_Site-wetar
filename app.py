import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
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
        # Membersihkan spasi di nama kolom agar tidak error
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter ---
    st.sidebar.header("🔍 Pencarian NFM")
    search_nfm = st.sidebar.text_input("Cari Nomor Form (Contoh: 715)")
    search_dept = st.sidebar.text_input("Cari Departement") 
    search_req = st.sidebar.text_input("Cari Requestor") # Fitur Baru

    # Logika Filter
    res = df.copy()
    
    # Filter Nomor Form
    if search_nfm:
        if 'Nomor Form' in res.columns:
            res = res[res['Nomor Form'].astype(str).str.contains(search_nfm, na=False)]
    
    # Filter Departement
    if search_dept:
        if 'Departement' in res.columns:
            res = res[res['Departement'].astype(str).str.contains(search_dept, case=False, na=False)]

    # Filter Requestor (Logika Baru)
    if search_req:
        if 'Requestor' in res.columns:
            res = res[res['Requestor'].astype(str).str.contains(search_req, case=False, na=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        
        # --- TABEL UTAMA ---
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # Kolom yang ingin ditampilkan (Outstanding di samping Description)
        kolom_tampil = [
            'Nomor Form', 
            'Requestor',
            'NOMOR PR', 
            'Status PR', 
            'Item Code', 
            'Description', 
            'Amount Outstanding', 
            'Departement'
        ]
        
        # Hanya tampilkan kolom yang benar-benar ada di file Sheets
        cols_to_show = [c for c in kolom_tampil if c in res.columns]
        
        if cols_to_show:
            st.dataframe(res[cols_to_show], use_container_width=True)
        else:
            st.dataframe(res, use_container_width=True)
            
        # Detail Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                items = res['Item Code'].unique()
                for i in items:
                    st.write(f"- {i}")
    else:
        st.info("Data tidak ditemukan. Masukkan kata kunci di sidebar.")

else:
    st.error("Gagal memuat data. Periksa koneksi internet atau link Google Sheets kamu.")
