import pandas as pd
import plotly.graph_objects as go
from .constants import *

# Load Dataset
df_reviews = pd.read_csv(DIR_CLEAN_DATASET + "reviews_clean.csv")


def get_review_scores_data():
    df_review_scores = df_reviews.groupby('review_score')['review_id'].count()

    # Calculate the percentage
    total_reviews = df_review_scores.sum()
    percentage_by_review_status = (df_review_scores / total_reviews) * 100

    # Combine counts and percentages into a single DataFrame
    df_review_scores_summary = pd.DataFrame({
        'Count': df_review_scores,
        'Percentage': percentage_by_review_status
    })

    return df_review_scores_summary


def plot_review_scores():
    df_review_scores_summary = get_review_scores_data()

    # Sort values by 'review_score' for better visual ordering
    sorted_data = df_review_scores_summary.sort_index(ascending=False)

    # Extract counts and percentages
    counts = sorted_data['Count']
    percentages = sorted_data['Percentage']

    max_value = sorted_data['Count'].max()

    # Define colors for the bars
    colors = [COLOR_GREEN, COLOR_GREEN, COLOR_GRAY, COLOR_RED, COLOR_RED]

    # Create the Plotly bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=sorted_data.index.astype(str),  # Convert index to string for proper labeling
            y=counts,
            marker_color=colors,
            text=[f'{count:,.0f} ({percent:.0f}%)' for count, percent in zip(counts, percentages)],
            textposition='outside',  # Display labels outside the bars
            showlegend=False
        )
    )

    # Update layout for styling
    fig.update_layout(
        title={
            'text': "Review Scores Frequency",
            'font': {'size': TITLE_FONTSIZE1},
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis=dict(
            showline=False,
            showgrid=False
        ),
        yaxis=dict(
            visible=False,
            range=[0, max_value * 1.15],  # Set y-axis range with a buffer
        ),
        height=440,  # Adjust height as needed
        bargap=0.2  # Add spacing between bars
    )

    return fig
