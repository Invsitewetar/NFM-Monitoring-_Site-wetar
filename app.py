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
        # Menghapus spasi gaib agar kolom terbaca sempurna
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter ---
    st.sidebar.header("🔍 Pencarian NFM")
    search_nfm = st.sidebar.text_input("Cari Nomor Form")
    search_dept = st.sidebar.text_input("Cari Departement") 
    search_req = st.sidebar.text_input("Cari Requestor")

    # Logika Filter
    res = df.copy()
    if search_nfm:
        res = res[res.iloc[:, 0].astype(str).str.contains(search_nfm, na=False)]
    if search_dept:
        # Cari kolom Departement secara otomatis
        c_dept = next((c for c in res.columns if 'departement' in c.lower() or 'dept' in c.lower()), None)
        if c_dept:
            res = res[res[c_dept].astype(str).str.contains(search_dept, case=False, na=False)]
    if search_req:
        if 'Requestor' in res.columns:
            res = res[res['Requestor'].astype(str).str.contains(search_req, case=False, na=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # --- MENYUSUN TABEL SECARA PAKSA AGAR MUNCUL ---
        # Kita panggil nama kolomnya satu per satu
        kolom_tampil = [
            'Nomor Form', 
            'Requestor', 
            'NOMOR PR', 
            'Status PR', 
            'Item Code', 
            'Description', 
            'Outstanding On Site Value', # Nama ini harus sama persis dengan di Sheets
            'Departement'
        ]
        
        # Cek mana kolom yang benar-benar ada di file kamu
        final_cols = [c for c in kolom_tampil if c in res.columns]
        
        # Jika kolom Outstanding masih tidak ketemu, kita cari yang ada kata 'Value'
        if 'Outstanding On Site Value' not in final_cols:
            alt_out = next((c for c in res.columns if 'value' in c.lower() and 'site' in c.lower()), None)
            if alt_out:
                # Masukkan kolom alternatif ini setelah Description
                desc_idx = final_cols.index('Description') + 1 if 'Description' in final_cols else len(final_cols)
                final_cols.insert(desc_idx, alt_out)

        # Tampilkan Tabel
        st.dataframe(res[final_cols], use_container_width=True)
            
        # Detail Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                items = res['Item Code'].unique()
                for i in items:
                    st.write(f"- {i}")
    else:
        st.info("Gunakan filter di samping untuk melihat data.")
else:
    st.error("Gagal memuat data. Periksa link Google Sheets kamu.")
