import streamlit as st
import pandas as pd

# Link CSV Database Anda
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")
st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

# Cache dimatikan (ttl=0) agar selalu ambil data paling baru dari Excel
@st.cache_data(ttl=0)
def get_data():
    df = pd.read_csv(URL_DATA)
    df.columns = [str(c).strip().upper() for c in df.columns] # Paksa semua judul kolom jadi HURUF BESAR
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Cari data berdasarkan Nomor Form
        result = data[data['NOMOR FORM'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            first_row = result.iloc[0]
            st.success("✅ Data Ditemukan")
            
            with st.container(border=True):
                st.subheader(f"📄 {first_row['NOMOR FORM']}")
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**🏢 Dept:** {first_row.get('DEPARTEMENT', '-')}")
                    st.write(f"**👤 Requestor:** {first_row.get('REQUESTOR', '-')}")
                
                with col2:
                    # KODE SAKTI: Mencari kolom yang mengandung kata 'PR' tapi bukan 'STATUS'
                    pr_cols = [c for c in data.columns if 'PR' in c and 'STATUS' not in c]
                    pr_val = first_row.get(pr_cols[0], '-') if pr_cols else '-'
                    
                    st.write(f"**📑 Nomor PR:** {pr_val}")
                    st.write(f"**✅ Status PR:** {first_row.get('STATUS PR', '-')}")
                    
                    # Ambil Outstanding On Site Value
                    out_cols = [c for c in data.columns if 'OUTSTANDING' in c]
                    out_val = result[out_cols[0]].sum() if out_cols else 0
                    st.write(f"**💰 Outstanding:** Rp {out_val:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {first_row.get('STATUS REQ', '-')}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")

except Exception as e:
    st.error(f"Koneksi terganggu. Silakan refresh halaman. Error: {e}")
