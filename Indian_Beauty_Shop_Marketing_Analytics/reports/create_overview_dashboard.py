import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Database.db_connector import DatabaseConnector

db = DatabaseConnector()

fct_campaign_kpis = db.query("SELECT * FROM fct_campaign_kpis")
agg_brand_kpis = db.query("SELECT * FROM agg_brand_kpis")

def format_compact(val):
    if pd.isna(val) or not isinstance(val, (int, float)):
        return val
    abs_val = abs(val)

    if abs_val >= 1e9:
        return f"{val / 1e9:.1f} B"
    elif abs_val >= 1e6:
        return f"{val / 1e6:.1f} M"
    elif abs_val >= 1e3:
        return f"{val / 1e3:.1f} K"

    return f"{val:.1f}"

def format_volume(x):
    if x >= 1e9:
        return f"{x*1e-9:.1f} B"
    elif x >= 1e6:
        return f"{x*1e-6:.1f} M"
    elif x >= 1e3:
        return f"{x*1e-3:.1f} K"
    return f"{int(x):,}"

def add_chart_header(ax, title, subtitle, y_title=1.12, y_sub=1.03):
    """Thêm Title (đậm, to) và Subtitle (nhỏ, xám) vào góc trên bên trái của Subplot.

    - transform=ax.transAxes: Tọa độ theo % của subplot (0: mép trái/dưới, 1:
    mép phải/trên)
    """
    # Title chính
    ax.text(
        0.0,
        y_title,
        title,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        color="#1a252f",
        ha="left",
        va="bottom",
    )

    # Subtitle phụ
    ax.text(
        0.0,
        y_sub,
        subtitle,
        transform=ax.transAxes,
        fontsize=10,
        color="#555555",
        style="italic",  # Có thể nghiêng hoặc không
        ha="left",
        va="bottom",
    )
    

total_revenue_3_shop = sum(agg_brand_kpis["total_revenue"])
total_spend_3_shop = sum(agg_brand_kpis["total_spend"])
total_profit_3_shop = sum(agg_brand_kpis["total_profit"])
total_campaign_3_shop = sum(agg_brand_kpis["total_campaigns"])
total_weighted_roi_3_shop = (total_revenue_3_shop - total_spend_3_shop)/total_spend_3_shop

dict_overview = {
    "Total Revenue": total_revenue_3_shop,
    "Total Spend": total_spend_3_shop,
    "Total profit": total_profit_3_shop,
    "Total Campaign": total_campaign_3_shop,
    "Total Weighted ROI": round(total_weighted_roi_3_shop, 4)
}

kpis_card = pd.DataFrame(dict_overview, index = [0])
kpis_card[["Total Revenue", "Total Spend", "Total profit", "Total Campaign"]] = kpis_card[["Total Revenue", "Total Spend", "Total profit", "Total Campaign"]].map(format_compact)

# ==========================================
# 0. SETUP CANVAS & GRIDSPEC LAYOUT
# ==========================================
# Tạo canvas tỉ lệ chuẩn 16:20 tối ưu cho Dashboard Overview
fig = plt.figure(figsize=(18, 20), facecolor="#f8f9fa")

# 2. Giảm height_ratio của hàng KPI và kéo top=0.945
gs = gridspec.GridSpec(
    4,
    2,
    height_ratios=[0.35, 2.0, 2.2, 2.2],  # Giảm từ 0.55 xuống 0.35
    width_ratios=[1.2, 1],
    hspace=0.5,
    wspace=0.25,
    top=0.945,  # Đẩy mép trên lưới sát lên Subtitle (cũ là 0.93)
    bottom=0.04,
    left=0.06,
    right=0.94,
)

# 3. Ép tọa độ Title và Subtitle gọn lại
fig.suptitle(
    "SYSTEM-WIDE MARKETING PERFORMANCE OVERVIEW",
    fontsize=20,
    fontweight="bold",
    color="#1a252f",
    y=0.98,
)
fig.text(
    0.5,
    0.95,
    "Executive summary of financial trends, conversion efficiency, ROI health distribution, and performance outliers.",
    ha="center",
    fontsize=14,
    color="#555555",
)

# ==========================================
# ROW 1: KPI CARDS
# ==========================================
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis("off")
ax_kpi.set_ylim(0, 1)

kpi_labels = [
    "Total Revenue",
    "Total Spend",
    "Total Profit",
    "Total Campaign",
    "Weighted ROI",
]
kpi_values = [
    kpis_card["Total Revenue"].iloc[0],
    kpis_card["Total Spend"].iloc[0],
    kpis_card["Total profit"].iloc[0],
    kpis_card["Total Campaign"].iloc[0],
    f"{dict_overview['Total Weighted ROI']:.2f}",
]
kpi_colors = ["#1f77b4", "#d62728", "#2ca02c", "#7f7f7f", "#8c564b"]
positions = np.linspace(0.08, 0.92, len(kpi_labels))

for label, val, pos, col in zip(kpi_labels, kpi_values, positions, kpi_colors):
    # Giá trị KPI (Hạ từ 0.90 xuống 0.55 để né Subtitle chính phía trên)
    ax_kpi.text(
        pos,
        0.55,
        val,
        ha="center",
        va="center",
        fontsize=14.5,
        fontweight="bold",
        color=col,
        bbox=dict(
            boxstyle="round,pad=0.45",
            facecolor="white",
            edgecolor="#e0e0e0",
            linewidth=1.5,
        ),
    )

    # Nhãn tên KPI (Đặt ở 0.10 để giữ khoảng cách cân đối với ô số)
    ax_kpi.text(
        pos,
        0.10,
        label.upper(),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#555555",
    )

# ==========================================
# ROW 2: FINANCIAL TREND
# ==========================================
ax_trend = fig.add_subplot(gs[1, :])

monthly_kpis = (
    fct_campaign_kpis.groupby("campaign_month")[
        ["Revenue", "calc_total_spend", "calc_profit"]
    ]
    .sum()
    .reset_index()
    .sort_values("campaign_month")
)

ax_trend.plot(
    monthly_kpis["campaign_month"],
    monthly_kpis["Revenue"] / 1e6,
    marker="o",
    linewidth=2.5,
    markersize=6,
    color="#1f77b4",
    label="Revenue",
)
ax_trend.plot(
    monthly_kpis["campaign_month"],
    monthly_kpis["calc_total_spend"] / 1e6,
    marker="s",
    linewidth=2.0,
    markersize=5,
    color="#d62728",
    label="Total Spend",
)
ax_trend.plot(
    monthly_kpis["campaign_month"],
    monthly_kpis["calc_profit"] / 1e6,
    marker="^",
    linewidth=2.0,
    markersize=5,
    color="#2ca02c",
    label="Profit",
)

ax_trend.annotate(
    "Incomplete Data Cut-off\n(Data recorded up to Jun 24)",
    xy=(11, 2750),
    xytext=(8.0, 4200),
    arrowprops=dict(facecolor="red", shrink=0.05, width=1.5, headwidth=6),
    bbox=dict(boxstyle="round,pad=0.3", fc="papayawhip", ec="orange", lw=1),
    fontsize=9,
)

ax_trend.set_ylabel("Amount (Millions $)", fontsize=10, fontweight="bold")
ax_trend.grid(True, linestyle="--", alpha=0.5)
ax_trend.spines["top"].set_visible(False)
ax_trend.spines["right"].set_visible(False)
ax_trend.legend(
    frameon=True, facecolor="white", edgecolor="none", loc="center left"
)

# Căn chỉnh x-ticks gọn gàng
ax_trend.set_xticks(range(len(monthly_kpis["campaign_month"])))
ax_trend.set_xticklabels(
    monthly_kpis["campaign_month"], rotation=30, ha="right", fontsize=9
)

add_chart_header(
    ax_trend,
    "Consistent ~66% Profit Margin Maintained Across 11 Months Despite June Scale Contraction",
    "Marketing spend remained strictly controlled (~$2.5B/mo), yielding a predictable ~$5.0B net profit monthly.\n"
        "The Jun 2025 pull-back reflects lower campaign volume and partial data (cut-off Jun 24), maintaining positive profitability ($1.8B).",
    )

# ==========================================
# ROW 3 - LEFT: CONVERSION FUNNEL
# ==========================================
ax_funnel = fig.add_subplot(gs[2, 0])

stages = ["Impressions", "Clicks", "Leads", "Conversions"]
fn_colors = ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78"]

system_funnel = fct_campaign_kpis[stages].sum()
values = [system_funnel[s] for s in stages]
max_val = values[0] if values[0] > 0 else 1
widths = [np.sqrt(v / max_val) for v in values]
n_stages = len(stages)
y_coords = np.arange(n_stages, 0, -1)

for j in range(n_stages - 1):
    y_top, y_bottom = y_coords[j], y_coords[j + 1]
    w_top, w_bottom = widths[j], widths[j + 1]

    ax_funnel.fill_betweenx(
        [y_top, y_bottom],
        [-w_top / 2, -w_bottom / 2],
        [w_top / 2, w_bottom / 2],
        color=fn_colors[j],
        alpha=0.85,
        edgecolor="white",
        linewidth=2,
    )

    step_cvr = (values[j + 1] / values[j] * 100) if values[j] > 0 else 0
    ax_funnel.text(
        0,
        (y_top + y_bottom) / 2,
        f"Step CVR: {step_cvr:.2f}%",
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
    val_str = format_volume(values[j])
    ax_funnel.text(
        0,
        y_coords[j],
        f"{stages[j]}: {val_str}",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="#1f2d3d",
            alpha=0.8,
            edgecolor="none",
        ),
    )

ax_funnel.set_xlim(-0.75, 0.75)
ax_funnel.axis("off")
add_chart_header(
    ax_funnel,
    "High Downstream Conversion (55% Lead CVR) Contrasts with Top-of-Funnel Bottleneck (8.5% CTR)",
    f"Overall CVR (Clicks -> Conv): {(values[3]/values[1]*100):.2f}% | Top-of-Funnel CTR: {(values[1]/values[0]*100):.2f}%\n"
        "Recommendation: Focus optimization on ad creatives to widen the funnel rather than sales/checkout steps.",
)

# ==========================================
# ROW 3 - RIGHT: ROI DONUT CHART
# ==========================================
ax_donut = fig.add_subplot(gs[2, 1])

conditions = [
    fct_campaign_kpis["calc_roi"] < 0,
    (fct_campaign_kpis["calc_roi"] >= 0) & (fct_campaign_kpis["calc_roi"] <= 2),
    (fct_campaign_kpis["calc_roi"] > 2) & (fct_campaign_kpis["calc_roi"] <= 5),
    fct_campaign_kpis["calc_roi"] > 5,
]
choices = [
    "Poor (ROI < 0)",
    "Moderate (ROI 0–2)",
    "Good (ROI 2–5)",
    "Excellent (ROI > 5)",
]

fct_campaign_kpis["roi_category"] = np.select(
    conditions, choices, default="Unknown"
)
overall_counts = (
    fct_campaign_kpis["roi_category"]
    .value_counts()
    .reindex(choices, fill_value=0)
)
total_campaigns = overall_counts.sum()
donut_colors = ["#d9534f", "#f0ad4e", "#5cb85c", "#2e7d32"]

# Đưa Legend ra cạnh phải để không bị dính chữ trên bánh Donut
wedges, texts, autotexts = ax_donut.pie(
    overall_counts.values,
    autopct="%1.1f%%",
    startangle=140,
    colors=donut_colors,
    pctdistance=0.75,
    wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
)

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(9.5)
    autotext.set_weight("bold")

ax_donut.legend(
    wedges,
    choices,
    title="ROI Categories",
    loc="center left",
    bbox_to_anchor=(0.95, 0.5),
    frameon=False,
)

ax_donut.text(
    0,
    0,
    f"WHOLE SYSTEM\n\n{total_campaigns:,}\nCampaigns",
    ha="center",
    va="center",
    fontsize=9.5,
    fontweight="bold",
    color="#222222",
)
add_chart_header(
    ax_donut,
    "76.2% of Campaigns are Profitable, but 23.8% (39k+ Campaigns) Suffer ROI Loss",
    "High-performing campaigns (ROI >= 2) cover system losses to maintain overall ~66% profit margin.\n"
    "Priority: Implement automated stop-loss rules for Poor campaigns (ROI < 0) to boost net revenue.",
)

# ==========================================
# ROW 4: TOP 10 vs BOTTOM 10
# ==========================================
gs_bottom = gridspec.GridSpecFromSubplotSpec(
    1, 2, subplot_spec=gs[3, :], wspace=0.18
)
ax_top10 = fig.add_subplot(gs_bottom[0])
ax_bot10 = fig.add_subplot(gs_bottom[1])

top10_roi = fct_campaign_kpis.nlargest(10, "calc_roi").sort_values(
    "calc_roi", ascending=True
)
bottom10_roi = fct_campaign_kpis.nsmallest(10, "calc_roi").sort_values(
    "calc_roi", ascending=True
)

bars1 = ax_top10.barh(
    top10_roi["Campaign_ID"].astype(str),
    top10_roi["calc_roi"],
    color="#27ae60",
    height=0.65,
)
ax_top10.set_title(
    "Top 10 High-Performing Campaigns (Best ROI)",
    fontsize=10.5,
    fontweight="bold",
    color="#1e8449",
    pad=10,
)
ax_top10.set_xlabel("ROI Ratio", fontsize=9, fontweight="bold")
ax_top10.grid(True, linestyle="--", alpha=0.5, axis="x")
ax_top10.spines["top"].set_visible(False)
ax_top10.spines["right"].set_visible(False)
ax_top10.bar_label(
    bars1, fmt="%.2f", padding=4, fontsize=8, fontweight="bold", color="#1e8449"
)

bars2 = ax_bot10.barh(
    bottom10_roi["Campaign_ID"].astype(str),
    bottom10_roi["calc_roi"],
    color="#e74c3c",
    height=0.65,
)
ax_bot10.set_title(
    "Bottom 10 Underperforming Campaigns (Worst ROI)",
    fontsize=10.5,
    fontweight="bold",
    color="#c0392b",
    pad=10,
)
ax_bot10.set_xlabel("ROI Ratio", fontsize=9, fontweight="bold")
ax_bot10.grid(True, linestyle="--", alpha=0.5, axis="x")
ax_bot10.yaxis.tick_right()
ax_bot10.yaxis.set_label_position("right")
ax_bot10.spines["top"].set_visible(False)
ax_bot10.spines["left"].set_visible(False)
ax_bot10.bar_label(
    bars2, fmt="%.2f", padding=4, fontsize=8, fontweight="bold", color="#c0392b"
)

pos_layer3 = ax_donut.get_position()  # Hoặc ax_funnel
pos_layer4 = ax_top10.get_position()

# 2. Tìm điểm NẰM CHÍNH GIỮA khoảng trắng giữa 2 tầng
# (Đít của Tầng 3 là pos_layer3.y0, Đầu của Tầng 4 là pos_layer4.y1)
mid_y = (pos_layer3.y0 + pos_layer4.y1) / 2
center_x = (pos_layer4.x0 + ax_bot10.get_position().x1) / 2

# 3. In Section Title & Subtitle đúng vào trung điểm mid_y đó
fig.text(
    center_x,
    mid_y + 0.006,
    "Extreme Performance Asymmetry: Top Performers (60–79x ROI) Offset ~100% Capital Loss in Bottom Campaigns",
    ha="center",
    va="bottom",
    fontsize=12.0,
    fontweight="bold",
    color="#1a252f",
)

fig.text(
    center_x,
    mid_y - 0.002,
    "Top campaigns drive system profitability, while bottom campaigns suffer total capital erosion (-0.99 ROI) from missing stop-loss controls.\n"
    "Action: Replicate high-ROI winning attributes and enforce automated campaign pausing when ROI dips below -0.50.",
    ha="center",
    va="top",
    fontsize=10,
    color="#444444",
)

plt.savefig("reports\\figures\\overview_dashboard", dpi=300, bbox_inches="tight")