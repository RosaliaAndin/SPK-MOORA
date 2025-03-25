import streamlit as st
import numpy as np
import pandas as pd
import json
import os

USER_DATA_FILE = "user.json"

# Fungsi untuk memuat pengguna dari file JSON
def load_user():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Fungsi untuk menyimpan pengguna ke file JSON
def save_user(user):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user, f)

def register():
    st.title("Register")
    new_username = st.text_input("Buat Username")
    new_password = st.text_input("Buat Password", type="password")
   
    if st.button("Daftar"):
        if new_username and new_password:
            users = load_user()
            if new_username in users:
                st.error("Username sudah digunakan, pilih yang lain.")
            else:
                users[new_username] = new_password
                save_user(users)
                st.success("Pendaftaran berhasil! Silakan login.")
                st.session_state["registered"] = True
                st.session_state["redirect_to_login"] = True
                st.rerun()
        else:
            st.error("Harap isi username dan password.")

def login():
    st.title("Login")
    users = load_user()
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Username atau password salah")

def calculate_moora(matrix, weights, types, alternatives):
    if not len(matrix):
        st.error("Masukkan data terlebih dahulu.")
        return None
    #Konversi ke array numpy
    matrix = np.array(matrix, dtype=float)
    #Normalisasi matriks keputusan
    norm_matrix = matrix/np.sqrt((matrix**2).sum(axis=0))
    #HItung matriks terbobot
    weighted_matrix = norm_matrix * weights
    #Hitung skor MOORA
    moora_scores = (weighted_matrix*types).sum(axis=1)
    #Buat DataFrame hasil
    results=pd.DataFrame({
        "Alternatif":alternatives,
        "Skor MOORA": moora_scores
    })
    #Urutkan berdasarkan skor MOORA tertinggi 
    results=results.sort_values(by="Skor MOORA", ascending=False).reset_index(drop=True)
    return results


def halaman_menu():
    menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Daftar Konversi Kriteria", "Daftar Kriteria", "Daftar Alternatif", "Perhitungan MOORA", "Laporan", "Tentang"])
    
    if menu == "Home":
        st.header("Selamat Datang di Sistem Pendukung Keputusan Pemilihan Lokasi Peternakan Ayam di Kabupaten Semarang Menggunakan Metode MOORA")

    elif menu == "Daftar Konversi Kriteria":
        st.subheader("Daftar Konversi Kriteria")
        data = {
            "No": [1, 2, 3],
            "Jarak Dari Pemukiman": ["> 1.000 m", "500 m – 1.000 m", "< 500 m"],
            "Bobot": [3, 2, 1],
            "Keterangan": ["Sangat Sesuai", "Sesuai", "Tidak Sesuai"]
        }

        data1 = {
            "No": [1, 2, 3, 4],
            "Luas Lahan": ["> 400 m²", "250 m² – 400 m²", "100 m² – 250 m²", "< 100 m²"], 
            "Jumlah Ayam": ["6.000 ekor", "3.750 ekor – 6.000 ekor", "1.500 ekor – 3.750 ekor", "1.500 ekor"],
            "Bobot": [4, 3, 2, 1],
            "Keterangan": ["Sangat Banyak", "Banyak", "Sedikit", "Sangat Sedikit"]
        }

        data2 = {
            "No": [1, 2, 3, 4],
            "Jarak Sumber Air": ["0 m - 50 m", "51 m - 100 m", "101 m - 200 m", "<200 m"], 
            "Bobot": [4, 3, 2, 1],
            "Keterangan": ["Sangat Dekat", "Dekat", "Jauh", "Sangat Jauh"]
        }

        data3 = {
            "No": [1, 2, 3, 4],
            "Jarak Sumber Listrik": ["0 m - 50 m", "51 m - 100 m", "101 m - 200 m", "<200 m"], 
            "Bobot": [4, 3, 2, 1],
            "Keterangan": ["Sangat Dekat", "Dekat", "Jauh", "Sangat Jauh"]
        }

        data4 = {
            "No": [1, 2, 3, 4],
            "Jneis Permukaan Akses Jalan": ["Jalan Sudah Bersapal", "Jalan Menggunakan Beton", "Jalan Makadam", "Jalan Masih Berupa Tanah Lempung"], 
            "Bobot": [4, 3, 2, 1],
            "Keterangan": ["Sangat Baik", "Baik", "Tidak Baik", "Sangat Tidak Baik"]
        }

        data5 = {
            "No": [1, 2, 3],
            "Lebar Jalan": [">6 m", "3 m - 6 m", "<3 m"], 
            "Bobot": [3, 2, 1],
            "Keterangan": ["Sangat Disarankan", "Disarankan", "Tidak Disarankan"]
        }

        data6 = {
            "No": [1, 2],
            "Kepemilikan Lahan": ["Lahan Sendiri", "Menyewa Lahan"], 
            "Bobot": [2, 1],
            "Keterangan": ["Lebih Baik", "Kurang Baik"]
        }

        data7 = {
            "No": [1, 2, 3],
            "Jarak Lokasi Dengan Jalan Utama": [">500 m", "100 m - 500 m", "<100 m"], 
            "Bobot": [3, 2, 1],
            "Keterangan": ["Sangat Sesuai", "Sesuai", "Tidak Sesuai"]
        }

        data8 = {
            "No": [1, 2, 3],
            "Jarak Lokasi Dengan Peternakan Lain": [">1.000 m", "100 m - 1.000 m", "<100 m"], 
            "Bobot": [3, 2, 1],
            "Keterangan": ["Sangat Sesuai", "Sesuai", "Tidak Sesuai"]
        }

        #Konversi kedalam DataFrame
        df = pd.DataFrame(data)
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        df3 = pd.DataFrame(data3)
        df4 = pd.DataFrame(data4)
        df5 = pd.DataFrame(data5)
        df6 = pd.DataFrame(data6)
        df7 = pd.DataFrame(data7)
        df8 = pd.DataFrame(data8)

        #Tampilan Tabel
        st.subheader("Tabel Jarak dari Pemukiman")
        st.table(df)
        st.subheader("Tabel Luas Lahan")
        st.table(df1)
        st.subheader("Tabel Jarak Sumber Air")
        st.table(df2)
        st.subheader("Tabel Jarak Sumber Listrik")
        st.table(df3)
        st.subheader("Tabel Jenis Permukaan Akses Jalan")
        st.table(df4)
        st.subheader("Tabel Lebar Jalan")
        st.table(df5)
        st.subheader("Tabel Kepemilikan Lahan")
        st.table(df6)
        st.subheader("Tabel Jarak Lokasi Dengan Jalan Utama")
        st.table(df7)
        st.subheader("Tabel Jarak Lokasi Dengan Peternakan Lain")
        st.table(df8)


    elif menu == "Daftar Kriteria":
        st.subheader ("Daftar Kriteria")
        data9 = {
            'Kriteria': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], 
            'Keterangan': ['Jarak Dari Pemukiman', 'Luas Lahan', 'Jarak Sumber Air', 'Jarak Sumber Listrik', 'Jenis Permukaan Akses Jalan', 'Lebar Jalan', 'Kepemilikan Lahan', 'Jarak dengan Jalan Utama', 'Jarak dengan Peterakan Lain'],
            'Bobot': ['0.18', '0.12', '0.10', '0.08', '0.15', '0.10', '0.12', '0.07', '0.08'],
            'Jenis': ['Benefit', 'Benefit', 'Cost', 'Cost', 'Benefit', 'Benefit', 'Cost', 'Benefit', 'Benefit']
        }
        df9 = pd.DataFrame(data9)
        st.table(df9)

    elif menu == "Daftar Alternatif":
        st.subheader ("Input Data Alternatif")
        #Membuat list untuk menyimpan data input
        if "data" not in st.session_state:
            st.session_state.data=[]

        def konversi_C1(nilai):
            if nilai > 1000:
                return 3
            elif 500 <= nilai <= 1000:
                return 2
            else:
                return 1
        
        def konversi_C2(nilai):
            if nilai > 400:
                return 4
            elif 250 <= nilai <= 400:
                return 3
            elif 100 <= nilai < 250:
                return 2
            else:
                return 1
        
        def konversi_C3(nilai):
            if 0 <= nilai <= 50:
                return 4
            elif 51 <= nilai <= 100:
                return 3
            elif 101 <= nilai <= 200:
                return 2
            else:
                return 1
            
        def konversi_C4(nilai):
            if 0 <= nilai <= 50:
                return 4
            elif 51 <= nilai <= 100:
                return 3
            elif 101 <= nilai <= 200:
                return 2
            else:
                return 1
            
        def konversi_C5(nilai):
            if nilai == "Aspal":
                return 4
            elif nilai == "Beton":
                return 3
            elif nilai == "Makadam":
                return 2
            elif nilai == "Lempung":
                return 1
            
        def konversi_C6(nilai):
            if nilai > 6:
                return 3
            elif 3 <= nilai <= 6:
                return 2
            else:
                return 1
        
        def konversi_C7(nilai):
            if nilai == "Lahan Sendiri":
                return 2
            elif nilai == "Menyewa Lahan":
                return 1
            
        def konversi_C8(nilai):
            if nilai > 500:
                return 3
            elif 100 <= nilai <= 500:
                return 2
            else:
                return 1
            
        def konversi_C9(nilai):
            if nilai > 1000:
                return 3
            elif 100 <= nilai <= 1000:
                return 2
            else:
                return 1

        #Input untuk setiap kolom
        with st.form("form_input"):
            alternatif = st.text_input("Alternatif (Masukkan Nama Daerah Lokasi Berada)")
            c1 = st.number_input("Jarak Dari Pemukiman (m)", min_value=0)
            c2 = st.number_input("Luas Lahan (m²)", min_value=0)
            c3 = st.number_input("Jarak Sumber Air (m)", min_value=0)
            c4 = st.number_input("Jarak Sumber Listrik (m)", min_value=0)
            c5 = st.selectbox("Jenis Permukaan Akses Jalan", ["Aspal", "Beton", "Makadam", "Lempung"])
            c6 = st.number_input("Lebar Jalan (m)", min_value=0.0, step=0.5)
            c7 = st.selectbox("Kepemilikan Lahan", ["Lahan Sendiri", "Menyewa Lahan"])
            c8 = st.number_input("Jarak Dengan Jalan Utama (jalan kampung) (m)", min_value=0)
            c9 = st.number_input("Jarak Dengan Peternakan Lain (m)", min_value=0)
            
            submit_button = st.form_submit_button("Tambahkan Data")

        #Jika tombol submit ditekan, tambahkan data
        if submit_button:
            if alternatif.strip():
                new_entry = {              
                    "Alternatif": alternatif,
                    "Jarak Dari Pemukiman (m)": c1, "C1 (Bobot)": konversi_C1(c1),
                    "Luas Lahan (m²)": c2, "C2 (Bobot)": konversi_C2(c2),
                    "Jarak Sumber Air (m)": c3, "C3 (Bobot)": konversi_C3(c3),
                    "Jarak Sumber Listrik (m)": c4, "C4 (Bobot)": konversi_C4(c4), 
                    "Jenis Permukaan Akses Jalan": c5, "C5 (Bobot)": konversi_C5(c5),
                    "Lebar Jalan (m)": c6, "C6 (Bobot)": konversi_C6(c6),
                    "Kepemilikan Lahan": c7, "C7 (Bobot)": konversi_C7(c7),
                    "Jarak Dengan Jalan Utama (m)": c8, "C8 (Bobot)": konversi_C8(c8),
                    "Jarak Dengan Peternakan Lain (m)": c9, "C9 (Bobot)": konversi_C9(c9), 
                }
                st.session_state.data.append(new_entry)
                st.success(f"Data {alternatif} berhasil ditambahkan!")
                st.rerun()
            else:
                st.warning("Harap isi semua kolom sebelum menambahkan data.")
        #st.write("Debugging Data Saat ini:", st.session_state.data)

            
            #Jika ada data, tampilkan dalam tabel yang bisa diedit
        if st.session_state.data:
            df = pd.DataFrame(st.session_state.data)
            st.write("### Data yang telah dimasukkan:")
            #Tampilkan data yang bisa diedit langsung
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

            #Tombol untuk memperbaharui data setelah diedit
            if st.button("Simpan Perubahan"):
                st.session_state.data = edited_df.to_dict("records")
                st.success("Perubahan data berhasil disimpan!")

            #Tombol untuk menghapus semua data
            if st.button("Hapus Semua Data"):
                st.session_state.data = []
                st.warning ("Semua data telah dihapus")
                st.rerun()

    elif menu == "Perhitungan MOORA":
        st.header ("Perhitungan MOORA")

        if not st.session_state.data:
            st.warning ("Belum ada data alternatif. Silahkan input data terlebih dahulu di menu Data Alternatif")
        else:
            df = pd.DataFrame(st.session_state.data)[["Alternatif", "C1 (Bobot)", "C2 (Bobot)", "C3 (Bobot)", "C4 (Bobot)", "C5 (Bobot)", "C6 (Bobot)", "C7 (Bobot)", "C8 (Bobot)", "C9 (Bobot)"]]

            st.write ("### Data Alternatif yang telah dikonversi")
            st.dataframe(df)

            #Bobot dan jenis kriteria sudah ditentukan
            weights = np.array([0.18, 0.12, 0.10, 0.08, 0.15, 0.10, 0.12, 0.07, 0.08])
            types = np.array([1, 1, -1, -1, 1, 1, -1, 1, 1]) #Benefit = 1, Cost = -1

            if st.button("Hitung MOORA"):
                matrix = df.iloc[:, 1:].values.tolist()
                alternatives = df["Alternatif"].tolist()
                results= calculate_moora(matrix, weights, types, alternatives)
                if results is not None:
                    st.write("### Hasil Perhitungan MOORA:")
                    st.dataframe(results)

                    best_alternative = results.iloc[0]["Alternatif"]
                    best_score = results.iloc[0]["Skor MOORA"]

                    st.success(f"Alternatif terbaik adalah **{best_alternative}** dengan skor tertinggi yaitu **{best_score}**")

                    #Simpan hasil ke session_state
                    st.session_state["moora_results"] = results
                    st.session_state["best_alternative"] = best_alternative
                    st.session_state["best_score"] = best_score
       
    elif menu == "Laporan":
        st.header("Hasil Laporan Perhitungan Alternatif Terbaik Menggunakan MOORA")
        
        if "moora_results" in st.session_state:
            st.dataframe(st.session_state["moora_results"])
            
            # Ambil data terbaik dari session_state
            best_alternative = st.session_state["best_alternative"]
            best_score = st.session_state["best_score"]
            
            st.success(f"Berdasarkan analisis yang dilakukan, alternatif terbaik yang diperoleh adalah **{best_alternative}** dengan skor tertinggi yaitu **{best_score}**. Hasil ini menunjukkan bahwa **{best_alternative}** memenuhi beberapa kriteria penting untuk pembangunan peternakan ayam. Dengan analisis berbasis skor ini, keputusan yang diambil lebih objektif dan terukur. Langkah selanjutnya adalah melakukan survei lapangan serta memastikan aspek regulasi dan perizinan agar pembangunan peternakan dapat berjalan lancar sesuai aturan yang berlaku.")
        else:
            st.warning("Belum ada perhitungan yang dilakukan. Silakan hitung MOORA terlebih dahulu.")

    elif menu == "Tentang":
        st.header("Tentang Aplikasi")
        st.write("Aplikasi Sistem Pendukung Keputusan (SPK) adalah aplikasi berbasis komputer yang dirancang untuk membantu proses pengambilan keputusan, terutama dalam situasi yang kompleks atau tidak terstruktur."
        " Sistem Pendukung Keputusan berfungsi sebagai alat bantu yang menyediakan data, analisis, atau rekomendasi untuk mendukung pengambilkan keputusan dalam memilih solusi terbaik. "
        " Aplikasi yang saya buat ini merupakan aplikasi yang yang dibuat untuk para peternak ayam pemula yang ingin mendirikan peternakan ayam, namun bingung dalam menentukan lokasi yang cocok untuk di dirikannya peternakan tersebut."
        " Dengan adanya permasalahan tersebut, saya membuat aplikasi ini untuk menyelesaikan dan memberikan solusi terkait kebingungan yang dialami."
        " Sistem ini menggunakan metode MOORA yang digunakan untuk melakukan analisis multi-kriteria dalam menentukan lokasi yang paling optimal berdasarkan beberapa parameter yang telah saya tentukan."
        " Metode Multi-Objective Optimization on the Basis of Ratio Analysis) bekerja dengan cara membandingkan setiap alternatif berdasarkan kriteria yang relevan dengan pemilihan lokasi peternakan ayam."
        " Hasil dari analisis tersebut akan memberikan peringkat dari setiap alternatif lokasi, sehingga para peternak ayam pemula dapat mengambil keputusan dengan lebih mudah dan didasarkan pada data yang akurat."
        " Dengan aplikasi ini, diharapkan para peternak dapat mengoptimalkan peluang keberhasilan dalam mendirikan peternakan ayam yang produktif dan efisien.")


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if "registered" not in st.session_state:
        st.session_state["registered"] = False
    
    if not st.session_state["registered"]:
        register()
        return
    
    if "redirect_to_login" in st.session_state and st.session_state["redirect_to_login"]:
        del st.session_state["redirect_to_login"]
        login()
        return
    
    if not st.session_state["logged_in"]:
        login()
        return
    
    halaman_menu()
if __name__ == "__main__":
    main()
