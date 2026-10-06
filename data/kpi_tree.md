# KPI Tree — Google Photos Search Feature

## 1. Top-Level Metric
**Total No. of Successful Searches** = Total No. of Search Queries (Attempts) × Search Success Rate (%)

## 2. Query Volume Breakdown
**Total No. of Search Queries (Attempts)** = Total No. of Search Users × Average No. of Searches per User (⬇)

## 3. User Volume Breakdown
**Total No. of Search Users** = Total No. of Active Users × % of Active Users Who Are Search Users

## 4. Frequency Breakdown [Friction Metric — Target: MINIMIZE]
**Average No. of Searches per User (⬇)** = Average No. of Search Sessions per User × Average No. of Queries per Search Session (⬇)

> A high number of queries per session indicates friction — users are retrying because search isn't working.

## 5. Success Rate Breakdown
**Search Success Rate (%)** = Number of Searches Resulting in a Target Action (View, Share, or Edit) ÷ Total No. of Search Queries (Attempts)

---

## Guardrail Metrics

| Guardrail | What It Protects |
|-----------|-----------------|
| Search Result Relevance | Core quality — are the right photos shown? |
| Search Latency | Performance — results load fast enough |
| Zero-Result Query Rate | Coverage — queries that return nothing |
| Crash Rate | Stability — app doesn't break during search |
| Infrastructure/Compute Costs | Business — AI features don't bankrupt ops |
| Demographic Parity Gap | Fairness — facial recognition works across all skin tones |
| Device Battery/Resource Drain | UX — search doesn't kill user's phone |
| Backup Sync Reliability | Data — photos are actually available to search |
