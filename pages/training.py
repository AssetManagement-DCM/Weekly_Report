import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Training Heavy Equipment",
    page_icon="👷‍♂️",
    layout="wide"
)

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="stSidebar"] {display: none;}

        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
html { scroll-behavior: smooth; }
section.main > div { padding-top: 0rem; }

.navbar {
    background-color: #1a1a1a;
    padding: 14px 40px;
    display: flex;
    gap: 40px;
    font-size: 15px;
    color: white;
    width: 100%;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-item { position: relative; cursor: pointer; }
.nav-item a { color: white !important; text-decoration: none !important; }
.nav-item:hover a { opacity: 0.8; }
.dropdown {
    display: none;
    position: absolute;
    top: 32px;
    left: 0;
    background-color: #2b2b2b;
    padding: 8px 0;
    border-radius: 8px;
    min-width: 180px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
    z-index: 1000;
}
.nav-item:hover .dropdown { display: block; }
.dropdown a { padding: 8px 15px; display: block; }
.dropdown a:hover { background-color: #3c3c3c; display : block}
</style>

<div class="navbar">
    <div class="nav-item"><a href="?nav=overview">Overview</a></div>
    <div class="nav-item">
        Activity ▼
        <div class="dropdown">
            <a href="?nav=induksi">Induksi</a>
            <a href="?nav=training">Training</a>
            <a href="?nav=sharing">Sharing Knowledge</a>
        </div>
    </div>
</div>""",unsafe_allow_html=True)

nav = st.query_params.get("nav", None)

if nav == "overview":
    st.switch_page("home.py")

elif nav == "induksi":
    st.switch_page("pages/induksi.py")

elif nav == "sharing":
    st.switch_page("sharing.py")

elif nav == "training":
    pass

st.header("🏗️ Training Heavy Equipment")
# ================= AUTH ==================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

spreadsheet_name = "TRAINING 2025"
sheet = client.open(spreadsheet_name)

# === ambil sheet induksi ===
nameSheetDok = "DOKUMENTASI"
sheet_dok = client.open(nameSheetDok)
ws_training = sheet.worksheet("Training")
values_training = ws_training.get("E:N")
df_training = pd.DataFrame(values_training[1:], columns=values_training[0])

# === ambil sheet dokumentasi ===
ws_dok = sheet_dok.worksheet("Dokumentasi")
values_dok = ws_dok.get("E:L")
dokumentasi = pd.DataFrame(values_dok[1:], columns=values_dok[0])

# ================= WEEK FILTER ==================
weeks = sorted(df_training["Week"].dropna().unique())

week1_start = date(2024, 12, 27)
today = date.today()
days_since = (today - week1_start).days
current_week = (days_since // 7) + 1
default_week = f"Week {current_week}"

a,b,c,d,e=st.columns(5)
with e:
    # select_all = st.checkbox("Pilih semua Week")

    # if select_all:
    #     week_filter = weeks   # semua otomatis terpilih
    # else:
    #     week_filter = st.multiselect(
    #         "Pilih Week",
    #         weeks,
    #         default="Week 48"
    #     )

    options = ["Select All"] + weeks

    selected = st.multiselect(
        "Pilih Week",
        options,
        default=None
    )

    if "Select All" in selected:
        week_filter = weeks
    else:
        week_filter = selected

# ================= FILTER KE 2 DATA ==================
filtered_training = df_training[df_training["Week"].isin(week_filter)]
training_dokumentasi = dokumentasi[
    (dokumentasi["Week"].isin(week_filter)) &
    (dokumentasi["Kegiatan"] == "Training")
]

x1, x2, x3, x4,x5 = st.columns(5)
st.markdown("""
        <style>

        .metric-card {
            background: black;
            padding : 10px;
            border-radius: 12px;
            border: 1px solid #d9d9d9;
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
            text-align: left;
        }

        .metric-card h4 {
            margin: 0;
            margin-left : 20px;
            margin-bottom : -30px;
            text-align: left;
            font-size: 16px;
            font-weight: 600;
            color: white;
        }

        .metric-card .value {
            margin-top : -100px;
            margin-left : 20px;
            font-size: 48px;
            text-align: left;
            font-weight: 700;
            margin-top: 0px;
            color: white;
        }

        </style>
        """, unsafe_allow_html=True)
with x1:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Peserta Training</h4>
            <div class="value">{len(filtered_training)}</div>
        </div>
    """, unsafe_allow_html=True)
with x2:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Total Perusahaan</h4>
            <div class="value">{filtered_training["Perusahaan"].nunique()}</div>
        </div>
        
    """, unsafe_allow_html=True)
with x3:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Jenis Training</h4>
            <div class="value">{filtered_training["Jenis Training"].nunique()}</div>
        </div>
        
    """, unsafe_allow_html=True)
with x4:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Alat Berat</h4>
            <div class="value">{filtered_training["Jenis A2B"].nunique()}</div>
        </div>
        
    """, unsafe_allow_html=True)

st.divider()
col1, col2 = st.columns([3,4])
with col1 :
    # pivot = filtered_training.pivot_table(
    #     index="Perusahaan",     # baris
    #     columns="BU",           # kolom (DCM / HPAL / ONC)
    #     values="Nama",           # hitung berdasarkan NIK / baris
    #     aggfunc="count",        # hitung jumlah
    #     fill_value=0
    # ).reset_index()

    # # --- 3. Tambah kolom Total ---
    # pivot["Total"] = pivot[["DCM", "HPAL", "ONC"]].sum(axis=1)

    # # --- 4. Urutkan sesuai kebutuhan (opsional) ---
    # pivot = pivot.sort_values("Total", ascending=False)

    # st.dataframe(pivot, height=600)

    pivot = filtered_training.pivot_table(
        index="Perusahaan",
        columns="BU",
        values="Nama",
        aggfunc="count",
        fill_value=0
    ).reset_index()

    # --- Kolom BU yang mungkin ---
    possible_bus = ["DCM", "HPAL", "ONC"]

    # --- Kolom BU yang benar-benar ada di pivot ---
    available_bus = [bu for bu in possible_bus if bu in pivot.columns]

    # --- Jika tidak ada sama sekali, buat kolom Total = 0 ---
    if len(available_bus) == 0:
        pivot["Total"] = 0
    else:
        pivot["Total"] = pivot[available_bus].sum(axis=1)

    # --- Urutkan pivot ---
    pivot = pivot.sort_values("Total", ascending=False, ignore_index=True)

    st.dataframe(pivot, height=600)
with col2:
    # bu_totals = {
    #     "DCM": pivot["DCM"].sum(),
    #     "HPAL": pivot["HPAL"].sum(),
    #     "ONC": pivot["ONC"].sum()
    # }

    # labels = list(bu_totals.keys())
    # sizes  = list(bu_totals.values())

    # # Buat pie chart
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # ax1.axis('equal')

    # st.pyplot(fig1)

    possible_bus = ["DCM", "HPAL", "ONC"]

    # Ambil BU yang kolomnya memang ada di pivot
    available_bus = [bu for bu in possible_bus if bu in pivot.columns]

    # Kalau tidak ada kolom satupun → skip
    if len(available_bus) == 0:
        st.info("Tidak ada data BU untuk ditampilkan.")
    else:
        # Hitung total
        bu_totals = {bu: pivot[bu].sum() for bu in available_bus}

        labels = list(bu_totals.keys())
        sizes  = list(bu_totals.values())

        # Jika total semua = 0, skip chart
        if sum(sizes) == 0:
            st.info("Data BU kosong, tidak bisa menampilkan chart.")
        else:
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)


st.divider()

st.subheader("📸 Dokumentasi Kegiatan")
import requests
import streamlit as st

cols_per_row = 3
rows = training_dokumentasi.to_dict("records")

for i in range(0, len(rows), cols_per_row):
    cols = st.columns(cols_per_row)

    for col, row in zip(cols, rows[i:i+cols_per_row]):
        url = row["url_clean"]

        if url:
            try:
                response = requests.get(url, stream=True)

                content_type = response.headers.get("Content-Type", "")

                with col:
                    # Jika benar-benar image
                    if "image" in content_type:
                        st.image(
                            response.content,
                            caption=row.get("Keterangan", "")
                        )
                    else:
                        st.warning("Link tidak mengembalikan file gambar.")
                        st.write(row["url_clean"])

            except Exception as e:
                with col:

                    st.error(f"Error load: {e}")
