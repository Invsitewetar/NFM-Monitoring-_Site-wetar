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
        data.columns = data.columns.str.strip() # Hapus spasi gaib
        return data
    except:
        return None

df = load_data()

if df is not None:
    # --- Cari Nama Kolom Otomatis (Cegah KeyError) ---
    all_cols = df.columns.tolist()
    # Mencari kolom yang mengandung kata 'Departement', 'Form', atau 'Outstanding'
    col_dept = next((c for c in all_cols if 'departement' in c.lower() or 'dept' in c.lower()), None)
    col_form = next((c for c in all_cols if 'form' in c.lower()), None)
    col_out = next((c for c in all_cols if 'outstanding' in c.lower() or 'out' in c.lower()), None)

    # --- Sidebar Filter (Unit dihapus) ---
    st.sidebar.header("🔍 Pencarian NFM")
    search_nfm = st.sidebar.text_input("Cari Nomor Form (Contoh: 715)")
    search_dept = st.sidebar.text_input("Cari Departement") 

    # Logika Filter
    res = df.copy()
    if search_nfm and col_form:
        res = res[res[col_form].astype(str).str.contains(search_nfm, na=False)]
    if search_dept and col_dept:
        res = res[res[col_dept].astype(str).str.contains(search_dept, case=False, na=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        
        # --- TABEL UTAMA ---
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # Susunan kolom permintaanmu: Description lalu Outstanding di sampingnya
        # Kita masukkan kolom-kolom penting ke dalam list
        kolom_pilihan = [col_form, 'NOMOR PR', 'Status PR', 'Item Code', 'Description', col_out, col_dept]
        
        # Filter hanya kolom yang benar-benar ada di database
        cols_to_show = [c for c in kolom_pilihan if c is not None and c in res.columns]
        
        # Menampilkan tabel
        st.dataframe(res[cols_to_show], use_container_width=True)
            
        # Bagian Daftar Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                for i in res['Item Code'].unique():
                    st.write(f"- {i}")
    else:
        st.info("Silakan cari berdasarkan Nomor Form atau Departement.")
else:
    st.error("Gagal memuat data. Periksa link Google Sheets kamu.")error("Gagal memuat data. Periksa link Google Sheets kamu."
