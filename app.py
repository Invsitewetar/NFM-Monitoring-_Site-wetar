import streamlit as st
import pandas as pd

# Link CSV yang sudah Anda dapatkan sebelumnya
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="Monitoring NFM Wetar", layout="wide", page_icon="🚢")

st.title("🚢 Monitoring Part Non-Fast Moving (NFM)")
st.subheader("Site Wetar Logistics Tracker")

@st.cache_data(ttl=60)
def get_data():
    df = pd.read_csv(URL_DATA)
    # Membersihkan spasi di nama kolom agar tidak error
    df.columns = df.columns.str.strip()
    return df

try:
    data = get_data()
    
    # Input Pencarian
    search_query = st.text_input("🔍 Cari Nomor Form Anda (Contoh: 289):")

    if search_query:
        # Filter data berdasarkan kolom 'Nomor Form' sesuai screenshot Excel Anda
        result = data[data['Nomor Form'].astype(str).str.contains(search_query, case=False, na=False)]

        if not result.empty:
            for index, row in result.iterrows():
                with st.expander(f"📌 Detail Form: {row['Nomor Form']} - {row['Description']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Requestor:** {row.get('Requestor', '-')}")
                        st.write(f"**Item Code:** {row.get('Item Code', '-')}")
                        st.write(f"**Departement:** {row.get('Departement', '-')}")
                    with col2:
                        st.write(f"**Status REQ:** {row.get('STATUS REQ', '-')}")
                        st.write(f"**Status PR:** {row.get('STATUS PR', '-')}")
                        st.info(f"**Waiting Approval:** {row.get('Waiting Approval', '-')}")
                    with col3:
                        st.error(f"⌛ **Aging:** {row.get('Aging', '-')} Days")
                        st.write(f"**Aging Month:** {row.get('Aging Month', '-')}")
                        st.write(f"**Value:** {row.get('Value On site', '-')}")
        else:
            st.warning("Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat status.")

except Exception as e:
    st.error(f"Aplikasi gagal membaca data. Pastikan link CSV benar. Error: {e}")
