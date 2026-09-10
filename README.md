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


### Results & Business Recommendation

Pipeline Overview
Of 8,800 total opportunities, 6,711 have closed (76%) and 2,089 remain open (24%). Among closed deals, the company wins 63.2% of the time, generating $10.0M in total revenue at an average deal size of $2,361. Won deals take longer to close than lost ones — 51.8 days versus 41.5 days on average — which is expected: deals that are ultimately lost tend to be disqualified or abandoned earlier, while deals that convert go through a fuller negotiation cycle.
<img width="734" height="353" alt="image" src="https://github.com/user-attachments/assets/d797bd8d-4892-4487-8b1b-6b4d522540ca" />
Figure 1. Pipeline composition across all 8,800 opportunities, October 2016–December 2017.

1. Regional Office Performance
All three regional offices perform within a narrow band — no office is dramatically underperforming, but the ranking is consistent and revenue-meaningful.

<img width="734" height="411" alt="image" src="https://github.com/user-attachments/assets/d780b76e-38df-40b0-b91a-d7d408aa3e3a" />
Figure 2. Revenue won and win rate by regional office.
Regional Office	Closed Deals	Win Rate	Revenue Won	Avg Deal Size
West	2,249	63.9%	$3.57M	$2,482
Central	2,604	62.6%	$3.35M	$2,054
East	1,858	63.0%	$3.09M	$2,639

West leads on both revenue and win rate despite handling fewer deals than Central, and East posts the highest average deal size of any office — suggesting East's agents are working a smaller number of higher-value opportunities. Central handles the most volume (2,604 deals) but converts at the lowest rate (62.6%) and has the smallest average deal size, making it the office with the most room for coaching-driven improvement: closing Central's win-rate gap to West's level alone would be worth roughly $135K in incremental won revenue on its existing pipeline.
2. Are Any Sales Agents Lagging Behind?
Yes — and the gap is large enough to matter. Plotting each of the 30 agents by win rate and revenue (bubble size = deals worked) makes the pattern clear: a cluster of agents sits well below the 63.5% company-average win rate line, and it is not simply the agents with fewer deals.

<img width="734" height="489" alt="image" src="https://github.com/user-attachments/assets/528d0211-0d7d-4f0f-aa05-b2f33a7c7140" /> 
Figure 3. Agent win rate vs. revenue won; bubble size reflects deal volume.

Agent	Regional Office	Deals	Win Rate	Revenue Won
Lajuana Vencill	Central	231	55.0%	$194,632
Markita Hansen	West	227	57.3%	$328,792
Donn Cantrell	East	275	57.5%	$445,860
Gladys Colclough	Central	232	58.2%	$345,674
Niesha Huffines	Central	175	60.0%	$176,961

These five agents are carrying deal volumes in line with or above the company median (175–275 deals each) but converting 6–14 points below the 63.2% company average. That combination — adequate volume, low conversion — points to a coaching and technique gap rather than a territory or lead-quality problem, since these agents are clearly being given opportunities to work. Notably, three of the five bottom performers by win rate sit in the Central office, reinforcing the regional finding above. Separately, Violet Mclelland and Wilburn Farren post the lowest total revenue despite decent win rates (63.2% and 69.6%), because they are working the fewest deals overall (193 and 79) — a pipeline-volume issue rather than a conversion issue, and a different kind of intervention.
3. Quarter-over-Quarter Trends
This is the most urgent finding in the dataset. Win rate has declined every quarter since Q1 2017, from 82.1% down to 60.3% by Q4 — a 22-point drop — even though deal volume stayed roughly flat (2,032 to 1,985 closed deals per quarter from Q2 onward). Revenue has softened in step, falling from $3.09M in Q2 to $2.80M in Q4.

<img width="734" height="411" alt="image" src="https://github.com/user-attachments/assets/58c99a22-b6af-40de-a2ec-6c73cdf4530d" /> 
Figure 4. Quarterly revenue won and win rate, 2017. (Q1 reflects a smaller early cohort as the pipeline ramped up and should be read as a baseline rather than a directly comparable quarter.)
Because deal volume didn't drop while win rate did, the decline is best explained by conversion — how effectively opportunities are being closed — rather than a shrinking pipeline. This is consistent with, and likely connected to, the agent-level gaps identified above: if underperforming agents are absorbing a growing share of the pipeline over the year, or if the whole team's technique has drifted without reinforcement, the aggregate win rate would erode exactly like this. This trend deserves the highest priority of any finding in this report, since a continued decline at the current rate would erase another 10–15 points of win rate by mid-2018.
4. Product Win Rates
Product-level win rates cluster tightly between 60% and 65%, but the revenue each product generates is highly uneven — and the two dimensions don't always move together.

<img width="734" height="433" alt="image" src="https://github.com/user-attachments/assets/e1c50b18-0e74-4f7f-a43a-6df02a2f4c57" /> 
Figure 5. Win rate by product, with total revenue won shown alongside each bar.
Product	Series	Deals Closed	Win Rate	Revenue Won
GTX Pro	GTX	1,147	63.6%	$3.51M
GTX Plus Pro	GTX	745	64.3%	$2.63M
MG Advanced	MG	1,084	60.3%	$2.22M
GTX Plus Basic	GTX	1,051	62.1%	$0.71M
GTX Basic	GTX	1,436	63.7%	$0.50M
GTK 500	GTK	25	60.0%	$0.40M
MG Special	MG	1,223	64.8%	$0.04M

GTX Pro and GTX Plus Pro together account for 61% of all won revenue ($6.14M of $10.0M) and both convert above the company average — they are the business's clear anchor products. MG Advanced is the concerning outlier: it is the second-highest-volume product (1,084 deals closed) but converts 3 points below the company average at 60.3%. Closing that gap to the 63.2% company average would be worth approximately $110K in additional won revenue from the same pipeline, with no increase in deal volume required. GTK 500 is a small-volume, high-price outlier (only 25 deals, but a $26,768 list price) and MG Special is the inverse — highest win rate of any product (64.8%) but negligible revenue impact ($55 list price) — useful as a low-friction entry product but not a revenue lever.

