import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.dates import DateFormatter

# Load data
data = pd.read_csv('eigenlayer_tvl.csv')

# Convert the 'day' column to a datetime format if necessary
data['day'] = pd.to_datetime(data['day']).dt.date

# Filter out the 'Total' category if necessary
data = data[data['token_type'] != 'Total']

# Pivot the data for plotting, index for x-axis, values for y-axis, columns for labels
data_pivot = data.pivot(index='day', columns='token_type', values='tvl_eth').fillna(0)

fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#CA822F', '#76A1CA', '#7EC7A1', '#2E87C8', '#F1B631']
ax.stackplot(data_pivot.index, data_pivot.T, labels=data_pivot.columns, alpha=0.9, colors=colors)

title_font = FontProperties(fname='./fonts/aeonik.ttf', size=18, weight='bold')
label_font = FontProperties(fname='./fonts/inter.ttf', size=10)
legend_font = FontProperties(fname='./fonts/ataero.ttf', size=8)


ax.set_title('Eigenlayer TVL [ETH]', fontproperties=title_font, color='#FFFFFF', pad=20, loc='left') # Set title
ax.tick_params(axis='x', colors='#FFFFFF', labelsize=10)
ax.tick_params(axis='y', colors='#FFFFFF', labelsize=10)

def format_thousands(x, _):
    if x >= 1e9:
        return f'{x / 1e9:.0f}B'
    elif x >= 1e6:
        return f'{x / 1e6:.0f}M'
    elif x >= 1e3:
        return f'{x / 1e3:.0f}K'
    else:
        return f'{x:.0f}'

ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
ax.xaxis.set_major_formatter(DateFormatter("%m-%Y"))


ax.legend(loc='upper left', fontsize=8, frameon=False, ncol=3, bbox_to_anchor=(0.05, 1.02),
          prop=legend_font)
for text in ax.get_legend().get_texts():
    text.set_color("white")


logo = plt.imread('./fonts/logo_small.png')
imagebox = OffsetImage(logo, zoom=0.7, alpha=0.25)
ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, xycoords='axes fraction', zorder=-1)
ax.add_artist(ab)


fig.patch.set_facecolor('#1A1A1A')
ax.set_facecolor('#1A1A1A')

plt.tight_layout()
#plt.savefig("stacked_area_chart_with_large_watermark.png", dpi=300, bbox_inches='tight')
plt.show()
