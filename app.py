import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Study Planner", page_icon="📚")

st.title("📚 Study Planner & Manajer Tugas")
st.write("Aplikasi interaktif untuk mencatat dan mengurutkan tugas sekolahmu.")

# Inisialisasi Data Sementara (Session State)
if "daftar_tugas" not in st.session_state:
    st.session_state.daftar_tugas = []

# Sidebar untuk Input
st.sidebar.header("➕ Tambah Tugas Baru")
matpel = st.sidebar.text_input("Mata Pelajaran")
nama_tugas = st.sidebar.text_input("Deskripsi Tugas")
deadline = st.sidebar.text_input("Deadline (cth: Besok/Senin)")
prioritas = st.sidebar.selectbox("Prioritas", ["Tinggi", "Sedang", "Rendah"])

if st.sidebar.button("Tambah Tugas"):
    if matpel and nama_tugas:
        st.session_state.daftar_tugas.append({
            "matpel": matpel,
            "tugas": nama_tugas,
            "deadline": deadline,
            "prioritas": prioritas,
            "selesai": False
        })
        st.sidebar.success(f"Tugas '{nama_tugas}' berhasil ditambahkan!")
    else:
        st.sidebar.error("Mata Pelajaran dan Deskripsi Tugas wajib diisi!")

# Tampilan Utama - Daftar Tugas
st.subheader("📋 Daftar Tugas Kamu")

if not st.session_state.daftar_tugas:
    st.info("Belum ada tugas tersimpan. Gunakan menu di sebelah kiri untuk menambah tugas!")
else:
    # Urutkan berdasarkan prioritas
    skor = {"Tinggi": 1, "Sedang": 2, "Rendah": 3}
    tugas_terurut = sorted(st.session_state.daftar_tugas, key=lambda x: skor[x["prioritas"]])

    for i, item in enumerate(tugas_terurut):
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                status_icon = "✅" if item["selesai"] else "⏳"
                st.markdown(f"### {status_icon} [{item['matpel']}] {item['tugas']}")
                st.write(f"**Deadline:** {item['deadline']} | **Prioritas:** {item['prioritas']}")
            with col2:
                if not item["selesai"]:
                    if st.button("Selesai", key=f"btn_{i}"):
                        item["selesai"] = True
                        st.rerun()
            st.divider()
          
