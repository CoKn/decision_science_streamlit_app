# Decision Science Streamlit App

Simple Streamlit tool that collects perceived attention spans and daily social media usage, then compares the two on a scatter plot.

## Features

- Two-page interface that separates data entry from visualization
- Validated numeric inputs for attention span (minutes) and social media usage (minutes)
- Interactive Altair scatter plot with tooltips and zoom/pan
- Optional table preview plus a quick way to clear collected entries

## Getting Started

1. Install dependencies (uv is recommended because the project already uses it):

```bash
uv sync
```

Or, if you prefer pip:

```bash
pip install -e .
```

1. Launch the app:

```bash
streamlit run main.py
```

## Configure Google Sheets persistence

1. Create/choose a Google Cloud project, enable the **Google Sheets API**, and create a **service account** with a JSON key file.
2. Share the target Google Sheet with the service account email (Editor access). Create a worksheet named `responses` (or change the value below).
3. Add the following to `.streamlit/secrets.toml` (values copied from the JSON key):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "sheet-writer@your-project-id.iam.gserviceaccount.com"
client_id = "..."

[google_sheet]
id = "<spreadsheet_id_from_url>"
# Optional: override the worksheet/tab name (defaults to "responses")
worksheet = "responses"
```

When these secrets are present, new submissions are appended to the shared sheet (with a UTC timestamp) and both the table and scatter plot read directly from it. Without secrets the app gracefully falls back to in-memory session storage.

## Usage

1. Use the **Data Entry** page (default) to add one or more anonymous responses.
2. Switch to **Scatter Plot** in the sidebar to see how the submissions relate.
3. Use **Clear all entries** on the entry page whenever you want to start fresh.

