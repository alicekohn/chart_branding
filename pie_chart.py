import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties

# Load data
data = pd.read_csv('restaking_distr.csv')

# Group data by `token_symbol` and calculate the total balance for each
grouped_data = data.groupby('token_symbol', as_index=False)['token_balance'].sum()

# Calculate percentages for the pie chart
grouped_data['percentage'] = (grouped_data['token_balance'] / grouped_data['token_balance'].sum()) * 100

# Group smaller contributors into "Other"
threshold = 1  # Minimum percentage for individual labels
grouped_data['label'] = grouped_data.apply(
    lambda row: f"{row['token_symbol']} ({row['percentage']:.1f}%)" if row['percentage'] >= threshold else 'Other',
    axis=1
)

# Aggregate "Other" contributions
grouped_data = grouped_data.groupby('label', as_index=False)['percentage'].sum()
grouped_data = grouped_data.sort_values(by='percentage', ascending=False)  # Organize by pie size

# Prepare labels and sizes
labels = grouped_data['label']
sizes = grouped_data['percentage']
colors = plt.cm.tab20c(range(len(labels)))

fig, ax = plt.subplots(figsize=(8, 8))

# Plot the pie chart
ax.pie(sizes, labels=labels, colors=colors, startangle=90,
       textprops={'color': '#FFFFFF', 'fontsize': 10})

# Title and styling
title_font = FontProperties(fname='./fonts/aeonik.ttf', size=18, weight='bold')
fig.patch.set_facecolor('#1A1A1A')
ax.set_facecolor('#1A1A1A')
ax.set_title('Restaking Strategies', fontproperties=title_font, color='#FFFFFF', pad=20)

# Add watermark logo
logo = plt.imread('./fonts/logo_small.png')
imagebox = OffsetImage(logo, zoom=0.7, alpha=0.25)
ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, xycoords='axes fraction', zorder=-1)
ax.add_artist(ab)

plt.tight_layout()
#plt.savefig("pie_chart_with_large_watermark.png", dpi=300, bbox_inches='tight')
plt.show()
