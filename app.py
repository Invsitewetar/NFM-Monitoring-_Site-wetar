function sendEmailOnStatusChange(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;
  var editedColumn = range.getColumn();
  
  // --- KONFIGURASI KOLOM (Hitung dari A=1, B=2, dst) ---
  var kolomNomorForm = 1;   // Kolom A (Nomor NFM)
  var kolomItemCode = 2;    // Kolom B (Item Code)
  var kolomDescription = 3; // Kolom C (Description)
  var kolomX_NomorPR = 24;  // Kolom X (Nomor PR)
  var kolomAB_StatusPR = 28; // Kolom AB (Status PR)
  
  var emailAnda = "patricia.mauleky@merdekacoppergold.com";

  // Pastikan memantau kolom AB (28) atau W (23)
  if (editedColumn == kolomAB_StatusPR || editedColumn == 23) {
    var row = range.getRow();
    var statusBaru = range.getValue().toString().toUpperCase();
    
    // AMBIL DATA - Gunakan .getDisplayValue() agar formatnya sesuai dengan yang terlihat di Excel
    var nomorNFM = sheet.getRange(row, kolomNomorForm).getDisplayValue(); 
    var nomorPR = sheet.getRange(row, kolomX_NomorPR).getDisplayValue();
    var itemCode = sheet.getRange(row, kolomItemCode).getDisplayValue();
    var deskripsi = sheet.getRange(row, kolomDescription).getDisplayValue();
    
    var pesanKustom = "";
    
    // --- LOGIKA KALIMAT DENGAN NOMOR NFM ---
    if (statusBaru.includes("PR")) {
      pesanKustom = "Status <b>NFM " + nomorNFM + "</b> sudah di <b>full approval</b> dan cover <b>Nomor PR: " + nomorPR + "</b>.";
    } 
    else if (statusBaru.includes("ON SITE") || statusBaru.includes("ONSITE")) {
      pesanKustom = "Status <b>NFM " + nomorNFM + "</b> sudah berubah menjadi <b>Onsite</b>, silakan diambil barangnya ke warehouse.";
    } 
    else if (statusBaru.includes("ON ORDER")) {
      pesanKustom = "Status <b>NFM " + nomorNFM + "</b> sementara diproses oleh team Expeditor.";
    } 
    else {
      pesanKustom = "Status <b>NFM " + nomorNFM + "</b> telah diperbarui menjadi: <b>" + statusBaru + "</b>.";
    }

    if (statusBaru !== "" && nomorNFM !== "") {
      var subjek = "UPDATE NFM: " + nomorNFM + " [" + statusBaru + "]";
      
      var pesanHTML = "<div style='font-family: sans-serif; padding: 25px; border: 1px solid #e0e0e0; border-radius: 12px; max-width: 600px; background-color: #ffffff;'>" +
                  "<h3 style='color: #1a73e8; margin-top: 0;'>🚢 NFM Tracking Site Wetar</h3>" +
                  "<p style='font-size: 16px; color: #333; line-height: 1.6;'>" + pesanKustom + "</p>" +
                  
                  // TABEL RINCIAN BARANG
                  "<div style='margin-top: 20px; border: 1px solid #eee; border-radius: 8px; overflow: hidden;'>" +
                  "<table style='width: 100%; border-collapse: collapse; font-size: 14px;'>" +
                  "<tr style='background-color: #f8f9fa;'><th style='padding: 10px; border-bottom: 1px solid #eee; text-align: left;'>Item Code</th><th style='padding: 10px; border-bottom: 1px solid #eee; text-align: left;'>Description</th></tr>" +
                  "<tr><td style='padding: 10px; border-bottom: 1px solid #eee;'>" + itemCode + "</td><td style='padding: 10px; border-bottom: 1px solid #eee;'>" + deskripsi + "</td></tr>" +
                  "</table></div>" +

                  "<p style='margin-top: 20px; font-size: 13px; color: #555;'>Cek rincian lainnya di website tracking NFM.</p>" +
                  "<hr style='border: 0; border-top: 1px solid #eee; margin: 25px 0;'>" +
                  "<p style='font-size: 11px; color: #9aa0a6; text-align: center;'>Notifikasi otomatis Site Wetar - Merdeka Copper Gold.</p>" +
                  "</div>";
      
      MailApp.sendEmail({
        to: emailAnda,
        subject: subjek,
        htmlBody: pesanHTML
      });
      
      SpreadsheetApp.getActiveSpreadsheet().toast("Email NFM " + nomorNFM + " sukses terkirim!");
    }
  }
}
    # --- Tabel Detail ---
    st.subheader("📋 Daftar Rincian Barang")
    st.dataframe(df_f, use_container_width=True)

else:
    st.error("⚠️ Data tidak terbaca. Pastikan link Google Sheets benar.")
