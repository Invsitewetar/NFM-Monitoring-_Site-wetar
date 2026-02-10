import streamlit as st
import pandas as pd

# 1. Judul Dashboard
st.set_page_config(page_title="NFM Monitoring", layout="wide")
st.title("🚢 NFM Tracking Site Wetar")
st.markdown("---")

# Link Google Sheets NFM kamu
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        return data
    except:
        return None

df = load_data()

if df is not None:
    # Pencarian Nomor Form NFM
    search_nfm = st.text_input("🔍 Masukkan Nomor Form NFM (Contoh: 724):")
    
    if search_nfm:
        # Mencari semua baris yang mengandung nomor NFM tersebut
        # Ini kuncinya: kita ambil SEMUA baris, bukan cuma satu
        res = df[df['Nomor Form'].astype(str).str.contains(search_nfm, na=False)]
        
        if not res.empty:
            st.success(f"✅ Ditemukan {len(res)} baris data untuk NFM ini")
            
            # --- Bagian Atas: Informasi Umum NFM (Ambil dari baris pertama) ---
            first_row = res.iloc[0]
            st.subheader(f"📄 {first_row.get('Nomor Full', 'Detail NFM')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"🏢 **Dept:** {first_row.get('Dept', '-')}")
                st.write(f"👤 **Requestor:** {first_row.get('Requestor', '-')}")
            
            # --- Bagian Bawah: Tabel PR/PO (Menampilkan semua PO yang ada) ---
            st.markdown("---")
            st.subheader("📑 Daftar PR / PO & Status Outstanding")
            
            # Menampilkan kolom-kolom penting saja agar ringkas
            po_columns = ['NOMOR PR', 'Status PR', 'Total Value', 'GR Dated', 'SOH ON SITE']
            # Pastikan kolom ada di data
            existing_cols = [c for c in po_columns if c in res.columns]
            
            if existing_cols:
                # Menampilkan tabel khusus untuk PO-PO tersebut
                st.table(res[existing_cols])
            else:
                st.warning("Kolom detail PR/PO tidak ditemukan di database.")
                
            # Detail Stock Codes (Expander)
            with st.expander("📦 Lihat Rincian Stock Codes"):
                for code in res['Stock Code'].unique():
                    st.code(code)
        else:
            st.error("❌ Nomor Form NFM tidak ditemukan.")
else:
    st.error("Gagal memuat data.")
    st.error(f"Terjadi kendala pembacaan data: {e}")
