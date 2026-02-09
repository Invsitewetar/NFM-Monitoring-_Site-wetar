import streamlit as st
import pandas as pd

# Judul Utama
st.set_page_config(page_title="NFM Tracking Site Wetar", layout="centered")
st.title("🚢 NFM Tracking Site Wetar")
st.divider()

# Link CSV dari Google Sheets kamu
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?gid=0&single=true&output=csv"

# Fungsi untuk membaca data
@st.cache_data(ttl=600) # Data di-refresh setiap 10 menit
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Pastikan kolom Nomor Form dibaca sebagai string agar mudah dicari
    df['Nomor Form'] = df['Nomor Form'].astype(str)
    return df

try:
    df = load_data()

    # Input Nomor Form
    search_query = st.text_input("🔍 Masukkan Nomor Form:", placeholder="Contoh: 511")

    if search_query:
        # Cari data berdasarkan kolom 'Nomor Form'
        # Sesuaikan nama kolom 'Nomor Form' dengan yang ada di Excel kamu
        result = df[df['Nomor Form'] == search_query]

        if not result.empty:
            row = result.iloc[0] # Ambil baris pertama yang ditemukan
            
            st.success("✅ Data Ditemukan")
            
            # Judul Dokumen (Sesuaikan nama kolomnya)
            # Misalnya kolom 'Deskripsi' atau 'Judul'
            st.markdown(f"### 📄 {row['Nomor Form']} - {row.get('Judul/Deskripsi', 'Deskripsi Tidak Ada')}")
            st.divider()

            # Layout 2 Kolom
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"🏢 **Dept:** {row.get('Dept', 'N/A')}")
                st.write(f"👤 **Requestor:** {row.get('Requestor', 'N/A')}")
                with st.expander("📦 Lihat Rincian Item Codes"):
                    st.write(row.get('Item Codes', 'Tidak ada rincian'))

            with col2:
                st.write(f"📋 **Nomor PR:** {row.get('Nomor PR', 'N/A')}")
                st.write(f"✅ **Status PR:** {row.get('Status PR', 'N/A')}")
                # Outstanding dengan format mata uang
                outstanding = row.get('Outstanding', 0)
                st.warning(f"💰 Outstanding: Rp {outstanding:,.2f}")

            st.divider()

            # Status Request (Banner Biru)
            status_req = row.get('Status Req', 'DALAM PROSES')
            st.info(f"📑 **STATUS REQ:** {status_req}")

            # Expander Bawah
            with st.expander("📝 Lihat Detail Deskripsi Barang"):
                st.write(row.get('Detail Deskripsi', 'Tidak ada detail tambahan.'))
        else:
            st.error("❌ Nomor Form tidak ditemukan. Silakan cek kembali.")
    else:
        st.info("Silakan masukkan Nomor Form untuk melacak status.")

except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.error("⚠️ Data tidak terbaca. Pastikan link Google Sheets benar.")
