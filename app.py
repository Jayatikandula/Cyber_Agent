import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

from main import run_pipeline
from risk_model import calculate_risk
from pdf_generator import generate_pdf
from auth import auth_page
from reports_db import create_reports_table, save_report, get_user_reports

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CyberGuard AI", layout="wide")
create_reports_table()

if not auth_page():
    st.stop()

# ---------------- HEADER ----------------
st.title("🛡 CyberGuard AI")
st.caption(
    f"User: {st.session_state.user} | "
    f"Organization: {st.session_state.organization}"
)

col1, col2 = st.columns([9,1])
with col2:
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.divider()

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Threat Analyzer",
        "Threat Feed",
        "Risk Insights",
        "Action Center",
        "Analytics",
        "Reports",
        "Alerts",
        "Admin"
    ]
)

sector_filter = st.sidebar.selectbox(
    "Sector",
    ["Banking","Healthcare","Energy","Fintech"]
)

reports = get_user_reports(st.session_state.organization)

if reports:
    df = pd.DataFrame(
        reports,
        columns=["id","username","organization","report","risk_score","sector","created_at"]
    )
    df["created_at"] = pd.to_datetime(df["created_at"])
else:
    df = pd.DataFrame(columns=[
        "id","username","organization","report",
        "risk_score","sector","created_at"
    ])

# =====================================================
# OVERVIEW
# =====================================================
if page == "Overview":

    st.header("Executive Overview")

    total = len(df)
    avg_risk = df["risk_score"].mean() if total > 0 else 0
    security_score = max(0, 100 - (avg_risk * 3))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reports", total)
    col2.metric("Average Risk", round(avg_risk,2))
    col3.metric("Security Score", round(security_score,2))

# =====================================================
# THREAT ANALYZER
# =====================================================
elif page == "Threat Analyzer":

    st.header("Threat Intelligence Analyzer")

    query = st.text_input("Enter Threat Query")

    if st.button("Analyze Threat") and query.strip() != "":

        with st.spinner("Analyzing threat intelligence..."):
            report = run_pipeline(query)

        risk = calculate_risk()
        score = risk["score"]

        st.session_state.generated_report = report

        save_report(
            st.session_state.user,
            st.session_state.organization,
            report,
            score,
            sector_filter
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Score", score)
        col2.metric("Sector", sector_filter)
        col3.metric("Risk Level", risk["level"])

        st.divider()

        # Gauge
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Risk Meter"},
            gauge={'axis': {'range': [0, 25]}}
        ))

        st.plotly_chart(gauge, use_container_width=True)

        st.subheader("Threat Report")
        st.write(report)

    if "generated_report" in st.session_state:

        if st.button("Generate PDF"):
            generate_pdf(st.session_state.generated_report)

        try:
            with open("report.pdf", "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="Download Threat PDF",
                data=pdf_bytes,
                file_name="Threat_Report.pdf",
                mime="application/pdf"
            )
        except:
            pass

# =====================================================
# THREAT FEED
# =====================================================
elif page == "Threat Feed":

    st.header("Threat Feed")

    if df.empty:
        st.info("No threats yet.")
    else:
        for _, row in df.sort_values("created_at", ascending=False).iterrows():
            st.subheader(f"{row['sector']} | Risk {row['risk_score']}")
            st.caption(row["created_at"])
            st.write(row["report"])
            st.divider()

# =====================================================
# RISK INSIGHTS
# =====================================================
elif page == "Risk Insights":

    st.header("Risk Insights")

    if df.empty:
        st.info("No data.")
    else:
        avg_risk = df["risk_score"].mean()
        max_risk = df["risk_score"].max()
        vulnerable_sector = df.groupby("sector")["risk_score"].mean().idxmax()

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Risk", round(avg_risk,2))
        col2.metric("Highest Risk", max_risk)
        col3.metric("Most Vulnerable Sector", vulnerable_sector)

# =====================================================
# ACTION CENTER
# =====================================================
elif page == "Action Center":

    st.header("Action Center")

    if df.empty:
        st.info("No threats.")
    else:
        for _, row in df.iterrows():
            if row["risk_score"] >= 20:
                st.error(f"Immediate Action Required - {row['sector']}")
            elif row["risk_score"] >= 16:
                st.warning(f"Mitigation Recommended - {row['sector']}")
            else:
                st.success(f"Monitoring - {row['sector']}")

# =====================================================
# ANALYTICS
# =====================================================
elif page == "Analytics":

    st.header("Advanced Analytics")

    if df.empty:
        st.info("No analytics data.")
        st.stop()

    df["month"] = df["created_at"].dt.strftime("%Y-%m")

    # Trend Line
    monthly = df.groupby("month")["risk_score"].mean().reset_index()
    fig_trend = px.line(
        monthly,
        x="month",
        y="risk_score",
        markers=True,
        title="Monthly Risk Trend",
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Pie Chart
    sector_counts = df["sector"].value_counts().reset_index()
    sector_counts.columns = ["sector","count"]

    fig_pie = px.pie(
        sector_counts,
        names="sector",
        values="count",
        hole=0.4,
        title="Threat Distribution by Sector"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar Chart
    fig_bar = px.bar(
        df,
        x="sector",
        y="risk_score",
        color="risk_score",
        title="Risk by Sector",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Heatmap
    heat_df = df.pivot_table(
        values="risk_score",
        index="sector",
        columns="month",
        aggfunc="mean"
    )

    fig_heat = px.imshow(
        heat_df,
        aspect="auto",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# =====================================================
# REPORTS
# =====================================================
elif page == "Reports":
    if df.empty:
        st.info("No reports.")
    else:
        st.dataframe(df, use_container_width=True)

# =====================================================
# ALERTS
# =====================================================
elif page == "Alerts":
    if df.empty:
        st.info("No alerts.")
    else:
        for _, row in df.iterrows():
            if row["risk_score"] >= 20:
                st.error(f"CRITICAL | {row['sector']} | {row['risk_score']}")
            elif row["risk_score"] >= 16:
                st.warning(f"HIGH | {row['sector']} | {row['risk_score']}")
            else:
                st.success(f"NORMAL | {row['sector']} | {row['risk_score']}")

# =====================================================
# ADMIN
# =====================================================
elif page == "Admin":
    if st.session_state.role != "admin":
        st.error("Access Denied")
    else:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, role FROM users WHERE organization=?",
            (st.session_state.organization,)
        )

        users = cursor.fetchall()
        users_df = pd.DataFrame(users, columns=["Username","Role"])
        st.dataframe(users_df, use_container_width=True)

        conn.close()