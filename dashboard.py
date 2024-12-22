import streamlit as st
from dashboard.logistics_plot import plot_delivery_status, plot_delivery_value_product_category
from dashboard.map import map
from dashboard.payments_plot import plot_payment_type_orders, plot_payment_type_avg_value
from dashboard.reviews_plot import plot_review_scores
from dashboard.sales_plot import plot_monthly_sales_trend, plot_product_category
from streamlit_folium import folium_static

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
def reset_top_category():
    st.session_state.top_reset = True


def reset_bottom_category():
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
            labels=['Revenue (R$)', 'ATV (R$)']
        )
        st.plotly_chart(fig1, use_container_width=True)

    with subtab2:
        fig2 = plot_monthly_sales_trend(
            title='Monthly Sales Trend (Orders & AUR)',
            fields=['Orders', 'AUR'],
            labels=['Orders', 'AUR (R$)']
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
                if st.button(
                    "Reset",
                    key=f"reset_{config['order']}", 
                    on_click=reset_top_category if config["order"] == "top" else reset_bottom_category
                ):
                    pass

            with col1:
                # Set the default value based on reset state
                default_value = 10 if st.session_state.get(
                    f"{config['order']}_reset", False) else st.session_state.get(config["order"], 10)

                # Create the number input
                n = st.number_input(
                    f"Set # Product Category to Show",
                    min_value=1,
                    max_value=30,
                    value=default_value,
                    step=1,
                    key=config["order"]
                )

            # Reset the reset flag
            if st.session_state.get(f"{config['order']}_reset", False):
                st.session_state[f"{config['order']}_reset"] = False

            figs = plot_product_category(order=config["order"], n=n)
            columns = st.columns(3)

            for fig, col in zip(figs, columns):
                with col:
                    st.plotly_chart(fig, use_container_width=True)

with tab3:  # Payment Types
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = plot_payment_type_orders()
        st.plotly_chart(fig_pie)

    with col2:
        fig_bar = plot_payment_type_avg_value()
        st.plotly_chart(fig_bar)

with tab4:  # Logistics
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = plot_delivery_status()
        st.plotly_chart(fig_pie)

    with col2:
        fig_boxes = plot_delivery_value_product_category()
        st.plotly_chart(fig_boxes)

with tab5:  # Reviews
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:  # Center column
        fig = plot_review_scores()
        st.plotly_chart(fig, use_container_width=True)

with tab6:  # Geolocation
    col1, col2 = st.columns(2)

    with col1:  # Customers
        st.subheader("Customer Location Distribution")
        customers_map = map("customers")
        folium_static(customers_map)

    with col2:  # Sellers
        st.subheader("Sellers Location Distribution")
        sellers_map = map("sellers")
        folium_static(sellers_map)
