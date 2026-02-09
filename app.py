import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFM Tracking Site Wetar", layout="centered")
st.title("🚢 NFM Tracking Site Wetar")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60) 
def load_data():
    # Membaca CSV dan membersihkan nama kolom dari spasi yang tidak sengaja terketik
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip() 
    return df

try:
    df = load_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Mencocokkan data tanpa peduli spasi di depan/belakang angka
        df['Nomor Form'] = df['Nomor Form'].astype(str).str.strip()
        result = df[df['Nomor Form'] == search_query]

        if not result.empty:
            row = result.iloc[0]
            st.success("✅ Data Ditemukan")
            
            # --- Bagian Tampilan ---
            st.markdown(f"### 📄 {row.get('Nomor Form', '')} - {row.get('Deskripsi', 'No Description')}")
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"🏢 **Dept:** {row.get('Dept', '-')}")
                st.write(f"👤 **Requestor:** {row.get('Requestor', '-')}")
                with st.expander("📦 Lihat Rincian Item Codes"):
                    st.write(row.get('Item Codes', 'Tidak ada data'))
            
            with c2:
                st.write(f"📋 **Nomor PR:** {row.get('Nomor PR', '-')}")
                st.write(f"✅ **Status PR:** {row.get('Status PR', '-')}")
                st.warning(f"💰 Outstanding: {row.get('Outstanding', 'Rp 0.00')}")

            st.info(f"📑 **STATUS REQ:** {row.get('Status Req', '-')}")
            # -----------------------
            
        else:
            st.error("❌ Nomor Form tidak ditemukan. Silakan cek kembali.")
            # Baris di bawah ini untuk bantu kamu debug, hapus kalau sudah jalan
            with st.expander("Klik untuk cek daftar nomor yang tersedia"):
                st.write(df['Nomor Form'].tolist())

except Exception as e:
    st.error(f"Error: {e}")
