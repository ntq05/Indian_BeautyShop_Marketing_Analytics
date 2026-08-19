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
        fontsize=15,
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
        fontsize=12,
        color="#555555",
        style="italic",  # Có thể nghiêng hoặc không
        ha="left",
        va="bottom",
    )