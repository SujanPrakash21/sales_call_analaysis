
import ast
import re
from datetime import timedelta
import os
import gspread
import pandas as pd
import plotly.express as px
import streamlit as st
from google.oauth2.service_account import Credentials
import textwrap
import html
# ============================================================
# 1. CONFIGURATION
# ============================================================
os.environ["STREAMLIT_THEME_BASE"] = "light"
st._config.set_option("theme.base", "light")

st.set_page_config(
    page_title="Liquide | Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

GCP_CREDS = dict(st.secrets["gcp_service_account"])

SHEET_ID = "1bpyB0aXUiUGA0j5OwiEXMtifLnvE1dU-nKHR7COgxcY"
SHEET_NAMES = ["September 2026", "October 2026"]

BLUE = "#3975EF"
GREEN = "#16A37A"
ORANGE = "#F4A340"
RED = "#E56C78"
NAVY = "#17243D"


CUSTOMER_INTELLIGENCE_COLUMNS = [
    "call_id",
    "agent_name",
    "customer_number",
    "call_datetime",
    "analysis_status",
    "call_disposition",
    "call_outcome",
    "customer_type",
    "plan_pitched",
    "price_discussed",
    "not_interested_reason",
    "not_interested_reason_summary",
    "customer_interest_level",
    "interest_evidence",
    "overall_call_score",
    "propensity_score",
    "propensity_bucket"
]

SCORE_COLUMNS = {
    "overall_call_score": "Overall Call",
    "sales_effectiveness_score": "Sales Effectiveness",
    "communication_clarity_score": "Communication Clarity",
    "call_structure_score": "Call Structure",
    "customer_engagement_score": "Customer Engagement",
    "needs_identification_score": "Needs Identification",
    "solution_relevance_score": "Solution Relevance",
    "professionalism_score": "Professionalism",
    "compliance_score": "Compliance"
}

NAME_MAP = {

    "Abhishek": "Abhishek Ziraya",

    "Abhishek_Ziraya": "Abhishek Ziraya",

    "Aditi": "Aditi Verma",
    "Aditi_Verma": "Aditi Verma",

    "Adithya": "LV Adithya",

    "Adnan": "Adnan Kaify",
    "Adnan_Kaify": "Adnan Kaify",

    "Akash_Harkude": "Akash Harkude",

    "Aryan_Sahu" : "Aryan Sahu",
    
    "Ayush": "Ayush Singh",
    "Ayush_Ziraya": "Ayush Singh",

    "Bandana": "Bandana Kumari Nagar",

    "Chandra": "Chandra Bhushan",
    "Chandra_Ziraya": "Chandra Bhushan",

    "Chytanya": "Chytanya Netalkar",

    "Debangi": "Debangi Majumder",

    "Divya": "Divya Rashmi",

    "Garv": "Garv Tandan",
    "Garv_Ziraya": "Garv Tandan",

    "Garvit": "Garvit Jat",

    "Goresh": "Goresh Sharma",
    "Goresh_Ziraya": "Goresh Sharma",

    "Iftekhar": "Iftekhar Alam",

    "Irfan_S": "Irfan S",

    "Imdad": "Imdad P",
    "Imdad_P": "Imdad P",

    "Izaz_Ahmed": "Izaz Ahmed",
    "Izaz": "Izaz Ahmed",

    "Jaya": "Jaya Prajapat",

    "Jinson": "Jinson",

    "Jiya": "Jiya Pandey",

    "Krishna": "Krishna Kumar",

    "Kayum": "Kayum",

    "Kaushal_Kishor": "Kaushal Kishor",

    "Mohammed": "Mohammed Zeeshan",
    "Mohammed_Zeeshan": "Mohammed Zeeshan",

    "Nameet": "Nameet Karadi",

    "Namratha": "Namratha Chauhan",

    "Akash": "Akash Harkude",
    "Akash_Harkude": "Akash Harkude",

    "Ayan": "Ayan Dey",
    "Ayan_Dey": "Ayan Dey",

    "Manan": "Manan Shah",
    "Manan_Shah": "Manan Shah",

    "Mayank": "Mayank Biswas",
    "Mayank_Biswas": "Mayank Biswas",

    "Omkar": "Omkar Kaktikar",

    "Pawan": "Pawan Chahar",
    "Pawan_Ziraya": "Pawan Chahar",

    "Pradeep": "Pradeep Bhandari",

    "Pravesh": "Pravesh Singh",

    "Prathamsinha": "Pratham Sinha",

    "Preeti": "Preeti Tahilramani",

    "Priya": "Priya Khanna",
    "Priya_Ziraya": "Priya Khanna",

    "Priyanshi": "Priyanshi Kamal Das",

    "Priyap": "Priyadharshini P",

    "Puja": "Puja",

    "Rahaman": "Khan Rahaman",

    "Rajeev": "Rajeev Ranjan",

    "Rakshith": "Rakshith Pai",

    "Rishabh": "Rishabh Singh",

    "Rishabh_Ziraya": "Rishabh Kushwah",

    "Rishi": "Rishi Sarkar",

    "Ritik": "Ritik Raje",

    "Sabiha": "Shaik Sabiha",

    "Sagar": "Sagar Kumar",
    "Sagar_Ziraya": "Sagar Kumar",

    "Saif": "Saif Khan",
    "Saif_Ziraya": "Saif Khan",

    "Shahbaz": "Shahbaz Mansoori",

    "Shaik":"Shaik Aleem",
    "Shaik_Aleem": "Shaik Aleem",

    "Sibajit": "Sibajit Gope",
    "Sibajit_Gope": "Sibajit Gope",

    "Simran": "Simran",

    "Shreya": "Shreya Hari",
    "Shreya_H": "Shreya Hari",

    "Soumyajeet": "Soumyajeet Behera",

    "Sourav": "Sourav Chowdhury",

    "Sweta":"Sweta Raj",
    "Sweta_Raj": "Sweta Raj",

    "Sukanya": "Sukanya Kokate",
    "Sukanya_Kokate": "Sukanya Kokate",

    "Supriya": "Supriya Raj",

    "Umar": "Mohammad Umar Ali",

    "Umar_Farooq": "Umar Farooq",

    "Vanita": "Vanita Hiremath",
    "Vanita_Hiremath": "Vanita Hiremath",

    "Veervart": "Veervart Karnwal",
    "Veervart_Karnwal": "Veervart Karnwal",

    "Vibhanshu": "Vibhanshu Mishra",

    "Vinay": "Vinay Vyas",
    "Vinay_Vyas": "Vinay Vyas",

    "Vishal": "Vishal Gautam",

    "Vishals": "Vishal Singh",

    "Zain": "Zain Real",
}

TEAM_MAP = {
    "Garvit": [
        "Ritik Raje",
        "Iftekhar Alam",
        "Khan Rahaman",
        "Soumyajeet Behera",
        "Zain Real",
        "Priyadharshini P",
        "Sourav Chowdhury",
        "Aditi Verma",
        "Shreya Hari",
    ],

    "Krishna": [
        "Priyanshi Kamal Das",
        "Jiya Pandey",
        "Nameet Karadi",
        "Rishabh Singh",
        "Vishal Singh",
        "Mohammad Umar Ali",
        "LV Adithya",
    ],

    "Priya": [
        "Izaz Ahmed",
        "Rishi Sarkar",
        "Imdad P",
        "Akash Harkude",
    ],

    "Rakshith": [
        "Omkar Kaktikar",
        "Umar Farooq",
        "Mayank Biswas",
        "Sibajit Gope",
        "Puja",
        "Vishal Gautam",
        "Manan Shah",
        "Vinay Vyas",
        "Supriya Raj",
        "Jinson",
        "Shaik Aleem",
    ],

    "Pravesh Singh": [
        "Adnan Kaify",
        "Kayum",
        "Mohammed Zeeshan",
        "Aryan Sahu",
        "Irfan S",
        "Kaushal Kishor",
    ],
}

TEAM_LOOKUP = {
    agent: leader
    for leader, members in TEAM_MAP.items()
    for agent in [leader] + members
}

EMPTY_VALUES = {"", "none", "nan", "null", "unknown", "[]"}


# ============================================================
# 2. LIGHT THEME — FIXES WHITE TEXT
# ============================================================

st.markdown("""
<style>
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #F3F6FC !important;
    color: #17243D !important;
}

.block-container {
    max-width: 1600px;
    padding: 1.5rem 2rem 2rem;
}

[data-testid="stHeader"] {
    background: #F6F8FC !important;
}

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5EAF2;
}

[data-testid="stSidebar"] * {
    color: #24334C !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE3EE !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent !important;
}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] span {
    color: #17243D;
}

[data-testid="stMain"] h1 {
    font-size: 27px;
    font-weight: 750;
}

[data-testid="stMain"] h3 {
    font-size: 17px;
    font-weight: 700;
}

/* Premium KPI cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F1 !important;
    border-left: 4px solid #3975EF !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    min-height: 78px !important;
    box-shadow: 0 4px 16px rgba(30,55,100,0.06);
}

[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] {
    color: #60718D !important;
    font-size: 12px !important;
}

[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] {
    color: #15233E !important;
    font-size: 22px !important;
    font-weight: 750 !important;
}

[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F1;
    border-radius: 13px;
    padding: 8px;
}

/* Light dataframe styling */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F1 !important;
    border-radius: 12px !important;
    overflow: hidden;
    color-scheme: light !important;
}

[data-testid="stDataFrame"] iframe {
    color-scheme: light !important;
}

[data-testid="stMain"] [data-baseweb="select"] > div,
[data-testid="stMain"] input {
    background: #FFFFFF !important;
    color: #17243D !important;
}

[data-testid="stMain"] [data-baseweb="select"] span {
    color: #17243D !important;
}

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F1;
    border-radius: 10px;
}

[data-testid="stMain"] button[data-baseweb="tab"] {
    color: #17243D !important;
}

hr {
    border-color: #E5EAF2 !important;
}

.call-total [data-testid="stMetric"] {
    min-height: 235px !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.call-total [data-testid="stMetricValue"] {
    font-size: 42px !important;
}


/* Call Analysis Breakdown */
div[data-testid="stMetric"] {
    position: relative;
}

/* Smaller KPI cards in the middle column */

[data-testid="stMetric"] {
    min-height: 90px;
    padding: 12px !important;
}

/* Dashboard chart cards */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div[data-testid="stVerticalBlock"] [data-testid="stPlotlyChart"]) {
    border-radius: 14px;
}

[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #DFE7F2;
}

[data-testid="stMain"] [data-testid="stPlotlyChart"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Compact dashboard headings */
[data-testid="stMain"] h3 {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #17243D !important;
}

/* Softer dashboard background */
[data-testid="stAppViewContainer"] {
    background: #F0F4FB !important;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 14px rgba(26, 48, 91, 0.06);
}


/* Chart headings */
[data-testid="stMain"] h3 {
    font-size: 19px !important;
    font-weight: 750 !important;
}

/* Chart descriptions */
[data-testid="stMain"] [data-testid="stCaptionContainer"] {
    font-size: 14px !important;
}

/* Plotly chart text */
[data-testid="stPlotlyChart"] text {
    font-size: 13px !important;
}


</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. GOOGLE SHEETS
# ============================================================

@st.cache_data(ttl=300, show_spinner="Loading sales call data...")
def load_data():

    creds = Credentials.from_service_account_info(
        GCP_CREDS,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    book = gspread.authorize(creds).open_by_key(SHEET_ID)
    frames = []

    for name in SHEET_NAMES:
        try:
            values = book.worksheet(name).get_all_values()
        except gspread.exceptions.WorksheetNotFound:
            continue

        if len(values) < 2:
            continue

        headers = [str(x).strip() for x in values[0]]
        rows = [
            (list(row) + [""] * len(headers))[:len(headers)]
            for row in values[1:]
        ]

        part = pd.DataFrame(rows, columns=headers)
        part = part.loc[:, ~part.columns.duplicated()].copy()
        part["source_sheet"] = name
        frames.append(part)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ============================================================
# 4. DATA PREPARATION
# ============================================================

def clean(series):
    return series.fillna("").astype(str).str.strip()


# def avg(df, col):
#     values = pd.to_numeric(df[col], errors="coerce").dropna()
#     return values.mean() if not values.empty else float("nan")


def avg(df, col):
    values = pd.to_numeric(df[col], errors="coerce").dropna()

    if col == "compliance_score":
        values = values[values > 0]

    return values.mean() if not values.empty else float("nan")


def fmt(value, digits=2):
    return f"{value:.{digits}f}" if pd.notna(value) else "—"


def split_items(value):

    if pd.isna(value):
        return []

    value = str(value).strip()

    if value.casefold() in EMPTY_VALUES:
        return []

    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except (ValueError, SyntaxError):
            pass

    return [
        x.strip(" •-\n")
        for x in re.split(r"\s*\|\s*", value)
        if x.strip(" •-\n")
    ]


def prepare(raw):

    df = raw.copy()

    required = list(SCORE_COLUMNS) + [
        "call_id", "agent_name", "customer_number",
        "call_datetime", "analysis_status", "call_outcome",
        "call_disposition", "propensity_score",
        "propensity_bucket", "mistake_count",
        "violations_found", "mistakes", "improvements",
        "what_agent_should_have_done", "next_best_action",
        "customer_interest_level", "not_interested_reason",
        "plan_pitched", "customer_type", "interest_evidence",
        "overall_call_score_reason",
        "not_interested_reason_summary", "violations"
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ""

    df["agent_name"] = clean(df["agent_name"]).replace(NAME_MAP)
    df["team_leader"] = df["agent_name"].map(TEAM_LOOKUP).fillna("Ziraya")

    df["call_datetime"] = pd.to_datetime(
        df["call_datetime"], errors="coerce", format="mixed"
    )
    df["date"] = df["call_datetime"].dt.date

    for col in list(SCORE_COLUMNS) + ["propensity_score", "mistake_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in [
        "analysis_status", "call_outcome",
        "propensity_bucket", "violations_found"
    ]:
        df[col] = clean(df[col])

    status = df["analysis_status"].str.upper()
    outcome = df["call_outcome"].str.casefold()

    # Original dashboard logic:
    # Analyzable calls exclude these two statuses.
    df["valid"] = ~status.isin([
        "SKIPPED_SHORT_AUDIO",
        "EMPTY_TRANSCRIPT"
    ])

    # Score calculations use positive scored calls.
    # df["score_valid"] = (
    #     status.ne("SKIPPED_SHORT_AUDIO")
    #     & df["overall_call_score"].notna()
    #     & df["overall_call_score"].gt(0)
    # )


    df["score_valid"] = (
        df["valid"]
        & df["overall_call_score"].notna()
        & df["overall_call_score"].gt(0)
    )


    df["sold"] = outcome.eq("subscription sold")
    df["followup"] = outcome.str.contains("follow", na=False)
    df["appointment"] = outcome.eq("appointment fixed")
    df["not_interested"] = outcome.eq("not interested")

    df["violation"] = (
        df["violations_found"]
        .str.casefold()
        .isin(["true", "yes", "1"])
    )

    ids = clean(df["call_id"])
    missing = ids.eq("") | ids.str.casefold().isin(EMPTY_VALUES)

    df["call_key"] = ids
    df.loc[missing, "call_key"] = (
        "__missing_" + df.index[missing].astype(str)
    )

    return df.drop_duplicates("call_key", keep="last").reset_index(drop=True)


# ============================================================
# 5. KPI CALCULATIONS
# ============================================================

def calculate_metrics(df):

    analyzed = df[df["valid"]]
    scored = df[df["score_valid"]]

    n = len(analyzed)
    sold = int(analyzed["sold"].sum())

    return {
        "Total Calls": len(df),
        "Skipped Calls": len(df) - n,
        "Analyzable Calls": n,
        "Subscription Sold": sold,
        "Follow Ups": int(analyzed["followup"].sum()),
        "Appointments": int(analyzed["appointment"].sum()),
        "Not Interested": int(analyzed["not_interested"].sum()),
        "Conversion %": f"{sold / n * 100:.2f}%" if n else "0.00%",
        "Avg Overall Score": fmt(avg(scored, "overall_call_score")),
        "Avg Compliance": fmt(avg(scored, "compliance_score")),
        "Avg Propensity": fmt(avg(analyzed, "propensity_score")),
        "Total Mistakes": int(analyzed["mistake_count"].fillna(0).sum()),
        "Compliance Violations": int(analyzed["violation"].sum())
    }


def kpis(values, per_row=6):

    items = list(values.items())

    for start in range(0, len(items), per_row):
        batch = items[start:start + per_row]
        cols = st.columns(len(batch), gap="small")

        for col, (name, value) in zip(cols, batch):
            with col:
                st.metric(name, value)





def call_analysis_breakdown(m):
    st.markdown("### Call Analysis Breakdown")

    total = m["Total Calls"]
    skipped = m["Skipped Calls"]
    analyzed = m["Analyzable Calls"]
    sold = m["Subscription Sold"]

    def card(title, value, description, color):
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #DFE7F3;
            border-top: 4px solid {color};
            border-radius: 12px;
            padding: 16px 18px;
            height: 135px;
            box-sizing: border-box;
        ">
            <div style="font-size:13px;color:#64748B;">{title}</div>
            <div style="font-size:28px;font-weight:750;color:#172541;margin:6px 0;">
                {value}
            </div>
            <div style="font-size:12px;color:#64748B;">{description}</div>
        </div>
        """, unsafe_allow_html=True)


    # ROW 1 — KPI CARDS
    c1, c2 = st.columns(2, gap="small")

    with c1:
        overview_kpi("Average Call Score", m["Avg Overall Score"], PURPLE)

    with c2:
        overview_kpi("Subscriptions Sold", f"{sold:,}", ORANGE)

    st.write("")

    # ROW 2 — TOTAL CALLS + KEY INSIGHTS
    left, right = st.columns([1.2, 1], gap="medium")

    with left:
        overview_total_calls_kpi(data)

    with right:
        with st.container(border=True):
            overview_card("Key Insights")

            insights = [
                (GREEN, "Analysis Coverage", f"{coverage:.1f}%",
                f"{skipped:,} skipped calls"),
                (BLUE, "Sales Conversion", f"{conversion:.2f}%",
                f"{sold:,} subscriptions sold"),
                (PURPLE, "Follow-Up Opportunities", f"{followups + appointments:,}",
                f"{followups:,} follow-ups · {appointments:,} appointments"),
                (RED, "Sales Mistakes", f"{mistakes_total:,}",
                f"{violations:,} compliance violations")
            ]

            for color, label, value, detail in insights:
                st.markdown(
                    f'<div style="border-left:3px solid {color};'
                    f'padding:8px 12px;margin-bottom:8px;background:#FFFFFF;'
                    f'border-radius:7px;">'
                    f'<div style="font-size:11px;color:#64748B;">{label}</div>'
                    f'<div style="font-size:19px;font-weight:700;color:#172642;">{value}</div>'
                    f'<div style="font-size:11px;color:#64748B;">{detail}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.write("")

    # ROW 3 — CALL SCORE ANALYSIS
    with st.container(border=True):
        overview_score_card(data)


    if total > 0:
        skipped_pct = skipped / total * 100
        analyzed_pct = analyzed / total * 100

        st.markdown("#### Call Distribution")

        st.markdown(
            f"""
<div style="display:flex;width:100%;height:52px;border-radius:10px;overflow:hidden;">
    <div style="width:{skipped_pct}%;background:#F59E0B;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#422006;">
        <strong style="font-size:18px;">{skipped:,}</strong>
        <span style="font-size:12px;">{skipped_pct:.1f}% Skipped</span>
    </div>
    <div style="width:{analyzed_pct}%;background:#10B981;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#052E23;">
        <strong style="font-size:18px;">{analyzed:,}</strong>
        <span style="font-size:12px;">{analyzed_pct:.1f}% Analyzed</span>
    </div>
</div>
""",
            unsafe_allow_html=True
        )

def key_insights(df):
    m = calculate_metrics(df)
    analyzed_df = df[df["valid"]].copy()

    total = m["Total Calls"]
    analyzed_count = m["Analyzable Calls"]
    coverage = analyzed_count / total * 100 if total else 0

    insights = [
        (
            "Call Analysis Coverage",
            f"{coverage:.1f}%",
            f"{analyzed_count:,} of {total:,} calls analyzed",
            "#16A37A"
        ),
        (
            "Sales Conversion",
            m["Conversion %"],
            f'{m["Subscription Sold"]:,} subscriptions sold',
            "#3975EF"
        ),
        (
            "Follow-Up Opportunities",
            f'{m["Follow Ups"] + m["Appointments"]:,}',
            f'{m["Follow Ups"]} follow-ups · {m["Appointments"]} appointments',
            "#8B5CF6"
        ),
        (
            "Sales Mistakes",
            f'{m["Total Mistakes"]:,}',
            f'{m["Compliance Violations"]} compliance violations',
            "#E56C78"
        )
    ]

    reasons = clean(analyzed_df.loc[
        analyzed_df["not_interested"], "not_interested_reason"
    ])
    reasons = reasons[~reasons.str.casefold().isin(EMPTY_VALUES)]

    if not reasons.empty:
        top_reason = reasons.value_counts().index[0]
        insights.append((
            "Top Customer Objection",
            str(top_reason),
            f'{reasons.value_counts().iloc[0]:,} occurrences',
            "#F4A340"
        ))

    perf = performance_table(df, "agent_name")
    # perf = perf[
    #     (perf["Analyzable_Calls"] >= 5) & perf["Avg_Score"].notna()
    # ]

    perf = perf[
        (perf["Scored_Calls"] >= 5) & perf["Avg_Score"].notna()
    ]

    if not perf.empty:
        # best = perf.sort_values(
        #     ["Avg_Score", "Analyzable_Calls"],
        #     ascending=[False, False]
        # ).iloc[0]

        best = perf.sort_values(
            ["Avg_Score", "Scored_Calls"],
            ascending=[False, False]
        ).iloc[0]

        insights.append((
            "Top Quality Agent",
            str(best["agent_name"]),
            f'Avg score {best["Avg_Score"]:.2f}/10',
            "#16A37A"
        ))

    st.markdown("### Key Insights")

    for title, value, detail, color in insights:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E2E8F1;
                border-left:4px solid {color};
                border-radius:10px;
                padding:11px 13px;
                margin-bottom:10px;
            ">
                <div style="font-size:12px;color:#64748B;">{html.escape(title)}</div>
                <div style="
                    font-size:17px;
                    font-weight:750;
                    color:#17243D;
                    margin:5px 0;
                    overflow-wrap:anywhere;
                ">{html.escape(value)}</div>
                <div style="font-size:11px;color:#64748B;">
                    {html.escape(detail)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# 6. CHART HELPERS
# ============================================================


def show_chart(fig, height=280):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=8, r=25, t=48, b=20),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial", size=13, color="#53647E"),
        title=dict(
            font=dict(size=17, color="#17243D", family="Arial"),
            x=0.02,
            xanchor="left",
            y=0.97,
            yanchor="top"
        ),
        showlegend=False,
        xaxis=dict(
            gridcolor="#EDF2F8",
            zeroline=False,
            title=None
        ),
        yaxis=dict(
            gridcolor="#EDF2F8",
            zeroline=False,
            title=None,
            automargin=True
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        config={"displayModeBar": False}
    )




def category_chart(df, column, title, limit=8):
    values = clean(df[column])
    values = values[~values.str.casefold().isin(EMPTY_VALUES)]
    counts = values.value_counts().head(limit)
    total = int(counts.sum())

    if not total:
        st.info("No classified calls available.")
        return

    descriptions = {
        "customer_interest_level": "Interest levels recorded across classified calls",
        "propensity_bucket": "Conversion propensity across scored calls"
    }

    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.caption(descriptions.get(column, "Distribution across classified calls"))

        st.markdown(
            f'<div style="font-size:13px;color:#64748B;'
            f'margin-bottom:18px;">'
            f'<b style="color:#172642;">{total:,}</b> classified calls'
            f'</div>',
            unsafe_allow_html=True
        )

        rows = []

        for label, count in counts.items():
            pct = count / total * 100
            label = html.escape(str(label).title())

            rows.append(f"""
                <div style="margin-bottom:19px;">
                    <div style="display:flex;justify-content:space-between;
                                align-items:center;gap:12px;margin-bottom:8px;">
                        <span style="font-size:13px;font-weight:600;
                                     color:#344563;">{label}</span>
                        <span style="font-size:13px;color:#172642;
                                     white-space:nowrap;">
                            <b>{count:,}</b>
                            <span style="color:#8491A5;">({pct:.1f}%)</span>
                        </span>
                    </div>
                    <div style="height:12px;background:#EAF0F8;
                                border-radius:20px;overflow:hidden;">
                        <div style="height:100%;width:{pct:.2f}%;
                                    background:#3976EF;
                                    border-radius:20px;"></div>
                    </div>
                </div>
            """)
        st.markdown(
            textwrap.dedent(
                '<div style="padding:4px 0 0;">'
                + "".join(rows)
                + '</div>'
            ).replace("\n", ""),
            unsafe_allow_html=True
        )




def outcome_chart(df, title="Call Outcome Disposition"):
    if df.empty:
        st.info("No analyzed calls available")
        return

    counts = (
        df["call_outcome"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
    )

    labels = counts.index.tolist()
    values = counts.values.tolist()
    total = sum(values)

    color_map = {
        "unknown": BLUE,
        "appointment fixed": GREEN,
        "not interested": ORANGE,
        "follow up": RED,
        "subscription sold": "#A0A9C0"
    }

    colors = [
        color_map.get(label.lower(), "#A0A9C0")
        for label in labels
    ]

    st.markdown(f"**{title}**")
    st.caption(f"Distribution of outcomes across {total:,} analyzed calls")

    left, right = st.columns([1, 1], gap="medium")

    with left:
        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.72,
            sort=False,
            marker=dict(
                colors=colors,
                line=dict(color="white", width=3)
            ),
            textinfo="none",
            showlegend=False,
            hovertemplate=(
                "<b>%{label}</b><br>"
                "%{value} calls (%{percent})"
                "<extra></extra>"
            )
        ))

        fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            showlegend=False,
            annotations=[
                dict(
                    text=f"<b>{total:,}</b><br>Analyzed Calls",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color=NAVY)
                )
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with right:
        for label, count, color in zip(labels, values, colors):
            pct = count / total * 100 if total else 0

            st.markdown(
                f"""
                <div style="margin:4px 0 10px;">
                    <div style="display:flex;justify-content:space-between;
                                align-items:center;gap:10px;margin-bottom:7px;">
                        <span style="font-size:13px;color:#17243D;">
                            <span style="color:{color};font-size:17px;">●</span>
                            {html.escape(label)}
                        </span>
                        <span style="font-size:13px;color:#17243D;white-space:nowrap;">
                            <b>{count:,}</b> ({pct:.1f}%)
                        </span>
                    </div>
                    <div style="background:#EDF2F8;height:7px;
                                border-radius:10px;overflow:hidden;">
                        <div style="width:{pct:.1f}%;height:100%;
                                    background:{color};border-radius:10px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )



def score_chart(df, title="Quality Score Breakdown"):

    values = [
        (label, avg(df, col))
        for col, label in SCORE_COLUMNS.items()
    ]

    view = (
        pd.DataFrame(values, columns=["Metric", "Score"])
        .dropna()
        .sort_values("Score")
    )

    if view.empty:
        st.info("No scores available")
        return

    fig = px.bar(
        view,
        x="Score",
        y="Metric",
        orientation="h",
        text="Score",
        color_discrete_sequence=[BLUE]
    )

    fig.update_traces(
        marker=dict(cornerradius=6),
        texttemplate="%{x:.2f}",
        textposition="outside",
        textfont=dict(size=11, color=NAVY),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Score: %{x:.2f}/10<extra></extra>"
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=NAVY), x=0.02),
        height=380,
        margin=dict(l=10, r=45, t=55, b=30),
        xaxis=dict(
            title=None,
            range=[0, 11],
            tickvals=[0, 2, 4, 6, 8, 10],
            gridcolor="#EDF2F8",
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            automargin=True,
            tickfont=dict(size=11)
        ),
        bargap=0.35,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", color="#52627B")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def daily_chart(df):

    daily = df.groupby("date").size().reset_index(name="Calls")

    if daily.empty:
        st.info("No daily data available")
        return

    fig = px.area(
        daily,
        x="date",
        y="Calls",
        markers=True,
        title="Calls by Date"
    )

    fig.update_traces(
        line_color="#3975EF",
        line_width=3,
        marker=dict(size=7, color="#3975EF"),
        fillcolor="rgba(57,117,239,0.18)"
    )

    show_chart(fig, 330)


# ============================================================
# 7. PERFORMANCE TABLE
# ============================================================

def performance_table(df, group):

    base = df.groupby(group).agg(
        Raw_Calls=("call_key", "size"),
        Analyzable_Calls=("valid", "sum")
    )

    analyzed = df[df["valid"]]
    scored = df[df["score_valid"]]

    outcomes = analyzed.groupby(group).agg(
        Sold=("sold", "sum"),
        Follow_Ups=("followup", "sum"),
        Appointments=("appointment", "sum"),
        Not_Interested=("not_interested", "sum"),
        Avg_Propensity=("propensity_score", "mean"),
        Total_Mistakes=("mistake_count", "sum"),
        Violations=("violation", "sum")
    )

    # scores = scored.groupby(group).agg(
    #     Avg_Score=("overall_call_score", "mean"),
    #     Avg_Compliance=("compliance_score", "mean")
    # )


    # scores = scored.groupby(group).agg(
    #     Avg_Score=("overall_call_score", "mean")
    # )


    scores = scored.groupby(group).agg(
        Scored_Calls=("overall_call_score", "count"),
        Avg_Score=("overall_call_score", "mean")
    )

    compliance_scores = scored[scored["compliance_score"] > 0].groupby(group)["compliance_score"].mean()

    scores["Avg_Compliance"] = compliance_scores

    result = base.join(outcomes).join(scores)

    result["Scored_Calls"] = (
        result["Scored_Calls"].fillna(0).astype(int)
    )

    for col in [
        "Sold", "Follow_Ups", "Appointments",
        "Not_Interested", "Total_Mistakes", "Violations"
    ]:
        result[col] = result[col].fillna(0)

    result["Skipped_Calls"] = (
        result["Raw_Calls"] - result["Analyzable_Calls"]
    )

    result["Conversion_%"] = (
        100 * result["Sold"] /
        result["Analyzable_Calls"].replace(0, float("nan"))
    )

    result["Avg_Mistakes_per_Call"] = (
        result["Total_Mistakes"] /
        result["Analyzable_Calls"].replace(0, float("nan"))
    )

    return (
        result.reset_index()
        .round(2)
        .sort_values("Analyzable_Calls", ascending=False)
    )

def hourly_activity_chart(df):
    hours = df["call_datetime"].dropna().dt.hour
    hours = hours.value_counts().sort_index()

    if hours.empty:
        st.info("No hourly call data available")
        return

    view = hours.rename_axis("Hour").reset_index(name="Calls")
    view["Time"] = view["Hour"].map(lambda h: f"{h:02d}:00")

    fig = px.bar(
        view, x="Time", y="Calls",
        title="Hourly Calling Activity",
        text="Calls",
        color_discrete_sequence=[BLUE]
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    show_chart(fig, 280)


def mistakes_chart(df):
    from collections import Counter

    excluded = {
        "", "none", "n/a", "unknown",
        "no major mistake identified",
        "no mistakes identified"
    }

    items = []
    for value in df["mistakes"]:
        for item in split_items(value):
            item = item.strip()
            if item and item.casefold() not in excluded:
                items.append(item)

    if not items:
        total = int(df["mistake_count"].fillna(0).sum())
        st.metric("Total Sales Mistakes", f"{total:,}")
        st.caption("Mistake categories are not available for these calls.")
        return

    counts = Counter(items).most_common(6)
    view = pd.DataFrame(counts, columns=["Mistake", "Occurrences"])
    view["Mistake"] = view["Mistake"].str.wrap(35)

    fig = px.bar(
        view.iloc[::-1],
        x="Occurrences",
        y="Mistake",
        orientation="h",
        text="Occurrences",
        color_discrete_sequence=[ORANGE]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(title=None, margin=dict(l=10, r=30, t=10, b=20))
    show_chart(fig, 280)

# ============================================================
# 8. INSIGHTS AND RECORD HELPERS
# ============================================================

def insight_table(df, column, title):

    items = [
        item
        for value in df[column]
        for item in split_items(value)
        if item.strip().casefold() not in {
            "no major mistake identified",
            "no improvement identified",
            "no mistakes identified",
            "no improvements identified",
            "none",
            "n/a"
        }
    ]

    st.markdown(f"#### {title}")

    if not items:
        st.info("No insights available")
        return

    counts = (
        pd.Series(items)
        .value_counts()
        .head(20)
        .rename_axis("Insight")
        .reset_index(name="Occurrences")
    )

    st.dataframe(
        counts,
        use_container_width=True,
        hide_index=True,
        height=300
    )


def show_field(label, value):

    st.markdown(f"**{label}**")

    items = split_items(value)

    if not items:
        st.caption("Not available")
        return

    for item in items:
        st.write("• " + item)


def call_records(df, height=320):

    cols = [
        "call_datetime", "agent_name", "team_leader",
        "customer_number", "call_outcome",
        "overall_call_score", "propensity_bucket",
        "next_best_action"
    ]

    st.dataframe(
        df.sort_values("call_datetime", ascending=False)[cols],
        use_container_width=True,
        hide_index=True,
        height=height
    )

# ============================================================
# 9. LOAD DATA
# ============================================================

try:
    raw = load_data()
except Exception as exc:
    st.error(f"Google Sheets connection failed: {exc}")
    st.stop()

if raw.empty:
    st.warning("No data found in the configured worksheets.")
    st.stop()

raw = raw.reset_index(drop=True)
raw["_source_row_id"] = raw.index

data = prepare(raw)


# ============================================================
# 10. SIDEBAR
# ============================================================

st.sidebar.markdown("## LIQUIDE")
st.sidebar.caption("SALES INTELLIGENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Team Performance",
        "Agent Performance",
        "Customer Intelligence",
        "Customer Timeline",
        
        
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Filters")

all_data = data.copy()

dates = all_data["date"].dropna()

if dates.empty:
    st.error("No valid call dates found.")
    st.stop()

min_date = dates.min()
max_date = dates.max()

start_date = end_date = max_date
leaders = []
agents = []
outcomes = []

if page == "Customer Timeline":
    pass

else:

    selected_dates = st.sidebar.date_input(
        "Select Date / Date Range",
        value=(max_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    if isinstance(selected_dates, (tuple, list)):
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates
        elif len(selected_dates) == 1:
            start_date = end_date = selected_dates[0]
    else:
        start_date = end_date = selected_dates

    data = data[data["date"].between(start_date, end_date)].copy()

    leaders = st.sidebar.multiselect(
        "Team Leader",
        sorted(data["team_leader"].dropna().unique())
    )

    if leaders:
        data = data[data["team_leader"].isin(leaders)].copy()

    agents = st.sidebar.multiselect(
        "Agent",
        sorted(data["agent_name"].dropna().unique())
    )

    if agents:
        data = data[data["agent_name"].isin(agents)].copy()

    outcomes = st.sidebar.multiselect(
        "Call Outcome",
        sorted(data["call_outcome"].dropna().unique())
    )

    if outcomes:
        data = data[data["call_outcome"].isin(outcomes)].copy()

if st.sidebar.button("↻ Refresh Data", use_container_width=True):
    load_data.clear()
    st.rerun()

st.sidebar.caption("Google Sheets · Refreshes every 5 minutes")



from collections import Counter
import ast
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BLUE = "#3976EF"
GREEN = "#13A77C"
ORANGE = "#F5A03A"
RED = "#E66A75"
PURPLE = "#9065EB"
INK = "#172642"

def overview_kpi(label, value, color=BLUE, subtitle=""):
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #DFE5F0;border-left:4px solid {color};
                border-radius:12px;padding:13px 15px;min-height:83px;">
        <div style="font-size:12px;color:#60718D;">{label}</div>
        <div style="font-size:23px;font-weight:750;color:{INK};margin-top:4px;">{value}</div>
        <div style="font-size:11px;color:#8490A5;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def overview_chart(fig, height=290, margin_left=15, margin_right=25):
    fig.update_layout(
        height=height,
        margin=dict(l=margin_left, r=margin_right, t=12, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", size=11, color="#50617D"),
        showlegend=False,
        bargap=0.28
    )
    fig.update_xaxes(gridcolor="#E9EDF5", zeroline=False)
    fig.update_yaxes(gridcolor="#E9EDF5", zeroline=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



def overview_bar(labels, values, color=BLUE, height=270, horizontal=True, total=None):
    if not labels:
        st.info("No data available.")
        return

    labels = [str(x) for x in labels]
    values = [int(x) for x in values]
    denominator = total if total is not None else sum(values)
    denominator = denominator or 1

    value_text = [
        f"{v:,} ({v / denominator * 100:.1f}%)"
        for v in values
    ]

    fig = go.Figure()

    if horizontal:
        fig.add_trace(go.Bar(
            x=values[::-1],
            y=labels[::-1],
            orientation="h",
            marker_color=color,
            text=value_text[::-1],
            textposition="outside",
            textfont=dict(size=11, color="#344563"),
            cliponaxis=False,
            hovertemplate="%{y}<br>%{text}<extra></extra>"
        ))

        fig.update_layout(
            xaxis=dict(visible=False, range=[0, max(values) * 1.35]),
            yaxis=dict(showgrid=False, automargin=True),
            bargap=0.38
        )

    else:
        fig.add_trace(go.Bar(
            x=labels,
            y=values,
            marker_color=color,
            text=value_text,
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x}<br>%{text}<extra></extra>"
        ))

        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(visible=False, range=[0, max(values) * 1.2]),
            bargap=0.45
        )

    fig.update_layout(
        height=height,
        margin=dict(l=5, r=55, t=20, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#53647E"),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def overview_card(title):
    st.markdown(
        f"<div style='font-size:15px;font-weight:700;color:{INK};margin:2px 0 8px;'>{title}</div>",
        unsafe_allow_html=True
    )


def overview_counts(frame, column, limit=7):
    if column not in frame.columns:
        return pd.Series(dtype=int)
    s = frame[column].fillna("").astype(str).str.strip()
    s = s[~s.str.lower().isin(["", "nan", "none", "unknown", "null"])]
    return s.value_counts().head(limit)




def overview_mistakes(frame, limit=7):
    counts = Counter()

    excluded = {
        "", "none", "nan", "n/a", "[]",
        "no major mistake identified",
        "no mistakes identified",
        "no mistake identified",
        "no major mistakes",
        "no mistakes"
    }

    for value in frame["mistakes"]:
        for item in split_items(value):
            item = item.strip()

            if item.casefold() not in excluded:
                counts[item] += 1

    result = pd.Series(dict(counts), dtype=int).sort_values(ascending=False)
    return result.head(limit) if limit is not None else result


def overview_table(frame, height=320):
    st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
        height=height
    )




def overview_disposition_card(data):
    df = data[data["valid"]].copy()

    outcomes = [
        ("Subscription Sold", "sold", "#14B8A6"),
        ("Follow Up", "followup", "#48A9F8"),
        ("Appointment Fixed", "appointment", "#A879E6"),
        ("Not Interested", "not_interested", "#FB9B55"),
    ]

    rows = []
    assigned = pd.Series(False, index=df.index)

    for label, column, color in outcomes:
        mask = df[column].fillna(False).astype(bool) & ~assigned
        rows.append({"Outcome": label, "Calls": int(mask.sum()), "Color": color})
        assigned |= mask

    rows.append({
        "Outcome": "Unknown / Other",
        "Calls": int((~assigned).sum()),
        "Color": "#94A3B8"
    })

    summary = pd.DataFrame(rows)
    total = len(df)
    summary["Pct"] = summary["Calls"] / total * 100 if total else 0

    st.markdown("#### Call Outcome Dispositions")
    st.caption(f"Outcomes of {total:,} analyzed calls")

    left, right = st.columns([0.9, 1.1], gap="medium")

    with left:

        fig = go.Figure(go.Pie(
            labels=summary["Outcome"],
            values=summary["Calls"],
            hole=0.76,
            marker=dict(
                colors=summary["Color"],
                line=dict(color="#F5F7FC", width=2)
            ),
            textinfo="none",
            sort=False,
            showlegend=False,
            hovertemplate="%{label}<br>%{value:,} calls (%{percent})<extra></extra>"
        ))

        fig.update_layout(
            height=270,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(
                text=f"<b>{total:,}</b><br><span style='font-size:13px'>Analyzed Calls</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=23, color="#172642")
            )]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with right:
        breakdown = []

        for row in summary.to_dict("records"):
            label = html.escape(str(row["Outcome"]))
            count = int(row["Calls"])
            pct = float(row["Pct"])
            color = row["Color"]

            breakdown.append(f"""
                <div style="margin-bottom:17px;">
                    <div style="display:flex;justify-content:space-between;
                        align-items:center;gap:8px;margin-bottom:7px;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="width:9px;height:9px;border-radius:50%;
                                flex-shrink:0;background:{color};"></span>
                            <span style="font-size:14px;font-weight:600;
                                color:#344563;">{label}</span>
                        </div>
                        <span style="font-size:14px;white-space:nowrap;
                            color:#172642;">
                            <b>{count:,}</b>
                            <span style="font-size:13px;color:#8491A5;
                                margin-left:6px;">
                                {pct:.1f}%</span>
                        </span>
                    </div>
                    <div style="height:8px;background:#E5EBF4;
                        border-radius:20px;overflow:hidden;">
                        <div style="height:100%;width:{pct:.2f}%;
                            background:{color};border-radius:20px;"></div>
                    </div>
                </div>
            """)

        st.markdown("".join(breakdown), unsafe_allow_html=True)

def overview_score_card(data):
    df = data[data["score_valid"]].copy()

    scores = pd.to_numeric(df["overall_call_score"], errors="coerce").dropna()
    scores = scores[scores.between(0, 10)]
    average = float(scores.mean()) if len(scores) else 0

    criteria = []
    for column in SCORE_COLUMNS:
        if column not in df.columns or column == "overall_call_score":
            continue

        # values = pd.to_numeric(df[column], errors="coerce")
        # values = values[values.between(0, 10)]

        values = pd.to_numeric(df[column], errors="coerce")
        values = values[values.between(0, 10)]

        if column == "compliance_score":
            values = values[values > 0]
        if not values.empty:
            label = column.replace("_score", "").replace("_", " ").title()
            criteria.append((label, float(values.mean())))

    criteria.sort(key=lambda x: x[1], reverse=True)

    bins = pd.cut(
        scores,
        bins=[-0.01, 5, 6, 7, 8, 10],
        labels=["0–5", "5–6", "6–7", "7–8", "8–10"]
    )
    distribution = bins.value_counts().reindex(
        ["0–5", "5–6", "6–7", "7–8", "8–10"], fill_value=0
    )

    st.markdown("#### Call Score Analysis")
    st.caption("Quality performance across analyzed calls")

    left, right = st.columns([0.85, 1.15], gap="large")

    with left:
        pct = max(0, min(average * 10, 100))

        st.markdown(
            f"""
            <div style="text-align:center;padding:10px 0;">
                <div style="width:205px;height:205px;border-radius:50%;
                    background:conic-gradient(#14B8A6 {pct:.2f}%,
                    #E4EAF3 0);display:flex;align-items:center;
                    justify-content:center;margin:0 auto;">
                    <div style="width:168px;height:168px;border-radius:50%;
                        background:#F5F7FC;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;">
                        <div style="font-size:38px;font-weight:800;color:#172642;">
                            {average:.2f}
                        </div>
                        <div style="font-size:12px;color:#71809B;">out of 10</div>
                    </div>
                </div>
                <div style="font-size:13px;font-weight:650;color:#172642;
                    margin-top:14px;">Average Call Score</div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown("**Score Distribution**")

        total = max(len(scores), 1)
        colors = ["#F59E32", "#F6B65B", "#60A5FA", "#377CF6", "#14B8A6"]

        rows = []
        for (label, count), color in zip(distribution.items(), colors):
            pct = count / total * 100
            rows.append(f"""
                <div style="margin-bottom:17px;">
                    <div style="display:flex;justify-content:space-between;
                        font-size:12px;margin-bottom:7px;">
                        <span style="font-weight:600;color:#344563;">{label}</span>
                        <span style="color:#172642;">
                            <b>{count:,}</b>
                            <span style="color:#8491A5;margin-left:7px;">
                                {pct:.1f}%</span>
                        </span>
                    </div>
                    <div style="height:9px;background:#E5EBF4;
                        border-radius:20px;overflow:hidden;">
                        <div style="height:100%;width:{pct:.2f}%;
                            background:{color};border-radius:20px;"></div>
                    </div>
                </div>
            """)

        st.markdown("".join(rows), unsafe_allow_html=True)

    st.markdown(
        '<div style="border-top:1px solid #E0E7F1;margin:14px 0 20px;"></div>',
        unsafe_allow_html=True
    )

    st.markdown("**Score by Criteria**")

    if not criteria:
        st.info("Criterion scores unavailable")
        return

    cols = st.columns(2, gap="large")
    split = (len(criteria) + 1) // 2

    for col, items in zip(cols, [criteria[:split], criteria[split:]]):
        with col:
            rows = []

            for label, value in items:
                pct = max(0, min(value * 10, 100))
                color = "#14B8A6" if value >= 8 else "#377CF6" if value >= 5 else "#F59E32"

                rows.append(f"""
                    <div style="margin-bottom:18px;">
                        <div style="display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:7px;gap:10px;">
                            <span style="font-size:12px;font-weight:600;
                                color:#344563;">{html.escape(label)}</span>
                            <span style="font-size:12px;font-weight:750;
                                color:#172642;">{value:.2f}
                                <span style="font-weight:400;color:#8491A5;">/10</span>
                            </span>
                        </div>
                        <div style="height:8px;background:#E5EBF4;
                            border-radius:20px;overflow:hidden;">
                            <div style="height:100%;width:{pct:.2f}%;
                                background:{color};border-radius:20px;"></div>
                        </div>
                    </div>
                """)

            st.markdown("".join(rows), unsafe_allow_html=True)

# ============================================================
# 11. PAGE HEADER
# ============================================================

st.title(
    "Sales Call Dashboard"
    if page == "Overview" else page
)

if page == "Customer Timeline":
    st.caption("Complete customer call history across all available dates")
else:
    st.caption(f"{start_date:%d %b %Y} – {end_date:%d %b %Y}")

if data.empty:
    st.info("No calls match the selected filters.")
    st.stop()

analyzed = data[data["valid"]].copy()
scored = data[data["score_valid"]].copy()






def overview_total_calls_kpi(data):
    total = len(data)
    analyzed = int(data["valid"].sum())
    skipped = total - analyzed
    coverage = analyzed / total * 100 if total else 0

    st.markdown(
        f"""
<div style="background:#FFFFFF;border:1px solid #DCE4EF;border-left:4px solid #377CF6;
            border-radius:12px;padding:22px 24px;height:279px;box-sizing:border-box;
            display:flex;align-items:center;justify-content:space-between;gap:10px;">
    <div style="min-width:0;">
        <div style="font-size:21px;font-weight:650;color:#60718D;">Total Calls</div>
        <div style="font-size:52px;font-weight:800;color:#172642;
                    margin-top:12px;line-height:1.1;">{total:,}</div>
    </div>
    <div style="width:240px;max-width:55%;text-align:center;flex-shrink:0;">
        <svg viewBox="0 0 160 92" width="100%" style="display:block;">
            <path d="M 15 76 A 65 65 0 0 1 145 76"
                  fill="none" stroke="#F59E32" stroke-width="12"/>
            <path d="M 15 76 A 65 65 0 0 1 145 76"
                  fill="none" stroke="#377CF6" stroke-width="12"
                  pathLength="100"
                  stroke-dasharray="{coverage:.2f} 100"/>
            <text x="80" y="70" text-anchor="middle"
                  font-size="27" font-weight="800" fill="#172642">{coverage:.2f}%</text>
        </svg>
        <div style="display:flex;justify-content:space-between;gap:8px;
                    font-size:12px;font-weight:650;margin-top:-4px;">
            <span style="color:#377CF6;">● {analyzed:,} Analyzed</span>
            <span style="color:#F59E32;">● {skipped:,} Skipped</span>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )



import html

def premium_leaderboard(df, columns, score_col="Quality"):

    css = """
    <style>
    .premium-table{width:100%;border-collapse:separate;border-spacing:0;font-family:inherit;font-size:14px}
    .premium-table th{background:#EAF0FA;color:#52627B;text-align:left;padding:12px 9px;font-size:12px;font-weight:750;letter-spacing:.4px}
    .premium-table td{padding:12px 9px;border-bottom:1px solid #E8EDF5;color:#263650;font-size:14px}
    .premium-table tbody tr:nth-child(even){background:#F8FAFE}
    .premium-table tbody tr:first-child{background:#EFF5FF}
    .premium-table .rank{color:#71809B;font-weight:700}
    .premium-table .name{font-weight:650;color:#172642}
    .premium-table .num{text-align:right;font-variant-numeric:tabular-nums}
    .premium-table .score{display:inline-block;background:#EAF1FF;color:#2869D9;
        border-radius:6px;padding:5px 9px;font-size:14px;font-weight:750}
    </style>
    """

    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in columns)
    rows = ""

    for _, row in df.iterrows():
        cells = ""
        for col in columns:
            value = row[col]
            # if col == "Rank":
            #     value = "🏆" if int(value) == 1 else str(int(value))
            #     cells += f'<td class="rank">{value}</td>'

            if col == "Rank":
                if str(value) == "Not Eligible":
                    display_value = "Not Eligible"
                else:
                    rank = int(value)
                    display_value = "🏆" if rank == 1 else str(rank)

                cells += f'<td class="rank">{display_value}</td>'
            elif col == score_col:
                cells += f'<td class="num"><span class="score">{float(value):.2f}</span></td>'
            elif col in ("Team Leader", "Agent Name"):
                cells += f'<td class="name">{html.escape(str(value))}</td>'
            elif isinstance(value, (int, float)):
                cells += f'<td class="num">{value:,.0f}</td>'
            else:
                cells += f'<td>{html.escape(str(value))}</td>'
        rows += f"<tr>{cells}</tr>"

    st.markdown(
        css + f'<table class="premium-table"><thead><tr>{head}</tr></thead>'
        f'<tbody>{rows}</tbody></table>',
        unsafe_allow_html=True
    )


def premium_data_table(df):
    view = df.copy()

    css = """
    <style>
    .premium-data-wrap {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #DFE5F0;
        border-radius: 12px;
        background: #FFFFFF;
    }
    .premium-data-table {
        width: 100%;
        border-collapse: collapse;
        font-family: inherit;
        font-size: 12px;
        white-space: nowrap;
    }
    .premium-data-table th {
        background: #EAF0FA;
        color: #52627B;
        padding: 13px 12px;
        text-align: right;
        font-weight: 750;
        border-bottom: 1px solid #DCE4F0;
    }
    .premium-data-table td {
        padding: 13px 12px;
        text-align: right;
        color: #263650;
        border-bottom: 1px solid #E8EDF5;
        font-variant-numeric: tabular-nums;
    }
    .premium-data-table th:first-child,
    .premium-data-table td:first-child {
        text-align: left;
        position: sticky;
        left: 0;
        z-index: 1;
    }
    .premium-data-table th:first-child {
        background: #EAF0FA;
        z-index: 2;
    }
    .premium-data-table tbody tr:nth-child(odd) {
        background: #FFFFFF;
    }
    .premium-data-table tbody tr:nth-child(even) {
        background: #F8FAFE;
    }
    .premium-data-table tbody tr:first-child {
        background: #EFF5FF;
    }
    .premium-data-table tbody tr:hover {
        background: #EAF2FF;
    }
    .premium-data-table tbody td:first-child {
        background: inherit;
        font-weight: 700;
        color: #172642;
    }
    .premium-data-table tbody tr:last-child td {
        border-bottom: none;
    }
    .premium-data-table .score-badge {
        display: inline-block;
        background: #EAF1FF;
        color: #2869D9;
        border-radius: 6px;
        padding: 5px 9px;
        font-weight: 750;
    }
    </style>
    """

    score_columns = {"Avg_Score", "Avg_Compliance"}

    headers = "".join(
        f"<th>{html.escape(str(col))}</th>"
        for col in view.columns
    )

    rows = ""

    for _, row in view.iterrows():
        cells = ""

        for col in view.columns:
            value = row[col]

            if pd.isna(value):
                display = "—"
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                display = f"{value:,.2f}" if col in score_columns else f"{value:,}"
            else:
                display = html.escape(str(value))

            if col in score_columns and pd.notna(value):
                display = f'<span class="score-badge">{display}</span>'

            cells += f"<td>{display}</td>"

        rows += f"<tr>{cells}</tr>"

    st.markdown(
        css
        + '<div class="premium-data-wrap">'
        + '<table class="premium-data-table">'
        + f"<thead><tr>{headers}</tr></thead>"
        + f"<tbody>{rows}</tbody>"
        + "</table></div>",
        unsafe_allow_html=True
    )


def premium_breakdown(labels, values, color=BLUE, total=None, max_items=7):
    import html

    pairs = [(str(k), int(v)) for k, v in zip(labels, values)]
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)[:max_items]

    if not pairs:
        st.info("No data available.")
        return

    denominator = total if total is not None else sum(v for _, v in pairs)
    denominator = max(int(denominator), 1)
    max_value = max(v for _, v in pairs) or 1

    rows = []

    for label, count in pairs:
        pct = count / denominator * 100
        width = count / max_value * 100

        rows.append(f"""
        <div style="margin-bottom:17px;">
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;gap:12px;margin-bottom:7px;">
                <span style="font-size:14px;font-weight:600;color:#344563;
                             line-height:1.4;flex:1;">
                    {html.escape(label)}
                </span>
                <span style="font-size:14px;white-space:nowrap;color:#172642;">
                    <b>{count:,}</b>
                    <span style="font-size:13px;color:#8491A5;margin-left:5px;">
                        {pct:.1f}%</span>
                </span>
            </div>
            <div style="height:8px;background:#E9EEF6;border-radius:20px;
                        overflow:hidden;">
                <div style="height:100%;width:{width:.2f}%;
                            background:{color};border-radius:20px;"></div>
            </div>
        </div>
        """)

    st.markdown("".join(rows), unsafe_allow_html=True)

# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================



if page == "Overview":

    m = calculate_metrics(data)
    analyzed_df = data[data["valid"]].copy()

    total = int(m["Total Calls"])
    skipped = int(m["Skipped Calls"])
    analyzed_count = int(m["Analyzable Calls"])
    sold = int(m["Subscription Sold"])
    followups = int(m["Follow Ups"])
    appointments = int(m["Appointments"])
    mistakes_total = int(m["Total Mistakes"])
    violations = int(m["Compliance Violations"])

    coverage = analyzed_count / total * 100 if total else 0
    conversion = sold / analyzed_count * 100 if analyzed_count else 0



    st.write("")


    # ROW 1 — TOTAL CALLS + 6 KEY INSIGHTS
    left, right = st.columns([1, 1.5], gap="medium")

    with left:
        overview_total_calls_kpi(data)

    with right:
        with st.container(border=True):
            overview_card("Key Insights")

            team_perf = performance_table(data, "team_leader")
            agent_perf = performance_table(data, "agent_name")

            team_perf = team_perf[
                (team_perf["Analyzable_Calls"] >= 10) &
                (team_perf["Avg_Score"].notna()) &
                (team_perf["team_leader"].notna()) &
                (team_perf["team_leader"] != "Unmapped")
            ]

            agent_perf = agent_perf[
                # (agent_perf["Analyzable_Calls"] >= 5) &
                (agent_perf["Scored_Calls"] >= 5) &
                (agent_perf["Avg_Score"].notna()) &
                (agent_perf["agent_name"].notna())
            ]

            top_team = team_perf.sort_values(
                ["Avg_Score", "Analyzable_Calls"],
                ascending=[False, False]
            ).head(1)

            # top_agent = agent_perf.sort_values(
            #     ["Avg_Score", "Analyzable_Calls"],
            #     ascending=[False, False]
            # ).head(1)

            top_agent = agent_perf.sort_values(
                ["Avg_Score", "Scored_Calls"],
                ascending=[False, False]
            ).head(1)

            team_name = str(top_team.iloc[0]["team_leader"]) if not top_team.empty else "N/A"
            team_score = float(top_team.iloc[0]["Avg_Score"]) if not top_team.empty else 0

            agent_name = str(top_agent.iloc[0]["agent_name"]) if not top_agent.empty else "N/A"
            agent_score = float(top_agent.iloc[0]["Avg_Score"]) if not top_agent.empty else 0


            propensity = analyzed_df["propensity_bucket"].fillna("").astype(str).str.strip().str.casefold()
            high_prop = int(propensity.isin(["high", "very high"]).sum())
            high_prop_pct = high_prop / len(analyzed_df) * 100 if len(analyzed_df) else 0


            followup_count = int((analyzed_df["followup"] | analyzed_df["appointment"]).sum())
            followup_pct = followup_count / analyzed_count * 100 if analyzed_count else 0

            mistakes_pct = (
                (analyzed_df["mistake_count"].fillna(0) > 0).sum()
                / analyzed_count * 100
                if analyzed_count else 0
            )




            insights = [
                (BLUE, "On-Call Sales Conversion", f"{conversion:.2f}%",
                 f"{sold:,} subscriptions sold"),

                (GREEN, "High Propensity", f"{high_prop:,}",
                f"{high_prop_pct:.1f}% of analyzed calls",
                "High + Very High propensity"),

                (PURPLE, "Follow-Up Opportunities", f"{followup_count:,}",
                f"{followup_pct:.1f}% of analyzed calls",
                "Follow-Ups + Appointments"),

                (RED, "Sales Mistakes", f"{mistakes_total:,}",
                f"{violations:,} compliance violation{'s' if violations != 1 else ''}"),

                (ORANGE, "Top Quality Team", team_name,
                 f"Score: {team_score:.2f}/10" if not top_team.empty else "No data"),

                (GREEN, "Top Quality Agent", agent_name,
                 f"Score: {agent_score:.2f}/10" if not top_agent.empty else "No data",
                 "Minimum 5 scored calls")
            ]


            insights = [
                    (*item, "") if len(item) == 4 else item
                    for item in insights
                ]


            for start in range(0, 6, 3):
                cols = st.columns(3, gap="small")

                for col, (color, label, value, detail, description) in zip(cols, insights[start:start + 3]):
                    with col:
                        st.markdown(
                            f'<div style="border:1px solid #E3EAF4;'
                            f'border-left:3px solid {color};'
                            f'border-radius:9px;background:#FFFFFF;'
                            f'padding:13px 12px;height:132px;'
                            f'box-sizing:border-box;overflow:hidden;">'
                            f'<div style="font-size:14px;font-weight:600;'
                            f'color:#64748B;line-height:1.2;">'
                            f'{html.escape(label)}</div>'
                            f'<div style="font-size:24px;font-weight:800;'
                            f'color:#172642;margin:9px 0;'
                            f'overflow-wrap:anywhere;line-height:1.15;">'
                            f'{html.escape(str(value))}</div>'
                            f'<div style="font-size:13px;color:#64748B;'
                            f'line-height:1.3;">'
                            f'{html.escape(detail)}</div>'
                            f'<div style="font-size:11px;color:#94A3B8;'
                            f'margin-top:7px;line-height:1.3;">'
                            f'{html.escape(description)}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )


    st.write("")

    # ROW 2 — CALL SCORE ANALYSIS
    st.write("")

    with st.container(border=True):
        overview_score_card(data)

    st.write("")


    # ROW 3 — DISPOSITIONS + NOT INTERESTED REASONS
    left, right = st.columns([1.15, 1], gap="medium")

    with left:
        with st.container(border=True):
            overview_disposition_card(data)



    with right:
        with st.container(border=True):
            overview_card("Not Interested Reasons")

            ni = analyzed_df[analyzed_df["not_interested"]]

            st.caption(
                f"{len(ni):,} Not Interested calls · "
                "Percentages are based on these calls"
            )

            # Fetch all reasons, not just the top 6
            reasons = overview_counts(
                ni,
                "not_interested_reason",
                limit=None
            )

            # Show a fixed number of reasons, scroll for the rest
            with st.container(height=285, border=False):
                premium_breakdown(
                    reasons.index.tolist(),
                    reasons.values.tolist(),
                    color=BLUE,
                    total=len(ni),
                    max_items=len(reasons)
                )





    # ROW 4 — SALES MISTAKES + CUSTOMER PROPENSITY
    left, right = st.columns([1.1, 1], gap="medium")


    with left:
        with st.container(border=True):
            # overview_card("Most Common Sales Mistakes")

            overview_card("Sales Mistakes")

            analyzed_mistakes = analyzed_df.copy()

            # Get all identified mistakes, not only the top 7
            mistakes = overview_mistakes(analyzed_mistakes, limit=None)

            total_mistakes = int(
                analyzed_mistakes["mistake_count"].fillna(0).sum()
            )

            st.caption(
                f"{total_mistakes:,} total sales mistakes · "
                "Percentages are based on all recorded mistakes"
            )

            # Scroll to see every mistake
            with st.container(height=250, border=False):
                premium_breakdown(
                    mistakes.index.tolist(),
                    mistakes.values.tolist(),
                    color=ORANGE,
                    total=total_mistakes,
                    max_items=len(mistakes)
                )


    with right:
        with st.container(border=True):

            overview_card("Customer Propensity")


            prop = overview_counts(analyzed_df, "propensity_bucket", 8)
            total_prop = max(len(analyzed_df), 1)

            propensity_colors = {
                "Low": "#94A3B8",
                "Medium": "#60A5FA",
                "High": "#2563EB",
                "Very High": "#10B981"
            }

            st.markdown(
                f'<div style="text-align:right;font-size:11px;'
                f'color:#71809B;margin-bottom:18px;">'
                f'{len(analyzed_df):,} analyzed calls</div>',
                unsafe_allow_html=True
            )

            for label in ["Low", "Medium", "High", "Very High"]:
                count = int(prop.get(label, 0))
                pct = count / total_prop * 100
                color = propensity_colors[label]

                st.markdown(
                    f"""
                    <div style="margin-bottom:24px;">
                        <div style="display:flex;justify-content:space-between;
                                    align-items:center;margin-bottom:9px;">
                            <span style="font-size:13px;font-weight:600;
                                         color:#253550;">{label}</span>
                            <span style="font-size:13px;color:#172642;">
                                <b>{count:,}</b>
                                <span style="color:#71809B;margin-left:8px;">
                                    {pct:.1f}%</span>
                            </span>
                        </div>
                        <div style="background:#E9EEF6;border-radius:20px;
                                    height:10px;overflow:hidden;">
                            <div style="width:{pct:.2f}%;height:100%;
                                        background:{color};border-radius:20px;">
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )



    st.write("")



    # # ROW 5 — CALLING ACTIVITY (HOURLY TODAY, DAILY OTHERWISE)
    # is_single_day = start_date == end_date

    # with st.container(border=True):
    #     overview_card(
    #         "Hourly Calling Activity" if is_single_day else "Daily Calling Activity"
    #     )

    #     if is_single_day:
    #         hours = data["call_datetime"].dropna().dt.hour
    #         activity = hours.value_counts().sort_index()
    #         activity = activity.reindex(range(9, 22), fill_value=0)

    #         x = [f"{h:02d}:00" for h in activity.index]
    #         y = activity.values

    #     else:
    #         activity = data.groupby("date").size().sort_index()
    #         x = [d.strftime("%d %b") for d in activity.index]
    #         y = activity.values

    #     fig = go.Figure()

    #     fig.add_trace(go.Scatter(
    #         x=x,
    #         y=y,
    #         mode="lines+markers+text",
    #         text=[f"{v:,}" for v in y],
    #         textposition="top center",
    #         textfont=dict(
    #             size=15,
    #             color="#172642",
    #             family="Arial"
    #         ),
    #         line=dict(
    #             color=BLUE,
    #             width=3,
    #             shape="spline",
    #             smoothing=0.4
    #         ),
    #         marker=dict(
    #             size=10,
    #             color=BLUE,
    #             line=dict(color="#FFFFFF", width=2)
    #         ),
    #         fill="tozeroy",
    #         fillcolor="rgba(57,118,239,0.09)",
    #         cliponaxis=False,
    #         hovertemplate="<b>%{x}</b><br>%{y:,} calls<extra></extra>"
    #     ))

    #     max_calls = max(y) if len(y) else 0

    #     fig.update_layout(
    #         height=320,
    #         margin=dict(l=55, r=65, t=65, b=45),
    #         paper_bgcolor="rgba(0,0,0,0)",
    #         plot_bgcolor="rgba(0,0,0,0)",
    #         font=dict(
    #             family="Arial",
    #             size=13,
    #             color="#64748B"
    #         ),
    #         showlegend=False,
    #         hovermode="x unified",
    #         xaxis=dict(
    #             title=None,
    #             type="category",
    #             showgrid=False,
    #             showline=False,
    #             automargin=True
    #         ),
    #         yaxis=dict(
    #             title=None,
    #             range=[0, max_calls * 1.2 if max_calls else 1],
    #             gridcolor="#E8EDF5",
    #             zeroline=False,
    #             tickformat=",",
    #             automargin=True
    #         )
    #     )

    #     # Add breathing room on both ends so labels stay visible
    #     if len(x) > 1:
    #         fig.update_xaxes(range=[-0.35, len(x) - 0.65])
    #     else:
    #         fig.update_xaxes(range=[-0.7, 0.7])

    #     st.plotly_chart(
    #         fig,
    #         use_container_width=True,
    #         config={"displayModeBar": False}
    #     )

    # st.write("")



    is_single_day = start_date == end_date

    with st.container(border=True):
        overview_card(
            "Hourly Calling Activity" if is_single_day else "Daily Calling Activity"
        )

        chart_data = data.dropna(subset=["call_datetime"]).copy()

        if is_single_day:
            chart_data["Period"] = chart_data["call_datetime"].dt.hour

            activity = chart_data.groupby("Period").agg(
                Raw_Calls=("call_key", "size"),
                Analyzed_Calls=("valid", "sum")
            ).reindex(range(9, 22), fill_value=0)

            x = [f"{h:02d}:00" for h in activity.index]

        else:
            activity = chart_data.groupby("date").agg(
                Raw_Calls=("call_key", "size"),
                Analyzed_Calls=("valid", "sum")
            )

            x = [d.strftime("%d %b") for d in activity.index]

        raw_calls = activity["Raw_Calls"].astype(int).tolist()
        analyzed_calls = activity["Analyzed_Calls"].astype(int).tolist()

        fig = go.Figure()

        # RAW CALLS — PREMIUM BLUE BARS
        fig.add_trace(go.Bar(
            x=x,
            y=raw_calls,
            name="Raw Calls",
            marker=dict(
                color="rgba(57, 117, 239, 0.75)",
                line=dict(color="rgba(57, 117, 239, 0.95)", width=1),
                cornerradius=7
            ),
            width=0.48,
            text=[f"{v:,}" if v else "" for v in raw_calls],
            textposition="outside",
            textfont=dict(size=11, color="#475569"),
            cliponaxis=False,
            hovertemplate="<b>Raw Calls</b><br>%{y:,}<extra></extra>"
        ))

        # ANALYZED CALLS — EMERALD LINE
        fig.add_trace(go.Scatter(
            x=x,
            y=analyzed_calls,
            name="Analyzed Calls",
            mode="lines+markers+text",
            line=dict(
                color="#059669",
                width=3.5,
                shape="spline",
                smoothing=0.45
            ),
            marker=dict(
                size=9,
                color="#059669",
                line=dict(color="#FFFFFF", width=2.5)
            ),
            text=[f"{v:,}" if v else "" for v in analyzed_calls],
            textposition="bottom center",
            textfont=dict(size=11, color="#047857"),
            cliponaxis=False,
            hovertemplate="<b>Analyzed Calls</b><br>%{y:,}<extra></extra>"
        ))

        max_calls = max(raw_calls) if raw_calls else 0

        fig.update_layout(
            height=365,
            barmode="overlay",
            bargap=0.40,
            margin=dict(l=45, r=25, t=65, b=45),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                size=12,
                color="#64748B"
            ),

            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                bordercolor="#E2E8F0",
                font=dict(size=12, color="#17243D")
            ),

            legend=dict(
                orientation="h",
                x=0,
                y=1.15,
                font=dict(size=12, color="#334155"),
                bgcolor="rgba(0,0,0,0)",
                itemsizing="constant"
            ),

            xaxis=dict(
                title=None,
                type="category",
                showgrid=False,
                showline=False,
                zeroline=False,
                tickfont=dict(size=11, color="#64748B")
            ),

            yaxis=dict(
                title=None,
                range=[0, max_calls * 1.22 if max_calls else 1],
                gridcolor="#E9EEF5",
                griddash="dot",
                gridwidth=1,
                zeroline=False,
                tickformat=",",
                tickfont=dict(size=11, color="#94A3B8"),
                nticks=5
            ),

            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            }
        )



    # ROW 6 — TEAM PERFORMANCE + TOP AGENTS
    st.write("")

    left, right = st.columns(2, gap="medium")

    with left:
        with st.container(border=True):
            overview_card("Team Quality Performance")

            team = performance_table(data, "team_leader")
            team = team[
                (team["team_leader"] != "Unmapped") &
                team["Avg_Score"].notna()
            ].copy()

            team = team.sort_values(
                ["Avg_Score", "Analyzable_Calls"],
                ascending=[False, False]
            ).reset_index(drop=True)

            team.insert(0, "Rank", range(1, len(team) + 1))

            team_view = team[
                ["Rank", "team_leader", "Raw_Calls",
                 "Analyzable_Calls", "Sold", "Avg_Score"]
            ].rename(columns={
                "team_leader": "Team Leader",
                "Raw_Calls": "Raw Calls",
                "Analyzable_Calls": "Analyzed",
                "Sold": "Sales",
                "Avg_Score": "Quality Score"
            })

            premium_leaderboard(
                team_view.rename(columns={"Quality Score": "Quality"}),
                ["Rank", "Team Leader", "Raw Calls", "Analyzed", "Sales", "Quality"]
            )

    with right:
        with st.container(border=True):
            overview_card("Agent Quality Leaderboard")

            # agents = performance_table(data, "agent_name")
            # agents = agents[
            #     (agents["Analyzable_Calls"] >= 0) &
            #     agents["Avg_Score"].notna()
            # ].copy()

            # agents = agents.sort_values(
            #     ["Avg_Score", "Analyzable_Calls"],
            #     ascending=[False, False]
            # ).reset_index(drop=True)

            # agents.insert(0, "Rank", range(1, len(agents) + 1))

            # agent_view = agents[
            #     ["Rank", "agent_name", "Raw_Calls", "Analyzable_Calls", "Avg_Score"]
            # ].rename(columns={
            #     "agent_name": "Agent Name",
            #     "Analyzable_Calls": "Analyzed",
            #     "Raw_Calls": "Raw Calls",
            #     "Avg_Score": "Quality Score"
            # })


            # with st.container(height=387, border=False):
            #     premium_leaderboard(
            #         agent_view.rename(columns={"Quality Score": "Quality"}),
            #         ["Rank", "Agent Name", "Raw Calls", "Analyzed", "Quality"]
            #     )






            # overview_card("Top Quality Agents")

            agents = performance_table(data, "agent_name").copy()

            # Priority: minimum 5 scored calls
            agents["ranking_priority"] = (
                agents["Scored_Calls"] >= 5
            ).astype(int)

            # Eligible agents first, sorted by quality.
            # Others remain visible below.
            agents = agents.sort_values(
                by=[
                    "ranking_priority",
                    "Avg_Score",
                    "Scored_Calls"
                ],
                ascending=[False, False, False],
                na_position="last"
            ).reset_index(drop=True)

            # Recalculate rank AFTER sorting
            agents["Rank"] = range(1, len(agents) + 1)

            agent_view = agents[
                [
                    "Rank",
                    "agent_name",
                    "Raw_Calls",
                    "Analyzable_Calls",
                    "Scored_Calls",
                    "Avg_Score"
                ]
            ].rename(columns={
                "agent_name": "Agent Name",
                "Raw_Calls": "Raw Calls",
                "Analyzable_Calls": "Analyzed Calls",
                "Scored_Calls": "Scored Calls",
                "Avg_Score": "Quality"
            })

            with st.container(height=387, border=False):
                premium_leaderboard(
                    agent_view,
                    [
                        "Rank",
                        "Agent Name",
                        "Raw Calls",
                        "Analyzed Calls",
                        "Scored Calls",
                        "Quality"
                    ]
                )



#Team performance

elif page == "Team Performance":

    teams = performance_table(data, "team_leader")

        # Team KPIs
    mapped_teams = teams[teams["team_leader"] != "Unmapped"].copy()

    eligible_teams = mapped_teams[
        mapped_teams["Analyzable_Calls"] >= 10
    ].copy()

    top_team = eligible_teams.sort_values(
        ["Conversion_%", "Sold"],
        ascending=[False, False]
    ).iloc[0]["team_leader"] if not eligible_teams.empty else "—"

    m = calculate_metrics(data)

    st.markdown("### Team Performance Summary")

    kpis({
        "Total Calls": m["Total Calls"],
        "Total Teams": len(mapped_teams),
        "On-Call Subscription Sold": m["Subscription Sold"],
        "On-Call Conversion %": m["Conversion %"],
        "Avg Quality Score": m["Avg Overall Score"],
        "Compliance Violations": m["Compliance Violations"],
        "Highest Call Conversion Team": top_team
    }, 7)

    st.write("")


    # ============================================================
    # TEAM COMPARISON
    # ============================================================

    # ============================================================
    # TEAM COMPARISON
    # ============================================================

    st.markdown("### Team Comparison")

    left, right = st.columns(2, gap="medium")

    # TOTAL CALLS BY TEAM
    with left:
        with st.container(border=True):
            st.markdown("**Total Calls by Team**")
            st.caption("Total calls, analyzable calls and analysis rate")

            volume = teams.sort_values("Raw_Calls", ascending=True).copy()

            volume["Analysis_Pct"] = (
                volume["Analyzable_Calls"]
                .div(volume["Raw_Calls"].replace(0, float("nan")))
                .mul(100)
                .fillna(0)
            )

            volume["Label"] = volume.apply(
                lambda row: (
                    f'{int(row["Raw_Calls"]):,} total · '
                    f'{int(row["Analyzable_Calls"]):,} analyzed '
                    f'({row["Analysis_Pct"]:.1f}%)'
                ),
                axis=1
            )

            fig = px.bar(
                volume,
                x="Raw_Calls",
                y="team_leader",
                orientation="h",
                color_discrete_sequence=[BLUE],
                custom_data=["Label"]
            )

            fig.update_traces(
                hovertemplate="%{y}<br>%{customdata[0]}<extra></extra>"
            )

            # Labels positioned in a fixed right-side column
            max_calls = max(float(volume["Raw_Calls"].max()), 1)

            for _, row in volume.iterrows():
                fig.add_annotation(
                    x=max_calls * 1.03,
                    y=row["team_leader"],
                    text=row["Label"],
                    showarrow=False,
                    xanchor="left",
                    font=dict(size=10, color=NAVY),
                    align="left"
                )

            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=15, b=20),
                xaxis=dict(
                    visible=False,
                    range=[0, max_calls * 2.15]
                ),
                yaxis=dict(title=None, showgrid=False),
                showlegend=False,
                bargap=0.30,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    # TEAM CALL OUTCOME BREAKDOWN
    with right:
        with st.container(border=True):
            st.markdown("**Team Call Outcome Breakdown**")
            st.caption("Number of calls by outcome and team")

            outcome_cols = [
                "Sold",
                "Follow_Ups",
                "Appointments",
                "Not_Interested"
            ]

            outcome_df = teams[
                ["team_leader"] + outcome_cols
            ].melt(
                id_vars="team_leader",
                value_vars=outcome_cols,
                var_name="Outcome",
                value_name="Calls"
            )

            outcome_df["Outcome"] = outcome_df["Outcome"].replace({
                "Sold": "Subscription Sold",
                "Follow_Ups": "Follow Up",
                "Appointments": "Appointment Fixed",
                "Not_Interested": "Not Interested"
            })

            outcome_totals = (
                outcome_df.groupby("team_leader", as_index=False)["Calls"]
                .sum()
            )

            fig = px.bar(
                outcome_df,
                x="team_leader",
                y="Calls",
                color="Outcome",
                barmode="stack",
                color_discrete_map={
                    "Subscription Sold": GREEN,
                    "Follow Up": BLUE,
                    "Appointment Fixed": ORANGE,
                    "Not Interested": RED
                },
                category_orders={
                    "Outcome": [
                        "Subscription Sold",
                        "Follow Up",
                        "Appointment Fixed",
                        "Not Interested"
                    ],
                    "team_leader": teams["team_leader"].tolist()
                }
            )

            fig.update_traces(
                hovertemplate=(
                    "%{x}<br>"
                    "%{fullData.name}: %{y} calls"
                    "<extra></extra>"
                )
            )

            for _, row in outcome_totals.iterrows():
                fig.add_annotation(
                    x=row["team_leader"],
                    y=row["Calls"],
                    text=f'<b>{int(row["Calls"]):,}</b>',
                    showarrow=False,
                    yshift=12,
                    font=dict(size=11, color=NAVY)
                )

            max_outcomes = outcome_totals["Calls"].max()

            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=20, b=80),
                xaxis=dict(
                    title=None,
                    tickangle=-20,
                    showgrid=False
                ),
                yaxis=dict(
                    title=None,
                    gridcolor="#EDF2F8",
                    range=[0, max(1, max_outcomes * 1.20)]
                ),
                legend=dict(
                    orientation="h",
                    y=-0.40,
                    x=0,
                    title=None,
                    font=dict(size=10)
                ),
                showlegend=True,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    # ============================================================
    # TEAM RANKINGS
    # ============================================================

    st.markdown("### Team Rankings")

    ranked = mapped_teams.sort_values(
        "Avg_Score", ascending=True
    ).copy()

    conversion = mapped_teams.sort_values(
        "Conversion_%", ascending=True
    ).copy()

    left, right = st.columns(2, gap="medium")

    # TEAM QUALITY RANKING
    with left:
        with st.container(border=True):
            st.markdown("**Team Quality Ranking**")
            st.caption("Average call quality score out of 10")

            fig = px.bar(
                ranked,
                x="Avg_Score",
                y="team_leader",
                orientation="h",
                text="Avg_Score",
                color_discrete_sequence=[PURPLE]
            )

            fig.update_traces(
                texttemplate="%{x:.2f}",
                textposition="outside",
                textfont=dict(size=12, color=NAVY),
                cliponaxis=False
            )

            fig.update_layout(
                height=340,
                margin=dict(l=10, r=20, t=15, b=20),
                xaxis=dict(
                    visible=False,
                    range=[0, 10]
                ),
                yaxis=dict(title=None, showgrid=False),
                showlegend=False,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    # TEAM CONVERSION COMPARISON
    with right:
        with st.container(border=True):
            st.markdown("**Team Conversion Comparison**")
            st.caption("On-call subscriptions sold and conversion rate")

            conversion["Label"] = conversion.apply(
                lambda row: (
                    f'{int(row["Sold"]):,} sold '
                    f'({row["Conversion_%"]:.2f}%)'
                ),
                axis=1
            )

            fig = px.bar(
                conversion,
                x="Conversion_%",
                y="team_leader",
                orientation="h",
                color_discrete_sequence=[GREEN],
                custom_data=["Label"]
            )

            fig.update_traces(
                hovertemplate="%{y}<br>%{customdata[0]}<extra></extra>"
            )

            max_conversion = pd.to_numeric(
                conversion["Conversion_%"], errors="coerce"
            ).max()

            max_conversion = (
                float(max_conversion)
                if pd.notna(max_conversion) and max_conversion > 0
                else 1
            )

            # Fixed right-side labels
            for _, row in conversion.iterrows():
                fig.add_annotation(
                    x=max_conversion * 1.03,
                    y=row["team_leader"],
                    text=row["Label"],
                    showarrow=False,
                    xanchor="left",
                    font=dict(size=11, color=NAVY)
                )

            fig.update_layout(
                height=340,
                margin=dict(l=10, r=10, t=15, b=20),
                xaxis=dict(
                    visible=False,
                    range=[0, max_conversion * 1.90]
                ),
                yaxis=dict(title=None, showgrid=False),
                showlegend=False,
                bargap=0.30,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    premium_data_table(teams)

    st.divider()

    selected_team = st.selectbox(
        "Select Team Leader",
        sorted(data["team_leader"].unique())
    )

    team_df = data[data["team_leader"] == selected_team]
    tm = calculate_metrics(team_df)

    kpis({
        "Total Calls": tm["Total Calls"],
        "Analyzable Calls": tm["Analyzable Calls"],
        "Subscription Sold": tm["Subscription Sold"],
        "Follow Ups": tm["Follow Ups"],
        "Appointments": tm["Appointments"],
        "Conversion %": tm["Conversion %"]
    }, 6)

    st.markdown("### Agent Breakdown")

    premium_data_table(
        performance_table(team_df, "agent_name")
    )


# ============================================================
# PAGE 4 — AGENT PERFORMANCE
# ============================================================
elif page == "Agent Performance":

    selected_agent = st.selectbox(
        "Select Agent",
        ["All Agents"] + sorted(data["agent_name"].dropna().unique().tolist())
    )

    agent_df = (
        data.copy()
        if selected_agent == "All Agents"
        else data[data["agent_name"] == selected_agent].copy()
    )

    agent_analyzed = agent_df[agent_df["valid"]]
    agent_scored = agent_df[agent_df["score_valid"]]

    m = calculate_metrics(agent_df)

    kpis({
        "Raw Calls": len(agent_df),
        "Analyzable Calls": len(agent_analyzed),
        "Skipped Calls": len(agent_df) - len(agent_analyzed),
        "On-Call Subscription Sold": m["Subscription Sold"],
        "On-Call Conversion %": m["Conversion %"],
        "Avg Score": m["Avg Overall Score"]
    }, 6)

    st.write("")

    kpis({
        "Total Mistakes": m["Total Mistakes"],
        "Avg Mistake / Call": (
            fmt(agent_analyzed["mistake_count"].fillna(0).sum() / len(agent_analyzed))
            if len(agent_analyzed) else "—"
        ),
        "Compliance Violations": m["Compliance Violations"],
        "Avg Propensity": m["Avg Propensity"]
    }, 4)

    st.write("")

    left, right = st.columns([1.2, 1])

    with left:
        score_chart(agent_scored, "Selected Agent Score Snapshot")

    with right:
        outcome_chart(agent_analyzed, "Selected Agent Outcome Mix")

    with st.expander("Agent Coaching Panel", expanded=True):

        left, right = st.columns(2)

        with left:
            insight_table(agent_analyzed, "mistakes", "Common Mistakes")

        with right:
            insight_table(agent_analyzed, "improvements", "Common Improvements")
    # st.markdown("### 🏆 Agent Performance Leaderboard")

    # leaderboard = performance_table(data, "agent_name").copy()

    # # Minimum sample size for fair ranking
    # # leaderboard = leaderboard[leaderboard["Analyzable_Calls"] >= 30].copy()

    # # Rank by conversion, then sales, then quality
    # leaderboard = leaderboard.sort_values(
    #     ["Conversion_%", "Sold", "Avg_Score"],
    #     ascending=[False, False, False]
    # ).reset_index(drop=True)

    # leaderboard.insert(0, "Rank", leaderboard.index + 1)

    # leaderboard = leaderboard[[
    #     "Rank",
    #     "agent_name",
    #     "Analyzable_Calls",
    #     "Sold",
    #     "Conversion_%",
    #     "Avg_Score",
    #     "Avg_Compliance"
    # ]]

    # leaderboard.columns = [
    #     "Rank",
    #     "Agent",
    #     "Calls",
    #     "Sales",
    #     "Conversion %",
    #     "Quality Score",
    #     "Compliance"
    # ]

    # st.dataframe(
    #     leaderboard,
    #     use_container_width=True,
    #     hide_index=True,
    #     height=420,
    #     column_config={
    #         "Rank": st.column_config.NumberColumn("🏆 Rank", format="%d"),
    #         "Conversion %": st.column_config.ProgressColumn(
    #             "Conversion %",
    #             min_value=0,
    #             max_value=100,
    #             format="%.2f%%"
    #         ),
    #         "Quality Score": st.column_config.NumberColumn(
    #             "Quality Score", format="%.2f"
    #         ),
    #         "Compliance": st.column_config.NumberColumn(
    #             "Compliance", format="%.2f"
    #         )
    #     }
    # )

    st.markdown("### Agent Call Records")

    agent_raw = raw[
        raw["_source_row_id"].isin(agent_df["_source_row_id"])
    ].copy()

    agent_raw = agent_raw.drop(
        columns=["_source_row_id", "source_sheet"],
        errors="ignore"
    )

    st.dataframe(
        agent_raw,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.download_button(
        "⬇ Download Agent Call Data",
        data=agent_raw.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{selected_agent.replace(' ', '_')}_calls.csv",
        mime="text/csv"
    )


# # ============================================================
# # PAGE 5 — AI COACHING & INSIGHTS
# # ============================================================

# elif page == "AI Coaching & Insights":

#     selected_agent = st.selectbox(
#         "Agent",
#         ["All Agents"] + sorted(data["agent_name"].unique())
#     )

#     coaching = (
#         analyzed
#         if selected_agent == "All Agents"
#         else analyzed[analyzed["agent_name"] == selected_agent]
#     )

#     coaching_scored = coaching[coaching["score_valid"]]

#     kpis({
#         "Analyzable Calls": len(coaching),
#         "Avg Score": fmt(avg(coaching_scored, "overall_call_score")),
#         "Avg Compliance": fmt(avg(coaching_scored, "compliance_score")),
#         "Total Mistakes": int(coaching["mistake_count"].fillna(0).sum()),
#         "Violations": int(coaching["violation"].sum())
#     }, 5)

#     st.write("")

#     tab1, tab2, tab3, tab4 = st.tabs([
#         "Mistakes",
#         "Improvements",
#         "Compliance",
#         "Next Actions"
#     ])

#     with tab1:
#         insight_table(coaching, "mistakes", "Common Mistakes")

#     with tab2:
#         insight_table(coaching, "improvements", "Common Improvements")

#     with tab3:
#         insight_table(coaching, "violations", "Compliance Issues")

#     with tab4:
#         insight_table(coaching, "next_best_action", "Next Best Actions")

#     if not coaching.empty:

#         records = coaching.sort_values(
#             "call_datetime",
#             ascending=False
#         )

#         selected_call = st.selectbox(
#             "Inspect Call",
#             records.index.tolist(),
#             format_func=lambda i: (
#                 f"{records.loc[i, 'agent_name']} | "
#                 f"{records.loc[i, 'customer_number']} | "
#                 f"{records.loc[i, 'call_datetime']}"
#             )
#         )

#         record = records.loc[selected_call]

#         left, right = st.columns(2)

#         with left:
#             show_field("Mistakes", record["mistakes"])
#             show_field("Improvements", record["improvements"])

#         with right:
#             show_field(
#                 "What Agent Should Have Done",
#                 record["what_agent_should_have_done"]
#             )
#             show_field("Next Best Action", record["next_best_action"])

# ============================================================
# CUSTOMER TIMELINE
# ============================================================

elif page == "Customer Timeline":

    st.markdown("### Find Customer")

    col1, col2 = st.columns([1, 2])

    with col1:
        timeline_agents = st.multiselect(
            "Agent (Optional)",
            options=sorted(all_data["agent_name"].dropna().unique()),
            placeholder="All Agents"
        )

    # Filter customers based on selected agents
    customer_options_df = all_data.copy()

    if timeline_agents:
        customer_options_df = customer_options_df[
            customer_options_df["agent_name"].isin(timeline_agents)
        ]

    customer_numbers = sorted(
        customer_options_df["customer_number"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda x: x.ne("") & x.ne("nan")]
        .unique()
    )

    with col2:
        customer_number = st.selectbox(
            "Customer Number",
            options=customer_numbers,
            index=None,
            placeholder="Search customer number...",
            key="timeline_customer"
        )

    if not customer_number:
        st.info("Enter a customer number in the sidebar to view their call history.")

    else:
        customer_calls = all_data[
            all_data["customer_number"].astype(str).str.strip() == customer_number
        ].copy()

        if timeline_agents:
            customer_calls = customer_calls[
                customer_calls["agent_name"].isin(timeline_agents)
            ].copy()

        customer_calls = customer_calls.sort_values("call_datetime")

        if customer_calls.empty:
            st.warning("No calls found for this customer.")

        else:
            latest_call = customer_calls.iloc[-1]

            latest_date = latest_call["call_datetime"]
            days_since_last_call = (
                (pd.Timestamp.now() - latest_date).days
                if pd.notna(latest_date) else None
            )

            def display_value(value):
                if value is None or pd.isna(value) or str(value).strip().lower() in ["", "nan", "none"]:
                    return "—"
                return str(value)

            kpis({
                "Total Calls": len(customer_calls),
                "Agents Contacted": customer_calls["agent_name"].nunique(),
                "Latest Outcome": display_value(latest_call.get("call_outcome")),
                "Interest Level": display_value(latest_call.get("customer_interest_level")),
                "Latest Propensity": display_value(latest_call.get("propensity_score")),
                "Days Since Last Call": (
                    days_since_last_call if days_since_last_call is not None else "—"
                )
            }, 6)

            st.markdown("### Customer Call Timeline")

            for _, call in customer_calls.sort_values(
                "call_datetime", ascending=False
            ).iterrows():

                call_date = call["call_datetime"]
                date_label = (
                    call_date.strftime("%d %b %Y, %I:%M %p")
                    if pd.notna(call_date) else "Date unavailable"
                )

                def detail(column):
                    value = call.get(column)
                    if value is None or pd.isna(value) if not isinstance(value, (list, dict)) else False:
                        return "—"
                    return str(value).strip() or "—"

                agent = detail("agent_name")
                outcome = detail("call_outcome")

                with st.expander(f"📞 {date_label} | {agent} | {outcome}"):

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.write("**Call Outcome:**", outcome)
                        st.write("**Call Disposition:**", detail("call_disposition"))

                    with c2:
                        st.write("**Overall Score:**", detail("overall_call_score"))
                        st.write("**Propensity:**", detail("propensity_score"))

                    with c3:
                        st.write("**Interest Level:**", detail("customer_interest_level"))
                        st.write("**Propensity Bucket:**", detail("propensity_bucket"))

                    st.divider()

                    st.markdown("#### Customer Insights")

                    st.write("**Customer Type:**", detail("customer_type"))
                    st.write("**Interest Evidence:**", detail("interest_evidence"))
                    st.write("**Not Interested Reason:**", detail("not_interested_reason"))
                    st.write("**Reason Summary:**", detail("not_interested_reason_summary"))

                    st.markdown("#### Agent Coaching")

                    st.write(
                        "**What Agent Should Have Done:**",
                        detail("what_agent_should_have_done")
                    )

                    st.write(
                        "**Mistakes:**",
                        detail("mistakes")
                    )

                    st.write(
                        "**Improvements:**",
                        detail("improvements")
                    )

                    st.markdown("#### Next Steps")

                    st.info(
                        f"**Next Best Action:** {detail('next_best_action')}"
                    )

                    st.write(
                        "**Plan Pitched:**",
                        detail("plan_pitched")
                    )

                    st.write(
                        "**Price Discussed:**",
                        detail("price_discussed")
                    )

            st.markdown("### Complete Call History")

            timeline_columns = [
                "call_datetime",
                "agent_name",
                "call_outcome",
                "call_disposition",
                "customer_interest_level",
                "overall_call_score",
                "propensity_score",
                "propensity_bucket",
                "not_interested_reason",
                "what_agent_should_have_done",
                "next_best_action"
            ]

            timeline_columns = [
                col for col in timeline_columns if col in customer_calls.columns
            ]

            st.dataframe(
                customer_calls[timeline_columns].sort_values(
                    "call_datetime", ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# PAGE 6 — CUSTOMER INTELLIGENCE
# ============================================================

elif page == "Customer Intelligence":

    # st.title("Customer Intelligence")

    # Use already filtered dashboard data
    customer_df = data.copy()

    available_columns = [
        col for col in CUSTOMER_INTELLIGENCE_COLUMNS
        if col in customer_df.columns
    ]

    customer_df = customer_df[available_columns].copy()

    # ==============================
    # CUSTOMER KPIs
    # ==============================

    st.markdown("### Customer Overview")

    unique_customers = (
        customer_df["customer_number"].replace("", pd.NA).nunique()
        if "customer_number" in customer_df.columns else 0
    )

    interest = customer_df.get(
        "customer_interest_level",
        pd.Series("", index=customer_df.index)
    ).fillna("").astype(str).str.strip().str.lower()

    propensity = customer_df.get(
        "propensity_bucket",
        pd.Series("", index=customer_df.index)
    ).fillna("").astype(str).str.strip().str.lower()

    not_interested = customer_df[
        customer_df["call_outcome"].fillna("").astype(str).str.strip().str.lower()
        == "not interested"
    ]

    not_interested_customers = not_interested["customer_number"].replace("", pd.NA).nunique()

    high_interest = interest.isin(["high", "interested"]).sum()
    high_propensity = propensity.isin(["high", "very high"]).sum()
    plans_pitched = (~not_interested.isin(["", "[]", "nan", "none", "null"])).sum()

    kpis({
        "Unique Customers": unique_customers,
        "High Interest": high_interest,
        "High Propensity": high_propensity,
        "Not Interested Customers": not_interested_customers
    }, 4)


    # ==============================
    # CUSTOMER DISTRIBUTION
    # ==============================


    st.markdown("### Customer Analysis")
    st.caption(
        "Customer interest and conversion propensity across "
        "calls with available classifications"
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        category_chart(
            customer_df,
            "customer_interest_level",
            "Customer Interest Distribution"
        )

    with col2:
        category_chart(
            customer_df,
            "propensity_bucket",
            "Customer Propensity Distribution"
        )


    # ==============================
    # CUSTOMER INTELLIGENCE TABLE
    # ==============================

    st.markdown("### Customer Intelligence Records")

    st.caption(f"{len(customer_df):,} records")

    st.dataframe(
        customer_df,
        use_container_width=True,
        hide_index=True,
        height=550
    )

    # ==============================
    # DOWNLOAD
    # ==============================

    st.download_button(
        "⬇ Download Customer Intelligence",
        data=customer_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="customer_intelligence.csv",
        mime="text/csv"
    )

# ============================================================
# 12. EXPORT
# ============================================================

st.divider()

# Export original Google Sheets rows matching the sidebar filters
no_filters = (
    page == "Customer Timeline"
    or (
        start_date == min_date
        and end_date == max_date
        and not leaders
        and not agents
        and not outcomes
    )
)

if no_filters:
    export_df = raw.copy()
else:
    export_df = raw[raw["_source_row_id"].isin(data["_source_row_id"])].copy()

export_df = export_df.drop(columns=["_source_row_id"])

# st.download_button(
#     "⬇ Export Filtered Calls",
#     data=export_df.to_csv(index=False).encode("utf-8-sig"),
#     file_name="liquide_filtered_calls.csv",
#     mime="text/csv"
# )
