import os

__all__ = [
    'COLOR_GREEN', 'COLOR_BLUE', 'COLOR_GRAY', 'COLOR_RED', 'TITLE_FONTSIZE1',
    'DIR_CLEAN_DATASET', 'DIR_DASHBOARD_DATASET'
]

# Define colors
COLOR_GREEN = '#00e656'  # Green
COLOR_BLUE = '#0098FF'  # Blue
COLOR_RED = '#FF6B6B'  # Red for negative / bad context
COLOR_GRAY = '#CCCCCC'  # Gray for unhighlighted

# Define Fontsize
TITLE_FONTSIZE1 = 20
TITLE_FONTSIZE2 = 14

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DIR_CLEAN_DATASET = "../dataset/cleaned/"
DIR_DASHBOARD_DATASET = "../dataset/cleaned_for_dashboard/"