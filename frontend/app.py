
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mobile App Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    :root {
        --nexora-orange: #F0782B;
        --nexora-orange-light: #FF9A52;
        --nexora-black: #090909;
        --nexora-panel: #191919;
        --nexora-panel-soft: #222222;
        --nexora-border: #713B20;
        --nexora-text: #F5F5F5;
        --nexora-muted: #A7A7A7;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--nexora-black);
        color: var(--nexora-text);
    }
    [data-testid="stHeader"] { background: rgba(9,9,9,0.96); }
    .block-container { padding-top: 1.15rem; padding-bottom: 2rem; max-width: 1600px; }

    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
        color: var(--nexora-text);
    }
    h1 { font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { font-weight: 700; }
    .dashboard-subtitle { color: var(--nexora-muted); font-size: 0.95rem; }

    section[data-testid="stSidebar"] {
        background: #101010;
        border-right: 1px solid var(--nexora-border);
    }
    section[data-testid="stSidebar"] * { color: #F5F5F5; }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 0.35rem 0.5rem;
        border-radius: 7px;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #302016;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #202020, #151515);
        border: 1px solid var(--nexora-border);
        border-left: 4px solid var(--nexora-orange);
        border-radius: 12px;
        padding: 17px 19px;
        min-height: 112px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.20);
    }
    [data-testid="stMetricLabel"] { color: #C8C8C8 !important; font-weight: 600; }
    [data-testid="stMetricValue"] { color: var(--nexora-orange-light) !important; font-weight: 800; }
    [data-testid="stMetricDelta"] { color: #BDBDBD !important; }

    div.stButton > button, div.stDownloadButton > button,
    button[kind="primary"], [data-testid="stFormSubmitButton"] button {
        background: var(--nexora-orange);
        color: #111111 !important;
        border: 1px solid var(--nexora-orange);
        border-radius: 8px;
        font-weight: 750;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover,
    button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover {
        background: var(--nexora-orange-light);
        border-color: var(--nexora-orange-light);
        color: #000000 !important;
    }

    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid #383838;
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stPlotlyChart"] {
        background: #171717;
        border: 1px solid #60351F;
        border-radius: 12px;
        padding: 8px 8px 2px 8px;
    }
    [data-testid="stForm"] {
        background: #171717;
        border: 1px solid #60351F;
        border-radius: 12px;
        padding: 18px;
    }
    input, textarea, [data-baseweb="select"] > div {
        background-color: #242424 !important;
        color: #F5F5F5 !important;
        border-color: #555555 !important;
    }
    hr { border-color: #393939 !important; }
    .nexora-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        background: #050505;
        border: 1px solid #8A431E;
        border-radius: 12px;
        padding: 15px 22px;
        margin: 0 0 22px 0;
        box-shadow: 0 5px 18px rgba(0,0,0,0.28);
    }
    .nexora-brand { color: var(--nexora-orange) !important; font-size: 1.55rem; font-weight: 900; white-space: nowrap; }
    .nexora-heading { color: #FFFFFF !important; font-size: 1.45rem; font-weight: 850; text-align: center; letter-spacing: 0.4px; }
    .nexora-year { color: #FFFFFF !important; font-size: 1.35rem; font-weight: 800; white-space: nowrap; }
    .nexora-kicker { color: var(--nexora-orange-light) !important; font-size: 0.72rem; font-weight: 800; letter-spacing: 2px; }
    @media (max-width: 700px) {
        .nexora-header { flex-direction: column; text-align: center; }
        .nexora-heading { font-size: 1.05rem; }
    }
</style>
""", unsafe_allow_html=True)

# Apply a consistent dark Plotly theme and Power BI-inspired orange palette.
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#F0782B", "#FF9A52", "#F5C08A", "#B85B25", "#8E8E8E"]
px.defaults.color_continuous_scale = [[0, "#3A1D10"], [0.5, "#C85D22"], [1, "#FF9A52"]]


# =========================================================
# 3. API HELPER FUNCTIONS
# =========================================================

def api_get(endpoint, params=None):

    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        st.error(f"API Connection Error: {e}")

        return None


def api_post(endpoint, payload):

    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:

        try:
            detail = response.json().get("detail", str(e))

        except Exception:
            detail = str(e)

        st.error(f"API Error: {detail}")

        return None

    except requests.exceptions.RequestException as e:

        st.error(f"API Connection Error: {e}")

        return None


def get_analytics_data(endpoint):

    result = api_get(endpoint)

    if result and isinstance(result.get("data"), list):

        return pd.DataFrame(result["data"])

    return pd.DataFrame()


# =========================================================
# 4. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.title("📊 Customer Intelligence")

    st.caption("Business Intelligence Platform")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Business Overview",
            "Customer Records",
            "Device Analytics",
            "Category Analytics",
            "Marketing Analytics",
            "Monthly Analytics",
            "Purchase Prediction",
            "Explainable AI (SHAP)"
        ]
    )

    st.divider()

    st.subheader("Backend Connection")

    if st.button(
        "Check API Connection",
        use_container_width=True
    ):

        health = api_get("/health")

        if health and health.get("status") == "healthy":

            st.success("Backend Connected")

        else:

            st.error("Backend Not Available")

    st.caption("FastAPI: 127.0.0.1:8000")

    st.divider()

    st.caption(
        "Mobile App Business Intelligence Platform"
    )

    st.caption("Version 1.0")


# =========================================================
# 5. GLOBAL NEXORA DASHBOARD HEADER
# =========================================================

st.markdown(
    """
    <div class="nexora-header">
        <div class="nexora-brand">N · NEXORA</div>
        <div>
            <div class="nexora-kicker">BUSINESS INTELLIGENCE PLATFORM</div>
            <div class="nexora-heading">E-COMMERCE INTELLIGENCE</div>
        </div>
        <div class="nexora-year">2026</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 6. BUSINESS OVERVIEW
# =========================================================

if page == "Business Overview":

    st.title("📊 Business Overview")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Monitor your mobile app business performance and KPIs.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    result = api_get(
        "/api/v1/customers/summary"
    )

    if result and "summary" in result:

        summary = result["summary"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Records",
            f"{summary.get('total_records', 0):,}"
        )

        col2.metric(
            "Total Purchases",
            f"{summary.get('total_purchases', 0):,}"
        )

        col3.metric(
            "Conversion Rate",
            f"{summary.get('purchase_conversion_rate', 0)}%"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Non Purchases",
            f"{summary.get('total_non_purchases', 0):,}"
        )

        col5.metric(
            "Total Revenue",
            f"₹{summary.get('total_revenue', 0):,.2f}"
        )

        col6.metric(
            "Average Order Value",
            f"₹{summary.get('average_order_value', 0):,.2f}"
        )

    else:

        st.warning(
            "Business summary data is not available."
        )

    st.divider()

    st.subheader("Monthly Revenue Trend")

    monthly_df = get_analytics_data(
        "/api/v1/customers/analytics/monthly"
    )

    if not monthly_df.empty:

        if {
            "visit_month",
            "total_revenue"
        }.issubset(monthly_df.columns):

            fig = px.line(
                monthly_df,
                x="visit_month",
                y="total_revenue",
                markers=True,
                title="Monthly Revenue",
                labels={
                    "visit_month": "Month",
                    "total_revenue": "Revenue"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.dataframe(
                monthly_df,
                use_container_width=True
            )

    else:

        st.info("Monthly analytics are not available.")


# =========================================================
# 7. CUSTOMER RECORDS
# =========================================================

elif page == "Customer Records":

    st.title("👥 Customer Records")

    st.write(
        "Explore, filter, sort and paginate customer records."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        page_number = st.number_input(
            "Page Number",
            min_value=1,
            value=1
        )

    with col2:

        limit = st.selectbox(
            "Records Per Page",
            [10, 20, 50, 100]
        )

    with col3:

        device_filter = st.selectbox(
            "Device Type",
            ["All", "0", "1", "2"]
        )

    col4, col5 = st.columns(2)

    with col4:

        purchase_filter = st.selectbox(
            "Purchase Status",
            [
                "All",
                "Purchased",
                "Not Purchased"
            ]
        )

    with col5:

        sort_by = st.selectbox(
            "Sort By",
            [
                "revenue",
                "unit_price",
                "quantity"
            ]
        )

    order = st.selectbox(
        "Sort Order",
        ["desc", "asc"]
    )

    params = {
        "page": page_number,
        "limit": limit,
        "sort_by": sort_by,
        "order": order
    }

    if device_filter != "All":

        params["device_type"] = int(device_filter)

    if purchase_filter == "Purchased":

        params["purchased"] = 1

    elif purchase_filter == "Not Purchased":

        params["purchased"] = 0

    if st.button(
        "Apply Filters",
        type="primary"
    ):

        result = api_get(
            "/api/v1/customers",
            params=params
        )

        if result:

            records = result.get("data", [])

            pagination = result.get(
                "pagination",
                {}
            )

            st.metric(
                "Total Matching Records",
                pagination.get("total_records", 0)
            )

            if records:

                df = pd.DataFrame(records)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Customer Records",
                    data=csv,
                    file_name="customer_records.csv",
                    mime="text/csv"
                )

            else:

                st.info("No customer records found.")

            st.write(
                f"Page {pagination.get('page', 1)} "
                f"of {pagination.get('total_pages', 1)}"
            )


# =========================================================
# 8. DEVICE ANALYTICS
# =========================================================

elif page == "Device Analytics":

    st.title("📱 Device Analytics")

    st.write(
        "Understand customer behaviour across devices."
    )

    df = get_analytics_data(
        "/api/v1/customers/analytics/device"
    )

    if not df.empty:

        st.subheader("Device Analytics Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        if {
            "device_type",
            "total_records"
        }.issubset(df.columns):

            col1, col2 = st.columns(2)

            with col1:

                fig = px.bar(
                    df,
                    x="device_type",
                    y="total_records",
                    title="Records by Device Type"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col2:

                if "conversion_rate" in df.columns:

                    fig = px.bar(
                        df,
                        x="device_type",
                        y="conversion_rate",
                        title="Device Conversion Rate"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

    else:

        st.info("Device analytics are not available.")


# =========================================================
# 9. PRODUCT CATEGORY ANALYTICS
# =========================================================

elif page == "Category Analytics":

    st.title("🛍️ Product Category Analytics")

    st.write(
        "Analyse performance across product categories."
    )

    df = get_analytics_data(
        "/api/v1/customers/analytics/category"
    )

    if not df.empty:

        st.subheader("Category Analytics Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        if {
            "product_category",
            "total_revenue"
        }.issubset(df.columns):

            with col1:

                fig = px.bar(
                    df,
                    x="product_category",
                    y="total_revenue",
                    title="Revenue by Product Category"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if {
            "product_category",
            "total_purchases"
        }.issubset(df.columns):

            with col2:

                fig = px.pie(
                    df,
                    names="product_category",
                    values="total_purchases",
                    title="Purchases by Category"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    else:

        st.info("Category analytics are not available.")


# =========================================================
# 10. MARKETING CHANNEL ANALYTICS
# =========================================================

elif page == "Marketing Analytics":

    st.title("📢 Marketing Channel Analytics")

    st.write(
        "Evaluate the performance of marketing channels."
    )

    df = get_analytics_data(
        "/api/v1/customers/analytics/channel"
    )

    if not df.empty:

        st.subheader("Marketing Channel Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        if {
            "marketing_channel",
            "total_revenue"
        }.issubset(df.columns):

            with col1:

                fig = px.bar(
                    df,
                    x="marketing_channel",
                    y="total_revenue",
                    title="Revenue by Marketing Channel"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if {
            "marketing_channel",
            "conversion_rate"
        }.issubset(df.columns):

            with col2:

                fig = px.bar(
                    df,
                    x="marketing_channel",
                    y="conversion_rate",
                    title="Marketing Conversion Rate"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    else:

        st.info("Marketing analytics are not available.")


# =========================================================
# 11. MONTHLY ANALYTICS
# =========================================================

elif page == "Monthly Analytics":

    st.title("📅 Monthly Business Analytics")

    st.write(
        "Monitor monthly revenue and purchase behaviour."
    )

    df = get_analytics_data(
        "/api/v1/customers/analytics/monthly"
    )

    if not df.empty:

        st.subheader("Monthly Analytics Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        if {
            "visit_month",
            "total_revenue"
        }.issubset(df.columns):

            with col1:

                fig = px.line(
                    df,
                    x="visit_month",
                    y="total_revenue",
                    markers=True,
                    title="Monthly Revenue"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if {
            "visit_month",
            "total_purchases"
        }.issubset(df.columns):

            with col2:

                fig = px.bar(
                    df,
                    x="visit_month",
                    y="total_purchases",
                    title="Monthly Purchases"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    else:

        st.info("Monthly analytics are not available.")


# =========================================================
# 12. PURCHASE PREDICTION - RANDOM FOREST
# =========================================================

elif page == "Purchase Prediction":

    st.title("🤖 Customer Purchase Prediction")

    st.write(
        "Predict whether a customer will purchase a product "
        "using the trained Random Forest model."
    )

    st.divider()

    with st.form("prediction_form"):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.subheader("Customer Information")

            device_type = st.selectbox(
                "Device Type",
                [0, 1, 2]
            )

            user_type = st.selectbox(
                "User Type",
                [0, 1]
            )

            location = st.number_input(
                "Location Code",
                min_value=0,
                value=10
            )

            visit_day = st.number_input(
                "Visit Day",
                min_value=1,
                max_value=31,
                value=12
            )

            visit_month = st.number_input(
                "Visit Month",
                min_value=1,
                max_value=12,
                value=11
            )

            visit_weekday = st.selectbox(
                "Visit Weekday",
                list(range(7))
            )

            visit_season = st.selectbox(
                "Visit Season",
                list(range(4))
            )

        with col2:

            st.subheader("Product Information")

            product_id = st.number_input(
                "Product ID",
                min_value=0,
                value=10
            )

            product_category = st.selectbox(
                "Product Category",
                list(range(8))
            )

            unit_price = st.number_input(
                "Unit Price",
                min_value=0.01,
                value=500.0
            )

            quantity = st.selectbox(
                "Quantity",
                [1, 2, 3, 4]
            )

            discount_percent = st.slider(
                "Discount Percentage",
                min_value=0,
                max_value=30,
                value=10
            )

        with col3:

            st.subheader("Session Information")

            marketing_channel = st.selectbox(
                "Marketing Channel",
                list(range(6))
            )

            pages_viewed = st.number_input(
                "Pages Viewed",
                min_value=1,
                value=5
            )

            time_on_site_sec = st.number_input(
                "Time on Site (Seconds)",
                min_value=1,
                value=300
            )

            added_to_cart = st.selectbox(
                "Added to Cart",
                [0, 1],
                format_func=lambda x: (
                    "Yes" if x == 1 else "No"
                )
            )

            session_duration_bucket = st.selectbox(
                "Session Duration",
                [
                    "Short",
                    "Very Short",
                    "Long",
                    "Very Long"
                ]
            )

        submitted = st.form_submit_button(
            "Predict Purchase",
            type="primary",
            use_container_width=True
        )

    if submitted:

        payload = {

            "device_type": device_type,
            "user_type": user_type,
            "marketing_channel": marketing_channel,
            "product_id": product_id,
            "product_category": product_category,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_percent": discount_percent,
            "pages_viewed": pages_viewed,
            "time_on_site_sec": time_on_site_sec,
            "added_to_cart": added_to_cart,
            "visit_day": visit_day,
            "visit_month": visit_month,
            "visit_weekday": visit_weekday,
            "visit_season": visit_season,
            "session_duration_bucket": session_duration_bucket,
            "location": location
        }

        result = api_post(
            "/api/v1/predict",
            payload
        )

        if result:

            st.session_state["last_prediction_input"] = payload

            st.session_state["last_prediction_result"] = result

            st.divider()

            st.subheader("Prediction Result")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Prediction",
                result["prediction_label"]
            )

            col2.metric(
                "Purchase Probability",
                f"{result['purchase_probability'] * 100:.2f}%"
            )

            col3.metric(
                "No Purchase Probability",
                f"{result['no_purchase_probability'] * 100:.2f}%"
            )

            st.progress(
                max(
                    0.0,
                    min(
                        1.0,
                        float(result["purchase_probability"])
                    )
                )
            )

            if result["prediction"] == 1:

                st.success(
                    "The model predicts that this customer "
                    "is likely to purchase."
                )

            else:

                st.warning(
                    "The model predicts that this customer "
                    "is unlikely to purchase."
                )


# =========================================================
# 13. EXPLAINABLE AI - SHAP
# =========================================================

elif page == "Explainable AI (SHAP)":

    st.title("💡 Explainable AI Dashboard")

    st.write(
        "Understand which features influence the "
        "Random Forest purchase prediction using SHAP."
    )

    st.divider()

    if "last_prediction_input" not in st.session_state:

        st.info(
            "First generate a prediction on the Purchase "
            "Prediction page. Then return here to explain it."
        )

    else:

        st.subheader("Prediction to Explain")

        prediction = st.session_state.get(
            "last_prediction_result",
            {}
        )

        if prediction:

            st.metric(
                "Previous Prediction",
                prediction.get("prediction_label", "N/A")
            )

        if st.button(
            "Generate SHAP Explanation",
            type="primary"
        ):

            payload = st.session_state[
                "last_prediction_input"
            ]

            result = api_post(
                "/api/v1/explain",
                payload
            )

            if result:

                explanation = result.get(
                    "explanation",
                    {}
                )

                # Supports either a direct list of features
                # or a dictionary containing top_features.

                if isinstance(explanation, list):

                    features = explanation

                elif isinstance(explanation, dict):

                    features = explanation.get(
                        "top_features",
                        explanation.get("features", [])
                    )

                else:

                    features = []

                if features:

                    shap_df = pd.DataFrame(features)

                    st.subheader(
                        "Top Influencing Features"
                    )

                    st.dataframe(
                        shap_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    if {
                        "feature",
                        "shap_value"
                    }.issubset(shap_df.columns):

                        shap_df["impact"] = shap_df[
                            "shap_value"
                        ].apply(
                            lambda x: (
                                "Positive"
                                if x > 0
                                else "Negative"
                            )
                        )

                        shap_df = shap_df.sort_values(
                            "shap_value"
                        )

                        fig = px.bar(
                            shap_df,
                            x="shap_value",
                            y="feature",
                            color="impact",
                            orientation="h",
                            title="SHAP Feature Contributions",
                            labels={
                                "shap_value": "SHAP Value",
                                "feature": "Feature"
                            }
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    st.caption(
                        "Positive SHAP values push the model "
                        "output towards the purchase class. "
                        "Negative values push it away. "
                        "They represent model contributions, "
                        "not direct probability changes."
                    )

                else:

                    st.warning(
                        "No SHAP feature contributions returned. "
                        "Check the backend explanation response."
                    )


# =========================================================
# 14. FOOTER
# =========================================================

st.divider()

st.caption(
    "Mobile App Business Intelligence & Customer "
    "Intelligence Platform"
)

st.caption(
    "Built with Python | Streamlit | FastAPI | "
    "Machine Learning | Explainable AI"
)
