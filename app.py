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
    # --- Sidebar Pencarian (Pakai No. Form Pendek) ---
    st.sidebar.header("🔍 Pencarian NFM")
    search_no_form = st.sidebar.text_input("Masukkan No. Form (Contoh: 761)")
    search_dept = st.sidebar.text_input("Cari Departement") 

    # Logika Filter
    res = df.copy()
    
    # Cari Nama Kolom secara otomatis
    col_no_form = next((c for c in res.columns if 'NO FORM' == c.upper() or 'NO. FORM' == c.upper()), None)
    col_dept = next((c for c in res.columns if 'DEPARTEMENT' in c.upper() or 'DEPT' in c.upper()), None)
    col_out = next((c for c in res.columns if 'OUTSTANDING ON SITE VALUE' == c.upper()), None)
    
    # Filter No Form (Mencari angka pendek)
    if search_no_form and col_no_form:
        res = res[res[col_no_form].astype(str).str.contains(search_no_form, na=False)]
    
    # Filter Departement
    if search_dept and col_dept:
        res = res[res[col_dept].astype(str).str.contains(search_dept, na=False, case=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # --- MENYUSUN TABEL ---
        # Daftar kolom yang ingin ditampilkan
        kolom_pilihan = [col_no_form, 'Nomor Form', 'Requestor', 'NOMOR PR', 'Status PR', 'Item Code', 'Description', col_out, col_dept]
        
        # Ambil kolom yang memang ada di database dan buang yang None
        final_cols = [c for c in kolom_pilihan if c is not None and c in res.columns]
        
        # Pastikan 'Value On site' dibuang jika terbawa otomatis
        if 'Value On site' in final_cols:
            final_cols.remove('Value On site')

        # Tampilkan Tabel
        st.dataframe(res[final_cols], use_container_width=True)
            
        # Detail Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                for i in res['Item Code'].unique():
                    st.write(f"- {i}")
    else:
        st.info("Data tidak ditemukan. Coba ketik nomor pendeknya saja (misal: 761).")
else:
    st.error("Gagal memuat data. Periksa kembali link Google Sheets kamu.")
