import streamlit as st
from sales_plotly import plot_monthly_sales_trend, plot_top_product_category

# Set the page title and other configurations
st.set_page_config(
    page_title="Olist Dashboard",  # Set the title for the browser tab
    # page_icon=":shark:",  # Optional: set a favicon (use a string or path to an image)
    layout="wide",  # Optional: layout configuration (wide, centered)
)

# Main content
st.title("Olist E-commerce Performance")

# Create tabs
tab_titles = ["Sales Trend", "Product Category", "Payment Type", "Logistic", "Reviews", "Geolocation"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_titles)

with tab1:
    fig1 = plot_monthly_sales_trend(
        title='Monthly Sales Trend (Revenue & ATV)',
        fields=['Revenue', 'ATV'],
        labels=['Revenue (Thousands of Brazilian Reais)', 'ATV (Brazilian Reais)']
    )

    fig2 = plot_monthly_sales_trend(
        title='Monthly Sales Trend (Orders & AUR)',
        fields=['Orders', 'AUR'],
        labels=['Orders (Brazilian Reais)', 'AUR (Brazilian Reais)']
    )

    # st.write("Monthly Sales Trend for Revenue and ATV")
    st.plotly_chart(fig1, use_container_width=True)

    # st.write("Monthly Sales Trend for Orders and AUR")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Create sub-tabs for Product Category
    subtab_titles = ["Top Sales", "Bottom Sales"]
    subtab1, subtab2 = st.tabs(subtab_titles)

    fig1, fig2, fig3 = plot_top_product_category()

    # Content for Category Overview sub-tab
    with subtab1:
        # st.write("Top Product Category by Orders")
        st.plotly_chart(fig1, use_container_width=True)
        # st.write("Top Product Category by Revenue")
        st.plotly_chart(fig2, use_container_width=True)
        # st.write("Top Product Category by Unit")
        st.plotly_chart(fig3, use_container_width=True)
    
    # Content for Top Products sub-tab
    with subtab2:
        st.header("Lowest Products")
        # Add your top products analysis here
        # Example:
        # st.plotly_chart(plot_top_product_category())
