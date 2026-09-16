"""
CRM Sales Opportunities Analysis
=================================
B2B sales pipeline analysis: team/agent performance, quarterly trends,
and product win rates, with charts saved to `figs/`.

Data: place accounts.csv, products.csv, sales_pipeline.csv, sales_teams.csv
in a `data/` folder alongside this script (source: Maven Analytics
"CRM Sales Opportunities" dataset).

Usage:
    pip install pandas numpy matplotlib
    python crm_sales_analysis.py

Author: Jay (JJ)
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DATA_DIR = "data"
FIG_DIR = "figs"
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

NAVY, TEAL, ORANGE, GREY, RED, GREEN = (
    "#1F3B57", "#2E8B8B", "#E07A3F", "#8C97A8", "#C0453A", "#3F8F5C",
)


# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------
def load_data(data_dir: str = DATA_DIR) -> dict:
    """Load the four raw CRM tables."""
    return {
        "pipeline": pd.read_csv(f"{data_dir}/sales_pipeline.csv"),
        "accounts": pd.read_csv(f"{data_dir}/accounts.csv"),
        "products": pd.read_csv(f"{data_dir}/products.csv"),
        "teams": pd.read_csv(f"{data_dir}/sales_teams.csv"),
    }


# ---------------------------------------------------------------------------
# 2. Clean + join
# ---------------------------------------------------------------------------
def clean_and_merge(pipe: pd.DataFrame, acc: pd.DataFrame,
                     prod: pd.DataFrame, team: pd.DataFrame) -> pd.DataFrame:
    """
    Fix known data-quality issues and join the four tables into one
    analysis-ready dataframe (one row per opportunity).

    Known issues fixed:
    - "GTX Pro" is recorded as two distinct strings in sales_pipeline.csv
      ("GTX Pro" and "GTXPro", no space) across 1,480 rows (17% of the
      pipeline). Left unfixed, a standard join on `product` silently drops
      these rows from every product-level metric.
    - accounts.sector has a typo: "technolgy" -> "technology".
    """
    pipe = pipe.copy()
    pipe["product"] = pipe["product"].replace({"GTXPro": "GTX Pro"})
    pipe["engage_date"] = pd.to_datetime(pipe["engage_date"])
    pipe["close_date"] = pd.to_datetime(pipe["close_date"])

    acc = acc.copy()
    acc["sector"] = acc["sector"].replace({"technolgy": "technology"})

    df = (
        pipe.merge(team, on="sales_agent", how="left")
            .merge(prod, on="product", how="left")
            .merge(acc, on="account", how="left")
    )
    return df


# ---------------------------------------------------------------------------
# 3. Metrics
# ---------------------------------------------------------------------------
def split_closed_won(df: pd.DataFrame):
    """Return (closed, won) subsets. Win rate = won / closed."""
    closed = df[df["deal_stage"].isin(["Won", "Lost"])].copy()
    closed["cycle_days"] = (closed["close_date"] - closed["engage_date"]).dt.days
    won = df[df["deal_stage"] == "Won"].copy()
    return closed, won


def win_rate_table(closed: pd.DataFrame, won: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Deals / win rate / revenue won, grouped by any dimension (region, agent, product, ...)."""
    g = closed.groupby(group_col).agg(
        deals=("opportunity_id", "count"),
        won=("deal_stage", lambda x: (x == "Won").sum()),
    )
    g["win_rate"] = g["won"] / g["deals"]
    g["total_revenue"] = won.groupby(group_col)["close_value"].sum().reindex(g.index).fillna(0)
    return g.sort_values("total_revenue", ascending=False)


def quarterly_trend(closed: pd.DataFrame, won: pd.DataFrame) -> pd.DataFrame:
    """Revenue and win rate by close-date quarter."""
    won = won.copy()
    closed = closed.copy()
    won["quarter"] = won["close_date"].dt.to_period("Q").astype(str)
    closed["quarter"] = closed["close_date"].dt.to_period("Q").astype(str)
    revenue = won.groupby("quarter")["close_value"].sum()
    win_rate = closed.groupby("quarter").apply(lambda x: (x["deal_stage"] == "Won").mean())
    out = pd.DataFrame({"revenue": revenue, "win_rate": win_rate}).sort_index()
    out["qoq_growth"] = out["revenue"].pct_change()
    return out


# ---------------------------------------------------------------------------
# 4. Charts
# ---------------------------------------------------------------------------
def chart_regional_performance(reg: pd.DataFrame, path: str):
    fig, ax1 = plt.subplots(figsize=(7.5, 4.2))
    x = np.arange(len(reg))
    ax1.bar(x, reg["total_revenue"] / 1e6, color=NAVY, width=0.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg.index, fontsize=11)
    ax1.set_ylabel("Revenue Won ($M)", fontsize=10)
    for i, v in enumerate(reg["total_revenue"] / 1e6):
        ax1.text(i, v + 0.05, f"${v:.2f}M", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")

    ax2 = ax1.twinx()
    ax2.plot(x, reg["win_rate"] * 100, color=ORANGE, marker="o", markersize=7, linewidth=2.2)
    for i, v in enumerate(reg["win_rate"] * 100):
        ax2.text(i, v + 1.3, f"{v:.1f}%", ha="center", fontsize=9.5, color=ORANGE, fontweight="bold")
    ax2.set_ylabel("Win Rate (%)", fontsize=10)
    ax2.set_ylim(50, 75)

    ax1.set_title("Revenue and Win Rate by Regional Office", fontsize=12.5,
                   fontweight="bold", color=NAVY, pad=12)
    fig.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def chart_agent_scatter(agent: pd.DataFrame, overall_win_rate: float, path: str):
    office_colors = {"Central": NAVY, "East": TEAL, "West": ORANGE}
    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    for office, color in office_colors.items():
        sub = agent[agent.regional_office == office]
        ax.scatter(sub["win_rate"] * 100, sub["total_revenue"] / 1e3, s=sub["deals"] * 1.6,
                   color=color, alpha=0.75, edgecolor="white", linewidth=0.8, label=office)

    mean_wr = agent["win_rate"].mean() * 100
    ax.axvline(mean_wr, color=GREY, linestyle="--", linewidth=1, alpha=0.7)
    ax.text(mean_wr + 0.5, ax.get_ylim()[1] * 0.96, f"avg win rate {mean_wr:.0f}%",
            fontsize=8.5, color=GREY)

    laggards = agent[agent.deals >= 20].nsmallest(3, "win_rate")
    for name, row in laggards.iterrows():
        parts = name.split()
        label = f"{parts[0]} {parts[1][0]}."
        ax.annotate(label, (row["win_rate"] * 100, row["total_revenue"] / 1e3),
                    fontsize=8, color=RED, fontweight="bold", xytext=(5, -10),
                    textcoords="offset points")

    ax.set_xlabel("Win Rate (%)", fontsize=10)
    ax.set_ylabel("Total Revenue Won ($ thousands)", fontsize=10)
    ax.set_title("Agent Performance: Win Rate vs. Revenue\n(bubble size = number of deals worked)",
                 fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.legend(title="Regional Office", fontsize=9, title_fontsize=9, loc="upper left")
    fig.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def chart_quarterly_trend(qdf: pd.DataFrame, path: str):
    fig, ax1 = plt.subplots(figsize=(7.5, 4.2))
    x = np.arange(len(qdf))
    ax1.bar(x, qdf["revenue"] / 1e6, color=NAVY, width=0.5)
    for i, v in enumerate(qdf["revenue"] / 1e6):
        ax1.text(i, v + 0.05, f"${v:.2f}M", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(qdf.index, fontsize=10.5)
    ax1.set_ylabel("Revenue Won ($M)", fontsize=10)

    ax2 = ax1.twinx()
    ax2.plot(x, qdf["win_rate"] * 100, color=ORANGE, marker="o", markersize=7, linewidth=2.2)
    for i, v in enumerate(qdf["win_rate"] * 100):
        ax2.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=9.5, color=ORANGE, fontweight="bold")
    ax2.set_ylabel("Win Rate (%)", fontsize=10)
    ax2.set_ylim(50, 90)

    ax1.set_title("Quarterly Revenue and Win Rate, 2017", fontsize=12.5,
                   fontweight="bold", color=NAVY, pad=12)
    fig.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def chart_product_win_rate(pr: pd.DataFrame, overall_win_rate: float, path: str):
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    y = np.arange(len(pr))
    colors_bar = [GREEN if wr >= overall_win_rate else RED for wr in pr["win_rate"]]
    ax.barh(y, pr["win_rate"] * 100, color=colors_bar, height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(pr.index, fontsize=10.5)
    ax.invert_yaxis()
    ax.axvline(overall_win_rate * 100, color=GREY, linestyle="--", linewidth=1.3)
    ax.text(overall_win_rate * 100 + 0.6, -0.55, f"company avg {overall_win_rate * 100:.0f}%",
            fontsize=8.5, color=GREY)
    for i, (wr, rev) in enumerate(zip(pr["win_rate"] * 100, pr["total_revenue"])):
        ax.text(wr + 0.8, i, f"{wr:.1f}%  (${rev / 1e6:.2f}M won)", va="center", fontsize=9, color="#333")
    ax.set_xlabel("Win Rate (%)", fontsize=10)
    ax.set_xlim(0, 85)
    ax.set_title("Win Rate by Product (revenue won in parentheses)", fontsize=12,
                 fontweight="bold", color=NAVY, pad=10)
    fig.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def chart_funnel(counts: pd.Series, path: str):
    stages = ["Prospecting", "Engaging", "Won", "Lost"]
    vals = [counts.get(s, 0) for s in stages]
    colors_funnel = [GREY, TEAL, GREEN, RED]

    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    bars = ax.bar(stages, vals, color=colors_funnel, width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 40, f"{v:,}", ha="center",
                fontsize=10.5, fontweight="bold", color="#333")
    ax.set_ylabel("Number of Opportunities", fontsize=10)
    ax.set_title("Pipeline Composition, All Opportunities (Oct 2016 \u2013 Dec 2017)",
                 fontsize=12, fontweight="bold", color=NAVY, pad=12)
    ax.set_ylim(0, max(vals) * 1.18)
    fig.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    raw = load_data()
    df = clean_and_merge(raw["pipeline"], raw["accounts"], raw["products"], raw["teams"])
    closed, won = split_closed_won(df)

    overall_win_rate = len(won) / len(closed)
    total_revenue = won["close_value"].sum()
    avg_deal = won["close_value"].mean()
    print(f"Overall win rate:  {overall_win_rate:.1%}")
    print(f"Total won revenue: ${total_revenue:,.0f}")
    print(f"Avg deal size:     ${avg_deal:,.0f}")
    print(f"Avg cycle (won):   {closed[closed.deal_stage == 'Won'].cycle_days.mean():.1f} days")
    print(f"Avg cycle (lost):  {closed[closed.deal_stage == 'Lost'].cycle_days.mean():.1f} days\n")

    # --- Regional office performance ---
    reg = win_rate_table(closed, won, "regional_office")
    print("=== Regional office performance ===")
    print(reg, "\n")
    chart_regional_performance(reg, f"{FIG_DIR}/fig1_regional.png")

    # --- Agent performance ---
    agent = win_rate_table(closed, won, "sales_agent")
    agent = agent.merge(raw["teams"][["sales_agent", "regional_office"]],
                        left_index=True, right_on="sales_agent").set_index("sales_agent")
    print("=== Lowest win-rate agents (min. 20 deals) ===")
    print(agent[agent.deals >= 20].nsmallest(5, "win_rate")[["deals", "win_rate", "total_revenue"]], "\n")
    chart_agent_scatter(agent, overall_win_rate, f"{FIG_DIR}/fig2_agents.png")

    # --- Quarterly trend ---
    qdf = quarterly_trend(closed, won)
    print("=== Quarterly revenue & win rate ===")
    print(qdf, "\n")
    chart_quarterly_trend(qdf, f"{FIG_DIR}/fig3_quarterly.png")

    # --- Product performance ---
    pr = win_rate_table(closed, won, "product")
    print("=== Product performance ===")
    print(pr, "\n")
    chart_product_win_rate(pr, overall_win_rate, f"{FIG_DIR}/fig4_products.png")

    # --- Pipeline funnel ---
    chart_funnel(df["deal_stage"].value_counts(), f"{FIG_DIR}/fig5_funnel.png")

    print(f"\nAll charts saved to {FIG_DIR}/")


if __name__ == "__main__":
    main()
