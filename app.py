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
        data.columns = data.columns.str.strip() # Hapus spasi gaib di judul kolom
        return data
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Pencarian (Requestor sudah dihapus sesuai permintaan) ---
    st.sidebar.header("🔍 Pencarian NFM")
    search_nfm = st.sidebar.text_input("Cari Nomor Form")
    search_dept = st.sidebar.text_input("Cari Departement") 

    # Logika Filter
    res = df.copy()
    
    # Cari Nama Kolom secara otomatis agar tidak KeyError
    col_dept = next((c for c in res.columns if 'departement' in c.lower() or 'dept' in c.lower()), None)
    col_out = next((c for c in res.columns if 'outstanding' in c.lower() or ('value' in c.lower() and 'site' in c.lower())), None)
    
    # Filter Form (Tidak peduli huruf besar/kecil)
    if search_nfm:
        res = res[res.iloc[:, 0].astype(str).str.contains(search_nfm, na=False, case=False)]
    
    # Filter Departement (Sekarang 'mobile' atau 'MOBILE' dua-duanya bisa ketemu)
    if search_dept and col_dept:
        res = res[res[col_dept].astype(str).str.contains(search_dept, na=False, case=False)]
    
    if not res.empty:
        st.success(f"✅ Ditemukan {len(res)} baris data")
        st.subheader("📑 Daftar PR / PO & Status Outstanding")
        
        # --- MENYUSUN KOLOM AGAR OUTSTANDING MUNCUL ---
        kolom_wajib = ['Nomor Form', 'Requestor', 'NOMOR PR', 'Status PR', 'Item Code', 'Description']
        
        # Ambil kolom yang memang ada di database
        final_cols = [c for c in kolom_wajib if c in res.columns]
        
        # Masukkan kolom Outstanding tepat setelah Description
        if col_out and col_out not in final_cols:
            final_cols.append(col_out)
            
        # Masukkan Departement di paling akhir
        if col_dept and col_dept not in final_cols:
            final_cols.append(col_dept)

        # Tampilkan Tabel
        st.dataframe(res[final_cols], use_container_width=True)
            
        # Daftar Item Code
        if 'Item Code' in res.columns:
            with st.expander("📦 Lihat Daftar Item Code"):
                for i in res['Item Code'].unique():
                    st.write(f"- {i}")
    else:
        st.info("Data tidak ditemukan. Coba cek kembali ejaan Departement atau Nomor Form kamu.")
else:
    st.error("Gagal memuat data. Periksa link Google Sheets kamu.")
