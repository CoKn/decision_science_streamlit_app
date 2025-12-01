# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection


st.set_page_config(
    page_title="Social Media vs Attention",
    page_icon="📱",
    layout="centered",
)


def load_data() -> "st.dataframe":  # type: ignore[valid-type]
    """Fetch data from the configured Google Sheet via the gsheets connection."""

    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Sheet1", ttl="10m", usecols=[1, 2])
    return df


def show_qr_code_page() -> None:
    ...

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

    st.subheader("Summary statistics")
    st.write(
        df.describe(
            include="all",
        )[[col_attention, col_usage]]
    )


def show_analytics_page() -> None:
    st.header("Analytics")
    df = load_data()
    if df is None or df.empty:
        st.info("No data available yet to analyze.")
        return

    # Assume the first column is attention span and the second is social media usage
    col_attention = df.columns[0]
    col_usage = df.columns[1]

    st.subheader("Attention Span vs. Social Media Ussage")
    st.scatter_chart(
        df,
        x=col_attention,
        y=col_usage,
    )


def main() -> None:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("QR Code", "Data", "Summary", "Analytics"))

    if page == "QR Code":
        show_qr_code_page()
    elif page == "Data":
        show_data_page()
    elif page == "Summary":
        show_data_summary_page()
    else:
        show_analytics_page()


if __name__ == "__main__":
    main()