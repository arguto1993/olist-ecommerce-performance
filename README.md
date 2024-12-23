# **Olist E-Commerce Performance Analysis**

## About the Dataset

This project analyzes the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), a comprehensive dataset that includes sales, customer reviews, logistics, and geolocation data. It serves as the foundation for addressing key business questions and building a performance dashboard.

## Business Questions

### **Sales**  
1. What are the trends in sales metrics (orders, revenue, units sold, Average Transaction Value (ATV), Average Unit Revenue (AUR)) over the past months?  
2. Which product categories have the highest sales in terms of orders, revenue, and units sold?  
3. Which product categories have the lowest sales in terms of orders, revenue, and units sold?  

### **Payment Type**  
4. What is the most frequently used payment method?  
5. What is the average payment value for each payment method?  

### **Logistics**  
6. How accurate are the estimated delivery dates compared to the actual delivery dates?  
7. What are the minimum, maximum, and average shipping costs per product category (both in total and average per order)?  

### **Customer Satisfaction**  
8. What is the overall customer satisfaction level based on review scores?  

### **Geolocation**  
9. How are customers and sellers distributed geographically?  

## Notebook Contents

The notebook includes the following sections:

1. **Business Questions**: Outlines the objectives of the analysis.  
2. **Import Packages & Libraries**: Prepares the environment for analysis.  
3. **Data Wrangling**: Processes the data through gathering, assessing, and cleaning.  
4. **Exploratory Data Analysis (EDA)**: Identifies trends, patterns, and anomalies.  
5. **Visualization & Explanatory Data Analysis (ExDA)**: Provides insights through visualizations.  
6. **Geospatial Analysis**: Examines geographic distributions.  
7. **Saving Dataset for Dashboard**: Prepares cleaned data for visualization tools.  
8. **Conclusion**: Summarizes findings and actionable insights.  

## Dashboard Contents

### **Sales Trend**  
- **Line Charts**: Monthly Sales Trend (Revenue & ATV)
- **Line Charts**: Monthly Sales Trend (Orders, and AUR)  

### **Product Category**  
- **Horizontal Bar Charts**:  
  - Top product categories by orders, revenue, and units sold.  
  - Bottom product categories by orders, revenue, and units sold.  

### **Payment Type**  
- **Pie Chart**: Most frequently used payment methods.  
- **Bar Chart**: Average payment values by payment method.  

### **Logistics**  
- **Pie Chart**: Distribution of delivery statuses.  
- **Boxplots**: Freight costs per product category.  

### **Reviews**  
- **Bar Chart**: Review score frequency distribution.  

### **Geolocation**  
- **Map**: Customers Location Distribution
- **Map**: Sellers Location Distribution

## Live Dashboard

**[Access Live Dashboard Here](https://olist-ecommerce-performance-dashboard.streamlit.app/)**  

> **Note**: The geolocation tab is temporarily unavailable due to memory constraints on Streamlit Cloud. Efforts are underway to optimize and re-enable this feature.  

**[Watch Live & Local Dashboard Preview](https://youtu.be/WHZXjThvnz4)**

## Local Installation Guide

To run the dashboard locally:

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/arguto1993/olist-ecommerce-performance.git
   cd olist-ecommerce-performance```

2. **Install Dependencies**:

   Ensure you have Python installed. Use the following command to install the required packages:
   ```bash
   pip install -r requirements.txt```

3. **Run the App**:

   Launch the Streamlit app with::
   ```bash
   streamlit run dashboard.py```

4. **Access the Dashboard**:

   Open the URL provided in the terminal (default: http://localhost:8501) to view the dashboard.

## License

This project is developed as part of my submission for the Dicoding Indonesia Data Science Bootcamp Batch 4 (2024).  

If you find this project helpful or have ideas for improvements, I’d love to hear from you! Thank you :)