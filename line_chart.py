import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.dates import DateFormatter

# Load data
data = pd.read_csv('relative_diff_price.csv')

# Ensure the 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['snapped_at'])

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(data['Date'], data['relative_diff_price'], label='Peg Price Deviation', color='#76A1CA', linewidth=2)

title_font = FontProperties(fname='./fonts/aeonik.ttf', size=18, weight='bold')
label_font = FontProperties(fname='./fonts/inter.ttf', size=10)
legend_font = FontProperties(fname='./fonts/ataero.ttf', size=8)

ax.set_title('Historical Peg Performance eBTC to BTC', fontproperties=title_font, color='#FFFFFF', pad=20, loc='left')
ax.tick_params(axis='x', colors='#FFFFFF', labelsize=10)
ax.tick_params(axis='y', colors='#FFFFFF', labelsize=10)

ax.set_ylabel('Percentage', fontproperties=label_font, color='#FFFFFF')

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

ax.legend(loc='upper left', fontsize=8, frameon=False, ncol=1, bbox_to_anchor=(0.05, 1.02),
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
#plt.savefig("line_chart_with_large_watermark.png", dpi=300, bbox_inches='tight')
plt.show()
