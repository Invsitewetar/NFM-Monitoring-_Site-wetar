import streamlit as st
import pandas as pd

# Link CSV Database
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

# Membuat tampilan terpusat dan rapi
st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

# CSS rahasia agar kotak informasi tidak meluber di layar laptop
st.markdown("""
    <style>
    .block-container { max-width: 800px; padding-top: 2rem; }
    .stAlert { padding: 10px; }
    div[data-testid="stMetricValue"] { font-size: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

@st.cache_data(ttl=0)
def get_data():
    df = pd.read_csv(URL_DATA)
    df.columns = [str(c).strip() for c in df.columns]
    
    def clean_num(val):
        if pd.isna(val) or val == '-': return 0.0
        s = str(val).replace('Rp', '').replace('.', '').replace(',', '.').replace(' ', '').strip()
        try: return float(s)
        except: return 0.0

    if 'Value On site' in df.columns:
        df['Value On site'] = df['Value On site'].apply(clean_num)
    if 'Outstanding On Site Value' in df.columns:
        df['Outstanding On Site Value'] = df['Outstanding On Site Value'].apply(clean_num)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Cari berdasarkan Nomor Form
        res = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not res.empty:
            row = res.iloc[0]
            item_codes = res['Item Code'].astype(str).unique()
            st.success("✅ Data Ditemukan")
            
            with st.container(border=True):
                st.subheader(f"📄 {row['Nomor Form']}")
                st.divider()
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.write(f"**🏢 Dept:** \n{row.get('Departement', '-')}")
                    st.write(f"**👤 Requestor:** \n{row.get('Requestor', '-')}")
                    st.write("**📦 Item Codes:**")
                    for code in item_codes:
                        st.caption(f"`{code}`")
                
                with c2:
                    pr_val = row.get('NOMOR PR', row.get('Nomor PR', '-'))
                    st.write(f"**📑 Nomor PR:** {pr_val}")
                    st.write(f"**✅ Status PR:** {row.get('STATUS PR', '-')}")
                    
                    out_amt = res['Outstanding On Site Value'].sum() if 'Outstanding On Site Value' in res.columns else 0
                    st.warning(f"**💰 Outstanding:** \nRp {out_amt:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {row.get('STATUS REQ', '-')}")
                
                with st.expander("📝 Lihat Detail Deskripsi Barang"):
                    for _, item in res.iterrows():
                        st.write(f"• {item['Description']}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")

except Exception as e:
    st.error(f"Terjadi kesalahan data. Error: {e}")

except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
    st.error(f"Gagal memuat data. Error: {e}")
