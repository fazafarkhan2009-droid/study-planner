import streamlit as st
import random

# Setup Halaman
st.set_page_config(page_title="BeatMood - Rekomendasi Musik", page_icon="ðŸŽµ", layout="centered")

# --- PENGATURAN TEMA DI SIDEBAR ---
st.sidebar.title("âš™ï¸ Pengaturan")
pilihan_tema = st.sidebar.radio("Pilih Tema:", ["Terang â˜€ï¸", "Gelap ðŸŒ™"])

if "Terang" in pilihan_tema:
    bg_app = "#faf8f5"
    text_color = "#212529"
    card_bg = "#ffffff"
    card_border = "#dee2e6"
    input_bg = "#ffffff"
    input_text = "#212529"
    input_border = "#ced4da"
else:
    bg_app = "#0d0d0d"
    text_color = "#f2f2f2"
    card_bg = "#171717"
    card_border = "#ff8000"
    input_bg = "#242424"
    input_text = "#ffffff"
    input_border = "#404040"

# CSS Styling
css_code = f"""
    <style>
    .stApp {{
        background-color: {bg_app};
        color: {text_color};
    }}
    div[data-testid="stVerticalBlock"] > div {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-left: 5px solid #ff8000;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    h1, h2, h3 {{
        color: #ff8000 !important;
        font-weight: bold;
    }}
    p, label, .stMarkdown {{
        color: {text_color} !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #ff8000 0%, #e67300 100%);
        color: #ffffff;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        width: 100%;
        transition: all 0.2s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #ff9933 0%, #ff8000 100%);
        box-shadow: 0 0 10px rgba(255, 128, 0, 0.3);
        color: #ffffff;
    }}
    .stSelectbox>div>div>div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1px solid {input_border} !important;
        border-radius: 6px;
    }}
    </style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# Basis Data Lagu (List of Dictionaries)
DATABASE_LAGU = [
    # Sedih / Galau
    {"judul": "Watch", "penyanyi": "Billie Eilish", "mood": "Sedih", "aktivitas": "Santai", "genre": "Pop / Melancholy", "link": "https://open.spotify.com/track/79hStyTWIOdUiZs1LRI9n2"},
    {"judul": "Glimpse of Us", "penyanyi": "Joji", "mood": "Sedih", "aktivitas": "Santai", "genre": "R&B / Soul", "link": "https://open.spotify.com/track/6xGruYrP9YndvFAwcsA2qn"},
    {"judul": "Traitor", "penyanyi": "Olivia Rodrigo", "mood": "Sedih", "aktivitas": "Santai", "genre": "Pop", "link": "https://open.spotify.com/track/50R1hG526L9vGvQc05m9t8"},
    {"judul": "Jiwa Yang Bersedih", "penyanyi": "Ghea Indrawari", "mood": "Sedih", "aktivitas": "Pengantar Tidur", "genre": "Pop Indonesia", "link": "https://open.spotify.com/track/1J9v1aDk5a5Xp3f2a1b0c0"},

    # Semangat / Nge-gym / Olahraga
    {"judul": "Outside", "penyanyi": "Calvin Harris ft. Ellie Goulding", "mood": "Semangat", "aktivitas": "Nge-gym / Olahraga", "genre": "EDM", "link": "https://open.spotify.com/track/3Tsq7z7bC1b9f6mQe3W4r5"},
    {"judul": "Eye of the Tiger", "penyanyi": "Survivor", "mood": "Semangat", "aktivitas": "Nge-gym / Olahraga", "genre": "Rock", "link": "https://open.spotify.com/track/2tTmW7RDgOiR7bLR1V9Z1E"},
    {"judul": "Stronger", "penyanyi": "Kanye West", "mood": "Semangat", "aktivitas": "Nge-gym / Olahraga", "genre": "Hip-Hop", "link": "https://open.spotify.com/track/4fzsw1z12V6E9vG2t1a8b9"},
    {"judul": "Can't Hold Us", "penyanyi": "Macklemore & Ryan Lewis", "mood": "Semangat", "aktivitas": "Nge-gym / Olahraga", "genre": "Hip-Hop / Pop", "link": "https://open.spotify.com/track/3u9v1aDk5a5Xp3f2a1b0c0"},

    # Fokus / Belajar
    {"judul": "Lofi Study Beats", "penyanyi": "Lofi Girl", "mood": "Fokus", "aktivitas": "Belajar", "genre": "Lofi Hip-Hop", "link": "https://open.spotify.com/track/0v1aDk5a5Xp3f2a1b0c0d1"},
    {"judul": "River Flows in You", "penyanyi": "Yiruma", "mood": "Fokus", "aktivitas": "Belajar", "genre": "Instrumental / Classical", "link": "https://open.spotify.com/track/058p42h45a6g7f8e9d0c1b"},
    {"judul": "Clair de Lune", "penyanyi": "Claude Debussy", "mood": "Fokus", "aktivitas": "Belajar", "genre": "Klasik", "link": "https://open.spotify.com/track/1v1aDk5a5Xp3f2a1b0c0d2"},
    {"judul": "Experience", "penyanyi": "Ludovico Einaudi", "mood": "Fokus", "aktivitas": "Belajar", "genre": "Neoclassical", "link": "https://open.spotify.com/track/2v1aDk5a5Xp3f2a1b0c0d3"},

    # Santai / Pengantar Tidur / Perjalanan
    {"judul": "Night Changes", "penyanyi": "One Direction", "mood": "Santai", "aktivitas": "Perjalanan", "genre": "Pop", "link": "https://open.spotify.com/track/50R1hG526L9vGvQc05m9t9"},
    {"judul": "Sunflower", "penyanyi": "Post Malone & Swae Lee", "mood": "Semangat", "aktivitas": "Perjalanan", "genre": "Hip-Hop / Pop", "link": "https://open.spotify.com/track/3v1aDk5a5Xp3f2a1b0c0d4"},
    {"judul": "Until I Found You", "penyanyi": "Stephen Sanchez", "mood": "Santai", "aktivitas": "Pengantar Tidur", "genre": "Indie Pop", "link": "https://open.spotify.com/track/4v1aDk5a5Xp3f2a1b0c0d5"},
    {"judul": "Golden Hour", "penyanyi": "JVKE", "mood": "Santai", "aktivitas": "Perjalanan", "genre": "Pop", "link": "https://open.spotify.com/track/5v1aDk5a5Xp3f2a1b0c0d6"}
]

# Header Utama
st.title("ðŸŽµ BeatMood Generator")
st.write("Temukan rekomendasi musik yang tepat berdasarkan suasana hati dan aktivitasmu!")

# Input Form
st.subheader("ðŸŽ¯ Pilih Kondisi Kamu")
c1, c2 = st.columns(2)

with c1:
    mood_pilihan = st.selectbox("Suasana Hati (Mood):", ["Sedih", "Semangat", "Fokus", "Santai"])
with c2:
    aktivitas_pilihan = st.selectbox("Aktivitas:", ["Santai", "Nge-gym / Olahraga", "Belajar", "Perjalanan", "Pengantar Tidur"])

# Logic Eksekusi
if st.button("ðŸŽµ Cari Rekomendasi Lagu"):
    # 1. Filtering berpasangan (Exact Match)
    hasil_filter = [
        lagu for lagu in DATABASE_LAGU 
        if lagu["mood"] == mood_pilihan and lagu["aktivitas"] == aktivitas_pilihan
    ]
    
    catatan_fallback = False
    # 2. Fallback Logic: Jika tidak ada match persis, cari berdasarkan Aktivitas saja
    if not hasil_filter:
        hasil_filter = [
            lagu for lagu in DATABASE_LAGU 
            if lagu["aktivitas"] == aktivitas_pilihan
        ]
        catatan_fallback = True
    
    # 3. Fallback Cadangan: Jika masih kosong, ambil dari Mood saja
    if not hasil_filter:
        hasil_filter = [
            lagu for lagu in DATABASE_LAGU 
            if lagu["mood"] == mood_pilihan
        ]

    # 4. Pengacakan (Shuffle) & Limit (Maksimal 3 lagu)
    if hasil_filter:
        jumlah_tampil = min(3, len(hasil_filter))
        rekomendasi = random.sample(hasil_filter, jumlah_tampil)
        
        st.subheader("ðŸŽ§ Rekomendasi Musik Untukmu")
        if catatan_fallback:
            st.info(f"Kombinasi persis belum ditemukan, menyajikan lagu terbaik untuk aktivitas **{aktivitas_pilihan}**:")
            
        for idx, lagu in enumerate(rekomendasi, 1):
            with st.container():
                st.markdown(f"### {idx}. {lagu['judul']}")
                st.markdown(f"**Penyanyi:** {lagu['penyanyi']} | **Genre:** {lagu['genre']}")
                st.markdown(f"**Cocok untuk:** Mood *{lagu['mood']}* saat *{lagu['aktivitas']}*")
                st.markdown(f"[â–¶ï¸ Dengarkan di Spotify]({lagu['link']})")
                st.write("")
    else:
        st.warning("Belum ada lagu yang sesuai dengan pilihan tersebut.")
