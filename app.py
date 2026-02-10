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
        # Membersihkan spasi di awal/akhir nama kolom
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

if df is not None:
    # Sidebar Pencarian
    st.sidebar.header("🔍 Pencarian NFM")
    # Kamu bisa cari berdasarkan Nomor Form atau Unit
    search_nfm = st.sidebar.text_input("Cari Nomor Form (Contoh: 724)")
    search_unit = st.sidebar.text_input("Cari Unit")

    # Filter Data
    res = df.copy()
    if search_nfm:
        # Menyesuaikan nama kolom 'Nomor Form' di Sheets kamu
        res = res[res['Nomor Form'].astype(str).str.contains(search_nfm, na=False)]
    if search_unit:
        res = res[res['Unit'].astype(str).str.contains(search_unit, case=False, na=False)]
    
    if not res.empty:
        # Menampilkan Ringkasan
        st.success(f"✅ Ditemukan {len(res)} baris data (Bisa terdiri dari beberapa PO)")
        
        # TABEL UTAMA (Menampilkan semua PO yang ada untuk NFM tersebut)
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # Kolom yang akan ditampilkan di tabel
        kolom_tampil = ['Nomor Form', 'NOMOR PR', 'Status PR', 'Total Value', 'Item Code', 'Description', 'Unit']
        # Hanya tampilkan yang ada di Sheets kamu
        cols_to_show = [c for c in kolom_tampil if c in res.columns]
        
        if cols_to_show:
            st.dataframe(res[cols_to_show], use_container_width=True)
        else:
            # Jika kolom di atas tidak ketemu, tampilkan semua kolom saja
            st.dataframe(res, use_container_width=True)
            
        # Detail Item Code (Expander)
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                for item in res['Item Code'].unique():
                    st.write(f"- `{item}`")
