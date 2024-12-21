import streamlit as st
from dashboard.sales_plot import plot_monthly_sales_trend, plot_top_product_category, plot_bottom_product_category

# Set the page title and other configurations
st.set_page_config(
    page_title="Olist Dashboard",  # Set the title for the browser tab
    page_icon="dashboard/files/favicon.png",  # Optional: set a favicon (use a string or path to an image)
    layout="wide",  # Optional: layout configuration (wide, centered)
)

# Main content
st.title("Olist E-commerce Performance")

# Create tabs
tab_titles = ["Sales Trend", "Product Category", "Payment Type", "Logistic", "Reviews", "Geolocation"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_titles)

with tab1:  # Sales Trend
    subtab_titles = ["Revenue & ATV", "Orders & AUR"]
    subtab1, subtab2 = st.tabs(subtab_titles)

    fig1 = plot_monthly_sales_trend(
        title='Monthly Sales Trend (Revenue & ATV)',
        fields=['Revenue', 'ATV'],
        labels=['Revenue (Thousands of Brazilian Reais)', 'ATV (Brazilian Reais)']
    )

    fig2 = plot_monthly_sales_trend(
        title='Monthly Sales Trend (Orders & AUR)',
        fields=['Orders', 'AUR'],
        labels=['Orders', 'AUR (Brazilian Reais)']
    )

    with subtab1:
        # st.write("Monthly Sales Trend for Revenue and ATV")
        st.plotly_chart(fig1, use_container_width=True)
    with subtab2:
        # st.write("Monthly Sales Trend for Orders and AUR")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:  # Product Category
    subtab_titles = ["Top Sales", "Bottom Sales"]
    subtab1, subtab2 = st.tabs(subtab_titles)

    with subtab1:
        fig1, fig2, fig3 = plot_top_product_category()
        # st.write("Top Product Category by Orders")
        st.plotly_chart(fig1, use_container_width=True)
        # st.write("Top Product Category by Revenue")
        st.plotly_chart(fig2, use_container_width=True)
        # st.write("Top Product Category by Unit")
        st.plotly_chart(fig3, use_container_width=True)

    with subtab2:
        fig1, fig2, fig3 = plot_bottom_product_category()
        # st.write("Product Category with Fewest Orders")
        st.plotly_chart(fig1, use_container_width=True)
        # st.write("Top Product Category with Lowest Revenue")
        st.plotly_chart(fig2, use_container_width=True)
        # st.write("Top Product Category with Fewest Unit Sold")
        st.plotly_chart(fig3, use_container_width=True)
