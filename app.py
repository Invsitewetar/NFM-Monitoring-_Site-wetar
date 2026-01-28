import streamlit as st
import pandas as pd

# Link CSV Database Anda
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

# Setting Halaman agar tetap rapi di tengah
st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

# KODE UNTUK BACKGROUND HITAM & DESAIN RAPI
st.markdown("""
    <style>
    /* Mengubah background utama menjadi hitam */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Membatasi lebar kotak agar pas di tengah (Centered) */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
    }
    /* Mempercantik kotak container informasi */
    div[data-testid="stContainer"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
    }
    /* Warna teks input agar terlihat di background gelap */
    .stTextInput input {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

@st.cache_data(ttl=0)
def get_data():
    df = pd.read_csv(URL_DATA)
    # Membersihkan nama kolom
    df.columns = [str(c).strip() for c in df.columns]
    
    def clean_num(val):
        if pd.isna(val) or val == '-': return 0.0
        s = str(val).replace('Rp', '').replace('.', '').replace(',', '.').replace(' ', '').strip()
        try: return float(s)
        except: return 0.0

    # Pastikan kolom-kolom nilai uang diproses sebagai angka
    if 'Value On site' in df.columns:
        df['Value On site'] = df['Value On site'].apply(clean_num)
    if 'Outstanding On Site Value' in df.columns:
        df['Outstanding On Site Value'] = df['Outstanding On Site Value'].apply(clean_num)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Cari data berdasarkan Nomor Form
        res = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not res.empty:
            row = res.iloc[0]
            item_codes = res['Item Code'].astype(str).unique()
            st.success("✅ Data Ditemukan")
            
            with st.container():
                st.subheader(f"📄 {row['Nomor Form']}")
                st.divider()
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write(f"**🏢 Dept:** \n{row.get('Departement', '-')}")
                    st.write(f"**👤 Requestor:** \n{row.get('Requestor', '-')}")
                
                with col2:
                    # Menampilkan Nomor PR dari data Excel Anda
                    pr_val = row.get('NOMOR PR', row.get('Nomor PR', '-'))
                    st.write(f"**📑 Nomor PR:** {pr_val}")
                    st.write(f"**✅ Status PR:** {row.get('STATUS PR', '-')}")
                    
                    # Outstanding Value (menjumlahkan total sisa)
                    out_amt = res['Outstanding On Site Value'].sum() if 'Outstanding On Site Value' in res.columns else 0
                    st.warning(f"**💰 Outstanding:** \nRp {out_amt:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {row.get('STATUS REQ', '-')}")
                
                # REQUEST 1: Item Code dibuat dalam Expander seperti Deskripsi
                with st.expander("📦 Lihat Rincian Item Codes"):
                    for code in item_codes:
                        st.write(f"• `{code}`")
                
                # Deskripsi Barang lengkap
                with st.expander("📝 Lihat Detail Deskripsi Barang"):
                    for _, item in res.iterrows():
                        st.write(f"• {item['Description']} (Code: {item['Item Code']})")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")

except Exception as e:
    # Ini bagian yang tadi hilang sehingga menyebabkan error
    st.error(f"Gagal memuat data. Pastikan format Excel Anda benar. Error: {e}")
