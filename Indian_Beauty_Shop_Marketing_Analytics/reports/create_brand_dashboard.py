import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from Database.db_connector import DatabaseConnector
from utils.format import format_compact
from utils.add_header import add_chart_header

db = DatabaseConnector()

fct_campaign_kpis = db.query("SELECT * FROM fct_campaign_kpis")
agg_brand_kpis = db.query("SELECT * FROM agg_brand_kpis")

df_melted = agg_brand_kpis.melt(
    id_vars=["Brand"],
    value_vars=["total_revenue", "total_spend"],
    var_name="Metric",
    value_name="Amount",
)

# ============================================================
# 1. KHỞI TẠO DASHBOARD & MAIN TITLE TỔNG
# ============================================================
fig = plt.figure(figsize=(16, 28))

# TITLE TỔNG CHO TOÀN BỘ DASHBOARD
fig.suptitle(
    "BRAND PERFORMANCE & CAMPAIGN EFFICIENCY DASHBOARD",
    fontsize=20,
    fontweight="bold",
    y=0.97,
    ha="center",
)

gs = GridSpec(
    nrows=4,
    ncols=1,
    figure=fig,
    height_ratios=[1.0, 1.0, 1.0, 0.75],
    hspace=0.32,
)


# ============================================================
# CHART 1: BAR + LINE (ROI EFFICIENCY)
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_axisbelow(True)
ax1.grid(True, linestyle="--", alpha=0.5)

bars = sns.barplot(
    data=df_melted,
    x="Brand",
    y="Amount",
    hue="Metric",
    ax=ax1,
    palette=["#1A237E", "#81D4FA"],
)

for container in ax1.containers:
    labels = [format_compact(v.get_height()) for v in container]
    ax1.bar_label(
        container, labels=labels, padding=4, fontsize=9, fontweight="bold"
    )

ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.ticklabel_format(style="plain", useOffset=False, axis="y")
ax1.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: format_compact(x))
)

ax2 = ax1.twinx()
sns.lineplot(
    data=agg_brand_kpis,
    x="Brand",
    y="overall_roi",
    ax=ax2,
    color="#E64A19",
    marker="o",
    linewidth=3,
    label="Overall ROI",
)
ax2.set_ylabel("")
ax2.set_ylim(bottom=1.88, top=2.02)
ax2.grid(False)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
if ax2.legend_:
    ax2.legend_.remove()
ax1.legend(
    handles1 + handles2,
    labels1 + labels2,
    title="Metrics",
    loc="upper right",
    frameon=True,
)

add_chart_header(
    ax=ax1,
    title="Nykaa Leads ROI Efficiency Amid Neck-and-Neck Market Competition",
    subtitle=(
        "While revenue (~28.5B) and spend (~9.6B) remain near-identical across"
        " all brands, Nykaa maximizes return on spend."
    ),
    y_title=1.10,
    y_sub=1.06,
)


# ============================================================
# CHART 2: FUNNEL ANALYSIS
# ============================================================
funnel_gs = GridSpecFromSubplotSpec(
    1, 3, subplot_spec=gs[1, 0], wspace=0.15
)

stages = ["Impressions", "Clicks", "Leads", "Conversions"]
colors = ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78"]
brands = ["Nykaa", "Purplle", "Tira Beauty"]

axes_funnel = [fig.add_subplot(funnel_gs[0, i]) for i in range(3)]

for idx, brand in enumerate(brands):
    ax = axes_funnel[idx]
    brand_data = fct_campaign_kpis[fct_campaign_kpis["Brand"] == brand]
    brand_funnel = brand_data[stages].sum()
    values = [brand_funnel[s] for s in stages]

    max_val = values[0] if values[0] > 0 else 1
    widths = [np.sqrt(v / max_val) for v in values]
    n_stages = len(stages)
    y_coords = np.arange(n_stages, 0, -1)

    for j in range(n_stages - 1):
        y_top, y_bottom = y_coords[j], y_coords[j + 1]
        w_top, w_bottom = widths[j], widths[j + 1]

        ax.fill_betweenx(
            [y_top, y_bottom],
            [-w_top / 2, -w_bottom / 2],
            [w_top / 2, w_bottom / 2],
            color=colors[j],
            alpha=0.85,
            edgecolor="white",
            linewidth=2,
        )

        step_cvr = (
            (values[j + 1] / values[j] * 100) if values[j] > 0 else 0
        )
        ax.text(
            0,
            (y_top + y_bottom) / 2,
            f"Step CVR: {step_cvr:.1f}%",
            ha="center",
            va="center",
            fontsize=8.5,
            fontweight="bold",
            color="#1f2d3d",
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                alpha=0.9,
                edgecolor="none",
            ),
        )

    for j in range(n_stages):
        val_str = format_compact(float(values[j]))
        ax.text(
            0,
            y_coords[j],
            f"{stages[j]}: {val_str}",
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="white",
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="#1f2d3d",
                alpha=0.85,
                edgecolor="none",
            ),
        )

    ax.set_title(
        f"{brand}", fontsize=11, fontweight="bold", pad=10, color="#1B263B"
    )
    ax.set_xlim(-0.75, 0.75)
    ax.axis("off")

add_chart_header(
    ax=axes_funnel[0],
    title=(
        "Top-of-Funnel CTR (~8.5%) Holds Back Conversions Despite High"
        " Downstream Efficiency (~55%)"
    ),
    subtitle=(
        "Nykaa slightly outpaces Purplle and Tira Beauty across all funnel"
        " stages, but all three share identical bottlenecks from Impression to"
        " Click."
    ),
    y_title=1.20,
    y_sub=1.12,
)


# ============================================================
# CHART 3: ROI HEALTH DONUT
# ============================================================
conditions = [
    fct_campaign_kpis["calc_roi"] < 0,
    (
        (fct_campaign_kpis["calc_roi"] >= 0)
        & (fct_campaign_kpis["calc_roi"] <= 2)
    ),
    (
        (fct_campaign_kpis["calc_roi"] > 2)
        & (fct_campaign_kpis["calc_roi"] <= 5)
    ),
    fct_campaign_kpis["calc_roi"] > 5,
]
choices = [
    "Poor (ROI < 0)",
    "Moderate (ROI 0-2)",
    "Good (ROI 2-5)",
    "Excellent (ROI > 5)",
]
fct_campaign_kpis["roi_category"] = np.select(
    conditions, choices, default="Unknown"
)

colors = ["#d9534f", "#f0ad4e", "#5cb85c", "#2e7d32"]

donut_gs = GridSpecFromSubplotSpec(
    1, 3, subplot_spec=gs[2, 0], wspace=0.1
)
axes_donut = [fig.add_subplot(donut_gs[0, i]) for i in range(3)]

for idx, brand in enumerate(brands):
    ax = axes_donut[idx]
    brand_df = fct_campaign_kpis[fct_campaign_kpis["Brand"] == brand]
    counts = (
        brand_df["roi_category"]
        .value_counts()
        .reindex(choices, fill_value=0)
    )
    total_campaigns = counts.sum()

    wedges, texts, autotexts = ax.pie(
        counts.values,
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        textprops=dict(size=9, weight="bold"),
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    )

    for autotext in autotexts:
        autotext.set_color("white")

    ax.text(
        0,
        0,
        f"{brand.upper()}\n\n{total_campaigns:,}\nCampaigns",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="#222222",
    )

# ĐẶT LEGEND LÊN TRÊN CHIỀU CAO CỦA CHART 3 ĐỂ KHÔNG CHÈN XUỐNG CHART 4
axes_donut[1].legend(
    wedges,
    choices,
    title="ROI Health Category",
    title_fontsize=11.5,  # Tăng chữ tiêu đề (cũ: 9)
    fontsize=10.5,  # Tăng chữ nội dung (cũ: 8.5)
    loc="lower center",
    bbox_to_anchor=(
        0.5,
        -0.24,
    ),  # Hạ xuống chút (cũ: -0.18) để legend phình to không cạ vào donut
    ncol=4,
    frameon=True,
    markerscale=1.4,  # Phóng to ô màu đại diện (mặc định 1.0)
    handlelength=1.5,  # Tăng độ rộng ô màu
    handleheight=1.2,  # Tăng độ cao ô màu
    borderpad=0.8,  # Tăng khoảng không bên trong viền Legend
)

add_chart_header(
    ax=axes_donut[0],
    title=(
        "24% of Campaigns Suffer Losses: Automated Stop-Loss Needed to Maximize"
        " Profitability"
    ),
    subtitle=(
        "All three brands show an identical ROI distribution, with"
        " top-performing campaigns (ROI > 2) subsidizing ~13,200 loss-making"
        " campaigns per brand."
    ),
    y_title=1.20,
    y_sub=1.12,
)


# ============================================================
# CHART 4: CAMPAIGN TYPE EFFICIENCY
# ============================================================
summary = (
    fct_campaign_kpis.groupby(["Brand", "Campaign_Type"])
    .agg(
        total_spend=("calc_total_spend", "sum"),
        total_profit=("calc_profit", "sum"),
        total_conv=("Conversions", "sum"),
    )
    .reset_index()
)
summary["ROI"] = summary["total_profit"] / summary["total_spend"]
summary["CPA"] = summary["total_spend"] / summary["total_conv"]

# wspace=0.38 tạo khoảng trống vừa đủ cho 2 trục Y của 3 chart
efficiency_gs = GridSpecFromSubplotSpec(
    1, len(brands), subplot_spec=gs[3, 0], wspace=0.38
)
axes_efficiency = [
    fig.add_subplot(efficiency_gs[0, i]) for i in range(len(brands))
]

HIGHLIGHT_COLOR = "#1A237E"
GRAY_COLOR = "#D3D3D3"
LINE_COLOR = "#d9534f"

cpa_min, cpa_max = summary["CPA"].min() * 0.99, summary["CPA"].max() * 1.01

for idx, brand in enumerate(brands):
    ax1 = axes_efficiency[idx]
    brand_df = (
        summary[summary["Brand"] == brand]
        .sort_values(by="ROI", ascending=False)
        .reset_index(drop=True)
    )

    bar_colors = [
        HIGHLIGHT_COLOR if i == 0 else GRAY_COLOR
        for i in range(len(brand_df))
    ]

    bars = ax1.bar(
        brand_df["Campaign_Type"],
        brand_df["ROI"],
        color=bar_colors,
        width=0.45,  # Tăng nhẹ độ rộng bar cho cân đối
    )

    # TRỤC Y1 (ROI) - Giữ full ticks cho cả 3 chart
    ax1.tick_params(axis="y", labelcolor=HIGHLIGHT_COLOR, labelsize=8, pad=2)
    ax1.set_ylim(0, 2.2)
    ax1.set_xticks(range(len(brand_df)))
    ax1.set_xticklabels(
        brand_df["Campaign_Type"], rotation=35, ha="right", fontsize=8.5
    )

    # Tiêu đề từng Subplot ghi rõ chỉ số của 2 trục để bỏ nhãn dọc vướng víu
    ax1.set_title(
        f"{brand}\n(Bar: ROI | Line: CPA)",
        fontsize=10.5,
        fontweight="bold",
        pad=8,
        color="#0F172A",
    )

    max_roi = brand_df.loc[0, "ROI"]
    ax1.text(
        0,
        max_roi + 0.03,
        f"{max_roi:.2f}x",
        ha="center",
        va="bottom",
        fontweight="bold",
        color=HIGHLIGHT_COLOR,
        fontsize=9,
    )

    # TRỤC Y2 (CPA) - Giữ full ticks cho cả 3 chart
    ax2 = ax1.twinx()
    ax2.plot(
        brand_df["Campaign_Type"],
        brand_df["CPA"],
        color=LINE_COLOR,
        marker="o",
        linewidth=1.8,
        markersize=5,
        linestyle="--",
        alpha=0.85,
    )
    ax2.set_ylim(cpa_min, cpa_max)

    # Hiển thị số CPA rõ ràng trên cả 3 chart mà không bị đè nhờ pad=2 và labelsize=8
    ax2.tick_params(axis="y", labelcolor=LINE_COLOR, labelsize=8, pad=2)

    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

# Header của Chart 4
add_chart_header(
    ax=axes_efficiency[0],
    title=(
        "ROI Remains Stable Across Channels, While CPA Reveals the Real"
        " Efficiency Gap"
    ),
    subtitle=(
        "ROI remains tightly clustered across brands, while CPA separates"
        " channels: Social Media leads Nykaa, Email leads Purplle, and Paid"
        " Ads leads Tira Beauty."
    ),
    y_title=1.22,
    y_sub=1.14,
)

# CHỈNH CĂN LỀ TỔNG CHUẨN XÁC: top=0.92 DÀNH CHỖ CHO SUPTITLE
plt.subplots_adjust(top=0.92, bottom=0.03)

plt.savefig(
    "reports/figures/brand_dashboard.png", dpi=300, bbox_inches="tight"
)