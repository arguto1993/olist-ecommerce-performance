import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define colors & font size
color_green = '#009739'  # Brazilian Green
color_blue = '#3E4095'  # Brazilian Blue
color_red = '#8B0000'  # Red for negative / bad context
color_gray = '#A9A9A9'  # Gray for unhighlighted
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
    """Plot monthly sales trend with two y-axes for different metrics."""

    # Plot
    fig, ax1 = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')

    # Plot the first metric on the primary y-axis
    sns.lineplot(
        x="Year_Month", y=fields[0], data=df_orders_monthly,
        ax=ax1, color=color_green, linewidth=3, marker='s', label=labels[0]
    )

    # Add secondary y-axis for the second metric
    ax2 = ax1.twinx()
    sns.lineplot(
        x="Year_Month", y=fields[1], data=df_orders_monthly,
        ax=ax2, color=color_blue, linewidth=3, marker='s', label=labels[1]
    )

    ax1.xaxis.label.set_visible(False)  # Hide the x-axis title

    # Add data labels for both metrics
    for field, ax, color in zip(fields, [ax1, ax2], [color_green, color_blue]):
        x_offset = pd.Timedelta(days=-5)
        avg_value = df_orders_monthly[field].mean()
        y_offset = 0.015 * avg_value
        for x, y in zip(df_orders_monthly['Year_Month'], df_orders_monthly[field]):
            ax.text(x + x_offset, y + y_offset, f'{y:,.0f}', ha='right', va='bottom', fontsize=11, color=color)

    # Format x-axis
    ax1.xaxis.set_minor_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax1.xaxis.get_majorticklabels(), ha='center', rotation=0)

    # Hide spines for both axes
    for ax in [ax1, ax2]:
        for spine in ['top', 'left', 'right', 'bottom']:
            ax.spines[spine].set_visible(False)
        ax.set_ylabel('')  # Hide y-axis labels
        ax.yaxis.set_visible(False)  # Hide y-axis itself

    plt.title(title, fontsize=title_fontsize1, pad=30)

    # Set y-limits for both axes
    ax1.set_ylim(0, df_orders_monthly[fields[0]].max() * 1.12)
    ax2.set_ylim(0, df_orders_monthly[fields[1]].max() * 1.12)

    # Combine legends
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles.extend(handles2)
    labels.extend(labels2)
    ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.02))
    ax2.get_legend().remove()

    return fig


def get_top_product_category_data():
    # Get sorted category by 'orders' and add rank
    df_category_top_orders = (
        df_orders_sales_by_product_category
        .sort_values(by='orders', ascending=False)
        .reset_index(drop=True)
    )
    df_category_top_orders['orders_rank'] = range(1, len(df_category_top_orders) + 1)

    # Get sorted category by 'revenue' and add rank
    df_category_top_revenue = (
        df_orders_sales_by_product_category
        .sort_values(by='revenue', ascending=False)
        .reset_index(drop=True)
    )
    df_category_top_revenue['revenue_rank'] = range(1, len(df_category_top_revenue) + 1)

    # Get sorted category by 'unit' and add rank
    df_category_top_unit = (
        df_orders_sales_by_product_category
        .sort_values(by='unit', ascending=False)
        .reset_index(drop=True)
    )
    df_category_top_unit['unit_rank'] = range(1, len(df_category_top_unit) + 1)

    return df_category_top_orders, df_category_top_revenue, df_category_top_unit


def plot_top_product_category():
    df_category_top_orders, df_category_top_revenue, df_category_top_unit = get_top_product_category_data()

    title_field_df_dict = {
        'Top 10 Product Categories by Orders': ['orders', df_category_top_orders],
        'Top 10 Product Categories by Revenue (Brazilian Reais)': ['revenue', df_category_top_revenue],
        'Top 10 Product Categories by Unit Sold': ['unit', df_category_top_unit],
    }

    figs = []

    # Reverse the order of the bars
    for title, field_df in title_field_df_dict.items():
        df_category_top10 = field_df[1][['product_category_name_english', field_df[0], f'{field_df[0]}_rank']].head(10)
        df_category_top10 = df_category_top10.sort_values(field_df[0], ascending=True)  # Sort in ascending order for reverse effect

        # Plot the horizontal bar chart
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.barh(df_category_top10['product_category_name_english'], df_category_top10[field_df[0]], color=color_green)

        # Calculate the average width of the bars
        average_width = sum(bar.get_width() for bar in bars) / len(bars)
        offset = 0.02 * average_width  # 2% of the average width

        # Add data labels
        for bar in bars:
            ax.text(bar.get_width() + offset,  # Position slightly to the right of the bar
                    bar.get_y() + bar.get_height() / 2,  # Center vertically
                    f'{bar.get_width():,.0f}',  # Format number with commas
                    va='center', fontsize=10, color='black')

        ax.set_title(title, fontsize=title_fontsize2, pad=10, ha='right')

        # Hide spines
        spines_to_hide = ['top', 'left', 'right', 'bottom']
        for spine in spines_to_hide:
            ax.spines[spine].set_visible(False)

        # Remove x-axis
        ax.xaxis.set_visible(False)

        figs.append(fig)

    return figs[0], figs[1], figs[2]