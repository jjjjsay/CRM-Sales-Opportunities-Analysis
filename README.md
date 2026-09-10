# CRM-Sales-Opportunities-Analysis
### Executive Summary
This project analyzes twelve months of B2B sales pipeline activity (October 2016 – December 2017) for a fictitious computer-hardware company, covering 8,800 opportunities across three regional offices, six managers, 30 agents, seven products, and 85 client accounts. The goal was to move past top-line reporting and identify where revenue is being won or left on the table — and to translate that into specific, actionable recommendations.
Across the dataset, the sales team closed $10.0M in won revenue at a 63.2% win rate on 6,711 closed opportunities, with 2,089 opportunities still active in the pipeline. Three findings stand out:

●	Win rate is falling every quarter. From 82.1% in Q1 2017 to 60.3% in Q4 2017 — a 22-point decline over three consecutive quarters, even as deal volume held steady.

●	Performance gaps between agents are large and persistent. The five lowest-performing agents (by win rate) are 8–14 points below the company average despite carrying comparable or larger deal loads, pointing to a coaching and process gap rather than a market or territory problem.

●	Revenue is concentrated in two products with headroom in a third. GTX Pro and GTX Plus Pro alone generate 61% of won revenue at above-average win rates, while MG Advanced — the second-highest-volume product — wins 3 points below the company average, worth roughly $110K in recoverable revenue if it simply matched the mean.

A data-quality issue was also identified and corrected during this analysis: the product “GTX Pro” was recorded under two spellings (“GTX Pro” and “GTXPro”) across 1,480 opportunities — 17% of the pipeline — which silently excluded the company's single largest product from every product-level report until it was fixed. This is flagged in the Methodology section and is itself a recommendation: without correcting it, GTX Pro's true $3.51M in won revenue would not appear in any dashboard built directly on this table.

The recommendations that follow focus on three levers the business can act on directly: reversing the win-rate decline, closing the agent performance gap through targeted coaching, and reallocating sales focus toward the products and regions with the best return per opportunity.

### Business Problem
Sales leadership can see that deals are closing, but not why some regions, agents, and products consistently outperform others, or why performance seems to be softening over the course of the year. Without this visibility, management is limited to reactive, anecdotal coaching rather than targeted, data-backed intervention. The stakeholders below need answers to four connected questions before the next planning cycle:

●	Team performance — How does each sales team (regional office and manager) compare, and is the gap between the best and worst performers wide enough to justify reallocating headcount or coaching resources?

●	Agent performance — Which individual agents are lagging, and is it a volume problem (too few deals), a conversion problem (low win rate), or both?

●	Time trends — Is quarter-over-quarter performance improving, flat, or declining, and does that trend say something about the pipeline, the team, or the season?

●	Product performance — Do any products convert meaningfully better or worse than others, and should sales effort be redirected accordingly?

The intended audience for this analysis is sales leadership and regional managers who need a clear, evidence-based view of where to focus limited coaching and pipeline-management effort over the next two quarters.


### Methodology

Data Sources
Four related tables were combined into a single analytical dataset: sales_pipeline.csv (8,800 opportunities — the fact table), accounts.csv (85 client accounts), products.csv (7 products across 3 series), and sales_teams.csv (30 agents, 6 managers, 3 regional offices). A data dictionary confirmed field definitions and relationships prior to joining.

Data Cleaning
●	Product name mismatch: “GTX Pro” appeared as two distinct strings — “GTX Pro” in the products table and “GTXPro” (no space) in 1,480 pipeline rows. Left unfixed, a standard join drops these rows from every product-level metric, hiding the company's single largest product from analysis. All “GTXPro” values were standardized to “GTX Pro” before joining.

●	Sector typo: the value “technolgy” in accounts.csv was corrected to “technology” for consistent grouping.

●	Missing values: 1,425 opportunities have no account, and 2,089 unclosed opportunities (“Engaging” / “Prospecting”) have no close_date or close_value by definition — these were kept and analyzed separately as open pipeline rather than dropped.

Analytical Approach

●	Win rate is calculated only against closed opportunities (Won ÷ [Won + Lost]); open opportunities are excluded from win-rate denominators since their outcome is not yet known.

●	Revenue figures reflect close_value on Won deals only, aggregated by region, manager, agent, product, sector, and quarter.

●	Sales cycle length is measured as close_date minus engage_date in days, compared between Won and Lost outcomes.

●	Quarterly trend uses close_date to bucket deals into calendar quarters; Q1 2017 reflects a smaller, earlier cohort of the pipeline and is noted as a lower-volume baseline quarter rather than treated as equivalent to the fuller Q2–Q4 quarters.

All analysis was performed in Python (pandas for data manipulation, matplotlib for visualization) on the full population of 8,800 opportunities — no sampling was used.


### Skills Demonstrated

This project was used as a practical exercise across the following areas:

●	Data wrangling: multi-table joins, detecting and resolving a real-world entity-resolution issue (product name mismatch), handling missing and open-pipeline data appropriately rather than dropping it.

●	Exploratory & diagnostic analysis: cohort segmentation by region, manager, agent, product, sector, and time period; funnel and conversion-rate analysis; sales-cycle-length comparison.

●	Data visualization: designed a consistent chart system (dual-axis revenue/win-rate views, ranked bar charts, bubble scatter for two-dimensional agent comparison) built to make the underlying finding, not just the number, immediately legible.

●	Business translation: converting statistical findings (e.g., a 3-point win-rate gap on a specific product) into dollar-quantified, prioritized recommendations that a sales leader can act on without further analysis.

●	Tools: Python (pandas, matplotlib), CSV/relational data modeling, Microsoft Word report authoring.

