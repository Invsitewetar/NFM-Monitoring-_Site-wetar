import streamlit as st
import pandas as pd

# Link CSV Database
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

# Setting agar konten tetap di tengah dan tidak terlalu lebar di Web
st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

# Custom CSS untuk memperkecil ukuran font dan merapikan tampilan
st.markdown("""
    <style>
    .main { max-width: 800px; margin: 0 auto; }
    .stSubheader { font-size: 1.2rem !important; }
    .stText { font-size: 0.9rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

@st.cache_data(ttl=0)
def get_data():
    df = pd.read_csv(URL_DATA)
    df.columns = [str(c).strip() for c in df.columns]
    
    def clean_num(val):
        if pd.isna(val): return 0.0
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
    # Pencarian yang lebih ramping
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        res = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not res.empty:
            row = res.iloc[0]
            item_codes = res['Item Code'].astype(str).unique()
            
            st.success("✅ Data Ditemukan")
            
            # Wadah utama dengan ukuran yang lebih proporsional
            with st.container(border=True):
                st.subheader(f"📄 {row['Nomor Form']}")
                st.divider()
                
                # Menggunakan perbandingan kolom yang lebih manis (40% : 60%)
                c1, c2 = st.columns([2, 3])
                with c1:
                    st.markdown(f"**🏢 Dept:**\n{row.get('Departement', '-')}")
                    st.markdown(f"**👤 Requestor:**\n{row.get('Requestor', '-')}")
                    st.write("**📦 Item Codes:**")
                    for code in item_codes:
                        st.caption(f"`{code}`")
                
                with c2:
                    pr_val = row.get('NOMOR PR', row.get('Nomor PR', '-'))
                    st.write(f"**📑 Nomor PR:** {pr_val}")
                    st.write(f"**✅ Status PR:** {row.get('STATUS PR', '-')}")
                    
                    out_amt = res['Outstanding On Site Value'].sum() if 'Outstanding On Site Value' in res.columns else 0
                    st.warning(f"**💰 Outstanding:**\nRp {out_amt:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {row.get('STATUS REQ', '-')}")
                
                with st.expander("📝 Detail Deskripsi Barang"):
                    for _, item in res.iterrows():
                        st.write(f"• {item['Description']}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")

except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
