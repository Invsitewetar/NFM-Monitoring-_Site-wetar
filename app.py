import streamlit as st
import pandas as pd

# Link CSV Database Anda
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")
st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

# Paksa update data (ttl=0)
@st.cache_data(ttl=0)
def get_data():
    df = pd.read_csv(URL_DATA)
    # Bersihkan nama kolom: Hapus spasi dan ubah ke huruf BESAR
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Fungsi membersihkan angka agar bisa dijumlah
    def to_num(val):
        if pd.isna(val): return 0.0
        s = str(val).replace('Rp', '').replace('.', '').replace(',', '.').replace(' ', '').strip()
        try: return float(s)
        except: return 0.0

    # Otomatis bersihkan kolom bernilai uang
    for col in df.columns:
        if 'VALUE' in col:
            df[col] = df[col].apply(to_num)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Cari data berdasarkan Nomor Form
        res = data[data['NOMOR FORM'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not res.empty:
            row = res.iloc[0]
            st.success("✅ Data Ditemukan")
            
            with st.container(border=True):
                st.subheader(f"📄 {row['NOMOR FORM']}")
                st.divider()
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**🏢 Dept:** {row.get('DEPARTEMENT', row.get('DEPT', '-'))}")
                    st.write(f"**👤 Requestor:** {row.get('REQUESTOR', '-')}")
                
                with c2:
                    # Mencari kolom PR secara cerdas (mencari kata 'PR' yang bukan 'STATUS')
                    pr_cols = [c for c in data.columns if 'PR' in c and 'STATUS' not in c]
                    pr_val = row.get(pr_cols[0], '-') if pr_cols else '-'
                    
                    st.write(f"**📑 Nomor PR:** {pr_val}")
                    st.write(f"**✅ Status PR:** {row.get('STATUS PR', '-')}")
                    
                    # Outstanding Value
                    out_cols = [c for c in data.columns if 'OUTSTANDING' in c]
                    out_amt = res[out_cols[0]].sum() if out_cols else 0
                    st.write(f"**💰 Outstanding:** Rp {out_amt:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {row.get('STATUS REQ', '-')}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")

except Exception as e:
    st.error(f"Koneksi terkunci atau data tidak terbaca. Pastikan Google Sheets sudah 'Anyone with the link'. Error: {e}")
