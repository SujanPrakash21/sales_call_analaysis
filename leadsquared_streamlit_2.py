# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import gspread

# from google.oauth2.service_account import Credentials


# # ============================================================
# # CONFIG
# # ============================================================

# SHEET_ID = (
#     "1bpyB0aXUiUGA0j5OwiEXMtifLnvE1dU-nKHR7COgxcY"
# )

# SHEET_NAME = (
#     "September 2026"
# )


# st.set_page_config(
#     page_title="Sales Call Analytics",
#     page_icon="📊",
#     layout="wide"
# )


# # ============================================================
# # GOOGLE CREDENTIALS
# # ============================================================

# # Keep your existing GCP_CREDS variable here.
# # Example:
# #
# # import os
# # import json
# # GCP_CREDS = json.loads(os.getenv("GCP_CREDS"))

# GCP_CREDS = dict(st.secrets["gcp_service_account"])

# # ============================================================
# # CUSTOMER INTELLIGENCE COLUMNS
# # ============================================================

# CUSTOMER_INTELLIGENCE_COLUMNS = [

#     "call_id",

#     "agent_name",

#     "customer_number",

#     "call_datetime",

#     "analysis_status",

#     "call_disposition",

#     "call_outcome",

#     "customer_type",

#     "plan_pitched",

#     "price_discussed",

#     "not_interested_reason",

#     "not_interested_reason_summary",

#     "customer_interest_level",

#     "interest_evidence",

#     "overall_call_score",

#     "propensity_score",

#     "propensity_bucket",

#     # "total_call_duration"

# ]


# # ============================================================
# # SCORE COLUMNS
# # ============================================================

# NUMERIC_SCORE_COLUMNS = [

#     "overall_call_score",

#     "sales_effectiveness_score",

#     "communication_clarity_score",

#     "call_structure_score",

#     "customer_engagement_score",

#     "needs_identification_score",

#     "solution_relevance_score",

#     "professionalism_score",

#     "compliance_score"

# ]


# # ============================================================
# # GOOGLE SHEET CONNECTION
# # ============================================================

# @st.cache_data(ttl=300)
# def load_data():

#     credentials = (
#         Credentials.from_service_account_info(
#             GCP_CREDS,
#             scopes=[
#                 "https://www.googleapis.com/auth/spreadsheets"
#             ]
#         )
#     )

#     client = gspread.authorize(
#         credentials
#     )

#     spreadsheet = client.open_by_key(
#         SHEET_ID
#     )

#     worksheet = spreadsheet.worksheet(
#         SHEET_NAME
#     )

#     # --------------------------------------------------------
#     # READ SHEET
#     # --------------------------------------------------------

#     values = worksheet.get_all_values()

#     if not values:

#         return pd.DataFrame()

#     headers = [
#         str(header).strip()
#         for header in values[0]
#     ]

#     rows = values[1:]

#     # --------------------------------------------------------
#     # MAKE ROW LENGTH MATCH HEADER LENGTH
#     # --------------------------------------------------------

#     cleaned_rows = []

#     for row in rows:

#         row = list(row)

#         if len(row) < len(headers):

#             row.extend(
#                 [""] * (
#                     len(headers) - len(row)
#                 )
#             )

#         elif len(row) > len(headers):

#             row = row[
#                 :len(headers)
#             ]

#         cleaned_rows.append(
#             row
#         )

#     df = pd.DataFrame(
#         cleaned_rows,
#         columns=headers
#     )

#     # ========================================================
#     # REMOVE DUPLICATE COLUMN HEADERS
#     # ========================================================

#     if df.columns.duplicated().any():

#         duplicate_columns = (
#             df.columns[
#                 df.columns.duplicated()
#             ]
#             .tolist()
#         )

#         print(
#             "Duplicate columns found:",
#             duplicate_columns
#         )

#         # Keep the first occurrence
#         df = df.loc[
#             :,
#             ~df.columns.duplicated(
#                 keep="first"
#             )
#         ]

#     return df


# # ============================================================
# # LOAD DATA
# # ============================================================

# df = load_data()


# # ============================================================
# # NORMALIZE AGENT NAMES
# # ============================================================

# # AGENT_NAME_MAP = {
# #     "Abhishek_Ziraya": "Abhishek Ziraya",
# #     "Aditi_Verma": "Aditi Verma",
# #     "Adithya": "LV Adithya",
# #     "Ayush_Ziraya": "Ayush Singh",
# #     "Bandana": "Bandana Kumari Nagar",
# #     "Chandra_Ziraya": "Chandra Bhushan",
# #     'Chytanya':'Chytanya Netalkar',
# #     "Debangi": "Debangi Majumder",
# #     "Divya":"Divya Rashmi",
# #     "Garv_Ziraya": "Garv Tandan",
# #     'Garvit': 'Garvit Jat',
# #     "Goresh_Ziraya": "Goresh Sharma",
# #     "Iftekhar": "Iftekhar Alam",
# #     "Jaya": "Jaya Prajapat",
# #     "Jinson":"Jinson",
# #     "Jiya": "Jiya Pandey",
# #     "Krishna": "Krishna Kumar",
# #     "Nameet": "Nameet Karadi",
# #     "Namratha": "Namratha Chauhan",
# #     "Omkar": "Omkar Kaktikar",
# #     "Pawan_Ziraya": "Pawan Chahar",
# #     "Pradeep": "Pradeep Bhandari",
# #     "Pravesh": "Pravesh Singh",
# #     "Preeti": "Preeti Tahilramani",
# #     "Priya_Ziraya": "Priya Khanna",
# #     "Priyanshi": "Priyanshi Kamal Das",
# #     "Priyap": "Priyadharshini P",
# #     "Rahaman": "Khan Rahaman",
# #     'Rajeev':'Rajeev Ranjan',
# #     "Rakshith": "Rakshith Pai",
# #     "Rishabh": "Rishabh Singh",
# #     "Rishabh_Ziraya": "Rishabh Kushwah",
# #     "Rishi": "Rishi Sarkar",
# #     "Ritik": "Ritik Raje",
# #     "Sabiha": "Shaik Sabiha",
# #     "Sagar_Ziraya": "Sagar Kumar",
# #     "Saif_Ziraya": "Saif Khan",
# #     "Shahbaz": "Shahbaz Mansoori",
# #     "Shaik_Aleem": "Shaik Aleem",
# #     'Simran':'Simran',
# #     "Shreya_H": "Shreya Hari",
# #     "Sweta":"Sweta Raj",
# #     "Soumyajeet": "Soumyajeet Behera",
# #     "Sourav": "Sourav Chowdhury",
# #     "Sukanya_Kokate": "Sukanya Kokate",
# #     "Supriya": "Supriya Raj",
# #     "Umar": "Mohammad Umar Ali",
# #     "Umar_Farooq": "Umar Farooq",
# #     "Vanita_Hiremath": "Vanita Hiremath",
# #     "Veervart_Karnwal": "Veervart Karnwal",
# #     "Vibhanshu": "Vibhanshu Mishra",
# #     "Vinay_Vyas": "Vinay Vyas",
# #     "Vishal": "Vishal Gautam",
# #     "Vishals": "Vishal Singh",
# #     "Zain": "Zain Real",
# # }

# AGENT_NAME_MAP = {

#     "Abhishek": "Abhishek Ziraya",

#     "Abhishek_Ziraya": "Abhishek Ziraya",

#     "Aditi": "Aditi Verma",
#     "Aditi_Verma": "Aditi Verma",

#     "Adithya": "LV Adithya",

#     "Akash_Harkude": "Akash Harkude",

#     "Ayush": "Ayush Singh",
#     "Ayush_Ziraya": "Ayush Singh",

#     "Bandana": "Bandana Kumari Nagar",

#     "Chandra": "Chandra Bhushan",
#     "Chandra_Ziraya": "Chandra Bhushan",

#     "Chytanya": "Chytanya Netalkar",

#     "Debangi": "Debangi Majumder",

#     "Divya": "Divya Rashmi",

#     "Garv": "Garv Tandan",
#     "Garv_Ziraya": "Garv Tandan",

#     "Garvit": "Garvit Jat",

#     "Goresh": "Goresh Sharma",
#     "Goresh_Ziraya": "Goresh Sharma",

#     "Iftekhar": "Iftekhar Alam",

#     "Imdad": "Imdad P",
#     "Imdad_P": "Imdad P",

#     "Izaz_Ahmed": "Izaz Ahmed",
#     "Izaz": "Izaz Ahmed",

#     "Jaya": "Jaya Prajapat",

#     "Jinson": "Jinson",

#     "Jiya": "Jiya Pandey",

#     "Krishna": "Krishna Kumar",

#     "Nameet": "Nameet Karadi",

#     "Namratha": "Namratha Chauhan",

#     "Akash": "Akash Harkude",
#     "Akash_Harkude": "Akash Harkude",

#     "Ayan": "Ayan Dey",
#     "Ayan_Dey": "Ayan Dey",

#     "Manan": "Manan Shah",
#     "Manan_Shah": "Manan Shah",

#     "Mayank": "Mayank Biswas",
#     "Mayank_Biswas": "Mayank Biswas",

#     "Omkar": "Omkar Kaktikar",

#     "Pawan": "Pawan Chahar",
#     "Pawan_Ziraya": "Pawan Chahar",

#     "Pradeep": "Pradeep Bhandari",

#     "Pravesh": "Pravesh Singh",

#     "Preeti": "Preeti Tahilramani",

#     "Priya": "Priya Khanna",
#     "Priya_Ziraya": "Priya Khanna",

#     "Priyanshi": "Priyanshi Kamal Das",

#     "Priyap": "Priyadharshini P",

#     "Rahaman": "Khan Rahaman",

#     "Rajeev": "Rajeev Ranjan",

#     "Rakshith": "Rakshith Pai",

#     "Rishabh": "Rishabh Singh",

#     "Rishabh_Ziraya": "Rishabh Kushwah",

#     "Rishi": "Rishi Sarkar",

#     "Ritik": "Ritik Raje",

#     "Sabiha": "Shaik Sabiha",

#     "Sagar": "Sagar Kumar",
#     "Sagar_Ziraya": "Sagar Kumar",

#     "Saif": "Saif Khan",
#     "Saif_Ziraya": "Saif Khan",

#     "Shahbaz": "Shahbaz Mansoori",

#     "Shaik":"Shaik Aleem",
#     "Shaik_Aleem": "Shaik Aleem",

#     "Sibajit": "Sibajit Gope",
#     "Sibajit_Gope": "Sibajit Gope",

#     "Simran": "Simran",

#     "Shreya": "Shreya Hari",
#     "Shreya_H": "Shreya Hari",

#     "Soumyajeet": "Soumyajeet Behera",

#     "Sourav": "Sourav Chowdhury",

#     "Sweta":"Sweta Raj",
#     "Sweta_Raj": "Sweta Raj",

#     "Sukanya": "Sukanya Kokate",
#     "Sukanya_Kokate": "Sukanya Kokate",

#     "Supriya": "Supriya Raj",

#     "Umar": "Mohammad Umar Ali",

#     "Umar_Farooq": "Umar Farooq",

#     "Vanita": "Vanita Hiremath",
#     "Vanita_Hiremath": "Vanita Hiremath",

#     "Veervart": "Veervart Karnwal",
#     "Veervart_Karnwal": "Veervart Karnwal",

#     "Vibhanshu": "Vibhanshu Mishra",

#     "Vinay": "Vinay Vyas",
#     "Vinay_Vyas": "Vinay Vyas",

#     "Vishal": "Vishal Gautam",

#     "Vishals": "Vishal Singh",

#     "Zain": "Zain Real",
# }


# if "agent_name" in df.columns:

#     df["agent_name"] = (
#         df["agent_name"]
#         .fillna("")
#         .astype(str)
#         .str.strip()
#         .replace(AGENT_NAME_MAP)
#     )


# if df.empty:

#     st.warning(
#         "No data available in the Google Sheet."
#     )

#     st.stop()

# # ============================================================
# # DATA CLEANING
# # ============================================================

# # ------------------------------------------------------------
# # ENSURE REQUIRED COLUMNS EXIST
# # ------------------------------------------------------------

# required_columns = [

#     "call_id",
#     "agent_name",
#     "call_datetime",
#     "analysis_status",
#     "call_outcome",
#     "customer_interest_level",
#     "overall_call_score"

# ]

# for column in required_columns:

#     if column not in df.columns:

#         df[column] = ""


# # ------------------------------------------------------------
# # CALL DATETIME
# # ------------------------------------------------------------

# df["call_datetime"] = pd.to_datetime(
#     df["call_datetime"],
#     errors="coerce"
# )


# # ------------------------------------------------------------
# # NUMERIC SCORE COLUMNS
# # ------------------------------------------------------------

# for column in NUMERIC_SCORE_COLUMNS:

#     if column in df.columns:

#         df[column] = pd.to_numeric(
#             df[column],
#             errors="coerce"
#         )


# # ------------------------------------------------------------
# # PROPENSITY SCORE
# # ------------------------------------------------------------

# if "propensity_score" in df.columns:

#     df["propensity_score"] = pd.to_numeric(
#         df["propensity_score"],
#         errors="coerce"
#     )


# # ============================================================
# # DERIVED DATE COLUMNS
# # ============================================================

# df["day_name"] = (
#     df["call_datetime"]
#     .dt.day_name()
# )

# df["date"] = (
#     df["call_datetime"]
#     .dt.date
# )

# df["month"] = (
#     df["call_datetime"]
#     .dt.strftime(
#         "%B %Y"
#     )
# )

# df["hour"] = (
#     df["call_datetime"]
#     .dt.hour
# )


# # ============================================================
# # TITLE
# # ============================================================

# st.title(
#     "📊 Sales Call Analytics Dashboard"
# )

# # st.caption(
# #     "AI-powered call quality and sales performance analytics"
# # )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.header(
#     "Filters"
# )


# filtered_df = df.copy()


# # ============================================================
# # DATE FILTER
# # ============================================================

# valid_dates = (
#     df["date"]
#     .dropna()
# )

# if not valid_dates.empty:

#     min_date = valid_dates.min()
#     max_date = valid_dates.max()

#     selected_dates = st.sidebar.date_input(
#         "Call Date",
#         [
#             min_date,
#             max_date
#         ]
#     )

#     if (
#         isinstance(
#             selected_dates,
#             (list, tuple)
#         )
#         and len(selected_dates) == 2
#     ):

#         filtered_df = filtered_df[
#             (
#                 filtered_df["date"]
#                 >= selected_dates[0]
#             )
#             &
#             (
#                 filtered_df["date"]
#                 <= selected_dates[1]
#             )
#         ]


# # ============================================================
# # AGENT FILTER
# # ============================================================

# agent_values = sorted(
#     [
#         value
#         for value in
#         df["agent_name"]
#         .dropna()
#         .astype(str)
#         .unique()
#         if value.strip()
#     ]
# )


# agents = st.sidebar.multiselect(
#     "Agent",
#     agent_values
# )


# if agents:

#     filtered_df = filtered_df[
#         filtered_df["agent_name"]
#         .isin(agents)
#     ]


# # ============================================================
# # OUTCOME FILTER
# # ============================================================

# outcome_values = sorted(
#     [
#         value
#         for value in
#         df["call_outcome"]
#         .dropna()
#         .astype(str)
#         .unique()
#         if value.strip()
#     ]
# )


# outcomes = st.sidebar.multiselect(
#     "Call Outcome",
#     outcome_values
# )


# if outcomes:

#     filtered_df = filtered_df[
#         filtered_df["call_outcome"]
#         .isin(outcomes)
#     ]


# # ============================================================
# # CUSTOMER INTEREST FILTER
# # ============================================================

# interest_values = sorted(
#     [
#         value
#         for value in
#         df["customer_interest_level"]
#         .dropna()
#         .astype(str)
#         .unique()
#         if value.strip()
#     ]
# )


# interest = st.sidebar.multiselect(
#     "Customer Interest",
#     interest_values
# )


# if interest:

#     filtered_df = filtered_df[
#         filtered_df[
#             "customer_interest_level"
#         ].isin(
#             interest
#         )
#     ]

# # ============================================================
# # PROPENSITY FILTER
# # ============================================================

# propensity_values = sorted(
#     [
#         value
#         for value in
#         df["propensity_bucket"]
#         .dropna()
#         .astype(str)
#         .str.strip()
#         .unique()
#         if value.strip()
#         and value.lower() not in [
#             "nan",
#             "none",
#             "null",
#             "unknown"
#         ]
#     ]
# )


# propensity = st.sidebar.multiselect(
#     "Customer Propensity",
#     propensity_values
# )


# if propensity:

#     filtered_df = filtered_df[
#         filtered_df[
#             "propensity_bucket"
#         ]
#         .astype(str)
#         .str.strip()
#         .isin(propensity)
#     ]

# #Customer number filter

# customer_numbers = sorted(
#     [
#         value
#         for value in
#         df["customer_number"]
#         .dropna()
#         .astype(str)
#         .unique()
#         if value.strip()
#     ]
# )

# customer_number = st.sidebar.multiselect(
#     "Customer Number",
#     customer_numbers
# )

# if customer_number:

#     filtered_df = filtered_df[
#         filtered_df[
#             "customer_number"
#         ].isin(customer_number)
#     ]

# # ============================================================
# # CUSTOMER INTELLIGENCE SIDEBAR
# # ============================================================

# # st.sidebar.markdown("---")

# # st.sidebar.subheader(
# #     "🧠 Customer Intelligence"
# # )

# # show_customer_intelligence = st.sidebar.checkbox(
# #     "Open Customer Intelligence"
# # )


# # ============================================================
# # VALID SCORE DATA
# # ============================================================
# #
# # IMPORTANT:
# #
# # Skipped calls remain inside filtered_df.
# #
# # They are removed ONLY from score calculations.
# #
# # We also remove:
# #
# # - overall_call_score == 0
# # - missing overall_call_score
# # - skipped analysis
# #
# # ============================================================

# analysed_df = filtered_df.copy()

# analysed_df = analysed_df[
#     ~analysed_df["analysis_status"]
#     .astype(str)
#     .str.upper()
#     .isin([
#         "SKIPPED_SHORT_AUDIO",
#         "EMPTY_TRANSCRIPT"
#     ])
# ]

# score_df = filtered_df.copy()


# if "analysis_status" in score_df.columns:

#     score_df = score_df[
#         score_df[
#             "analysis_status"
#         ]
#         .astype(str)
#         .str.upper()
#         .ne(
#             "SKIPPED_SHORT_AUDIO"
#         )
#     ]


# # Remove zero scores

# score_df = score_df[
#     score_df[
#         "overall_call_score"
#     ].notna()
# ]


# score_df = score_df[
#     score_df[
#         "overall_call_score"
#     ] > 0
# ]


# # ============================================================
# # KPI SECTION
# # ============================================================

# st.subheader(
#     "Overview"
# )


# c1, c2, c3, c4, c5 = st.columns(5)


# # ------------------------------------------------------------
# # ANALYZED CALLS
# # ------------------------------------------------------------

# with c1:

#     st.metric(
#         "Analysed Calls",
#         len(analysed_df)
#     )


# # ------------------------------------------------------------
# # AVG CALL SCORE
# # ------------------------------------------------------------

# with c2:

#     avg_call_score = (
#         score_df[
#             "overall_call_score"
#         ].mean()
#         if not score_df.empty
#         else 0
#     )

#     st.metric(
#         "Avg Call Score",
#         f"{avg_call_score:.2f}"
#     )


# # ------------------------------------------------------------
# # AVG SALES SCORE
# # ------------------------------------------------------------

# with c3:

#     avg_sales_score = (
#         score_df[
#             "sales_effectiveness_score"
#         ].mean()
#         if (
#             not score_df.empty
#             and
#             "sales_effectiveness_score"
#             in score_df.columns
#         )
#         else 0
#     )

#     st.metric(
#         "Avg Sales Score",
#         f"{avg_sales_score:.2f}"
#     )


# # ------------------------------------------------------------
# # INTERESTED CALLS
# # ------------------------------------------------------------

# with c4:

#     interested = filtered_df[
#         filtered_df[
#             "customer_interest_level"
#         ]
#         .astype(str)
#         .str.lower()
#         .isin(
#             [
#                 "high",
#                 "interested"
#             ]
#         )
#     ]

#     st.metric(
#         "Interested Calls",
#         len(interested)
#     )


# # ------------------------------------------------------------
# # AVG COMPLIANCE
# # ------------------------------------------------------------

# with c5:

#     if (
#         not score_df.empty
#         and
#         "compliance_score"
#         in score_df.columns
#     ):

#         avg_compliance = (
#             score_df[
#                 "compliance_score"
#             ].mean()
#         )

#     else:

#         avg_compliance = 0

#     st.metric(
#         "Avg Compliance",
#         f"{avg_compliance:.2f}"
#     )


# # ============================================================
# # DATA QUALITY SUMMARY
# # ============================================================

# # st.subheader(
# #     "📋 Call Coverage"
# # )


# # q1, q2, q3, q4 = st.columns(4)


# # with q1:

# #     st.metric(
# #         "Total Calls",
# #         len(filtered_df)
# #     )


# # with q2:

# #     skipped_count = len(
# #         filtered_df[
# #             filtered_df[
# #                 "analysis_status"
# #             ]
# #             .astype(str)
# #             .str.upper()
# #             .eq(
# #                 "SKIPPED_SHORT_AUDIO"
# #             )
# #         ]
# #     )

# #     st.metric(
# #         "Short Audio",
# #         skipped_count
# #     )


# # with q3:

# #     empty_count = len(
# #         filtered_df[
# #             filtered_df[
# #                 "analysis_status"
# #             ]
# #             .astype(str)
# #             .str.upper()
# #             .eq(
# #                 "EMPTY_TRANSCRIPT"
# #             )
# #         ]
# #     )

# #     st.metric(
# #         "Empty Transcript",
# #         empty_count
# #     )


# # with q4:

# #     analyzed_count = len(
# #         score_df
# #     )

# #     st.metric(
# #         "Valid Analyses",
# #         analyzed_count
# #     )

# st.markdown("---")

# st.subheader(
#     "Propensity"
# )


# q1, q2, q3, q4 = st.columns(4)


# with q1:
#     Very_high = len(
#         filtered_df[
#             filtered_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "very high"
#                 ]
#             )
#         ]
#     )

#     st.metric(
#         "Very High",
#         Very_high
#     )

# with q2:
#     High = len(
#         filtered_df[
#             filtered_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "high"
#                 ]
#             )
#         ]
#     )

#     st.metric(
#         "High",
#         High
#     )


# with q3:
#     Medium = len(
#         filtered_df[
#             filtered_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "medium"
#                 ]
#             )
#         ]
#     )

#     st.metric(
#         "Medium",
#         Medium
#     )

# with q4:
#     Low = len(
#         filtered_df[
#             filtered_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "low"
#                 ]
#             )
#         ]
#     )
#     st.metric(
#         "Low",
#         Low
#     )


# # ============================================================
# # CUSTOMER INTELLIGENCE
# # ============================================================


# st.markdown("---")

# st.subheader(
#     "Customer Intelligence"
# )

# # --------------------------------------------------------
# # AVAILABLE COLUMNS ONLY
# # --------------------------------------------------------

# available_ci_columns = [
#     column
#     for column in
#     CUSTOMER_INTELLIGENCE_COLUMNS
#     if column in filtered_df.columns
# ]

# customer_df = filtered_df[
#     available_ci_columns
# ].copy()


# # --------------------------------------------------------
# # CUSTOMER KPIs
# # --------------------------------------------------------

# ci1, ci2, ci3, ci4 = st.columns(4)


# with ci1:

#     if "customer_number" in customer_df.columns:

#         customer_count = (
#             customer_df[
#                 "customer_number"
#             ]
#             .replace(
#                 "",
#                 pd.NA
#             )
#             .dropna()
#             .nunique()
#         )

#     else:

#         customer_count = 0

#     st.metric(
#         "Unique Customers",
#         customer_count
#     )


# with ci2:

#     if "customer_interest_level" in customer_df.columns:

#         high_interest = customer_df[
#             customer_df[
#                 "customer_interest_level"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "high",
#                     "interested"
#                 ]
#             )
#         ]

#         high_interest_count = len(
#             high_interest
#         )

#     else:

#         high_interest_count = 0

#     st.metric(
#         "High Interest",
#         high_interest_count
#     )


# with ci3:

#     if "propensity_bucket" in customer_df.columns:

#         high_propensity = customer_df[
#             customer_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.lower()
#             .isin(
#                 [
#                     "high",
#                     "very high"
#                 ]
#             )
#         ]

#         high_propensity_count = len(
#             high_propensity
#         )

#     else:

#         high_propensity_count = 0

#     st.metric(
#         "High Propensity",
#         high_propensity_count
#     )


# with ci4:

#     if "plan_pitched" in customer_df.columns:

#         plans_pitched = customer_df[
#             "plan_pitched"
#         ].astype(str)

#         plans_pitched_count = (
#             plans_pitched
#             .replace(
#                 [
#                     "",
#                     "[]",
#                     "nan",
#                     "None"
#                 ],
#                 pd.NA
#             )
#             .dropna()
#             .shape[0]
#         )

#     else:

#         plans_pitched_count = 0

#     st.metric(
#         "Plans Pitched",
#         plans_pitched_count
#     )


# # --------------------------------------------------------
# # CUSTOMER INTEREST DISTRIBUTION
# # --------------------------------------------------------

# ci_col1, ci_col2 = st.columns(2)


# with ci_col1:

#     if (
#         "customer_interest_level"
#         in customer_df.columns
#     ):

#         interest_data = (
#             customer_df[
#                 "customer_interest_level"
#             ]
#             .astype(str)
#             .replace(
#                 [
#                     "",
#                     "nan",
#                     "None",
#                     "Unknown",
#                     "unknown"
#                 ],
#                 pd.NA
#             )
#             .dropna()
#             .value_counts()
#             .reset_index()
#         )

#         interest_data.columns = [
#             "Interest",
#             "Count"
#         ]

#         fig = px.pie(
#             interest_data,
#             names="Interest",
#             values="Count",
#             title="Customer Interest"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )


# with ci_col2:

#     if (
#         "propensity_bucket"
#         in customer_df.columns
#     ):

#         propensity_data = (
#             customer_df[
#                 "propensity_bucket"
#             ]
#             .astype(str)
#             .str.strip()
#         )

#         propensity_data = propensity_data[
#             ~propensity_data.str.lower().isin(
#                 [
#                     "",
#                     "nan",
#                     "none",
#                     "null",
#                     "unknown"
#                 ]
#             )
#         ]

#         propensity_data = (
#             propensity_data
#             .value_counts()
#             .reset_index()
#         )

#         propensity_data.columns = [
#             "Propensity",
#             "Count"
#         ]

#         fig = px.bar(
#             propensity_data,
#             x="Propensity",
#             y="Count",
#             title="Customer Propensity"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )


# # --------------------------------------------------------
# # CUSTOMER INTELLIGENCE TABLE
# # --------------------------------------------------------

# st.subheader(
#     "Customer Intelligence Records"
# )

# st.dataframe(
#     customer_df,
#     use_container_width=True,
#     hide_index=True
# )

# st.markdown("---")

# # ============================================================
# # AGENT PERFORMANCE
# # ============================================================

# st.subheader(
#     "👥 Agent Performance"
# )


# if not score_df.empty:

#     agent_perf = (

#         score_df

#         .groupby(
#             "agent_name"
#         )

#         .agg(

#             Calls=(
#                 "call_id",
#                 "count"
#             ),

#             Avg_Score=(
#                 "overall_call_score",
#                 "mean"
#             ),

#             Sales_Score=(
#                 "sales_effectiveness_score",
#                 "mean"
#             )

#         )

#         .reset_index()

#     )


#     agent_perf = agent_perf.sort_values(
#         "Avg_Score",
#         ascending=False
#     )


#     agent_perf[
#         "Avg_Score"
#     ] = agent_perf[
#         "Avg_Score"
#     ].round(2)


#     agent_perf[
#         "Sales_Score"
#     ] = agent_perf[
#         "Sales_Score"
#     ].round(2)


#     col1, col2 = st.columns(2)


#     with col1:

#         fig = px.bar(
#             agent_perf,
#             x="agent_name",
#             y="Avg_Score",
#             title="Agent Ranking"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )


#     with col2:

#         st.dataframe(
#             agent_perf,
#             use_container_width=True,
#             hide_index=True
#         )

# else:

#     st.info(
#         "No valid analysed calls available for agent scoring."
#     )

# st.markdown("---")

# # ============================================================
# # DAILY CALL TREND
# # ============================================================

# st.subheader(
#     "📅 Daily Call Trend"
# )


# daily = (

#     filtered_df

#     .dropna(
#         subset=["date"]
#     )

#     .groupby(
#         "date"
#     )

#     .size()

#     .reset_index(
#         name="Calls"
#     )

# )


# if not daily.empty:

#     fig = px.line(
#         daily,
#         x="date",
#         y="Calls",
#         markers=True,
#         title="Calls Per Day"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# st.markdown("---")

# # ============================================================
# # CALL OUTCOME
# # ============================================================

# st.subheader(
#     "📞 Call Outcome Analysis"
# )


# col1, col2 = st.columns(2)


# with col1:

#     outcome = (
#         filtered_df[
#             "call_outcome"
#         ]
#         .astype(str)
#         .str.strip()
#     )

#     outcome = outcome[
#         ~outcome.str.lower().isin(
#             [
#                 "",
#                 "nan",
#                 "none",
#                 "null",
#                 "unknown"
#             ]
#         )
#     ]

#     outcome = (
#         outcome
#         .value_counts()
#         .reset_index()
#     )

#     outcome.columns = [
#         "Outcome",
#         "Count"
#     ]


#     if not outcome.empty:

#         fig = px.pie(
#             outcome,
#             names="Outcome",
#             values="Count",
#             title="Call Outcomes"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )


# with col2:

#     if (
#         "not_interested_reason"
#         in filtered_df.columns
#     ):

#         reason = (
#             filtered_df[
#                 "not_interested_reason"
#             ]
#             .astype(str)
#             .str.strip()
#         )

#         reason = reason[
#             ~reason.str.lower().isin(
#                 [
#                     "",
#                     "nan",
#                     "none",
#                     "null",
#                     "unknown"
#                 ]
#             )
#         ]

#         reason = (
#             reason
#             .value_counts()
#             .head(10)
#             .reset_index()
#         )

#         reason.columns = [
#             "Reason",
#             "Count"
#         ]

#         if not reason.empty:

#             fig = px.bar(
#                 reason,
#                 x="Count",
#                 y="Reason",
#                 orientation="h",
#                 title="Top Not-Interested Reasons"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True
#             )


# # ============================================================
# # SCORE BREAKDOWN
# # ============================================================

# st.markdown("---")

# st.subheader(
#     "Quality Score Breakdown"
# )


# if not score_df.empty:

#     available_score_columns = [
#         column
#         for column in NUMERIC_SCORE_COLUMNS
#         if column in score_df.columns
#     ]


#     score_breakdown_df = (

#         score_df[
#             available_score_columns
#         ]

#         .mean()

#         .reset_index()

#     )


#     score_breakdown_df.columns = [
#         "Metric",
#         "Score"
#     ]


#     score_breakdown_df[
#         "Score"
#     ] = score_breakdown_df[
#         "Score"
#     ].round(2)


#     fig = px.bar(
#         score_breakdown_df,
#         x="Metric",
#         y="Score",
#         title="Average Quality Scores"
#     )


#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# else:

#     st.info(
#         "No valid score data available."
#     )


# # ============================================================
# # AI COACHING / INSIGHTS
# # ============================================================

# st.markdown("---")

# st.subheader(
#     "🤖 Insights"
# )


# tab1, tab2, tab3 = st.tabs(
#     [
#         "Mistakes",
#         "Improvements",
#         "Score Reasons"
#     ]
# )


# # ============================================================
# # PREPARE AGENT INSIGHTS
# # ============================================================

# def prepare_agent_insights(
#     dataframe,
#     insight_column
# ):

#     if (
#         "agent_name" not in dataframe.columns
#         or insight_column not in dataframe.columns
#     ):

#         return {}


#     temp = dataframe[
#         [
#             "agent_name",
#             insight_column
#         ]
#     ].copy()


#     # --------------------------------------------------------
#     # CLEAN AGENT NAME
#     # --------------------------------------------------------

#     temp["agent_name"] = (
#         temp["agent_name"]
#         .fillna("")
#         .astype(str)
#         .str.strip()
#     )


#     # --------------------------------------------------------
#     # CLEAN INSIGHTS
#     # --------------------------------------------------------

#     temp[insight_column] = (
#         temp[insight_column]
#         .fillna("")
#         .astype(str)
#         .str.strip()
#     )


#     # Remove empty rows
#     temp = temp[
#         (temp["agent_name"] != "")
#         &
#         (temp[insight_column] != "")
#         &
#         (~temp[insight_column].str.lower().isin(
#             [
#                 "nan",
#                 "none",
#                 "null"
#             ]
#         ))
#     ]


#     if temp.empty:

#         return {}


#     # --------------------------------------------------------
#     # CREATE DICTIONARY
#     # --------------------------------------------------------

#     agent_insights = {}


#     for _, row in temp.iterrows():

#         agent = row["agent_name"]

#         raw_text = row[insight_column]


#         # ----------------------------------------------------
#         # SPLIT GEMINI INSIGHTS
#         # ----------------------------------------------------

#         insights = raw_text.split("|")


#         for insight in insights:

#             insight = insight.strip()


#             # Remove existing bullet characters
#             insight = (
#                 insight
#                 .lstrip("•")
#                 .strip()
#             )


#             if not insight:
#                 continue


#             if insight.lower() in [
#                 "nan",
#                 "none",
#                 "null"
#             ]:
#                 continue


#             if agent not in agent_insights:

#                 agent_insights[agent] = []


#             # ------------------------------------------------
#             # REMOVE DUPLICATES
#             # ------------------------------------------------

#             if insight not in agent_insights[agent]:

#                 agent_insights[agent].append(
#                     insight
#                 )


#     return agent_insights


# # ============================================================
# # DISPLAY FUNCTION
# # ============================================================

# def display_agent_insights(
#     dataframe,
#     insight_column
# ):

#     agent_insights = prepare_agent_insights(
#         dataframe,
#         insight_column
#     )

#     if not agent_insights:

#         st.info(
#             "No insights available."
#         )

#         return


#     # ========================================================
#     # AGENT SELECTOR
#     # ========================================================

#     agents = sorted(
#         agent_insights.keys()
#     )


#     selected_agent = st.selectbox(
#         "Select Agent",
#         agents,
#         key=f"agent_{insight_column}"
#     )


#     # ========================================================
#     # DISPLAY SELECTED AGENT
#     # ========================================================

#     insights = agent_insights[
#         selected_agent
#     ]


#     with st.container(
#         border=True
#     ):

#         st.markdown(
#             f"### {selected_agent}"
#         )


#         for insight in insights:

#             st.markdown(
#                 f"- {insight}"
#             )

# # ============================================================
# # MISTAKES
# # ============================================================

# with tab1:

#     display_agent_insights(
#         filtered_df,
#         "mistakes"
#     )


# # ============================================================
# # IMPROVEMENTS
# # ============================================================

# with tab2:

#     display_agent_insights(
#         filtered_df,
#         "improvements"
#     )


# # ============================================================
# # SCORE REASONS
# # ============================================================

# with tab3:

#     display_agent_insights(
#         filtered_df,
#         "overall_call_score_reason"
#     )

# # ============================================================
# # DOWNLOAD
# # ============================================================

# st.markdown("---")

# st.subheader(
#     "⬇️ Export"
# )


# csv = filtered_df.to_csv(
#     index=False
# )


# st.download_button(
#     "Download Filtered Data",
#     csv,
#     "filtered_calls.csv",
#     "text/csv"
# )


# # ============================================================
# # RAW DATA
# # ============================================================

# with st.expander(
#     "View Complete Data"
# ):

#     st.dataframe(
#         filtered_df,
#         use_container_width=True,
#         hide_index=True
#     )


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

# AGENT_NAME_MAP = {
#     "Abhishek_Ziraya": "Abhishek Ziraya",
#     "Aditi_Verma": "Aditi Verma",
#     "Adithya": "LV Adithya",
#     "Ayush_Ziraya": "Ayush Singh",
#     "Bandana": "Bandana Kumari Nagar",
#     "Chandra_Ziraya": "Chandra Bhushan",
#     'Chytanya':'Chytanya Netalkar',
#     "Debangi": "Debangi Majumder",
#     "Divya":"Divya Rashmi",
#     "Garv_Ziraya": "Garv Tandan",
#     'Garvit': 'Garvit Jat',
#     "Goresh_Ziraya": "Goresh Sharma",
#     "Iftekhar": "Iftekhar Alam",
#     "Jaya": "Jaya Prajapat",
#     "Jinson":"Jinson",
#     "Jiya": "Jiya Pandey",
#     "Krishna": "Krishna Kumar",
#     "Nameet": "Nameet Karadi",
#     "Namratha": "Namratha Chauhan",
#     "Omkar": "Omkar Kaktikar",
#     "Pawan_Ziraya": "Pawan Chahar",
#     "Pradeep": "Pradeep Bhandari",
#     "Pravesh": "Pravesh Singh",
#     "Preeti": "Preeti Tahilramani",
#     "Priya_Ziraya": "Priya Khanna",
#     "Priyanshi": "Priyanshi Kamal Das",
#     "Priyap": "Priyadharshini P",
#     "Rahaman": "Khan Rahaman",
#     'Rajeev':'Rajeev Ranjan',
#     "Rakshith": "Rakshith Pai",
#     "Rishabh": "Rishabh Singh",
#     "Rishabh_Ziraya": "Rishabh Kushwah",
#     "Rishi": "Rishi Sarkar",
#     "Ritik": "Ritik Raje",
#     "Sabiha": "Shaik Sabiha",
#     "Sagar_Ziraya": "Sagar Kumar",
#     "Saif_Ziraya": "Saif Khan",
#     "Shahbaz": "Shahbaz Mansoori",
#     "Shaik_Aleem": "Shaik Aleem",
#     'Simran':'Simran',
#     "Shreya_H": "Shreya Hari",
#     "Sweta":"Sweta Raj",
#     "Soumyajeet": "Soumyajeet Behera",
#     "Sourav": "Sourav Chowdhury",
#     "Sukanya_Kokate": "Sukanya Kokate",
#     "Supriya": "Supriya Raj",
#     "Umar": "Mohammad Umar Ali",
#     "Umar_Farooq": "Umar Farooq",
#     "Vanita_Hiremath": "Vanita Hiremath",
#     "Veervart_Karnwal": "Veervart Karnwal",
#     "Vibhanshu": "Vibhanshu Mishra",
#     "Vinay_Vyas": "Vinay Vyas",
#     "Vishal": "Vishal Gautam",
#     "Vishals": "Vishal Singh",
#     "Zain": "Zain Real",
# }

AGENT_NAME_MAP = {

    "Abhishek": "Abhishek Ziraya",

    "Abhishek_Ziraya": "Abhishek Ziraya",

    "Aditi": "Aditi Verma",
    "Aditi_Verma": "Aditi Verma",

    "Adithya": "LV Adithya",

    "Akash_Harkude": "Akash Harkude",

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

    "Imdad": "Imdad P",
    "Imdad_P": "Imdad P",

    "Izaz_Ahmed": "Izaz Ahmed",
    "Izaz": "Izaz Ahmed",

    "Jaya": "Jaya Prajapat",

    "Jinson": "Jinson",

    "Jiya": "Jiya Pandey",

    "Krishna": "Krishna Kumar",

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

    "Preeti": "Preeti Tahilramani",

    "Priya": "Priya Khanna",
    "Priya_Ziraya": "Priya Khanna",

    "Priyanshi": "Priyanshi Kamal Das",

    "Priyap": "Priyadharshini P",

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

    "Divya Rashmi": [
        "LV Adithya",
        "Aditi Verma",
        "Jinson",
        "Pravesh Singh",
        "Preeti Tahilramani",
        "Shreya Hari",
        "Supriya Raj",
        "Rishi Sarkar",
    ],

    "Harish": [
        "Ayush Singh",
        "Garv Tandan",
        "Jaya Prajapat",
        "Priya Khanna",
        "Rajeev Ranjan",
        "Rishabh Kushwah",
        "Sagar Kumar",
        "Saif Khan",
        "Shahbaz Mansoori",
    ],

    "Krishna": [
        "Bandana Kumari Nagar",
        "Jiya Pandey",
        "Priyanshi Kamal Das",
        "Rishabh Singh",
        "Soumyajeet Behera",
        "Mohammad Umar Ali",
        "Vishal Gautam",
        "Zain Real",
        "Vanita Hiremath",
        "Sukanya Kokate",
        "Puja",
    ],

    "Garvit": [
        "Chytanya Netalkar",
        "Iftekhar Alam",
        "Khan Rahaman",
        "Nameet Karadi",
        "Omkar Kaktikar",
        "Ritik Raje",
        "Umar Farooq",
        "Vibhanshu Mishra",
        "Vishal Singh",
        "Sibajit Gope",
        "Mayank Biswas",
    ],

    "Rakshith": [
        "Namratha Chauhan",
        "Priyadharshini P",
        "Rakshith Pai",
        "Sourav Chowdhury",
        "Vinay Vyas",
        "Shaik Aleem",
        "Veervart Karnwal",
    ],

    "New Joinees": [
        "Ayan Dey",
        "Izaz Ahmed",
        "Manan Shah",
        "Imdad P",
        "Pratham Sinha",
        "Akash Shelar",
    ],
}

if "agent_name" in df.columns:

    df["agent_name"] = (
        df["agent_name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace(AGENT_NAME_MAP)
    )

def get_team_leader(agent_name):

    for leader, members in TEAM_MAP.items():

        if agent_name in members:
            return leader

    return "Unmapped"


df["team_leader"] = df["agent_name"].apply(
    get_team_leader
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
# PAGE NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigate",
    [
        "📊 Overview",
        "👥 Team Performance",
        "📈 Agent Performance"

    ]
)


if page == "📊 Overview":

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

                Scored_Calls=(
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

elif page == "👥 Team Performance":

    # ============================================================
    # TEAM PERFORMANCE
    # ============================================================

    st.title("👥 Team Performance")

    # st.caption(
    #     "Team leader and team member performance analytics"
    # )

    # ============================================================
    # TEAM FILTERS
    # ============================================================

    st.sidebar.markdown("---")
    st.sidebar.header("Team Performance Filters")

    team_filtered_df = df.copy()

    # ------------------------------------------------------------
    # DATE FILTER
    # ------------------------------------------------------------

    valid_team_dates = (
        df["date"]
        .dropna()
    )

    if not valid_team_dates.empty:

        team_min_date = valid_team_dates.min()
        team_max_date = valid_team_dates.max()

        team_selected_dates = st.sidebar.date_input(
            "Call Date",
            [
                team_min_date,
                team_max_date
            ],
            key="team_date_filter"
        )

        if (
            isinstance(
                team_selected_dates,
                (list, tuple)
            )
            and len(team_selected_dates) == 2
        ):

            team_filtered_df = team_filtered_df[
                (
                    team_filtered_df["date"]
                    >= team_selected_dates[0]
                )
                &
                (
                    team_filtered_df["date"]
                    <= team_selected_dates[1]
                )
            ]

    # ============================================================
    # TEAM LEADER FILTER
    # ============================================================

    team_leaders = sorted(
        [
            leader
            for leader in TEAM_MAP.keys()
            if leader.strip()
        ]
    )

    team_leaders.append("Unmapped")

    selected_team_leader = st.sidebar.multiselect(
        "Team Leader",
        team_leaders,
        key="team_leader_filter"
    )
    # if selected_team_leader:

    #     selected_members = []

    #     for leader in selected_team_leader:

    #         selected_members.extend(
    #             TEAM_MAP.get(
    #                 leader,
    #                 []
    #             )
    #         )

    #     team_filtered_df = team_filtered_df[
    #         team_filtered_df["agent_name"].isin(
    #             selected_members
    #         )
    #     ]

    if selected_team_leader:

        selected_members = []

        for leader in selected_team_leader:

            if leader == "Unmapped":

                mapped_members = [
                    member
                    for members in TEAM_MAP.values()
                    for member in members
                ]

                unmapped_members = [
                    member
                    for member in team_filtered_df["agent_name"]
                    .dropna()
                    .astype(str)
                    .unique()
                    if member not in mapped_members
                ]

                selected_members.extend(
                    unmapped_members
                )

            else:

                selected_members.extend(
                    TEAM_MAP.get(
                        leader,
                        []
                    )
                )

        team_filtered_df = team_filtered_df[
            team_filtered_df["agent_name"].isin(
                selected_members
            )
        ]
    # ============================================================
    # TEAM MEMBER FILTER
    # ============================================================

    available_members = sorted(
        team_filtered_df[
            "agent_name"
        ]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    available_members = [
        member
        for member in available_members
        if member
    ]

    selected_team_members = st.sidebar.multiselect(
        "Team Member",
        available_members,
        key="team_member_filter"
    )

    if selected_team_members:

        team_filtered_df = team_filtered_df[
            team_filtered_df["agent_name"].isin(
                selected_team_members
            )
        ]

    # ============================================================
    # CALL OUTCOME FILTER
    # ============================================================

    team_outcome_values = sorted(
        [
            value
            for value in
            team_filtered_df["call_outcome"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            if value
            and value.lower()
            not in [
                "nan",
                "none",
                "null",
                "unknown"
            ]
        ]
    )

    selected_team_outcomes = st.sidebar.multiselect(
        "Call Outcome",
        team_outcome_values,
        key="team_outcome_filter"
    )

    if selected_team_outcomes:

        team_filtered_df = team_filtered_df[
            team_filtered_df["call_outcome"].isin(
                selected_team_outcomes
            )
        ]

    # ============================================================
    # CUSTOMER INTEREST FILTER
    # ============================================================

    team_interest_values = sorted(
        [
            value
            for value in
            team_filtered_df[
                "customer_interest_level"
            ]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            if value
            and value.lower()
            not in [
                "nan",
                "none",
                "null",
                "unknown"
            ]
        ]
    )

    selected_team_interest = st.sidebar.multiselect(
        "Customer Interest",
        team_interest_values,
        key="team_interest_filter"
    )

    if selected_team_interest:

        team_filtered_df = team_filtered_df[
            team_filtered_df[
                "customer_interest_level"
            ].isin(
                selected_team_interest
            )
        ]

    # ============================================================
    # PROPENSITY FILTER
    # ============================================================

    team_propensity_values = sorted(
        [
            value
            for value in
            team_filtered_df[
                "propensity_bucket"
            ]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            if value
            and value.lower()
            not in [
                "nan",
                "none",
                "null",
                "unknown"
            ]
        ]
    )

    selected_team_propensity = st.sidebar.multiselect(
        "Customer Propensity",
        team_propensity_values,
        key="team_propensity_filter"
    )

    if selected_team_propensity:

        team_filtered_df = team_filtered_df[
            team_filtered_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.strip()
            .isin(
                selected_team_propensity
            )
        ]

    # ============================================================
    # CUSTOMER NUMBER FILTER
    # ============================================================

    team_customer_numbers = sorted(
        [
            value
            for value in
            team_filtered_df[
                "customer_number"
            ]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            if value
            and value.lower()
            not in [
                "nan",
                "none",
                "null"
            ]
        ]
    )

    selected_team_customer_numbers = st.sidebar.multiselect(
        "Customer Number",
        team_customer_numbers,
        key="team_customer_number_filter"
    )

    if selected_team_customer_numbers:

        team_filtered_df = team_filtered_df[
            team_filtered_df[
                "customer_number"
            ].isin(
                selected_team_customer_numbers
            )
        ]

    # ============================================================
    # EMPTY DATA CHECK
    # ============================================================

    if team_filtered_df.empty:

        st.warning(
            "No calls match the selected filters."
        )

    else:

        # ========================================================
        # VALID SCORE DATA
        # ========================================================

        team_score_df = team_filtered_df.copy()

        if "analysis_status" in team_score_df.columns:

            team_score_df = team_score_df[
                ~team_score_df[
                    "analysis_status"
                ]
                .astype(str)
                .str.upper()
                .isin(
                    [
                        "SKIPPED_SHORT_AUDIO",
                        "EMPTY_TRANSCRIPT"
                    ]
                )
            ]

        team_score_df = team_score_df[
            team_score_df[
                "overall_call_score"
            ].notna()
        ]

        analysed_calls_count = len(
            team_score_df
        )

        team_score_df = team_score_df[
            team_score_df[
                "overall_call_score"
            ] > 0
        ]

        # ========================================================
        # TOP KPI SECTION
        # ========================================================

        st.markdown("---")

        st.subheader("📊 Team Overview")

        k1, k2, k3, k4, k5 = st.columns(5)

        # --------------------------------------------------------
        # TOTAL CALLS
        # --------------------------------------------------------

        with k1:

            st.metric(
                "Total Calls",
                len(team_filtered_df)
            )

        # --------------------------------------------------------
        # ANALYSED CALLS
        # --------------------------------------------------------

        with k2:

            st.metric(
                "Analysed Calls",
                analysed_calls_count
            )

        # --------------------------------------------------------
        # AVG SCORE
        # --------------------------------------------------------

        with k3:

            avg_team_score = (
                team_score_df[
                    "overall_call_score"
                ].mean()
                if not team_score_df.empty
                else 0
            )

            st.metric(
                "Avg Call Score",
                f"{avg_team_score:.2f}"
            )

        # --------------------------------------------------------
        # AVG SALES SCORE
        # --------------------------------------------------------

        with k4:

            avg_team_sales_score = (
                team_score_df[
                    "sales_effectiveness_score"
                ].mean()
                if (
                    not team_score_df.empty
                    and
                    "sales_effectiveness_score"
                    in team_score_df.columns
                )
                else 0
            )

            st.metric(
                "Avg Sales Score",
                f"{avg_team_sales_score:.2f}"
            )

        # --------------------------------------------------------
        # HIGH PROPENSITY
        # --------------------------------------------------------

        with k5:

            high_propensity_count = len(
                team_filtered_df[
                    team_filtered_df[
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
            )

            st.metric(
                "High Propensity",
                high_propensity_count
            )

        # ========================================================
        # TEAM LEADER PERFORMANCE
        # ========================================================

        st.markdown("---")

        st.subheader(
            "👥 Team Performance"
        )

        if not team_score_df.empty:

            team_leader_perf = (

                team_score_df

                .groupby(
                    "team_leader"
                )

                .agg(

                    Scored_Calls=(
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

            team_leader_perf = (
                team_leader_perf
                .sort_values(
                    "Scored_Calls",
                    ascending=False
                )
            )

            team_leader_perf[
                "Avg_Score"
            ] = (
                team_leader_perf[
                    "Avg_Score"
                ].round(2)
            )

            team_leader_perf[
                "Sales_Score"
            ] = (
                team_leader_perf[
                    "Sales_Score"
                ].round(2)
            )

            st.dataframe(
                team_leader_perf,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No valid analysed calls available."
            )

        # ========================================================
        # TEAM LEADER CHART
        # ========================================================

        if not team_score_df.empty:

            team_chart_df = (

                team_score_df

                .groupby(
                    "team_leader"
                )

                .agg(
                    Avg_Score=(
                        "overall_call_score",
                        "mean"
                    )
                )

                .reset_index()
            )

            team_chart_df[
                "Avg_Score"
            ] = (
                team_chart_df[
                    "Avg_Score"
                ].round(2)
            )

            fig_team = px.bar(
                team_chart_df,
                x="team_leader",
                y="Avg_Score",
                title="Average Call Score by Team"
            )

            st.plotly_chart(
                fig_team,
                use_container_width=True
            )

        # ========================================================
        # TEAM MEMBER PERFORMANCE
        # ========================================================

        st.markdown("---")

        st.subheader(
            "👤 Team Member Performance"
        )

        if not team_score_df.empty:

            member_perf = (

                team_score_df

                .groupby(
                    [
                        "team_leader",
                        "agent_name"
                    ]
                )

                .agg(

                    Scored_Calls=(
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
                    ),

                    Avg_Propensity=(
                        "propensity_score",
                        "mean"
                    )

                )

                .reset_index()
            )

            member_perf = (
                member_perf
                .sort_values(
                    [
                        "team_leader",
                        "Avg_Score"
                    ],
                    ascending=[
                        True,
                        False
                    ]
                )
            )

            member_perf[
                "Avg_Score"
            ] = (
                member_perf[
                    "Avg_Score"
                ].round(2)
            )

            member_perf[
                "Sales_Score"
            ] = (
                member_perf[
                    "Sales_Score"
                ].round(2)
            )

            member_perf[
                "Avg_Propensity"
            ] = (
                member_perf[
                    "Avg_Propensity"
                ].round(2)
            )

            st.dataframe(
                member_perf,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No valid analysed calls available."
            )

        # ========================================================
        # MEMBER SCORE CHART
        # ========================================================

        if not team_score_df.empty:

            member_chart_df = (

                team_score_df

                .groupby(
                    "agent_name"
                )

                .agg(
                    Avg_Score=(
                        "overall_call_score",
                        "mean"
                    )
                )

                .reset_index()
            )

            member_chart_df[
                "Avg_Score"
            ] = (
                member_chart_df[
                    "Avg_Score"
                ].round(2)
            )

            fig_member = px.bar(
                member_chart_df,
                x="agent_name",
                y="Avg_Score",
                title="Average Call Score by Team Member"
            )

            fig_member.update_layout(
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig_member,
                use_container_width=True
            )

        # ========================================================
        # CALL OUTCOME BY TEAM
        # ========================================================

        st.markdown("---")

        st.subheader(
            "📞 Call Outcomes by Team"
        )

        outcome_team_df = (
            team_filtered_df[
                [
                    "team_leader",
                    "call_outcome"
                ]
            ]
            .copy()
        )

        outcome_team_df[
            "call_outcome"
        ] = (
            outcome_team_df[
                "call_outcome"
            ]
            .astype(str)
            .str.strip()
        )

        outcome_team_df = (
            outcome_team_df[
                ~outcome_team_df[
                    "call_outcome"
                ]
                .str.lower()
                .isin(
                    [
                        "",
                        "nan",
                        "none",
                        "null",
                        "unknown"
                    ]
                )
            ]
        )

        if not outcome_team_df.empty:

            outcome_summary = (
                outcome_team_df
                .groupby(
                    [
                        "team_leader",
                        "call_outcome"
                    ]
                )
                .size()
                .reset_index(
                    name="Calls"
                )
            )

            fig_outcome_team = px.bar(
                outcome_summary,
                x="team_leader",
                y="Calls",
                color="call_outcome",
                barmode="group",
                # title="Call Outcomes by Team Leader"
            )

            st.plotly_chart(
                fig_outcome_team,
                use_container_width=True
            )

        # ========================================================
        # CUSTOMER INTEREST BY TEAM
        # ========================================================

        st.subheader(
            "Customer Interest by Team"
        )

        interest_team_df = (
            team_filtered_df[
                [
                    "team_leader",
                    "customer_interest_level"
                ]
            ]
            .copy()
        )

        interest_team_df[
            "customer_interest_level"
        ] = (
            interest_team_df[
                "customer_interest_level"
            ]
            .astype(str)
            .str.strip()
        )

        interest_team_df = (
            interest_team_df[
                ~interest_team_df[
                    "customer_interest_level"
                ]
                .str.lower()
                .isin(
                    [
                        "",
                        "nan",
                        "none",
                        "null",
                        "unknown"
                    ]
                )
            ]
        )

        if not interest_team_df.empty:

            interest_summary = (
                interest_team_df
                .groupby(
                    [
                        "team_leader",
                        "customer_interest_level"
                    ]
                )
                .size()
                .reset_index(
                    name="Calls"
                )
            )

            fig_interest_team = px.bar(
                interest_summary,
                x="team_leader",
                y="Calls",
                color="customer_interest_level",
                barmode="group",
                # title="Customer Interest by Team Leader"
            )

            st.plotly_chart(
                fig_interest_team,
                use_container_width=True
            )

        # ========================================================
        # PROPENSITY BY TEAM
        # ========================================================

        st.subheader(
            "Customer Propensity by Team"
        )

        propensity_team_df = (
            team_filtered_df[
                [
                    "team_leader",
                    "propensity_bucket"
                ]
            ]
            .copy()
        )

        propensity_team_df[
            "propensity_bucket"
        ] = (
            propensity_team_df[
                "propensity_bucket"
            ]
            .astype(str)
            .str.strip()
            .str.title()
        )

        # Remove unknown / blank values
        propensity_team_df = (
            propensity_team_df[
                ~propensity_team_df[
                    "propensity_bucket"
                ]
                .str.lower()
                .isin(
                    [
                        "",
                        "nan",
                        "none",
                        "null",
                        "unknown"
                    ]
                )
            ]
        )

        # --------------------------------------------------------
        # FIX PROPENSITY ORDER
        # --------------------------------------------------------

        propensity_order = [
            "Very High",
            "High",
            "Medium",
            "Low"
        ]

        propensity_team_df[
            "propensity_bucket"
            ] = pd.Categorical(
            propensity_team_df[
                "propensity_bucket"
            ],
            categories=propensity_order,
            ordered=True
        )

        if not propensity_team_df.empty:

            propensity_summary = (
                propensity_team_df
                .groupby(
                    [
                        "team_leader",
                        "propensity_bucket"
                    ],
                    observed=False
                )
                .size()
                .reset_index(
                    name="Customers"
                )
            )

            # Remove categories with zero customers
            propensity_summary = (
                propensity_summary[
                    propensity_summary[
                        "Customers"
                    ] > 0
                ]
            )

            fig_propensity_team = px.bar(
                propensity_summary,
                x="team_leader",
                y="Customers",
                color="propensity_bucket",
                category_orders={
                    "propensity_bucket": propensity_order
                },
                barmode="group",
                title="Customer Propensity by Team Leader"
            )

            st.plotly_chart(
                fig_propensity_team,
                use_container_width=True
            )
        # ========================================================
        # DAILY TEAM PERFORMANCE
        # ========================================================

        st.markdown("---")

        st.subheader(
            "📅 Daily Team Performance"
        )

        daily_team = (
            team_filtered_df
            .dropna(
                subset=["date"]
            )
            .groupby(
                [
                    "date",
                    "team_leader"
                ]
            )
            .size()
            .reset_index(
                name="Calls"
            )
        )

        if not daily_team.empty:

            fig_daily_team = px.line(
                daily_team,
                x="date",
                y="Calls",
                color="team_leader",
                markers=True,
                title="Daily Calls by Team"
            )

            st.plotly_chart(
                fig_daily_team,
                use_container_width=True
            )

        # ========================================================
        # CUSTOMER INTELLIGENCE
        # ========================================================

        st.markdown("---")

        st.subheader(
            "🧠 Team Customer Intelligence"
        )

        team_ci_columns = [
            column
            for column in
            CUSTOMER_INTELLIGENCE_COLUMNS
            if column in team_filtered_df.columns
        ]

        team_customer_df = (
            team_filtered_df[
                team_ci_columns
            ]
            .copy()
        )

        st.dataframe(
            team_customer_df,
            use_container_width=True,
            hide_index=True
        )

        # ========================================================
        # EXPORT
        # ========================================================

        st.markdown("---")

        st.subheader(
            "⬇️ Export Team Data"
        )

        team_csv = (
            team_filtered_df
            .to_csv(
                index=False
            )
        )

        st.download_button(
            "Download Team Performance Data",
            team_csv,
            "team_performance.csv",
            "text/csv",
            key="team_performance_download"
        )



elif page == "📈 Agent Performance":

    st.title("📈 Agent Performance")

    # st.caption(
    #     "Compare agent performance across different time periods"
    # )

    # ========================================================
    # FILTERS
    # ========================================================

    st.sidebar.markdown("---")
    st.sidebar.header("Comparison Filters")

    # --------------------------------------------------------
    # COMPARISON PERIOD
    # --------------------------------------------------------

    comparison_period = st.sidebar.selectbox(
        "Comparison Period",
        [
            "Day",
            "Week",
            "Month",
            "Year"
        ],
        key="comparison_period"
    )

    # --------------------------------------------------------
    # DATE RANGE
    # --------------------------------------------------------

    valid_dates = (
        df["date"]
        .dropna()
    )

    if valid_dates.empty:

        st.warning(
            "No valid dates available."
        )

    else:

        min_date = valid_dates.min()
        max_date = valid_dates.max()

        comparison_dates = st.sidebar.date_input(
            "Date Range",
            [
                min_date,
                max_date
            ],
            key="comparison_date_range"
        )

        # ====================================================
        # AGENT SELECTION
        # ====================================================

        available_agents = sorted(
            [
                agent
                for agent in
                df["agent_name"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                if agent
            ]
        )

        selected_agents = st.sidebar.multiselect(
            "Select Agents",
            available_agents,
            default=[],
            key="comparison_agents"
        )

        # ====================================================
        # METRIC SELECTION
        # ====================================================

        comparison_metric = st.sidebar.selectbox(
            "Primary Metric",
            [
                "Total Calls",
                "Analysed Calls",
                "Average Call Score",
                "Sales Effectiveness",
                "Average Propensity",
                "Conversion Rate",
                # "Mistakes",
                # "Compliance Violations"
            ],
            key="comparison_metric"
        )

        # ====================================================
        # FILTER DATA
        # ====================================================

        comparison_df = df.copy()

        if (
            isinstance(
                comparison_dates,
                (list, tuple)
            )
            and len(comparison_dates) == 2
        ):

            comparison_df = comparison_df[
                (
                    comparison_df["date"]
                    >= comparison_dates[0]
                )
                &
                (
                    comparison_df["date"]
                    <= comparison_dates[1]
                )
            ]

        if selected_agents:

            comparison_df = comparison_df[
                comparison_df[
                    "agent_name"
                ].isin(
                    selected_agents
                )
            ]

        # ====================================================
        # ANALYSED CALLS
        #
        # Score 0 IS INCLUDED
        #
        # Used for:
        # - Analysed Calls
        # - Analysed call volume
        # ====================================================

        analysed_comparison_df = (
            comparison_df.copy()
        )

        if "analysis_status" in analysed_comparison_df.columns:

            analysed_comparison_df = (
                analysed_comparison_df[
                    ~analysed_comparison_df[
                        "analysis_status"
                    ]
                    .astype(str)
                    .str.upper()
                    .isin(
                        [
                            "SKIPPED_SHORT_AUDIO",
                            "EMPTY_TRANSCRIPT"
                        ]
                    )
                ]
            )

        # Keep analysed calls even when score = 0
        analysed_comparison_df = (
            analysed_comparison_df[
                analysed_comparison_df[
                    "overall_call_score"
                ].notna()
            ]
        )

        # ====================================================
        # SCORE DATA
        #
        # Score 0 IS EXCLUDED
        #
        # Used for:
        # - Average Call Score
        # - Sales Effectiveness
        # - Average Propensity
        # - Score comparisons
        # ====================================================

        score_comparison_df = (
            analysed_comparison_df[
                analysed_comparison_df[
                    "overall_call_score"
                ] > 0
            ].copy()
        )

        # ====================================================
        # CREATE PERIOD
        # ====================================================

        comparison_df[
            "period_date"
        ] = pd.to_datetime(
            comparison_df["date"]
        )

        analysed_comparison_df[
            "period_date"
        ] = pd.to_datetime(
            analysed_comparison_df["date"]
        )

        score_comparison_df[
            "period_date"
        ] = pd.to_datetime(
            score_comparison_df["date"]
        )

        # ----------------------------------------------------
        # DAY
        # ----------------------------------------------------

        if comparison_period == "Day":

            comparison_df[
                "period"
            ] = (
                comparison_df[
                    "period_date"
                ].dt.date
            )

            analysed_comparison_df[
                "period"
            ] = (
                analysed_comparison_df[
                    "period_date"
                ].dt.date
            )

            score_comparison_df[
                "period"
            ] = (
                score_comparison_df[
                    "period_date"
                ].dt.date
            )

        # ----------------------------------------------------
        # WEEK
        # ----------------------------------------------------

        elif comparison_period == "Week":

            comparison_df[
                "period"
            ] = (
                comparison_df[
                    "period_date"
                ]
                .dt.to_period("W")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            analysed_comparison_df[
                "period"
            ] = (
                analysed_comparison_df[
                    "period_date"
                ]
                .dt.to_period("W")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            score_comparison_df[
                "period"
            ] = (
                score_comparison_df[
                    "period_date"
                ]
                .dt.to_period("W")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

        # ----------------------------------------------------
        # MONTH
        # ----------------------------------------------------

        elif comparison_period == "Month":

            comparison_df[
                "period"
            ] = (
                comparison_df[
                    "period_date"
                ]
                .dt.to_period("M")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            analysed_comparison_df[
                "period"
            ] = (
                analysed_comparison_df[
                    "period_date"
                ]
                .dt.to_period("M")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            score_comparison_df[
                "period"
            ] = (
                score_comparison_df[
                    "period_date"
                ]
                .dt.to_period("M")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

        # ----------------------------------------------------
        # YEAR
        # ----------------------------------------------------

        else:

            comparison_df[
                "period"
            ] = (
                comparison_df[
                    "period_date"
                ]
                .dt.to_period("Y")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            analysed_comparison_df[
                "period"
            ] = (
                analysed_comparison_df[
                    "period_date"
                ]
                .dt.to_period("Y")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

            score_comparison_df[
                "period"
            ] = (
                score_comparison_df[
                    "period_date"
                ]
                .dt.to_period("Y")
                .apply(
                    lambda x:
                    x.start_time.date()
                )
            )

        # ====================================================
        # NO DATA
        # ====================================================

        if comparison_df.empty:

            st.warning(
                "No calls available for the selected filters."
            )

        else:

            # =================================================
            # PERFORMANCE SUMMARY
            # =================================================

            st.markdown("---")

            st.subheader(
                "📊 Performance Summary"
            )

            s1, s2, s3, s4 = st.columns(4)

            # -------------------------------------------------
            # TOTAL CALLS
            # -------------------------------------------------

            with s1:

                st.metric(
                    "Total Calls",
                    len(comparison_df)
                )

            # -------------------------------------------------
            # ANALYSED CALLS
            # Score 0 INCLUDED
            # -------------------------------------------------

            with s2:

                st.metric(
                    "Analysed Calls",
                    len(
                        analysed_comparison_df
                    )
                )

            # -------------------------------------------------
            # AVG CALL SCORE
            # Score 0 EXCLUDED
            # -------------------------------------------------

            with s3:

                avg_score = (
                    score_comparison_df[
                        "overall_call_score"
                    ].mean()
                    if not score_comparison_df.empty
                    else 0
                )

                st.metric(
                    "Avg Call Score",
                    f"{avg_score:.2f}"
                )

            # -------------------------------------------------
            # AVG SALES SCORE
            # Score 0 EXCLUDED
            # -------------------------------------------------

            with s4:

                avg_sales = (
                    score_comparison_df[
                        "sales_effectiveness_score"
                    ].mean()
                    if (
                        not score_comparison_df.empty
                        and
                        "sales_effectiveness_score"
                        in score_comparison_df.columns
                    )
                    else 0
                )

                st.metric(
                    "Avg Sales Score",
                    f"{avg_sales:.2f}"
                )

            # =================================================
            # PERIOD-WISE PERFORMANCE
            # =================================================

            st.markdown("---")

            st.subheader(
                "📋 Period-wise Performance"
            )

            if not analysed_comparison_df.empty:

                # ------------------------------------------------
                # CALL COUNT
                # Score 0 INCLUDED
                # ------------------------------------------------

                period_calls = (
                    analysed_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .agg(
                        Calls=(
                            "call_id",
                            "count"
                        )
                    )
                    .reset_index()
                )

                # ------------------------------------------------
                # SCORE METRICS
                # Score 0 EXCLUDED
                # ------------------------------------------------

                if not score_comparison_df.empty:

                    period_scores = (
                        score_comparison_df
                        .groupby(
                            [
                                "period",
                                "agent_name"
                            ]
                        )
                        .agg(

                            Avg_Score=(
                                "overall_call_score",
                                "mean"
                            ),

                            Sales_Score=(
                                "sales_effectiveness_score",
                                "mean"
                            ),

                            Avg_Propensity=(
                                "propensity_score",
                                "mean"
                            )
                        )
                        .reset_index()
                    )

                    period_performance = (
                        period_calls.merge(
                            period_scores,
                            on=[
                                "period",
                                "agent_name"
                            ],
                            how="left"
                        )
                    )

                else:

                    period_performance = (
                        period_calls.copy()
                    )

                    period_performance[
                        "Avg_Score"
                    ] = None

                    period_performance[
                        "Sales_Score"
                    ] = None

                    period_performance[
                        "Avg_Propensity"
                    ] = None

                # ------------------------------------------------
                # ROUND
                # ------------------------------------------------

                for column in [
                    "Avg_Score",
                    "Sales_Score",
                    "Avg_Propensity"
                ]:

                    if column in period_performance.columns:

                        period_performance[
                            column
                        ] = (
                            period_performance[
                                column
                            ].round(2)
                        )

                st.dataframe(
                    period_performance,
                    use_container_width=True,
                    hide_index=True
                )

            # =================================================
            # PERFORMANCE CHART
            # =================================================

            st.markdown("---")

            st.subheader(
                f"📈 {comparison_metric} Trend"
            )

            # -------------------------------------------------
            # TOTAL CALLS
            # -------------------------------------------------

            if comparison_metric == "Total Calls":

                chart_df = (
                    comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .size()
                    .reset_index(
                        name="Value"
                    )
                )

            # -------------------------------------------------
            # ANALYSED CALLS
            # Score 0 INCLUDED
            # -------------------------------------------------

            elif comparison_metric == "Analysed Calls":

                chart_df = (
                    analysed_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .size()
                    .reset_index(
                        name="Value"
                    )
                )

            # -------------------------------------------------
            # AVERAGE CALL SCORE
            # Score 0 EXCLUDED
            # -------------------------------------------------

            elif comparison_metric == "Average Call Score":

                chart_df = (
                    score_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )[
                        "overall_call_score"
                    ]
                    .mean()
                    .reset_index(
                        name="Value"
                    )
                )

            # -------------------------------------------------
            # SALES EFFECTIVENESS
            # Score 0 EXCLUDED
            # -------------------------------------------------

            elif comparison_metric == "Sales Effectiveness":

                chart_df = (
                    score_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )[
                        "sales_effectiveness_score"
                    ]
                    .mean()
                    .reset_index(
                        name="Value"
                    )
                )

            # -------------------------------------------------
            # AVERAGE PROPENSITY
            # Score 0 EXCLUDED
            # -------------------------------------------------

            elif comparison_metric == "Average Propensity":

                chart_df = (
                    score_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )[
                        "propensity_score"
                    ]
                    .mean()
                    .reset_index(
                        name="Value"
                    )
                )

            # -------------------------------------------------
            # CONVERSION RATE
            #
            # Subscription Sold / Analysed Calls
            # -------------------------------------------------

            elif comparison_metric == "Conversion Rate":

                analysed_calls = (
                    analysed_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .size()
                    .reset_index(
                        name="Analysed"
                    )
                )

                sold_calls = (
                    comparison_df[
                        comparison_df[
                            "call_outcome"
                        ]
                        .astype(str)
                        .str.lower()
                        .eq(
                            "subscription sold"
                        )
                    ]
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .size()
                    .reset_index(
                        name="Sold"
                    )
                )

                chart_df = (
                    analysed_calls.merge(
                        sold_calls,
                        on=[
                            "period",
                            "agent_name"
                        ],
                        how="left"
                    )
                )

                chart_df["Sold"] = (
                    chart_df["Sold"]
                    .fillna(0)
                )

                chart_df["Value"] = (
                    chart_df["Sold"]
                    /
                    chart_df["Analysed"]
                    *
                    100
                )

                chart_df["Value"] = (
                    chart_df["Value"]
                    .round(2)
                )

            # # -------------------------------------------------
            # # MISTAKES
            # # -------------------------------------------------

            # elif comparison_metric == "Mistakes":

            #     chart_df = (
            #         comparison_df
            #         .groupby(
            #             [
            #                 "period",
            #                 "agent_name"
            #             ]
            #         )[
            #             "mistake_count"
            #         ]
            #         .sum()
            #         .reset_index(
            #             name="Value"
            #         )
            #     )

            # # -------------------------------------------------
            # # COMPLIANCE VIOLATIONS
            # # -------------------------------------------------

            # else:

            #     chart_df = (
            #         comparison_df
            #         .groupby(
            #             [
            #                 "period",
            #                 "agent_name"
            #             ]
            #         )[
            #             "compliance_violation"
            #         ]
            #         .apply(
            #             lambda x:
            #             x.astype(str)
            #             .str.lower()
            #             .isin(
            #                 [
            #                     "yes",
            #                     "true",
            #                     "1"
            #                 ]
            #             )
            #             .sum()
            #         )
            #         .reset_index(
            #             name="Value"
            #         )
            #     )

            # =================================================
            # CHART
            # =================================================

            if not chart_df.empty:

                chart_df["Value"] = (
                    chart_df["Value"].round(2)
                )

                fig_comparison = px.line(
                    chart_df,
                    x="period",
                    y="Value",
                    color="agent_name",
                    markers=True,
                    title=(
                        f"{comparison_metric} "
                        f"by {comparison_period}"
                    )
                )

                if comparison_metric == "Conversion Rate":

                    fig_comparison.update_layout(
                        xaxis_title=comparison_period,
                        yaxis_title="Conversion Rate (%)"
                    )

                    fig_comparison.update_yaxes(
                        ticksuffix="%"
                    )

                else:

                    fig_comparison.update_layout(
                        xaxis_title=comparison_period,
                        yaxis_title=comparison_metric
                    )

                st.plotly_chart(
                    fig_comparison,
                    use_container_width=True
                )

            # =================================================
            # AGENT COMPARISON
            # =================================================

            if len(selected_agents) > 1:

                st.markdown("---")

                st.subheader(
                    "👥 Agent Comparison"
                )

                # ------------------------------------------------
                # CALL COUNT
                # Score 0 INCLUDED
                # ------------------------------------------------

                comparison_calls = (
                    analysed_comparison_df
                    .groupby(
                        "agent_name"
                    )
                    .agg(
                        Calls=(
                            "call_id",
                            "count"
                        )
                    )
                    .reset_index()
                )

                # ------------------------------------------------
                # SCORE METRICS
                # Score 0 EXCLUDED
                # ------------------------------------------------

                comparison_scores = (
                    score_comparison_df
                    .groupby(
                        "agent_name"
                    )
                    .agg(

                        Avg_Score=(
                            "overall_call_score",
                            "mean"
                        ),

                        Sales_Score=(
                            "sales_effectiveness_score",
                            "mean"
                        ),

                        Avg_Propensity=(
                            "propensity_score",
                            "mean"
                        )
                    )
                    .reset_index()
                )

                comparison_summary = (
                    comparison_calls.merge(
                        comparison_scores,
                        on="agent_name",
                        how="left"
                    )
                )

                comparison_summary[
                    "Avg_Score"
                ] = (
                    comparison_summary[
                        "Avg_Score"
                    ].round(2)
                )

                comparison_summary[
                    "Sales_Score"
                ] = (
                    comparison_summary[
                        "Sales_Score"
                    ].round(2)
                )

                comparison_summary[
                    "Avg_Propensity"
                ] = (
                    comparison_summary[
                        "Avg_Propensity"
                    ].round(2)
                )

                st.dataframe(
                    comparison_summary,
                    use_container_width=True,
                    hide_index=True
                )

            # =================================================
            # PERIOD-OVER-PERIOD CHANGE
            # =================================================

            st.markdown("---")

            st.subheader(
                "🔄 Period-over-Period Change"
            )

            if not analysed_comparison_df.empty:

                # ------------------------------------------------
                # CALLS
                # Score 0 INCLUDED
                # ------------------------------------------------

                pop_calls = (
                    analysed_comparison_df
                    .groupby(
                        [
                            "period",
                            "agent_name"
                        ]
                    )
                    .agg(
                        Calls=(
                            "call_id",
                            "count"
                        )
                    )
                    .reset_index()
                )

                # ------------------------------------------------
                # SCORES
                # Score 0 EXCLUDED
                # ------------------------------------------------

                if not score_comparison_df.empty:

                    pop_scores = (
                        score_comparison_df
                        .groupby(
                            [
                                "period",
                                "agent_name"
                            ]
                        )
                        .agg(

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

                    pop_df = (
                        pop_calls.merge(
                            pop_scores,
                            on=[
                                "period",
                                "agent_name"
                            ],
                            how="left"
                        )
                    )

                else:

                    pop_df = pop_calls.copy()

                    pop_df[
                        "Avg_Score"
                    ] = None

                    pop_df[
                        "Sales_Score"
                    ] = None

                # ------------------------------------------------
                # SORT
                # ------------------------------------------------

                pop_df = (
                    pop_df
                    .sort_values(
                        [
                            "agent_name",
                            "period"
                        ]
                    )
                )

                # ------------------------------------------------
                # SCORE CHANGE
                # ------------------------------------------------

                pop_df[
                    "Score_Change_%"
                ] = (
                    pop_df
                    .groupby(
                        "agent_name"
                    )[
                        "Avg_Score"
                    ]
                    .pct_change()
                    * 100
                )

                # ------------------------------------------------
                # SALES SCORE CHANGE
                # ------------------------------------------------

                pop_df[
                    "Sales_Change_%"
                ] = (
                    pop_df
                    .groupby(
                        "agent_name"
                    )[
                        "Sales_Score"
                    ]
                    .pct_change()
                    * 100
                )

                # ------------------------------------------------
                # CALL VOLUME CHANGE
                # ------------------------------------------------

                pop_df[
                    "Calls_Change_%"
                ] = (
                    pop_df
                    .groupby(
                        "agent_name"
                    )[
                        "Calls"
                    ]
                    .pct_change()
                    * 100
                )

                pop_df = (
                    pop_df.round(2)
                )

                st.dataframe(
                    pop_df,
                    use_container_width=True,
                    hide_index=True
                )