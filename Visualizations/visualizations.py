import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')


# CONFIG 
DATA_PATH   = r"C:\Users\hfras\Desktop\Classwork\Spring 2026\Data Warehousing\Final Project\Data"
OUTPUT_PATH = r"C:\Users\hfras\Desktop\Classwork\Spring 2026\Data Warehousing\Final Project\Visualizations"

import os
os.makedirs(OUTPUT_PATH, exist_ok=True)

def data(filename):
    return os.path.join(DATA_PATH, filename)

def out(filename):
    return os.path.join(OUTPUT_PATH, filename)



# COLOR PALETTE

BG      = '#0f1117'
CARD    = '#1a1d27'
ACCENT1 = '#6c63ff'
ACCENT2 = '#ff6584'
ACCENT3 = '#43e97b'
ACCENT4 = '#f9ca24'
ACCENT5 = '#fd79a8'
TEXT    = '#e8eaf0'
SUBTEXT = '#8b90a0'
GRID    = '#2a2d3a'

MFGR_COLORS = {
    'Nintendo':  '#e84855',
    'Sony':      '#4a90d9',
    'Microsoft': '#43b883',
}

SCORE_COLORS = {
    'Acclaimed (8+)': '#43e97b',
    'Good (7-8)':     '#6c63ff',
    'Mixed (5-7)':    '#f9ca24',
    'Poor (<5)':      '#ff6584',
}

GENRE_PALETTE = {
    'Shooter':  ACCENT1,
    'Action':   ACCENT2,
    'Platform': ACCENT3,
    'Sports':   ACCENT4,
    'Fighting': ACCENT5,
    'Racing':   '#00cec9',
}

def style_ax(ax):
    ax.set_facecolor(CARD)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)



# CHART 1: Dominant Genre Per Gaming Era

def chart1_genre_era():
    df = pd.read_csv(data('topic1_genre_era_ranked.csv'))
    top1 = df[(df['rank_in_era'] == 1) & (df['gaming_era'] != '9th Gen (2020+)')].copy()

    era_order = [
        '2nd Gen (1976-1982)',
        '3rd/4th Gen (1983-1992)',
        '5th Gen (1993-1998)',
        '6th Gen (1999-2005)',
        '7th Gen (2006-2012)',
        '8th Gen (2013-2019)',
    ]
    era_labels = [
        '2nd Gen\n(1976-82)', '3rd/4th Gen\n(1983-92)', '5th Gen\n(1993-98)',
        '6th Gen\n(1999-05)', '7th Gen\n(2006-12)', '8th Gen\n(2013-19)',
    ]

    top1['gaming_era'] = pd.Categorical(top1['gaming_era'], categories=era_order, ordered=True)
    top1 = top1.sort_values('gaming_era')

    bar_colors = [GENRE_PALETTE.get(g, '#aaa') for g in top1['genre_name']]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)

    bars = ax.bar(era_labels, top1['total_sales_millions'], color=bar_colors,
                  width=0.55, edgecolor='none', zorder=3)

    for bar, genre in zip(bars, top1['genre_name']):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 6,
                genre, ha='center', va='bottom',
                color=TEXT, fontsize=8.5, fontweight='bold')

    style_ax(ax)
    ax.set_ylabel('Total Sales (Millions)', color=TEXT, fontsize=10)
    ax.set_title('Dominant Genre Per Gaming Era  ·  Top-Ranked by Total Sales',
                 color=TEXT, fontsize=13, fontweight='bold', pad=14)
    ax.set_ylim(0, top1['total_sales_millions'].max() * 1.22)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))

    fig.tight_layout(pad=2)
    fig.savefig(out('chart1_genre_era.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart1_genre_era.png')



# CHART 2: Genre Growth: 2000s vs 2010s (Diverging Bar)

def chart2_genre_growth():
    df = pd.read_csv(data('topic1_genre_growth.csv'))
    df = df.dropna(subset=['pct_change']).sort_values('pct_change')

    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)

    colors = [ACCENT3 if v >= 0 else ACCENT2 for v in df['pct_change']]
    bars = ax.barh(df['genre_name'], df['pct_change'], color=colors,
                   edgecolor='none', height=0.65, zorder=3)

    for bar, val in zip(bars, df['pct_change']):
        x = bar.get_width()
        label = f'+{val:,.0f}%' if val >= 0 else f'{val:,.0f}%'
        ha = 'left' if val >= 0 else 'right'
        offset = 30 if val >= 0 else -30
        ax.text(x + offset, bar.get_y() + bar.get_height() / 2,
                label, va='center', ha=ha,
                color=TEXT, fontsize=8, fontweight='bold')

    ax.axvline(0, color=SUBTEXT, linewidth=1, zorder=4)
    style_ax(ax)
    ax.set_xlabel('% Change in Sales (2000s → 2010s)', color=TEXT, fontsize=10)
    ax.set_title('Genre Sales Growth: 2000s vs 2010s',
                 color=TEXT, fontsize=13, fontweight='bold', pad=14)
    ax.tick_params(axis='y', labelsize=9, colors=TEXT)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)

    legend_handles = [
        mpatches.Patch(color=ACCENT3, label='Growth'),
        mpatches.Patch(color=ACCENT2, label='Decline'),
    ]
    ax.legend(handles=legend_handles, facecolor=CARD, edgecolor=GRID,
              labelcolor=TEXT, fontsize=9, loc='lower right')

    fig.tight_layout(pad=2)
    fig.savefig(out('chart2_genre_growth.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart2_genre_growth.png')



# CHART 3: Platform Wars: Total Sales by Manufacturer

def chart3_platform_wars():
    df = pd.read_csv(data('topic2_manufacturer_totals.csv'))
    df = df.sort_values('total_sales_millions', ascending=False)
    colors = [MFGR_COLORS.get(m, '#aaa') for m in df['manufacturer']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.patch.set_facecolor(BG)

    # Left: total sales
    ax = axes[0]
    ax.set_facecolor(CARD)
    bars = ax.bar(df['manufacturer'], df['total_sales_millions'],
                  color=colors, width=0.5, edgecolor='none', zorder=3)
    for bar, val in zip(bars, df['total_sales_millions']):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 20,
                f'${val:,.0f}M', ha='center', va='bottom',
                color=TEXT, fontsize=9, fontweight='bold')
    style_ax(ax)
    ax.set_ylabel('Total Sales (Millions)', color=TEXT, fontsize=10)
    ax.set_title('Total Sales by Manufacturer', color=TEXT, fontsize=11, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
    ax.set_ylim(0, df['total_sales_millions'].max() * 1.18)

    # Right: avg sales per title
    ax2 = axes[1]
    ax2.set_facecolor(CARD)
    bars2 = ax2.bar(df['manufacturer'], df['avg_sales_per_title'],
                    color=colors, width=0.5, edgecolor='none', zorder=3)
    for bar, val in zip(bars2, df['avg_sales_per_title']):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.005,
                 f'{val:.3f}M', ha='center', va='bottom',
                 color=TEXT, fontsize=9, fontweight='bold')
    style_ax(ax2)
    ax2.set_ylabel('Avg Sales per Title (Millions)', color=TEXT, fontsize=10)
    ax2.set_title('Avg Sales per Title', color=TEXT, fontsize=11, fontweight='bold', pad=10)
    ax2.set_ylim(0, df['avg_sales_per_title'].max() * 1.25)

    fig.suptitle('Platform Wars: Nintendo vs Sony vs Microsoft',
                 color=TEXT, fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout(pad=2)
    fig.savefig(out('chart3_platform_wars.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart3_platform_wars.png')



# CHART 4: Platform Quartiles (Horizontal Bar)

def chart4_platform_quartiles():
    df = pd.read_csv(data('topic2_platform_quartiles.csv'))
    df = df.sort_values(['manufacturer', 'total_sales_millions'])
    colors = [MFGR_COLORS.get(m, '#aaa') for m in df['manufacturer']]

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)

    y_pos = range(len(df))
    ax.barh(list(y_pos), df['total_sales_millions'], color=colors,
            alpha=0.85, edgecolor='none', height=0.6, zorder=3)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(df['platform_name'], fontsize=8.5, color=TEXT)

    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(row['total_sales_millions'] + 8, i,
                f"Q{int(row['sales_quartile'])}",
                va='center', ha='left', color=SUBTEXT, fontsize=8)

    style_ax(ax)
    ax.set_xlabel('Total Sales (Millions)', color=TEXT, fontsize=10)
    ax.set_title('Platform Sales with Quartile Rankings (per Manufacturer)',
                 color=TEXT, fontsize=13, fontweight='bold', pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)

    legend_handles = [mpatches.Patch(color=c, label=m) for m, c in MFGR_COLORS.items()]
    ax.legend(handles=legend_handles, facecolor=CARD, edgecolor=GRID,
              labelcolor=TEXT, fontsize=9, loc='lower right')

    fig.tight_layout(pad=2)
    fig.savefig(out('chart4_platform_quartiles.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart4_platform_quartiles.png')



# CHART 5: Critic Score vs Avg Sales

def chart5_score_vs_sales():
    df = pd.read_csv(data('topic3_score_tier.csv'))
    tier_order = ['Acclaimed (8+)', 'Good (7-8)', 'Mixed (5-7)', 'Poor (<5)']
    df['score_tier'] = pd.Categorical(df['score_tier'], categories=tier_order, ordered=True)
    df = df.sort_values('score_tier')
    colors = [SCORE_COLORS[t] for t in df['score_tier']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.patch.set_facecolor(BG)

    # Left: avg sales
    ax = axes[0]
    ax.set_facecolor(CARD)
    bars = ax.bar(df['score_tier'], df['avg_sales_millions'],
                  color=colors, width=0.5, edgecolor='none', zorder=3)
    for bar, val in zip(bars, df['avg_sales_millions']):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.01,
                f'{val:.3f}M', ha='center', va='bottom',
                color=TEXT, fontsize=9, fontweight='bold')
    style_ax(ax)
    ax.set_ylabel('Avg Sales per Title (Millions)', color=TEXT, fontsize=10)
    ax.set_title('Avg Sales by Score Tier', color=TEXT, fontsize=11, fontweight='bold', pad=10)
    ax.tick_params(axis='x', labelsize=8)
    ax.set_ylim(0, df['avg_sales_millions'].max() * 1.2)

    # Right: game count
    ax2 = axes[1]
    ax2.set_facecolor(CARD)
    bars2 = ax2.bar(df['score_tier'], df['game_count'],
                    color=colors, width=0.5, edgecolor='none', zorder=3)
    for bar, val in zip(bars2, df['game_count']):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 5,
                 f'{val:,}', ha='center', va='bottom',
                 color=TEXT, fontsize=9, fontweight='bold')
    style_ax(ax2)
    ax2.set_ylabel('Number of Titles', color=TEXT, fontsize=10)
    ax2.set_title('Game Count by Score Tier', color=TEXT, fontsize=11, fontweight='bold', pad=10)
    ax2.tick_params(axis='x', labelsize=8)
    ax2.set_ylim(0, df['game_count'].max() * 1.18)

    fig.suptitle('Does Critical Acclaim Drive Sales?',
                 color=TEXT, fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout(pad=2)
    fig.savefig(out('chart5_score_vs_sales.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart5_score_vs_sales.png')



# CHART 6: Critic-Proof Games (Horizontal Bar)

def chart6_critic_proof():
    df = pd.read_csv(data('topic3_critic_proof.csv'))
    df = df.sort_values('total_sales', ascending=True).tail(15)
    colors = [MFGR_COLORS.get(m, '#aaa') for m in df['manufacturer']]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)

    bars = ax.barh(df['title'], df['total_sales'],
                   color=colors, edgecolor='none', height=0.65, zorder=3)

    for bar, score in zip(bars, df['critic_score']):
        ax.text(bar.get_width() + 0.05,
                bar.get_y() + bar.get_height() / 2,
                f'Score: {score}', va='center', ha='left',
                color=SUBTEXT, fontsize=8)

    style_ax(ax)
    ax.set_xlabel('Total Sales (Millions)', color=TEXT, fontsize=10)
    ax.set_title('"Critic-Proof" Games — High Sales Despite Mixed/Poor Reviews',
                 color=TEXT, fontsize=12, fontweight='bold', pad=14)
    ax.tick_params(axis='y', labelsize=8.5, colors=TEXT)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--', alpha=0.7)
    ax.yaxis.grid(False)
    ax.set_xlim(0, df['total_sales'].max() * 1.3)

    legend_handles = [mpatches.Patch(color=c, label=m) for m, c in MFGR_COLORS.items()]
    ax.legend(handles=legend_handles, facecolor=CARD, edgecolor=GRID,
              labelcolor=TEXT, fontsize=9, loc='lower right')

    fig.tight_layout(pad=2)
    fig.savefig(out('chart6_critic_proof.png'), dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print('  ✓ chart6_critic_proof.png')



# MAIN

if __name__ == '__main__':
    print('=' * 45)
    print('Generating Video Game Sales Visualizations')
    print('=' * 45)

    chart1_genre_era()
    chart2_genre_growth()
    chart3_platform_wars()
    chart4_platform_quartiles()
    chart5_score_vs_sales()
    chart6_critic_proof()

    print()
    print(f'All charts saved to:')
    print(f'  {OUTPUT_PATH}')
    print('=' * 45)
