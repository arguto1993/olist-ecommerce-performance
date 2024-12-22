import os
import pandas as pd
import plotly.graph_objects as go
from .theme import COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_GRAY, TITLE_FONTSIZE1

# Load Dataset
os.chdir(os.path.dirname(os.path.abspath(__file__)))
dir_dashboard_dataset = "../dataset/cleaned_for_dashboard/"
df_orders_delivered_accuracy = pd.read_csv(dir_dashboard_dataset + "orders_delivered_accuracy.csv")


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


def plot_delivery_status():
    df_orders_by_delivery_status_summary, most_delivery_status = get_orders_delivered_accuracy_data()

    pie_labels = df_orders_by_delivery_status_summary.index
    pie_count = df_orders_by_delivery_status_summary['Count']

    fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=pie_count,
        textinfo='label+percent+value',
        insidetextorientation='horizontal',
        textfont=dict(family="Arial", size=12),
        marker=dict(colors=[COLOR_BLUE, COLOR_RED, COLOR_GREEN])
    )])

    fig.update_layout(
        title=f'Most Delivery Status: {most_delivery_status}',
        titlefont=dict(size=TITLE_FONTSIZE1),
        showlegend=False
    )

    return fig
