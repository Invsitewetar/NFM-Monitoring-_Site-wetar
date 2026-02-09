import streamlit as st
import pandas as pd

# Link CSV Database
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

# Fungsi ambil data dengan pembersihan ekstra
@st.cache_data(ttl=10) # Cache dipercepat jadi 10 detik saja supaya cepat update
def get_data():
    df = pd.read_csv(URL_DATA)
    # Hapus spasi di awal/akhir nama kolom DAN ubah ke huruf besar semua agar sinkron
    df.columns = df.columns.str.strip().str.upper()
    
    # Bersihkan Value agar bisa dijumlah
    value_col = [c for c in df.columns if 'VALUE' in c]
    if value_col:
        df[value_col[0]] = pd.to_numeric(df[value_col[0]].astype(str).str.replace('Rp', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Cari kolom Nomor Form (huruf besar)
        form_col = [c for c in data.columns if 'NOMOR FORM' in c][0]
        result = data[data[form_col].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            first_row = result.iloc[0]
            
            # Cari kolom Value (huruf besar)
            v_col = [c for c in data.columns if 'VALUE' in c]
            total_value = result[v_col[0]].sum() if v_col else 0
            
            stock_list = result[[c for c in data.columns if 'ITEM CODE' in c][0]].astype(str).unique()
            
            st.success("✅ Data Ditemukan")
            
            with st.container(border=True):
                st.subheader(f"📄 {first_row[form_col]}")
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**🏢 Dept:** {first_row.get('DEPARTEMENT', first_row.get('DEPT', '-'))}")
                    st.write(f"**👤 Requestor:** {first_row.get('REQUESTOR', '-')}")
                    
                    with st.expander(f"📦 Lihat Rincian {len(stock_list)} Stock Codes"):
                        for code in stock_list:
                            st.write(f"- `{code}`")
                
                with col2:
                    # --- CARI NOMOR PR SECARA OTOMATIS (Tanpa Peduli Huruf Besar/Kecil) ---
                    pr_candidates = [c for c in data.columns if 'NOMOR PR' in c or 'NO. PR' in c]
                    pr_no = first_row.get(pr_candidates[0], '-') if pr_candidates else '-'
                    
                    st.write(f"**📑 Nomor PR:** {pr_no}")
                    st.write(f"**✅ Status PR:** {first_row.get('STATUS PR', '-')}")
                    st.write(f"**💰 Total Value:** Rp {total_value:,.2f}")

                st.divider()
                st.info(f"**📑 STATUS REQ:** {first_row.get('STATUS REQ', '-')}")
                
                with st.expander("📝 Rincian Nama Barang"):
                    desc_col = [c for c in data.columns if 'DESCRIPTION' in c][0]
                    for _, row in result.iterrows():
                        st.write(f"• {row[desc_col]}")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat ringkasan.")

except Exception as e:
    st.error(f"Terjadi kendala pembacaan data: {e}")
