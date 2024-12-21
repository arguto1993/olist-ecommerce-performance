import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Define colors
color_green = '#00e656'  # Green
color_blue = '#0098FF'  # Blue
color_red = '#FF4B4B'  # Red for negative / bad context
color_gray = '#CCCCCC'  # Gray for unhighlighted
title_fontsize1 = 20
title_fontsize2 = 14

# Load Dataset
os.chdir(os.path.dirname(os.path.abspath(__file__)))
dir_dashboard_dataset = "../dataset/cleaned_for_dashboard/"
df_orders_monthly = pd.read_csv(dir_dashboard_dataset + "orders_monthly.csv")
df_orders_sales_by_product_category = pd.read_csv(dir_dashboard_dataset + "orders_sales_by_product_category.csv")

# Ensure 'Year_Month' is in datetime format
df_orders_monthly['Year_Month'] = pd.to_datetime(df_orders_monthly['Year_Month'])


def plot_monthly_sales_trend(title, fields, labels):
    """Plot monthly sales trend with two y-axes for different metrics using Plotly."""

    # Create a figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add first metric to the primary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_orders_monthly['Year_Month'],
            y=df_orders_monthly[fields[0]],
            mode='lines+markers',
            name=labels[0],
            line=dict(color=color_green, width=3),
            marker=dict(symbol='square')
        ),
        secondary_y=False
    )

    # Add second metric to the secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_orders_monthly['Year_Month'],
            y=df_orders_monthly[fields[1]],
            mode='lines+markers',
            name=labels[1],
            line=dict(color=color_blue, width=3),
            marker=dict(symbol='square')
        ),
        secondary_y=True
    )

    # Update layout with titles and axis labels
    fig.update_layout(
        title=title,
        title_font=dict(size=title_fontsize1),
        yaxis_title=labels[0],
        yaxis2_title=labels[1],
        showlegend=True,
        height=600,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # Update y-axes properties
    fig.update_yaxes(title_text=labels[0], showgrid=False, secondary_y=False)
    fig.update_yaxes(title_text=labels[1], showgrid=False, secondary_y=True)

    return fig


def get_product_category_data(order='top'):
    """
    Get product category data sorted by orders, revenue, and unit, 
    and add ranks for the specified order ('top' or 'bottom').
    """
    ascending = True if order == 'bottom' else False
    rank_range = range(len(df_orders_sales_by_product_category), 0, -1) if order == 'bottom' else range(1, len(df_orders_sales_by_product_category) + 1)

    # Sort by 'orders' and add rank
    df_category_orders = (
        df_orders_sales_by_product_category
        .sort_values(by='orders', ascending=ascending)
        .reset_index(drop=True)
    )
    df_category_orders['orders_rank'] = rank_range

    # Sort by 'revenue' and add rank
    df_category_revenue = (
        df_orders_sales_by_product_category
        .sort_values(by='revenue', ascending=ascending)
        .reset_index(drop=True)
    )
    df_category_revenue['revenue_rank'] = rank_range

    # Sort by 'unit' and add rank
    df_category_unit = (
        df_orders_sales_by_product_category
        .sort_values(by='unit', ascending=ascending)
        .reset_index(drop=True)
    )
    df_category_unit['unit_rank'] = rank_range

    return df_category_orders, df_category_revenue, df_category_unit


def plot_product_category(order='top', n=10):
    """
    Plot product category data for top or bottom categories based on orders, revenue, and unit sold.
    """
    # Get data
    df_category_orders, df_category_revenue, df_category_unit = get_product_category_data(order=order)

    # Define title and fields
    color = color_green if order == 'top' else color_red
    if order == 'top':
        title_field_df_dict = {
            f"Top {n} Product Categories by Orders": ['orders', df_category_orders],
            f"Top {n} Product Categories by Revenue (Brazilian Reais)": ['revenue', df_category_revenue],
            f"Top {n} Product Categories by Units Sold": ['unit', df_category_unit],
        }
    else:
        title_field_df_dict = {
            f"{n} Product Categories with Fewest Orders": ['orders', df_category_orders],
            f"{n} Product Categories with Lowest Revenue (Brazilian Reais)": ['revenue', df_category_revenue],
            f"{n} Product Categories with Fewest Unit Sold": ['unit', df_category_unit],
        }

    figs = []

    # Plot bar charts
    for title, field_df in title_field_df_dict.items():
        df_category_10 = field_df[1][['product_category_name_english', field_df[0], f'{field_df[0]}_rank']].head(n)
        df_category_10 = df_category_10.sort_values(field_df[0], ascending=(order == 'top'))  # Reverse sorting for bottom categories

        # Create a horizontal bar chart
        fig = go.Figure(data=[go.Bar(
            y=df_category_10['product_category_name_english'],
            x=df_category_10[field_df[0]],
            orientation='h',
            marker=dict(color=color),
            text=df_category_10[field_df[0]].apply(lambda x: f'{x:,.0f}'),
            textposition='outside'
        )])

        # Update layout
        fig.update_layout(
            title=title,
            title_font=dict(size=title_fontsize2),
            xaxis=dict(
                visible=False  # Remove the x-axis entirely, including values
            ),
            yaxis=dict(showgrid=False),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
        )

        figs.append(fig)

    return figs
