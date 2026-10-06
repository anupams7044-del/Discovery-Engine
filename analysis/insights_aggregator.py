"""
Aggregates all analysis results into dashboard-ready metrics, KPI mapping, and survey comparisons.
"""
from database.database import SessionLocal
from database.models import AnalysisResult, ScrapedItem, IssueCategory
from sqlalchemy import func
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class InsightsAggregator:
    def _apply_source_filter(self, query, source_filter: str = None):
        if source_filter and source_filter != "All Sources":
            return query.filter(ScrapedItem.source == source_filter)
        return query

    def get_overview(self, source_filter: str = None) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            q_scraped = db.query(ScrapedItem)
            q_relevant = db.query(ScrapedItem).filter(ScrapedItem.is_relevant == True)
            q_analyzed = db.query(AnalysisResult).join(ScrapedItem, AnalysisResult.item_id == ScrapedItem.id)

            q_scraped = self._apply_source_filter(q_scraped, source_filter)
            q_relevant = self._apply_source_filter(q_relevant, source_filter)
            q_analyzed = self._apply_source_filter(q_analyzed, source_filter)

            total_scraped = q_scraped.count()
            total_relevant = q_relevant.count()
            total_analyzed = q_analyzed.count()

            # By source (no filter applied here to show all sources if needed, or filter it?)
            # Usually we don't filter the "by_source" chart by itself, or if we do it just shows 1 bar.
            # We'll leave it filtered so it reflects the selected slice.
            q_sources = db.query(ScrapedItem.source, func.count(ScrapedItem.id)).group_by(ScrapedItem.source)
            q_sources = self._apply_source_filter(q_sources, source_filter)
            sources = dict(q_sources.all())

            q_platforms = db.query(ScrapedItem.platform, func.count(ScrapedItem.id)).group_by(ScrapedItem.platform)
            q_platforms = self._apply_source_filter(q_platforms, source_filter)
            platforms = dict(q_platforms.all())

            return {
                "total_scraped": total_scraped,
                "total_relevant": total_relevant,
                "total_analyzed": total_analyzed,
                "relevance_rate": round((total_relevant / total_scraped * 100), 1) if total_scraped > 0 else 0,
                "by_source": sources,
                "by_platform": platforms,
            }
        finally:
            db.close()

    def get_sentiment_distribution(self, source_filter: str = None) -> Dict[str, int]:
        db = SessionLocal()
        try:
            q = db.query(AnalysisResult.sentiment_label, func.count(AnalysisResult.id))\
                .join(ScrapedItem, AnalysisResult.item_id == ScrapedItem.id)\
                .group_by(AnalysisResult.sentiment_label)
            q = self._apply_source_filter(q, source_filter)
            rows = q.all()
            return {r[0]: r[1] for r in rows if r[0]}
        finally:
            db.close()

    def get_issue_ranking(self, source_filter: str = None) -> List[Dict[str, Any]]:
        db = SessionLocal()
        try:
            q = db.query(
                AnalysisResult.primary_issue,
                func.count(AnalysisResult.id).label("cnt")
            ).join(ScrapedItem, AnalysisResult.item_id == ScrapedItem.id)\
             .group_by(AnalysisResult.primary_issue)\
             .order_by(func.count(AnalysisResult.id).desc())
            
            q = self._apply_source_filter(q, source_filter)
            results = q.all()

            total_issues = sum(r[1] for r in results) or 1
            return [
                {
                    "issue": r[0],
                    "count": r[1],
                    "percentage": round((r[1] / total_issues) * 100, 1),
                }
                for r in results if r[0]
            ]
        finally:
            db.close()

    def get_top_issue(self, source_filter: str = None) -> Dict[str, Any]:
        ranking = self.get_issue_ranking(source_filter)
        if ranking:
            return ranking[0]
        return {"issue": "N/A", "count": 0, "percentage": 0.0}

    def get_failure_point_distribution(self, source_filter: str = None) -> Dict[str, int]:
        db = SessionLocal()
        try:
            q = db.query(
                AnalysisResult.search_failure_point,
                func.count(AnalysisResult.id)
            ).join(ScrapedItem, AnalysisResult.item_id == ScrapedItem.id)\
             .group_by(AnalysisResult.search_failure_point)
            
            q = self._apply_source_filter(q, source_filter)
            rows = q.all()
            return {r[0]: r[1] for r in rows if r[0]}
        finally:
            db.close()

    def get_kpi_tree_impact(self, source_filter: str = None) -> Dict[str, Any]:
        """Maps discovered issue volume directly to KPI Tree metrics."""
        ranking = self.get_issue_ranking(source_filter)
        total_complaints = sum(r["count"] for r in ranking) or 1

        accuracy_issues = sum(r["count"] for r in ranking if r["issue"] in ("search_accuracy", "missing_results"))
        friction_issues = sum(r["count"] for r in ranking if r["issue"] in ("date_time_search", "natural_language", "filter_limitations"))
        fairness_issues = sum(r["count"] for r in ranking if "face" in r["issue"])

        return {
            "search_success_rate_impact": round((accuracy_issues / total_complaints) * 100, 1),
            "search_friction_impact": round((friction_issues / total_complaints) * 100, 1),
            "demographic_parity_impact": round((fairness_issues / total_complaints) * 100, 1),
            "leading_indicator": "High Queries per Session indicates retry loops caused by inaccurate retrieval.",
        }

    def get_full_summary(self, source_filter: str = None) -> Dict[str, Any]:
        return {
            "overview": self.get_overview(source_filter),
            "sentiment": self.get_sentiment_distribution(source_filter),
            "issues": self.get_issue_ranking(source_filter),
            "top_issue": self.get_top_issue(source_filter),
            "failure_points": self.get_failure_point_distribution(source_filter),
            "kpi_impact": self.get_kpi_tree_impact(source_filter),
        }

