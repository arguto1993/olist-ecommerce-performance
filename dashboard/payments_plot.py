import pandas as pd
import plotly.graph_objects as go
from .constants import *

# Load Dataset
df_payments = pd.read_csv(DIR_CLEAN_DATASET + "payments_clean.csv")


def get_payment_type_orders_data():
    # Group by 'payment_type' and calculate the number of unique orders, then sort by 'orders' in descending order
    df_payment_types_orders = (
        df_payments.groupby('payment_type')
        .agg(orders=('order_id', 'nunique'))
        .sort_values(by='orders', ascending=False)
    )

    # Sort the data in descending order
    sorted_data = df_payment_types_orders.sort_values('orders', ascending=False)

    # Get the top payment type
    top_payment_type = sorted_data.index[0]
    top_payment_orders = sorted_data.loc[top_payment_type, 'orders']

    # Sum up the rest of the payment types
    other_payment_types = sorted_data.iloc[1:]
    other_orders = other_payment_types['orders'].sum()

    return top_payment_type, top_payment_orders, other_orders


def get_payment_type_avg_value_data():
    df_payment_types_avg_value = (
        df_payments.groupby('payment_type')
        .agg(avg_value=('payment_value', 'mean'))
        .sort_values(by='avg_value', ascending=False)
    )

    # Sort values by 'avg_value' for better visual ordering
    df_payment_types_avg_value = df_payment_types_avg_value.sort_values('avg_value', ascending=False)

    return df_payment_types_avg_value


def plot_payment_type_orders():
    top_payment_type, top_payment_orders, other_orders = get_payment_type_orders_data()
    pie_labels = [top_payment_type, 'Other Payment Types']
    pie_orders = [top_payment_orders, other_orders]

    fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=pie_orders,
        textinfo='label+percent+value',
        insidetextorientation='horizontal',
        textfont=dict(family="Arial", size=12),
        marker=dict(colors=[COLOR_GREEN, COLOR_GRAY])
    )])

    fig.update_layout(
        title=f'Top Payment Type by Orders: {top_payment_type}',
        titlefont=dict(size=TITLE_FONTSIZE1),
        showlegend=False
    )

    return fig


def plot_payment_type_avg_value():
    df_payment_types_avg_value = get_payment_type_avg_value_data()

    fig = go.Figure(data=[go.Bar(
        x=df_payment_types_avg_value.index,
        y=df_payment_types_avg_value['avg_value'],
        marker_color=COLOR_GREEN
    )])

    # Add data labels
    for i, value in enumerate(df_payment_types_avg_value['avg_value']):
        fig.add_annotation(
            x=df_payment_types_avg_value.index[i],
            y=value,
            text=f"{value:,.2f}",
            showarrow=False,
            font=dict(color='white'),
            yshift=15  # Adjust the position above the bar
        )

    fig.update_layout(
        title="Average Payment Value by Payment Type (R$)",
        titlefont=dict(size=TITLE_FONTSIZE1),
        yaxis=dict(visible=False),  # Remove the y-axis entirely, including values
        showlegend=False
    )

    return fig
