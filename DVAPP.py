import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Sample Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# LOGIN SECTION
# -----------------------------

# Hard-coded credentials
USERNAME = "joseffadmin123"
PASSWORD = "concertinaftw"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Clean page styling
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                font-family: 'Roboto', sans-serif;
                background-color: #f5f6fa;
                color: #333;
            }
            .stTextInput>div>div>input {
                font-size: 16px;
                padding: 10px;
            }
            .stButton>button {
                background-color: #1a73e8;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 16px;
                font-weight: 500;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://static.wixstatic.com/media/5d2c96_6e0bc64a5a7142f5b4c0eecb0a51d6cd~mv2.png/v1/fill/w_396,h_112,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Logo%20on%20light.png",
            width=200
        )

        st.markdown("<h5 style='text-align: left; margin-top: 10px;'>Sample Data Dashboard</h5>", unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=True):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if username_input == USERNAME and password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

else:
    # -----------------------------
    # Load & Prepare Data
    # -----------------------------

    df = pd.read_csv("Sample Structured 2025 Monthly CVJ Data.csv")

    df.columns = [col.strip().lower() for col in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = (
                    df[col]
                    .str.replace(",", "")
                    .astype(float)
                )
            except:
                pass

    try:
        df['date_parsed'] = pd.to_datetime(df['date'], format="%B %Y", errors='coerce')
    except:
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date_parsed'])

    df['month'] = df['date_parsed'].dt.strftime("%B")
    df['year'] = df['date_parsed'].dt.year.astype(str)

    df = df.sort_values('date_parsed')

    filtered_df = df.copy()

    # -----------------------------
    # Custom Styling (Material Design)
    # -----------------------------

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
            html, body, [class*="css"]  {
                font-family: 'Roboto', sans-serif;
                background-color: #ffffff;
                color: #333333;
            }
            .stButton > button {
                background-color: #1a73e8;
                color: white;
                border-radius: 4px;
                padding: 0.5em 1em;
            }
            .stSelectbox, .stTextInput {
                background: #f9f9f9;
                border-radius: 4px;
                border: 1px solid #e0e0e0;
            }
        </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Sidebar - Logo & Filters
    # -----------------------------

    with st.sidebar:
        st.image(
            "https://static.wixstatic.com/media/5d2c96_6e0bc64a5a7142f5b4c0eecb0a51d6cd~mv2.png/v1/fill/w_396,h_112,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Logo%20on%20light.png",
            width=200
        )
        
        st.markdown("### Filters")

        years = sorted(df['year'].unique())
        selected_year = st.selectbox(
            "Select Year:",
            ["All"] + list(years)
        )
        
        if selected_year != "All":
            filtered_df = filtered_df[filtered_df['year'] == selected_year]
        
        months_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        available_months = filtered_df['month'].unique()
        available_months_sorted = [m for m in months_order if m in available_months]
        
        selected_month = st.selectbox(
            "Select Month:",
            ["All"] + available_months_sorted
        )
        
        if selected_month != "All":
            filtered_df = filtered_df[filtered_df['month'] == selected_month]

        show_data = st.checkbox("Show Data Table")

    # -----------------------------
    # Header
    # -----------------------------

    st.title("Sample CVJ Data Dashboard 🎯")

    filter_text = []
    if selected_year != "All":
        filter_text.append(selected_year)
    if selected_month != "All":
        filter_text.append(selected_month)

    if filter_text:
        st.markdown(
            f"<p style='color:#666;font-size:18px;'>Data shown for: <b>{' '.join(filter_text)}</b>.</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color:#666;font-size:18px;'>Data shown for all months.</p>",
            unsafe_allow_html=True
        )

    # -----------------------------
    # Data Table
    # -----------------------------

    if show_data:
        st.subheader("Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)

    # -----------------------------
    # Charts
    # -----------------------------

    st.divider()

    # Bar Chart
    if 'date' in filtered_df.columns and 'total impressions' in filtered_df.columns:
        title = "Total Impressions" if not filter_text else f"Total Impressions for {' '.join(filter_text)}"
        fig_bar = px.bar(
            filtered_df,
            x='date',
            y='total impressions',
            title=title,
            color='total impressions',
            color_continuous_scale='Blues',
            text='total impressions'
        )
        fig_bar.update_traces(
            texttemplate='%{text:.2s}'
        )
        fig_bar.update_layout(
            template='plotly_white',
            font=dict(family='Roboto', size=14, color="#333"),
            title_font_size=22,
            yaxis_tickformat=".2s"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    if 'date' in filtered_df.columns and 'total reach' in filtered_df.columns:
        title = "Total Reach Over Time" if not filter_text else f"Total Reach for {' '.join(filter_text)}"
        fig_line = px.line(
            filtered_df,
            x='date',
            y='total reach',
            title=title,
            markers=True,
            color_discrete_sequence=["#1a73e8"]
        )
        fig_line.update_layout(
            template='plotly_white',
            yaxis_tickformat=".2s"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Pie Chart
    if 'date' in filtered_df.columns and 'total website sessions' in filtered_df.columns:
        pie_title = "Website Sessions Share by Month" if not filter_text else f"Website Sessions for {' '.join(filter_text)}"
        fig_pie = px.pie(
            filtered_df,
            names='date',
            values='total website sessions',
            title=pie_title,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(
            textinfo='percent+label'
        )
        fig_pie.update_layout(template='plotly_white')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter Plot
    if all(col in filtered_df.columns for col in ['total impressions', 'total link clicks']):
        scatter_title = "Impressions vs Link Clicks" if not filter_text else f"Impressions vs Link Clicks for {' '.join(filter_text)}"
        fig_scatter = px.scatter(
            filtered_df,
            x='total impressions',
            y='total link clicks',
            size='total impressions',
            color='date',
            title=scatter_title,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_scatter.update_layout(
            template='plotly_white',
            xaxis_tickformat=".2s",
            yaxis_tickformat=".2s"
        )
        fig_scatter.update_traces(
            hovertemplate='<b>%{text}</b><br>Total Impressions: %{x:.2s}<br>Total Link Clicks: %{y:.2s}',
            text=filtered_df['date']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)