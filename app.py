import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Study Planner & AI Friend", page_icon="📚", layout="wide")

# CSS kustom untuk latar belakang Merah-Hitam & Dark Mode
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0000;
        color: #f1f1f1;
    }
    div[data-testid="stSidebar"] {
        background-color: #1a0000;
        border-right: 2px solid #800000;
    }
    h1, h2, h3 {
        color: #ff3333 !important;
    }
    .stButton>button {
        background-color: #800000;
        color: white;
        border-radius: 8px;
        border: 1px solid #ff3333;
    }
    .stButton>button:hover {
        background-color: #cc0000;
        border-color: #ffffff;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #260000;
        color: white;
        border: 1px solid #800000;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Study Planner & Teman AI")
st.write("Kelola tugas sekolahmu dan berdiskusi dengan Teman AI untuk membantumu belajar!")

# Inisialisasi State
if "daftar_tugas" not in st.session_state:
    st.session_state.daftar_tugas = []

# Sidebar - Tambah Tugas
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

# Layout Utama: 2 Kolom
col_tugas, col_ai = st.columns([3, 2])

# KOLOM 1: MANAJER TUGAS & WIDGET INTERAKTIF
with col_tugas:
    st.subheader("📋 Daftar & Progress Tugas")
    
    # Widget Interaktif: Progress Bar
    total_tugas = len(st.session_state.daftar_tugas)
    tugas_selesai = sum(1 for t in st.session_state.daftar_tugas if t["selesai"])
    
    if total_tugas > 0:
        persen = tugas_selesai / total_tugas
        st.progress(persen)
        st.caption(f"📊 **Progress Belajar:** {tugas_selesai} dari {total_tugas} tugas selesai ({int(persen*100)}%)")
    else:
        st.info("Belum ada tugas tersimpan.")

    st.divider()

    # Menampilkan Daftar Tugas
    if st.session_state.daftar_tugas:
        skor = {"Tinggi": 1, "Sedang": 2, "Rendah": 3}
        tugas_terurut = sorted(st.session_state.daftar_tugas, key=lambda x: skor[x["prioritas"]])

        for i, item in enumerate(tugas_terurut):
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    status_icon = "✅" if item["selesai"] else "⏳"
                    st.markdown(f"**{status_icon} [{item['matpel']}] {item['tugas']}**")
                    st.caption(f"Deadline: {item['deadline']} | Prioritas: {item['prioritas']}")
                with c2:
                    if not item["selesai"]:
                        if st.button("Selesai", key=f"btn_{i}"):
                            item["selesai"] = True
                            st.rerun()
                st.divider()

# KOLOM 2: WIDGET TEMAN AI
with col_ai:
    st.subheader("🤖 Teman AI (Asisten Belajar)")
    st.write("Tanyakan ide, rumus, atau bantuan pengerjaan tugas di sini:")
    
    # Widget Interaktif Input Pertanyaan AI
    topik = st.text_input("Topik/Materi Tugas", placeholder="cth: Rumus Fisika, Ide Cerpen, dll.")
    pertanyaan = st.text_area("Pertanyaan kamu:", placeholder="Tulis soal atau bantuan yang kamu butuhkan...", height=100)
    
    if st.button("Tanyakan ke Teman AI"):
        if pertanyaan:
            st.markdown("---")
            st.markdown("**🤖 Teman AI Menjawab:**")
            st.success(f"Dua poin utama untuk membantu tugas **{topik if topik else 'kamu'}**:\n\n"
                       f"1. **Pendekatan Logis:** Pecah soal ini menjadi beberapa bagian kecil untuk mempermudah analisis.\n"
                       f"2. **Saran Pengerjaan:** Mulai dari konsep dasar terlebih dahulu sebelum masuk ke detail rumitnya!")
        else:
            st.warning("Ketik pertanyaanmu terlebih dahulu!")
            
