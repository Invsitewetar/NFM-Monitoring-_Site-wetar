import streamlit as st
import pandas as pd

# Link CSV Database
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

@st.cache_data(ttl=60)
def get_data():
    df = pd.read_csv(URL_DATA)
    df.columns = df.columns.str.strip()
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Mencari semua item yang mengandung nomor form tersebut
        result = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            st.success(f"✅ Ditemukan {len(result)} item untuk Nomor Form: {search_query}")
            
            # Menampilkan SEMUA item satu per satu
            for i, row in result.iterrows():
                with st.container(border=True):
                    st.subheader(f"📝 {row['Description']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**👤 Requestor:** {row.get('Requestor', '-')}")
                        st.write(f"**📦 Item Code:** {row.get('Item Code', '-')}")
                        st.write(f"**🏢 Dept:** {row.get('Departement', '-')}")
                    
                    with col2:
                        st.write(f"**✅ Status PR:** {row.get('Status PR', row.get('STATUS PR', '-'))}")
                        st.write(f"**⏳ Aging:** {row.get('Aging', '-')} Days")
                        st.write(f"**💰 Value:** {row.get('Value On site', row.get('Value', '-'))}")

                    st.divider()
                    st.info(f"**📑 STATUS REQ:** {row.get('Status REQ', row.get('STATUS REQ', '-'))}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat detail semua item.")

except Exception as e:
    st.error(f"Terjadi kesalahan pembacaan data. Pastikan nama kolom di Excel benar. Error: {e}")
