import streamlit as st
import pandas as pd
import plotly.express as px
import gspread

from google.oauth2.service_account import Credentials


# ============================================================
# CONFIG
# ============================================================

SHEET_ID = (
    "1bpyB0aXUiUGA0j5OwiEXMtifLnvE1dU-nKHR7COgxcY"
)

SHEET_NAME = (
    "September 2026"
)


st.set_page_config(
    page_title="Sales Call Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# GOOGLE CREDENTIALS
# ============================================================

# Keep your existing GCP_CREDS variable here.
# Example:
#
# import os
# import json
# GCP_CREDS = json.loads(os.getenv("GCP_CREDS"))

GCP_CREDS = dict(st.secrets["gcp_service_account"])

# ============================================================
# CUSTOMER INTELLIGENCE COLUMNS
# ============================================================

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

    "propensity_bucket",

    # "total_call_duration"

]


# ============================================================
# SCORE COLUMNS
# ============================================================

NUMERIC_SCORE_COLUMNS = [

    "overall_call_score",

    "sales_effectiveness_score",

    "communication_clarity_score",

    "call_structure_score",

    "customer_engagement_score",

    "needs_identification_score",

    "solution_relevance_score",

    "professionalism_score",

    "compliance_score"

]


# ============================================================
# GOOGLE SHEET CONNECTION
# ============================================================

@st.cache_data(ttl=300)
def load_data():

    credentials = (
        Credentials.from_service_account_info(
            GCP_CREDS,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets"
            ]
        )
    )

    client = gspread.authorize(
        credentials
    )

    spreadsheet = client.open_by_key(
        SHEET_ID
    )

    worksheet = spreadsheet.worksheet(
        SHEET_NAME
    )

    # --------------------------------------------------------
    # READ SHEET
    # --------------------------------------------------------

    values = worksheet.get_all_values()

    if not values:

        return pd.DataFrame()

    headers = [
        str(header).strip()
        for header in values[0]
    ]

    rows = values[1:]

    # --------------------------------------------------------
    # MAKE ROW LENGTH MATCH HEADER LENGTH
    # --------------------------------------------------------

    cleaned_rows = []

    for row in rows:

        row = list(row)

        if len(row) < len(headers):

            row.extend(
                [""] * (
                    len(headers) - len(row)
                )
            )

        elif len(row) > len(headers):

            row = row[
                :len(headers)
            ]

        cleaned_rows.append(
            row
        )

    df = pd.DataFrame(
        cleaned_rows,
        columns=headers
    )

    # ========================================================
    # REMOVE DUPLICATE COLUMN HEADERS
    # ========================================================

    if df.columns.duplicated().any():

        duplicate_columns = (
            df.columns[
                df.columns.duplicated()
            ]
            .tolist()
        )

        print(
            "Duplicate columns found:",
            duplicate_columns
        )

        # Keep the first occurrence
        df = df.loc[
            :,
            ~df.columns.duplicated(
                keep="first"
            )
        ]

    return df


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# NORMALIZE AGENT NAMES
# ============================================================

AGENT_NAME_MAP = {
    "Abhishek_Ziraya": "Abhishek Ziraya",
    "Aditi_Verma": "Aditi Verma",
    "Adithya": "LV Adithya",
    "Ayush_Ziraya": "Ayush Singh",
    "Bandana": "Bandana Kumari Nagar",
    "Chandra_Ziraya": "Chandra Bhushan",
    'Chytanya':'Chytanya Netalkar',
    "Debangi": "Debangi Majumder",
    "Divya":"Divya Rashmi",
    "Garv_Ziraya": "Garv Tandan",
    'Garvit': 'Garvit Jat',
    "Goresh_Ziraya": "Goresh Sharma",
    "Iftekhar": "Iftekhar Alam",
    "Jaya": "Jaya Prajapat",
    "Jinson":"Jinson",
    "Jiya": "Jiya Pandey",
    "Krishna": "Krishna Kumar",
    "Nameet": "Nameet Karadi",
    "Namratha": "Namratha Chauhan",
    "Omkar": "Omkar Kaktikar",
    "Pawan_Ziraya": "Pawan Chahar",
    "Pradeep": "Pradeep Bhandari",
    "Pravesh": "Pravesh Singh",
    "Preeti": "Preeti Tahilramani",
    "Priya_Ziraya": "Priya Khanna",
    "Priyanshi": "Priyanshi Kamal Das",
    "Priyap": "Priyadharshini P",
    "Rahaman": "Khan Rahaman",
    'Rajeev':'Rajeev Ranjan',
    "Rakshith": "Rakshith Pai",
    "Rishabh": "Rishabh Singh",
    "Rishabh_Ziraya": "Rishabh Kushwah",
    "Rishi": "Rishi Sarkar",
    "Ritik": "Ritik Raje",
    "Sabiha": "Shaik Sabiha",
    "Sagar_Ziraya": "Sagar Kumar",
    "Saif_Ziraya": "Saif Khan",
    "Shahbaz": "Shahbaz Mansoori",
    "Shaik_Aleem": "Shaik Aleem",
    'Simran':'Simran',
    "Shreya_H": "Shreya Hari",
    "Sweta":"Sweta Raj",
    "Soumyajeet": "Soumyajeet Behera",
    "Sourav": "Sourav Chowdhury",
    "Sukanya_Kokate": "Sukanya Kokate",
    "Supriya": "Supriya Raj",
    "Umar": "Mohammad Umar Ali",
    "Umar_Farooq": "Umar Farooq",
    "Vanita_Hiremath": "Vanita Hiremath",
    "Veervart_Karnwal": "Veervart Karnwal",
    "Vibhanshu": "Vibhanshu Mishra",
    "Vinay_Vyas": "Vinay Vyas",
    "Vishal": "Vishal Gautam",
    "Vishals": "Vishal Singh",
    "Zain": "Zain Real",
}


if "agent_name" in df.columns:

    df["agent_name"] = (
        df["agent_name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace(AGENT_NAME_MAP)
    )


if df.empty:

    st.warning(
        "No data available in the Google Sheet."
    )

    st.stop()

# ============================================================
# DATA CLEANING
# ============================================================

# ------------------------------------------------------------
# ENSURE REQUIRED COLUMNS EXIST
# ------------------------------------------------------------

required_columns = [

    "call_id",
    "agent_name",
    "call_datetime",
    "analysis_status",
    "call_outcome",
    "customer_interest_level",
    "overall_call_score"

]

for column in required_columns:

    if column not in df.columns:

        df[column] = ""


# ------------------------------------------------------------
# CALL DATETIME
# ------------------------------------------------------------

df["call_datetime"] = pd.to_datetime(
    df["call_datetime"],
    errors="coerce"
)


# ------------------------------------------------------------
# NUMERIC SCORE COLUMNS
# ------------------------------------------------------------

for column in NUMERIC_SCORE_COLUMNS:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# PROPENSITY SCORE
# ------------------------------------------------------------

if "propensity_score" in df.columns:

    df["propensity_score"] = pd.to_numeric(
        df["propensity_score"],
        errors="coerce"
    )


# ============================================================
# DERIVED DATE COLUMNS
# ============================================================

df["day_name"] = (
    df["call_datetime"]
    .dt.day_name()
)

df["date"] = (
    df["call_datetime"]
    .dt.date
)

df["month"] = (
    df["call_datetime"]
    .dt.strftime(
        "%B %Y"
    )
)

df["hour"] = (
    df["call_datetime"]
    .dt.hour
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 Sales Call Analytics Dashboard"
)

# st.caption(
#     "AI-powered call quality and sales performance analytics"
# )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Filters"
)


filtered_df = df.copy()


# ============================================================
# DATE FILTER
# ============================================================

valid_dates = (
    df["date"]
    .dropna()
)

if not valid_dates.empty:

    min_date = valid_dates.min()
    max_date = valid_dates.max()

    selected_dates = st.sidebar.date_input(
        "Call Date",
        [
            min_date,
            max_date
        ]
    )

    if (
        isinstance(
            selected_dates,
            (list, tuple)
        )
        and len(selected_dates) == 2
    ):

        filtered_df = filtered_df[
            (
                filtered_df["date"]
                >= selected_dates[0]
            )
            &
            (
                filtered_df["date"]
                <= selected_dates[1]
            )
        ]


# ============================================================
# AGENT FILTER
# ============================================================

agent_values = sorted(
    [
        value
        for value in
        df["agent_name"]
        .dropna()
        .astype(str)
        .unique()
        if value.strip()
    ]
)


agents = st.sidebar.multiselect(
    "Agent",
    agent_values
)


if agents:

    filtered_df = filtered_df[
        filtered_df["agent_name"]
        .isin(agents)
    ]


# ============================================================
# OUTCOME FILTER
# ============================================================

outcome_values = sorted(
    [
        value
        for value in
        df["call_outcome"]
        .dropna()
        .astype(str)
        .unique()
        if value.strip()
    ]
)


outcomes = st.sidebar.multiselect(
    "Call Outcome",
    outcome_values
)


if outcomes:

    filtered_df = filtered_df[
        filtered_df["call_outcome"]
        .isin(outcomes)
    ]


# ============================================================
# CUSTOMER INTEREST FILTER
# ============================================================

interest_values = sorted(
    [
        value
        for value in
        df["customer_interest_level"]
        .dropna()
        .astype(str)
        .unique()
        if value.strip()
    ]
)


interest = st.sidebar.multiselect(
    "Customer Interest",
    interest_values
)


if interest:

    filtered_df = filtered_df[
        filtered_df[
            "customer_interest_level"
        ].isin(
            interest
        )
    ]

# ============================================================
# PROPENSITY FILTER
# ============================================================

propensity_values = sorted(
    [
        value
        for value in
        df["propensity_bucket"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        if value.strip()
        and value.lower() not in [
            "nan",
            "none",
            "null",
            "unknown"
        ]
    ]
)


propensity = st.sidebar.multiselect(
    "Customer Propensity",
    propensity_values
)


if propensity:

    filtered_df = filtered_df[
        filtered_df[
            "propensity_bucket"
        ]
        .astype(str)
        .str.strip()
        .isin(propensity)
    ]

#Customer number filter

customer_numbers = sorted(
    [
        value
        for value in
        df["customer_number"]
        .dropna()
        .astype(str)
        .unique()
        if value.strip()
    ]
)

customer_number = st.sidebar.multiselect(
    "Customer Number",
    customer_numbers
)

if customer_number:

    filtered_df = filtered_df[
        filtered_df[
            "customer_number"
        ].isin(customer_number)
    ]

# ============================================================
# CUSTOMER INTELLIGENCE SIDEBAR
# ============================================================

# st.sidebar.markdown("---")

# st.sidebar.subheader(
#     "🧠 Customer Intelligence"
# )

# show_customer_intelligence = st.sidebar.checkbox(
#     "Open Customer Intelligence"
# )


# ============================================================
# VALID SCORE DATA
# ============================================================
#
# IMPORTANT:
#
# Skipped calls remain inside filtered_df.
#
# They are removed ONLY from score calculations.
#
# We also remove:
#
# - overall_call_score == 0
# - missing overall_call_score
# - skipped analysis
#
# ============================================================

analysed_df = filtered_df.copy()

analysed_df = analysed_df[
    ~analysed_df["analysis_status"]
    .astype(str)
    .str.upper()
    .isin([
        "SKIPPED_SHORT_AUDIO",
        "EMPTY_TRANSCRIPT"
    ])
]

score_df = filtered_df.copy()


if "analysis_status" in score_df.columns:

    score_df = score_df[
        score_df[
            "analysis_status"
        ]
        .astype(str)
        .str.upper()
        .ne(
            "SKIPPED_SHORT_AUDIO"
        )
    ]


# Remove zero scores

score_df = score_df[
    score_df[
        "overall_call_score"
    ].notna()
]


score_df = score_df[
    score_df[
        "overall_call_score"
    ] > 0
]


# ============================================================
# KPI SECTION
# ============================================================

st.subheader(
    "Overview"
)


c1, c2, c3, c4, c5 = st.columns(5)


# ------------------------------------------------------------
# ANALYZED CALLS
# ------------------------------------------------------------

with c1:

    st.metric(
        "Analysed Calls",
        len(analysed_df)
    )


# ------------------------------------------------------------
# AVG CALL SCORE
# ------------------------------------------------------------

with c2:

    avg_call_score = (
        score_df[
            "overall_call_score"
        ].mean()
        if not score_df.empty
        else 0
    )

    st.metric(
        "Avg Call Score",
        f"{avg_call_score:.2f}"
    )


# ------------------------------------------------------------
# AVG SALES SCORE
# ------------------------------------------------------------

with c3:

    avg_sales_score = (
        score_df[
            "sales_effectiveness_score"
        ].mean()
        if (
            not score_df.empty
            and
            "sales_effectiveness_score"
            in score_df.columns
        )
        else 0
    )

    st.metric(
        "Avg Sales Score",
        f"{avg_sales_score:.2f}"
    )


# ------------------------------------------------------------
# INTERESTED CALLS
# ------------------------------------------------------------

with c4:

    interested = filtered_df[
        filtered_df[
            "customer_interest_level"
        ]
        .astype(str)
        .str.lower()
        .isin(
            [
                "high",
                "interested"
            ]
        )
    ]

    st.metric(
        "Interested Calls",
        len(interested)
    )


# ------------------------------------------------------------
# AVG COMPLIANCE
# ------------------------------------------------------------

with c5:

    if (
        not score_df.empty
        and
        "compliance_score"
        in score_df.columns
    ):

        avg_compliance = (
            score_df[
                "compliance_score"
            ].mean()
        )

    else:

        avg_compliance = 0

    st.metric(
        "Avg Compliance",
        f"{avg_compliance:.2f}"
    )


# ============================================================
# DATA QUALITY SUMMARY
# ============================================================

# st.subheader(
#     "📋 Call Coverage"
# )


# q1, q2, q3, q4 = st.columns(4)


# with q1:

#     st.metric(
#         "Total Calls",
#         len(filtered_df)
#     )


# with q2:

#     skipped_count = len(
#         filtered_df[
#             filtered_df[
#                 "analysis_status"
#             ]
#             .astype(str)
#             .str.upper()
#             .eq(
#                 "SKIPPED_SHORT_AUDIO"
#             )
#         ]
#     )

#     st.metric(
#         "Short Audio",
#         skipped_count
#     )


# with q3:

#     empty_count = len(
#         filtered_df[
#             filtered_df[
#                 "analysis_status"
#             ]
#             .astype(str)
#             .str.upper()
#             .eq(
#                 "EMPTY_TRANSCRIPT"
#             )
#         ]
#     )

#     st.metric(
#         "Empty Transcript",
#         empty_count
#     )


# with q4:

#     analyzed_count = len(
#         score_df
#     )

#     st.metric(
#         "Valid Analyses",
#         analyzed_count
#     )

st.markdown("---")

st.subheader(
    "Propensity"
)


q1, q2, q3, q4 = st.columns(4)


with q1:
    Very_high = len(
        filtered_df[
            filtered_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "very high"
                ]
            )
        ]
    )

    st.metric(
        "Very High",
        Very_high
    )

with q2:
    High = len(
        filtered_df[
            filtered_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "high"
                ]
            )
        ]
    )

    st.metric(
        "High",
        High
    )


with q3:
    Medium = len(
        filtered_df[
            filtered_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "medium"
                ]
            )
        ]
    )

    st.metric(
        "Medium",
        Medium
    )

with q4:
    Low = len(
        filtered_df[
            filtered_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "low"
                ]
            )
        ]
    )
    st.metric(
        "Low",
        Low
    )


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================


st.markdown("---")

st.subheader(
    "Customer Intelligence"
)

# --------------------------------------------------------
# AVAILABLE COLUMNS ONLY
# --------------------------------------------------------

available_ci_columns = [
    column
    for column in
    CUSTOMER_INTELLIGENCE_COLUMNS
    if column in filtered_df.columns
]

customer_df = filtered_df[
    available_ci_columns
].copy()


# --------------------------------------------------------
# CUSTOMER KPIs
# --------------------------------------------------------

ci1, ci2, ci3, ci4 = st.columns(4)


with ci1:

    if "customer_number" in customer_df.columns:

        customer_count = (
            customer_df[
                "customer_number"
            ]
            .replace(
                "",
                pd.NA
            )
            .dropna()
            .nunique()
        )

    else:

        customer_count = 0

    st.metric(
        "Unique Customers",
        customer_count
    )


with ci2:

    if "customer_interest_level" in customer_df.columns:

        high_interest = customer_df[
            customer_df[
                "customer_interest_level"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "high",
                    "interested"
                ]
            )
        ]

        high_interest_count = len(
            high_interest
        )

    else:

        high_interest_count = 0

    st.metric(
        "High Interest",
        high_interest_count
    )


with ci3:

    if "propensity_bucket" in customer_df.columns:

        high_propensity = customer_df[
            customer_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "high",
                    "very high"
                ]
            )
        ]

        high_propensity_count = len(
            high_propensity
        )

    else:

        high_propensity_count = 0

    st.metric(
        "High Propensity",
        high_propensity_count
    )


with ci4:

    if "plan_pitched" in customer_df.columns:

        plans_pitched = customer_df[
            "plan_pitched"
        ].astype(str)

        plans_pitched_count = (
            plans_pitched
            .replace(
                [
                    "",
                    "[]",
                    "nan",
                    "None"
                ],
                pd.NA
            )
            .dropna()
            .shape[0]
        )

    else:

        plans_pitched_count = 0

    st.metric(
        "Plans Pitched",
        plans_pitched_count
    )


# --------------------------------------------------------
# CUSTOMER INTEREST DISTRIBUTION
# --------------------------------------------------------

ci_col1, ci_col2 = st.columns(2)


with ci_col1:

    if (
        "customer_interest_level"
        in customer_df.columns
    ):

        interest_data = (
            customer_df[
                "customer_interest_level"
            ]
            .astype(str)
            .replace(
                [
                    "",
                    "nan",
                    "None",
                    "Unknown",
                    "unknown"
                ],
                pd.NA
            )
            .dropna()
            .value_counts()
            .reset_index()
        )

        interest_data.columns = [
            "Interest",
            "Count"
        ]

        fig = px.pie(
            interest_data,
            names="Interest",
            values="Count",
            title="Customer Interest"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with ci_col2:

    if (
        "propensity_bucket"
        in customer_df.columns
    ):

        propensity_data = (
            customer_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.strip()
        )

        propensity_data = propensity_data[
            ~propensity_data.str.lower().isin(
                [
                    "",
                    "nan",
                    "none",
                    "null",
                    "unknown"
                ]
            )
        ]

        propensity_data = (
            propensity_data
            .value_counts()
            .reset_index()
        )

        propensity_data.columns = [
            "Propensity",
            "Count"
        ]

        fig = px.bar(
            propensity_data,
            x="Propensity",
            y="Count",
            title="Customer Propensity"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------------
# CUSTOMER INTELLIGENCE TABLE
# --------------------------------------------------------

st.subheader(
    "Customer Intelligence Records"
)

st.dataframe(
    customer_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ============================================================
# AGENT PERFORMANCE
# ============================================================

st.subheader(
    "👥 Agent Performance"
)


if not score_df.empty:

    agent_perf = (

        score_df

        .groupby(
            "agent_name"
        )

        .agg(

            Calls=(
                "call_id",
                "count"
            ),

            Avg_Score=(
                "overall_call_score",
                "mean"
            ),

            Sales_Score=(
                "sales_effectiveness_score",
                "mean"
            )

        )

        .reset_index()

    )


    agent_perf = agent_perf.sort_values(
        "Avg_Score",
        ascending=False
    )


    agent_perf[
        "Avg_Score"
    ] = agent_perf[
        "Avg_Score"
    ].round(2)


    agent_perf[
        "Sales_Score"
    ] = agent_perf[
        "Sales_Score"
    ].round(2)


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            agent_perf,
            x="agent_name",
            y="Avg_Score",
            title="Agent Ranking"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        st.dataframe(
            agent_perf,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info(
        "No valid analysed calls available for agent scoring."
    )

st.markdown("---")

# ============================================================
# DAILY CALL TREND
# ============================================================

st.subheader(
    "📅 Daily Call Trend"
)


daily = (

    filtered_df

    .dropna(
        subset=["date"]
    )

    .groupby(
        "date"
    )

    .size()

    .reset_index(
        name="Calls"
    )

)


if not daily.empty:

    fig = px.line(
        daily,
        x="date",
        y="Calls",
        markers=True,
        title="Calls Per Day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ============================================================
# CALL OUTCOME
# ============================================================

st.subheader(
    "📞 Call Outcome Analysis"
)


col1, col2 = st.columns(2)


with col1:

    outcome = (
        filtered_df[
            "call_outcome"
        ]
        .astype(str)
        .str.strip()
    )

    outcome = outcome[
        ~outcome.str.lower().isin(
            [
                "",
                "nan",
                "none",
                "null",
                "unknown"
            ]
        )
    ]

    outcome = (
        outcome
        .value_counts()
        .reset_index()
    )

    outcome.columns = [
        "Outcome",
        "Count"
    ]


    if not outcome.empty:

        fig = px.pie(
            outcome,
            names="Outcome",
            values="Count",
            title="Call Outcomes"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with col2:

    if (
        "not_interested_reason"
        in filtered_df.columns
    ):

        reason = (
            filtered_df[
                "not_interested_reason"
            ]
            .astype(str)
            .str.strip()
        )

        reason = reason[
            ~reason.str.lower().isin(
                [
                    "",
                    "nan",
                    "none",
                    "null",
                    "unknown"
                ]
            )
        ]

        reason = (
            reason
            .value_counts()
            .head(10)
            .reset_index()
        )

        reason.columns = [
            "Reason",
            "Count"
        ]

        if not reason.empty:

            fig = px.bar(
                reason,
                x="Count",
                y="Reason",
                orientation="h",
                title="Top Not-Interested Reasons"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# SCORE BREAKDOWN
# ============================================================

st.markdown("---")

st.subheader(
    "Quality Score Breakdown"
)


if not score_df.empty:

    available_score_columns = [
        column
        for column in NUMERIC_SCORE_COLUMNS
        if column in score_df.columns
    ]


    score_breakdown_df = (

        score_df[
            available_score_columns
        ]

        .mean()

        .reset_index()

    )


    score_breakdown_df.columns = [
        "Metric",
        "Score"
    ]


    score_breakdown_df[
        "Score"
    ] = score_breakdown_df[
        "Score"
    ].round(2)


    fig = px.bar(
        score_breakdown_df,
        x="Metric",
        y="Score",
        title="Average Quality Scores"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No valid score data available."
    )


# ============================================================
# AI COACHING / INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "🤖 Insights"
)


tab1, tab2, tab3 = st.tabs(
    [
        "Mistakes",
        "Improvements",
        "Score Reasons"
    ]
)


# ============================================================
# PREPARE AGENT INSIGHTS
# ============================================================

def prepare_agent_insights(
    dataframe,
    insight_column
):

    if (
        "agent_name" not in dataframe.columns
        or insight_column not in dataframe.columns
    ):

        return {}


    temp = dataframe[
        [
            "agent_name",
            insight_column
        ]
    ].copy()


    # --------------------------------------------------------
    # CLEAN AGENT NAME
    # --------------------------------------------------------

    temp["agent_name"] = (
        temp["agent_name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # CLEAN INSIGHTS
    # --------------------------------------------------------

    temp[insight_column] = (
        temp[insight_column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # Remove empty rows
    temp = temp[
        (temp["agent_name"] != "")
        &
        (temp[insight_column] != "")
        &
        (~temp[insight_column].str.lower().isin(
            [
                "nan",
                "none",
                "null"
            ]
        ))
    ]


    if temp.empty:

        return {}


    # --------------------------------------------------------
    # CREATE DICTIONARY
    # --------------------------------------------------------

    agent_insights = {}


    for _, row in temp.iterrows():

        agent = row["agent_name"]

        raw_text = row[insight_column]


        # ----------------------------------------------------
        # SPLIT GEMINI INSIGHTS
        # ----------------------------------------------------

        insights = raw_text.split("|")


        for insight in insights:

            insight = insight.strip()


            # Remove existing bullet characters
            insight = (
                insight
                .lstrip("•")
                .strip()
            )


            if not insight:
                continue


            if insight.lower() in [
                "nan",
                "none",
                "null"
            ]:
                continue


            if agent not in agent_insights:

                agent_insights[agent] = []


            # ------------------------------------------------
            # REMOVE DUPLICATES
            # ------------------------------------------------

            if insight not in agent_insights[agent]:

                agent_insights[agent].append(
                    insight
                )


    return agent_insights


# ============================================================
# DISPLAY FUNCTION
# ============================================================

def display_agent_insights(
    dataframe,
    insight_column
):

    agent_insights = prepare_agent_insights(
        dataframe,
        insight_column
    )

    if not agent_insights:

        st.info(
            "No insights available."
        )

        return


    # ========================================================
    # AGENT SELECTOR
    # ========================================================

    agents = sorted(
        agent_insights.keys()
    )


    selected_agent = st.selectbox(
        "Select Agent",
        agents,
        key=f"agent_{insight_column}"
    )


    # ========================================================
    # DISPLAY SELECTED AGENT
    # ========================================================

    insights = agent_insights[
        selected_agent
    ]


    with st.container(
        border=True
    ):

        st.markdown(
            f"### {selected_agent}"
        )


        for insight in insights:

            st.markdown(
                f"- {insight}"
            )

# ============================================================
# MISTAKES
# ============================================================

with tab1:

    display_agent_insights(
        filtered_df,
        "mistakes"
    )


# ============================================================
# IMPROVEMENTS
# ============================================================

with tab2:

    display_agent_insights(
        filtered_df,
        "improvements"
    )


# ============================================================
# SCORE REASONS
# ============================================================

with tab3:

    display_agent_insights(
        filtered_df,
        "overall_call_score_reason"
    )

# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

st.subheader(
    "⬇️ Export"
)


csv = filtered_df.to_csv(
    index=False
)


st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_calls.csv",
    "text/csv"
)


# ============================================================
# RAW DATA
# ============================================================

with st.expander(
    "View Complete Data"
):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )