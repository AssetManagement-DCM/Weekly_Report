import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="induksi",
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

elif nav == "training":
    st.switch_page("pages/training.py")

elif nav == "sharing":
    st.switch_page("sharing.py")

elif nav == "induksi":
    pass


st.header("Induksi")
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

spreadsheet_name = "INDUKSI ALL BU 2025"
sheet = client.open(spreadsheet_name)

# === ambil sheet induksi ===
naemSheetDok = "DOKUMENTASI"
sheet_dok = client.open(naemSheetDok)
ws_induksi = sheet.worksheet("2025")
values_induksi = ws_induksi.get("E:N")
df_induksi = pd.DataFrame(values_induksi[1:], columns=values_induksi[0])

# === ambil sheet dokumentasi ===
ws_dok = sheet_dok.worksheet("Dokumentasi")
values_dok = ws_dok.get("E:L")
dokumentasi = pd.DataFrame(values_dok[1:], columns=values_dok[0])

# ================= WEEK FILTER ==================
weeks = sorted(df_induksi["Week"].dropna().unique())

week1_start = date(2024, 12, 27)
today = date.today()
days_since = (today - week1_start).days
current_week = (days_since // 7) + 1
default_week = f"Week {current_week}"

a,b,c,d,e=st.columns(5)
with e:
    week_filter = st.multiselect(
        "Pilih Week",
        weeks,
        default="Week 50",
        max_selections=None
    )

# ================= FILTER KE 2 DATA ==================
filtered_induksi = df_induksi[df_induksi["Week"].isin(week_filter)]
induksi_dokumentasi = dokumentasi[
    (dokumentasi["Week"].isin(week_filter)) &
    (dokumentasi["Kegiatan"] == "Induksi")
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
            <h4>Total induksi</h4>
            <div class="value">{len(filtered_induksi)}</div>
        </div>
    """, unsafe_allow_html=True)
with x2:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Total Perusahaan</h4>
            <div class="value">{filtered_induksi["Perusahaan"].nunique()}</div>
        </div>
        
    """, unsafe_allow_html=True)
with x3:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Total Perusahaan</h4>
            <div class="value">{filtered_induksi["Department"].nunique()}</div>
        </div>
        
    """, unsafe_allow_html=True)

st.divider()
col1, col2 = st.columns([3,4])
with col1 :
    pivot = filtered_induksi.pivot_table(
        index="Perusahaan",     # baris
        columns="BU",           # kolom (DCM / HPAL / ONC)
        values="Nama",           # hitung berdasarkan NIK / baris
        aggfunc="count",        # hitung jumlah
        fill_value=0
    ).reset_index()

    # --- 3. Tambah kolom Total ---
    pivot["Total"] = pivot[["DCM", "HPAL", "ONC"]].sum(axis=1)

    # --- 4. Urutkan sesuai kebutuhan (opsional) ---
    pivot = pivot.sort_values("Total", ascending=False)

    st.dataframe(pivot, height=600)
with col2:
    bu_totals = {
        "DCM": pivot["DCM"].sum(),
        "HPAL": pivot["HPAL"].sum(),
        "ONC": pivot["ONC"].sum()
    }

    labels = list(bu_totals.keys())
    sizes  = list(bu_totals.values())

    # Buat pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

st.divider()

st.subheader("📸 Dokumentasi Kegiatan")
import requests
import streamlit as st

cols_per_row = 3
rows = induksi_dokumentasi.to_dict("records")

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