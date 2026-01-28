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
    # Pastikan kolom Value adalah angka
    if 'Value On site' in df.columns:
        df['Value On site'] = pd.to_numeric(df['Value On site'].astype(str).str.replace('Rp', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Mencari semua item yang mengandung nomor form tersebut
        result = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            # --- PROSES DATA UNTUK TAMPILAN KESELURUHAN ---
            first_row = result.iloc[0]
            total_value = result['Value On site'].sum()
            # Gabungkan semua Item Code menjadi satu baris
            all_item_codes = ", ".join(result['Item Code'].astype(str).unique())
            # Gabungkan semua Description untuk judul utama
            main_desc = first_row['Description'] if len(result) == 1 else f"Multiple Items ({len(result)} items)"
            
            st.success(f"✅ Data Ditemukan")
            
            with st.container(border=True):
                # 1. JUDUL: Nomor NFM Lengkap (Warna Hijau di request Anda)
                st.subheader(f"📄 {first_row['Nomor Form']}")
                st.caption(f"**Description Utama:** {main_desc}")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**👤 Requestor:** {first_row.get('Requestor', '-')}")
                    # 2. STOCK CODE: Menampilkan semua Item Code dalam 1 NFM
                    st.write(f"**📦 Stock Codes:** {all_item_codes}")
                    st.write(f"**🏢 Dept:** {first_row.get('Departement', '-')}")
                
                with col2:
                    # 3. NOMOR PR: Ganti Aging jadi Nomor PR (Warna Oranye di request Anda)
                    # Jika kolom 'Nomor PR' tidak ada, akan menampilkan '-'
                    pr_no = first_row.get('Nomor PR', '-') 
                    st.write(f"**📑 Nomor PR:** {pr_no}")
                    
                    st.write(f"**✅ Status PR:** {first_row.get('STATUS PR', '-')}")
                    
                    # 4. TOTAL VALUE: Akumulasi keseluruhan 1 NFM (Warna Biru di request Anda)
                    st.write(f"**💰 Total Value:** Rp {total_value:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {first_row.get('STATUS REQ', '-')}")
                
                # Menampilkan rincian barang di bawah jika item lebih dari satu
                if len(result) > 1:
                    with st.expander("Lihat Rincian Item di Form Ini"):
                        for i, row in result.iterrows():
                            st.write(f"- {row['Description']} ({row['Item Code']})")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat ringkasan NFM.")

except Exception as e:
    st.error(f"Terjadi kesalahan. Pastikan nama kolom 'Nomor PR' sudah ada di Excel jika ingin ditampilkan. Error: {e}")
