import os
import base64

import bcrypt
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Social Media vs Attention",
    page_icon="📱",
    layout="centered",
)

def check_password() -> bool:
    """Simple shared-password auth using a hash in st.secrets and session_state.

    Expected secret layout in `.streamlit/secrets.toml`:

    [auth]
    password_hash = "<bcrypt-hash>"
    """
    if "password_correct" in st.session_state:
        return st.session_state.password_correct

    def _submit() -> None:
        auth_conf = st.secrets.get("auth", {})
        stored_hash = auth_conf.get("password_hash")

        if not stored_hash:
            st.error("Authentication is not configured: missing auth.password_hash in secrets.")
            st.session_state.password_correct = False
            return

        try:
            ok = bcrypt.checkpw(
                st.session_state["password_input"].encode("utf-8"),
                stored_hash.encode("utf-8"),
            )
        except Exception:
            ok = False

        st.session_state.password_correct = ok

    st.title("Social Media vs Attention")
    st.subheader("Login")

    st.text_input(
        "Password",
        type="password",
        key="password_input",
        on_change=_submit,
    )

    if "password_correct" in st.session_state and not st.session_state.password_correct:
        st.error("Incorrect password. Please try again.")

    return False

def load_data() -> "st.dataframe":  # type: ignore[valid-type]
    """Fetch data from the configured Google Sheet via the gsheets connection."""

    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Sheet1", ttl="10m", usecols=[1, 2])
    # Coerce both columns to numeric; drop rows where either is not a valid number.
    if df is not None and not df.empty:
        try:
            df[df.columns[0]] = st.utils.to_numpy(df[df.columns[0]])  # type: ignore[attr-defined]
        except Exception:
            pass
    return df

def show_data_page() -> None:
    st.header("Raw Data")
    df = load_data()
    if df is None or df.empty:
        st.info("No data available yet in the sheet.")
        return
    st.dataframe(data=df, use_container_width=True)

def show_data_summary_page() -> None:
    st.header("Raw Data")
    df = load_data()
    if df is None or df.empty:
        st.info("No data available yet in the sheet.")
        return
    col_attention = df.columns[0]
    col_usage = df.columns[1]

    # Only keep rows where both columns are valid numbers
    cleaned = df[[col_attention, col_usage]].apply(pd.to_numeric, errors="coerce").dropna()
    if cleaned.empty:
        st.info("All entries are non-numeric; nothing to summarize yet.")
        return

    st.subheader("Summary statistics")
    st.write(cleaned.describe())


def show_analytics_page() -> None:
    st.header("Analytics")
    df = load_data()
    if df is None or df.empty:
        st.info("No data available yet to analyze.")
        return

    # Assume the first column is attention span and the second is social media usage
    col_attention = df.columns[0]
    col_usage = df.columns[1]

    # Drop rows with non-numeric values before plotting
    cleaned = df[[col_attention, col_usage]].apply(pd.to_numeric, errors="coerce").dropna()
    if cleaned.empty:
        st.info("All entries are non-numeric; nothing to plot yet.")
        return

    st.subheader("Attention Span vs. Social Media Ussage")
    st.scatter_chart(
        cleaned,
        x=col_attention,
        y=col_usage,
    )


def main() -> None:
    if not check_password():
        return

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Data", "Summary", "Analytics"))

    if page == "Data":
        show_data_page()
    elif page == "Summary":
        show_data_summary_page()
    else:
        show_analytics_page()


if __name__ == "__main__":
    main()