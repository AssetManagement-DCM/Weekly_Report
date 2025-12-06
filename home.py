import streamlit as st
import pandas as pd
import altair as alt
from streamlit_navigation_bar import st_navbar
from datetime import date
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Dashboard Asset Management",
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

st.image("abc.png")

SHEET_ID = "1UCyov9SZzwCzruemj7eUCFpc_ONV9du3fio00K_JHtI"
SHEET_NAME = "Data"
SHEET_NAME_MANPOWER = "Manpower"

manpowerUrl = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_MANPOWER}"
all_data = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data
def load_data():
    return pd.read_csv(all_data)
df = load_data()
data = df.iloc[:, 3:7]

@st.cache_data
def load_data_manpower():
    return pd.read_csv(manpowerUrl)
df_manpower = load_data_manpower()

weeks = sorted(data["Week"].dropna().unique())
st.markdown("""
<style>
/* Tag item terpilih (chip) */
div[data-baseweb="tag"] {
    background-color: black !important; /* ganti sesuai warna kamu */
    color: black !important;
    border: 1px solid black!important;
}

/* Text X (remove button) */
div[data-baseweb="tag"] svg {
    color: black !important;
}

/* Dropdown box border */
div[data-baseweb="select"] > div {
    border: 1px solid black !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

week1_start = date(2024, 12, 27)  # Jumat
week1_end = date(2025, 1, 2)      # Kamis
today = date.today()

days_since_week1 = (today - week1_start).days
current_week_number = (days_since_week1 // 7) + 1

default_week = f"Week {current_week_number}"

week_filter = st.multiselect("Pilih Week", weeks, default=[default_week],width=250)

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
.dropdown a:hover { background-color: #3c3c3c; }
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

if nav == "induksi":
    st.switch_page("pages/induksi.py")

elif nav == "training":
    st.switch_page("pages/training.py")

elif nav == "sharing":
    st.switch_page("sharing.py")

elif nav == "overview":
    pass

tab1, tab2 = st.tabs(["📑 Overview", "👷‍♂️ Activity"])

##OVERVIEW
with tab1:

    filtered_df = data[
        data["Week"].isin(week_filter)
    ]

    # METRICS
    st.subheader("📊 Weekly Overview")

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

    sum_kegiatan = (
        filtered_df.groupby(["BU", "Kegiatan"])["Jumlah"]
        .sum()
        .reset_index()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Total Manpower</h4>
                <div class="value">{len(df_manpower)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Manpower On-Site</h4>
                <div class="value">{(df_manpower["On/Off Site"] == "On-Site").sum()}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Manpower Off-Site</h4>
                <div class="value">{(df_manpower["On/Off Site"] == "Off-Site").sum()}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Total Kegiatan</h4>
                <div class="value">{sum(sum_kegiatan["Jumlah"])}</div>
            </div>
        """, unsafe_allow_html=True)

    # PREPARE CHART

    total_kegiatan = (
        sum_kegiatan.groupby("Kegiatan", as_index=False)["Jumlah"]
        .sum()
    )

    chart = (
        alt.Chart(sum_kegiatan)
        .mark_bar()
        .encode(
            y=alt.Y("Kegiatan:N", sort="-x", axis=alt.Axis(title=None)),
            x=alt.X("Jumlah:Q", axis=alt.Axis(title=None, labels=False, grid=False)),
            color=alt.Color(
                "BU:N",
                scale=alt.Scale(
                    domain=["DCM", "HPAL", "ONC", "Lainnya"],
                    range=["#134f5c", "#2f9a7f", "#31681a", "#ff9900"]
                )
            )
        )
    )

    labels = (
        alt.Chart(total_kegiatan)
        .mark_text(align="left", baseline="middle", dx=3)
        .encode(
            y="Kegiatan:N",
            x="Jumlah:Q",
            text=alt.Text("Jumlah:Q", format="0")
        )
    )

    # CONDITIONAL FORMATTING
    def highlight_offsite(row):
        if row["On/Off Site"].strip().lower() == "off-site":
            return ["background-color: #CECECE"] * len(row)
        return [""] * len(row)

    df_manpower = df_manpower.copy()
    df_manpower.index = df_manpower.index + 1  # start index from 1

    styled_df = (
        df_manpower.style
        .apply(highlight_offsite, axis=1)
        .hide(axis="index")
        .set_properties(**{
            "border": "1px solid #ddd",
            "text-align": "center",
            "padding": "6px",
            "font-size": "12px",
        })  
    )

    st.divider()
    col1, col2 = st.columns([3,5], border=True)

    with col1:
        st.markdown("<h3 style='text-align: center;'>👬🏼 Manpowers</h3>", unsafe_allow_html=True)
        st.dataframe(styled_df)

    with col2:
        container2 = st.container()
        container2.markdown("<div class='card-container'>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center;'>📈 Jumlah per Kegiatan</h3>", unsafe_allow_html=True)
        st.altair_chart((chart + labels).properties(height=400), use_container_width=True)

        container2.markdown("</div>", unsafe_allow_html=True)
with tab2:
    # selector = option_menu(
    #     menu_title=None,
    #     options=[
    #         "Induksi","Training","Sharing Knowledge","Pembekalan","Refresh",
    #         "SIMPER","Tes Praktik","Commissioning/Recommissioning","Inspeksi","Observasi"
    #     ],
    #     orientation="horizontal",
    #     styles={
    #         "container": {
    #             "padding": "0",
    #             "background-color": "#e7e7e7",
    #             "width": "100%",           # agar full width
    #             "display": "flex",
    #             "justify-content": "space-between",  # biar merata
    #         },
    #         "nav-link": {
    #             "font-size": "12px",
    #             "font-weight": "400",
    #             "padding": "10px 14px",
    #             "color": "black",
    #             "text-align": "center",
    #             "--hover-color": "#dcdcdc",
    #         },
    #         "nav-link-selected": {
    #             "background-color": "black",
    #             "color": "white",
    #             "font-weight": "600",
    #         }
    #     }
    # )
    a,b,c,d= st.columns(4)
    with a:
        submenu = st.selectbox(
            "Pilih Kategori Activity",
            ["Induksi", "Training", "Sharing Knowledge", "Pembekalan", 
            "Refresh", "SIMPER", "Tes Praktik", 
            "Commissioning/Recommissioning", "Inspeksi", "Observasi"],
            index=0
        )

        
    st.write("tab2")



st.divider()
st.markdown(
    """
    <p style="text-align: left; color: gray; font-size: 13px;">
        Asset Management 2025
    </p>
    """,
    unsafe_allow_html=True)