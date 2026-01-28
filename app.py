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
    # Pembersihan data harga agar bisa dijumlahkan
    if 'Value On site' in df.columns:
        df['Value On site'] = pd.to_numeric(df['Value On site'].astype(str).str.replace('Rp', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Mencari semua item berdasarkan nomor form
        result = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            first_row = result.iloc[0]
            total_value = result['Value On site'].sum()
            # Mengambil daftar Stock Code unik
            stock_list = result['Item Code'].astype(str).unique()
            
            st.success(f"✅ Data Ditemukan")
            
            with st.container(border=True):
                # 1. JUDUL: Nomor NFM Lengkap
                st.subheader(f"📄 {first_row['Nomor Form']}")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    # Request: Dept di paling atas baru Requestor
                    st.write(f"**🏢 Dept:** {first_row.get('Departement', '-')}")
                    st.write(f"**👤 Requestor:** {first_row.get('Requestor', '-')}")
                    
                    # Rincian Stock Codes (Dibuat dalam expander agar tidak menumpuk)
                    with st.expander(f"📦 Lihat Rincian {len(stock_list)} Stock Codes"):
                        for code in stock_list:
                            st.write(f"- `{code}`")
                
                with col2:
                    # Tampilan Nomor PR
                    pr_no = first_row.get('Nomor PR', '-') 
                    st.write(f"**📑 Nomor PR:** {pr_no}")
                    st.write(f"**✅ Status PR:** {first_row.get('STATUS PR', '-')}")
                    
                    # Total Value Keseluruhan
                    st.write(f"**💰 Total Value:** Rp {total_value:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {first_row.get('STATUS REQ', '-')}")
                
                # Menampilkan rincian Description per item di bawah
                with st.expander("📝 Rincian Nama Barang"):
                    for i, row in result.iterrows():
                        st.write(f"• {row['Description']} (Code: {row['Item Code']})")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat ringkasan.")

except Exception as e:
    st.error(f"Format data berubah atau koneksi error. Periksa nama kolom di Excel. Error: {e}")
