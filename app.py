import streamlit as st
import pandas as pd

# Link CSV Database
URL_DATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL6oLuQJtXHGXlNYgM_7JgWYzFubZczo-JK9QYHJu8DmY0VzmZAFWIrC_JTDa6X77AkmxbYYd_zX0/pub?output=csv"

st.set_page_config(page_title="NFM Tracking", layout="centered", page_icon="🚢")

st.title("🚢 NFM Tracking Site Wetar")
st.write("---")

@st.cache_data(ttl=10)
def get_data():
    # Mengambil data dan membersihkan nama kolom
    df = pd.read_csv(URL_DATA)
    df.columns = df.columns.str.strip()
    
    # Fungsi pembersihan angka (Value)
    def clean_currency(value):
        if pd.isna(value): return 0.0
        val_str = str(value).replace('Rp', '').replace('.', '').replace(',', '.').strip()
        try:
            return float(val_str)
        except:
            return 0.0

    # Bersihkan kolom-kolom Value jika ada
    for col in df.columns:
        if 'Value' in col or 'VALUE' in col:
            df[col] = df[col].apply(clean_currency)
            
    return df

try:
    data = get_data()
    search_query = st.text_input("🔍 Masukkan Nomor Form:").strip()

    if search_query:
        # Filter data berdasarkan Nomor Form
        result = data[data['Nomor Form'].astype(str).str.contains(rf"^{search_query}(/|$)", na=False)]

        if not result.empty:
            first_row = result.iloc[0]
            
            # Hitung Total Value dan Outstanding Value
            total_val = result.get('Value On site', pd.Series([0])).sum()
            # Pastikan nama kolom 'Outstanding On Site Value' sesuai di Excel Anda
            out_val = result.get('Outstanding On Site Value', pd.Series([0])).sum()
            
            stock_list = result['Item Code'].astype(str).unique()
            
            st.success("✅ Data Ditemukan")
            
            with st.container(border=True):
                # Baris 1: Nomor Form
                st.subheader(f"📄 {first_row['Nomor Form']}")
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**🏢 Dept:** {first_row.get('Departement', '-')}")
                    st.write(f"**👤 Requestor:** {first_row.get('Requestor', '-')}")
                    with st.expander(f"📦 Lihat {len(stock_list)} Stock Codes"):
                        for code in stock_list:
                            st.write(f"- `{code}`")
                
                with col2:
                    # Pencarian fleksibel untuk kolom Nomor PR
                    pr_col = [c for c in data.columns if 'Nomor PR' in c or 'NO. PR' in c]
                    pr_display = first_row.get(pr_col[0], '-') if pr_col else '-'
                    
                    st.write(f"**📑 NOMOR PR:** {pr_display}")
                    st.write(f"**✅ Status PR:** {first_row.get('STATUS PR', '-')}")
                    st.write(f"**💰 Total Value:** Rp {total_val:,.2f}")

                st.divider()
                
                # TAMPILAN BARU: OUTSTANDING VALUE
                st.warning(f"**⚠️ Outstanding On Site Value: Rp {out_val:,.2f}**")
                st.info(f"**📑 STATUS REQ:** {first_row.get('STATUS REQ', '-')}")
                
                with st.expander("📝 Rincian Nama Barang"):
                    for _, row in result.iterrows():
                        st.write(f"• {row['Description']} (Code: {row['Item Code']})")
        else:
            st.error("❌ Nomor Form tidak ditemukan.")
    else:
        st.info("💡 Masukkan Nomor Form untuk melihat ringkasan.")

except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
    st.error(f"Format data berubah atau koneksi error. Error: {e}")
