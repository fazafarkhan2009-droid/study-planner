import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Study Planner & AI Friend", page_icon="📚", layout="centered")

# CSS Kustom: Latar Belakang Desain Lukisan Abstrak Merah-Hitam & Layout Kolom Tunggal
st.markdown("""
    <style>
    /* Latar Belakang Lukisan Abstrak Merah & Hitam */
    .stApp {
        background-color: #0d0003;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(179, 0, 0, 0.45) 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, rgba(128, 0, 32, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(255, 26, 26, 0.15) 0%, transparent 60%),
            linear-gradient(135deg, #050001 0%, #1a0003 50%, #000000 100%);
        background-attachment: fixed;
        color: #fce8e8;
    }

    /* Container Card Transparan Bergaya Abstrak */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(15, 2, 4, 0.65);
        border: 1px solid rgba(230, 0, 38, 0.3);
        border-radius: 12px;
        padding: 10px;
        backdrop-filter: blur(8px);
    }

    /* Teks & Judul */
    h1, h2, h3 {
        color: #ff3344 !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9), 0 0 12px rgba(255, 0, 51, 0.4);
    }

    /* Tombol Utama */
    .stButton>button {
        background: linear-gradient(135deg, #990012 0%, #4a0008 100%);
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ff1a35;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #e6001a 0%, #80000a 100%);
        box-shadow: 0 0 10px rgba(255, 26, 53, 0.6);
        border-color: #ffffff;
    }

    /* Form Input */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(25, 3, 7, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid #800014 !important;
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
