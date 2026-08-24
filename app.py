import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Study Planner & AI Friend", page_icon="🏎️", layout="centered")

# Inisialisasi State untuk Tema (Default: Terang / Light Mode)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Terang"

# Sidebar untuk Tombol Toggle Tema (Gaya Medsos)
st.sidebar.title("⚙️ Pengaturan")
pilihan_tema = st.sidebar.radio("Pilih Tema Tampilan:", ["Terang ☀️", "Gelap 🌙"], index=0 if st.session_state.theme_mode == "Terang" else 1)

if "Terang" in pilihan_tema:
    st.session_state.theme_mode = "Terang"
    # CSS Tema Terang (McLaren Orange & Clean White)
    bg_app = "#f8f9fa"
    text_color = "#212529"
    card_bg = "#ffffff"
    card_border = "#dee2e6"
    input_bg = "#ffffff"
    input_text = "#212529"
    input_border = "#ced4da"
else:
    st.session_state.theme_mode = "Gelap"
    # CSS Tema Gelap (McLaren Orange & Carbon Black)
    bg_app = "#0d0d0d"
    text_color = "#f2f2f2"
    card_bg = "#171717"
    card_border = "#ff8000"
    input_bg = "#242424"
    input_text = "#ffffff"
    input_border = "#404040"

# Menerapkan CSS Dinamis Berdasarkan Pilihan Tema
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_app};
        color: {text_color};
    }
    div[data-testid="stVerticalBlock"] > div {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-left: 5px solid #ff8000;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 {{
        color: #ff8000 !important;
        font-weight: bold;
    }}
    p, label, .stMarkdown {{
        color: {text_color} !important;
    }
    .stButton>button {{
        background: linear-gradient(135deg, #ff8000 0%, #e67300 100%);
        color: #ffffff;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {{
        background: linear-gradient(135deg, #ff9933 0%, #ff8000 100%);
        box-shadow: 0 0 10px rgba(255, 128, 0, 0.3);
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {input_border} !important;
        border-radius: 6px;
    }}
    .stProgress > div > div > div > div {{
        background-color: #ff8000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Utama
st.title("🏎️ Study Planner & Teman AI")
st.write("Pantau tugas sekolahmu dengan kecepatan F1 dan diskusikan materi bersama Teman AI!")

# Inisialisasi State Tugas
if "daftar_tugas" not in st.session_state:
    st.session_state.daftar_tugas = []

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

# --- WIDGET 2: PROGRESS & DAFTAR TUGAS ---
st.header("📋 Progress & Daftar Tugas")

total_tugas = len(st.session_state.daftar_tugas)
tugas_selesai = sum(1 for t in st.session_state.daftar_tugas if t["selesai"])

if total_tugas > 0:
    persen = tugas_selesai / total_tugas
    st.progress(persen)
    st.caption(f"📊 **Progress Lap Belajar:** {tugas_selesai} dari {total_tugas} tugas selesai ({int(persen*100)}%)")
else:
    st.info("Belum ada tugas tersimpan.")

if st.session_state.daftar_tugas:
    skor = {"Tinggi": 1, "Sedang": 2, "Rendah": 3}
    tugas_terurut = sorted(st.session_state.daftar_tugas, key=lambda x: skor[x["prioritas"]])

    for i, item in enumerate(tugas_terurut):
        c1, c2 = st.columns([3, 1])
        with c1:
            status_icon = "🏁" if item["selesai"] else "🏎️"
            st.markdown(f"**{status_icon} [{item['matpel']}] {item['tugas']}**")
            st.caption(f"Deadline: {item['deadline']} | Prioritas: {item['prioritas']}")
        with c2:
            if not item["selesai"]:
                if st.button("Selesai", key=f"btn_{i}"):
                    item["selesai"] = True
                    st.rerun()

# --- WIDGET 3: TEMAN AI (ASISTEN BELAJAR) ---
st.header("🤖 Teman AI (Pit Stop Asisten)")
st.write("Tanyakan ide, rumus, atau strategi pengerjaan tugas di sini:")

topik = st.text_input("Topik/Materi Tugas", placeholder="cth: Fisika Kuantum, Puisi, Sejarah, dll.")
pertanyaan = st.text_area("Pertanyaan kamu:", placeholder="Tuliskan kendala atau soal yang butuh bantuan...", height=100)

if st.button("Tanyakan ke Teman AI"):
    if pertanyaan:
        st.markdown("**🤖 Teman AI Menjawab:**")
        st.success(f"Dua strategi utama untuk menyelesaikan materi **{topik if topik else 'kamu'}**:\n\n"
                   f"1. **Strategi Pit Stop:** Bagi tugas ke beberapa segmen fokus (25 menit pengerjaan, 5 menit istirahat).\n"
                   f"2. **Akselerasi Poin:** Selesaikan poin utama dulu sebelum merapikan bagian detailnya!")
    else:
        st.warning("Ketik pertanyaanmu terlebih dahulu!")
