import streamlit as st
from dashboard.sales_plot import (
    plot_monthly_sales_trend, plot_product_category)

# Set the page title and other configurations
st.set_page_config(
    page_title="Olist Ecommerce Dashboard",
    page_icon="../dashboard/files/favicon.png",
    layout="wide",
)

# Initialize session state for reset functionality
if 'top_reset' not in st.session_state:
    st.session_state.top_reset = False
if 'bottom_reset' not in st.session_state:
    st.session_state.bottom_reset = False


# Reset handlers
def reset_top():
    st.session_state.top_reset = True


def reset_bottom():
    st.session_state.bottom_reset = True


# Main content
st.title("Olist E-commerce Performance")

# Create tabs
tab_titles = ["Sales Trend", "Product Category", "Payment Type", "Logistic", "Reviews", "Geolocation"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_titles)

with tab1:  # Sales Trend
    subtab_titles = ["Revenue & ATV", "Orders & AUR"]
    subtab1, subtab2 = st.tabs(subtab_titles)

    with subtab1:
        fig1 = plot_monthly_sales_trend(
            title='Monthly Sales Trend (Revenue & ATV)',
            fields=['Revenue', 'ATV'],
            labels=['Revenue (Thousands of Brazilian Reais)', 'ATV (Brazilian Reais)']
        )
        st.plotly_chart(fig1, use_container_width=True)

    with subtab2:
        fig2 = plot_monthly_sales_trend(
            title='Monthly Sales Trend (Orders & AUR)',
            fields=['Orders', 'AUR'],
            labels=['Orders', 'AUR (Brazilian Reais)']
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:  # Product Category
    subtab_config = [
        {"title": "Top Sales", "order": "top"},
        {"title": "Bottom Sales", "order": "bottom"},
    ]
    subtabs = st.tabs([config["title"] for config in subtab_config])

    for subtab, config in zip(subtabs, subtab_config):
        with subtab:
            col1, col2 = st.columns([1,2], border=False, gap="small", vertical_alignment="bottom")

            with col2:
                # Handle reset before creating the number_input
                if st.button("Reset", key=f"reset_{config['order']}", on_click=reset_top if config["order"] == "top" else reset_bottom):
                    pass

            with col1:
                # Set the default value based on reset state
                default_value = 10 if st.session_state.get(f"{config['order']}_reset", False) else st.session_state.get(config["order"], 10)

                # Create the number input
                n = st.number_input(
                    f"Set Product Category count to Show",
                    min_value=1,
                    max_value=50,
                    value=default_value,
                    step=1,
                    key=config["order"]
                )

            # Reset the reset flag
            if st.session_state.get(f"{config['order']}_reset", False):
                st.session_state[f"{config['order']}_reset"] = False

            # Display the charts
            figs = plot_product_category(order=config["order"], n=n)
            for fig in figs:
                st.plotly_chart(fig, use_container_width=True)