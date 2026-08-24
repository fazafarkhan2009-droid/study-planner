import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Study Planner & AI Friend", page_icon="📚", layout="centered")

# CSS Kustom Ringan (Red-Black Abstract Theme tanpa Blur)
st.markdown("""
    <style>
    /* Background Abstrak Merah-Hitam Ringan (Super Fast Rendering) */
    .stApp {
        background-color: #0a0002;
        background-image: 
            linear-gradient(135deg, rgba(128, 0, 16, 0.25) 0%, transparent 60%),
            radial-gradient(circle at 90% 10%, rgba(179, 0, 27, 0.2) 0%, transparent 40%),
            radial-gradient(circle at 10% 90%, rgba(90, 0, 10, 0.3) 0%, transparent 50%);
        background-attachment: fixed;
        color: #f5e6e8;
    }

    /* Container Card Ringan Tanpa Blur */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #120104;
        border: 1px solid #5e000d;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    /* Judul Merah menyala */
    h1, h2, h3 {
        color: #ff2a40 !important;
        font-weight: bold;
    }

    /* Tombol Utama */
    .stButton>button {
        background: #80000e;
        color: #ffffff;
        border-radius: 6px;
        border: 1px solid #ff1a35;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background: #b30014;
        border-color: #ffffff;
    }

    /* Form Input */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #1c0207 !important;
        color: #ffffff !important;
        border: 1px solid #66000e !important;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Utama
st.title("📚 Study Planner & Teman AI")
st.write("Kelola tugas sekolahmu dan berdiskusi dengan Teman AI dalam satu halaman interaktif.")

# Inisialisasi State
if "daftar_tugas" not in st.session_state:
    st.session_state.daftar_tugas = []

st.divider()

# --- WIDGET 1: INPUT TUGAS BARU ---
st.header("➕ Tambah Tugas Baru")
matpel = st.text_input("Mata Pelajaran")
nama_tugas = st.text_input("Deskripsi Tugas")
deadline = st.text_input("Deadline (cth: Besok/Senin)")
prioritas = st.selectbox("Prioritas", ["Tinggi", "Sedang", "Rendah"])

if st.button("Simpan Tugas"):
    if matpel and nama_tugas:
        st.session_state.daftar_tugas.append({
            "matpel": matpel,
            "tugas": nama_tugas,
            "deadline": deadline,
            "prioritas": prioritas,
            "selesai": False
        })
        st.success(f"Tugas '{nama_tugas}' berhasil ditambahkan!")
        st.rerun()
    else:
        st.error("Mata Pelajaran dan Deskripsi Tugas wajib diisi!")

st.divider()

# --- WIDGET 2: PROGRESS & DAFTAR TUGAS ---
st.header("📋 Progress & Daftar Tugas")

total_tugas = len(st.session_state.daftar_tugas)
tugas_selesai = sum(1 for t in st.session_state.daftar_tugas if t["selesai"])

if total_tugas > 0:
    persen = tugas_selesai / total_tugas
    st.progress(persen)
    st.caption(f"📊 **Progress Belajar:** {tugas_selesai} dari {total_tugas} tugas selesai ({int(persen*100)}%)")
else:
    st.info("Belum ada tugas tersimpan.")

if st.session_state.daftar_tugas:
    skor = {"Tinggi": 1, "Sedang": 2, "Rendah": 3}
    tugas_terurut = sorted(st.session_state.daftar_tugas, key=lambda x: skor[x["prioritas"]])

    for i, item in enumerate(tugas_terurut):
        c1, c2 = st.columns([3, 1])
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

# --- WIDGET 3: TEMAN AI (ASISTEN BELAJAR) ---
st.header("🤖 Teman AI (Asisten Belajar)")
st.write("Tanyakan ide, rumus, atau bantuan pengerjaan tugas di sini:")

topik = st.text_input("Topik/Materi Tugas", placeholder="cth: Rumus Fisika, Ide Cerpen, dll.")
pertanyaan = st.text_area("Pertanyaan kamu:", placeholder="Tulis soal atau bantuan yang kamu butuhkan...", height=100)

if st.button("Tanyakan ke Teman AI"):
    if pertanyaan:
        st.markdown("**🤖 Teman AI Menjawab:**")
        st.success(f"Dua panduan utama untuk membantu tugas **{topik if topik else 'kamu'}**:\n\n"
                   f"1. **Analisis Masalah:** Pecah soal/tugas ini menjadi 2-3 langkah kecil agar lebih mudah dikerjakan.\n"
                   f"2. **Langkah Awal:** Fokus selesaikan bagian termudah terlebih dahulu untuk membangun momentum belajar!")
    else:
        st.warning("Ketik pertanyaanmu terlebih dahulu!")
        
