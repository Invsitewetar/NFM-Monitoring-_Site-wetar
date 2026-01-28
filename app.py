import streamlit as st
import pandas as pd

# Link CSV Anda
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

st.title("🚢 Non Fast Moving (NFM) Tracker")
st.write("---")

@st.cache_data(ttl=60)
def get_data():
    df = pd.read_csv(URL_DATA)
    df.columns = df.columns.str.strip()
    return df

try:
    data = get_data()
    
    # Input pencarian yang lebih bersih
    search_query = st.text_input("🔍 Masukkan Nomor Form (Contoh: 002):").strip()

    if search_query:
        # Filter untuk mencari yang persis sama (Exact Match)
        # Ini akan mencegah munculnya banyak hasil jika hanya ketik angka pendek
        result = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            # Hanya ambil baris pertama jika ada lebih dari satu
            row = result.iloc[0]
            
            st.success(f"✅ Data Ditemukan: {row['Nomor Form']}")
            
            # Tampilan kartu informasi tunggal yang sederhana
            with st.container(border=True):
                st.subheader(f"📝 {row['Description']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**👤 Requestor:** {row.get('Requestor', '-')}")
                    st.write(f"**📦 Item Code:** {row.get('Item Code', '-')}")
                    st.write(f"**🏢 Dept:** {row.get('Departement', '-')}")
                
                with col2:
                    st.write(f"**📑 Status REQ:** {row.get('STATUS REQ', '-')}")
                    st.write(f"**✅ Status PR:** {row.get('STATUS PR', '-')}")
                    st.write(f"**⏳ Aging:** {row.get('Aging', '-')} Days")

                st.divider()
                st.info(f"**👤 Waiting Approval:** {row.get('Waiting Approval', '-')}")
        else:
            st.error("❌ Nomor Form tidak ditemukan. Periksa kembali nomor yang Anda masukkan.")
    else:
        st.info("💡 Silakan ketik nomor form Anda di atas.")

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan koneksi stabil. Error: {e}")
except Exception as e:
    st.error(f"Aplikasi gagal membaca data. Pastikan link CSV benar. Error: {e}")
