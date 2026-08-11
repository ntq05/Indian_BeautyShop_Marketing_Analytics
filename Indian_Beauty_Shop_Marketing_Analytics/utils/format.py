import pandas as pd

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
    