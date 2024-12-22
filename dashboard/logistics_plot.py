import pandas as pd
import plotly.graph_objects as go
from .constants import *
from plotly.subplots import make_subplots

# Load Dataset
df_orders_delivered_accuracy = pd.read_csv(DIR_DASHBOARD_DATASET + "orders_delivered_accuracy.csv")
df_orders_product_category_freight = pd.read_csv(DIR_DASHBOARD_DATASET + "orders_product_category_freight.csv")


def get_orders_delivered_accuracy_data():
    orders_by_delivery_status = df_orders_delivered_accuracy.groupby('delivery_status')['order_id'].count()

    # Calculate the percentage
    total_orders = orders_by_delivery_status.sum()
    percentage_by_delivery_status = (orders_by_delivery_status / total_orders) * 100

    # Combine counts and percentages into a single DataFrame
    df_orders_by_delivery_status_summary = pd.DataFrame({
        'Count': orders_by_delivery_status,
        'Percentage': percentage_by_delivery_status
    })

    # Sort the data in descending order
    sorted_data = df_orders_by_delivery_status_summary.sort_values('Count', ascending=False)

    # Get the top payment type
    most_delivery_status = sorted_data.index[0]

    return df_orders_by_delivery_status_summary, most_delivery_status


def get_delivery_value_product_category_data():
    return df_orders_product_category_freight


def plot_delivery_status():
    df_orders_by_delivery_status_summary, most_delivery_status = get_orders_delivered_accuracy_data()

    pie_labels = df_orders_by_delivery_status_summary.index
    pie_count = df_orders_by_delivery_status_summary['Count']

    fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=pie_count,
        textinfo='label+percent',
        insidetextorientation='horizontal',
        textfont=dict(family="Arial", size=12),
        marker=dict(colors=[COLOR_BLUE, COLOR_RED, COLOR_GREEN]),
    )])

    fig.update_layout(
        title=f'Most Delivery Status: {most_delivery_status}',
        titlefont=dict(size=TITLE_FONTSIZE1),
        showlegend=False,
        margin=dict(l=40, r=40, t=100, b=40)
    )

    return fig


def plot_delivery_value_product_category():
    df_orders_product_category_freight = get_delivery_value_product_category_data()
    numeric_columns = df_orders_product_category_freight[['total_freight_value', 'avg_freight_value']]

    fig = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.3,  # Increased spacing for better title placement
        subplot_titles=[
            'Total Freight Value Per Product Category',
            'Average Freight Value Per Product Category'
        ]
    )

    for i, column in enumerate(numeric_columns.columns):
        fig.add_trace(
            go.Box(
                x=numeric_columns[column],
                name=column,
                boxmean=False,
                marker_color=COLOR_RED,
                line_color='white',
                whiskerwidth=1,
                orientation='h',
                showlegend=False,
                notched=False,  # Remove violin plot lines
                hoverinfo='name'  # Show only the box name in the ho
            ),
            row=i + 1,
            col=1
        )

        # Calculate statistics
        min_value = numeric_columns[column].min()
        max_value = numeric_columns[column].max()
        mean_value = numeric_columns[column].mean()
        median_value = numeric_columns[column].median()

        # Add annotations with exact positioning as shown in the image
        annotations = [
            dict(
                x=min_value,
                y=1,
                text=f'Min: {min_value:,.2f}',
                showarrow=False,
                font=dict(color=COLOR_GREEN),
                xref=f'x{i+1}',
                yref=f'y{i+1}'
            ),
            dict(
                x=max_value,
                y=1,
                text=f'Max: {max_value:,.2f}',
                showarrow=False,
                font=dict(color=COLOR_GREEN),
                xref=f'x{i+1}',
                yref=f'y{i+1}'
            ),
            dict(
                x=median_value,
                y=1.5,
                text=f'Median: {median_value:,.2f}',
                showarrow=False,
                font=dict(color='white'),
                xref=f'x{i+1}',
                yref=f'y{i+1}'
            ),
            dict(
                x=mean_value,
                y=1,
                text=f'Average: {mean_value:,.2f}',
                showarrow=False,
                font=dict(color=COLOR_BLUE),
                xref=f'x{i+1}',
                yref=f'y{i+1}'
            )
        ]

        for annotation in annotations:
            fig.add_annotation(annotation)

    fig.update_layout(
        title=dict(
            text='Freight Value Per Product Category (R$)',
            font=dict(size=TITLE_FONTSIZE1),
        ),
        showlegend=False,
        height=440,
        margin=dict(l=40, r=40, t=100, b=40),
        yaxis=dict(showticklabels=False),
        yaxis2=dict(showticklabels=False),
    )

    return fig
