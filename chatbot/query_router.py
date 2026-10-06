"""
Query router analyzing user intent and categorizing incoming questions into:
- OUT_OF_SCOPE: Greetings, chit-chat, unrelated general queries, coding, trivia, etc.
- STATS: Quantitative aggregation questions (volumes, counts, sentiment %, top issues).
- RAG: Specific Google Photos search research, feedback, issues, themes, or survey inquiries.
"""
import re
from typing import Literal

QueryType = Literal["OUT_OF_SCOPE", "STATS", "RAG"]

class QueryRouter:
    # Common greetings and chit-chat patterns
    GREETINGS_PATTERN = re.compile(
        r"^(hi|hello|hey|hey there|howdy|hola|greetings|good morning|good afternoon|good evening|what'?s up|sup|yo)"
        r"([\s,!?.].*)?$",
        re.IGNORECASE
    )
    
    CHITCHAT_PATTERN = re.compile(
        r"(how are you|how('s| is) it going|how do you do|how are you doing|"
        r"who are you|who made you|what can you do|what is your name|are you an? ai|"
        r"tell me a joke|write a (poem|song|story|code)|what is the (weather|capital)|"
        r"thank(s| you)?|bye|goodbye|see you)",
        re.IGNORECASE
    )

    # Domain keywords relevant to Google Photos and the Discovery Engine
    DOMAIN_KEYWORDS = [
        "google photo", "google photos", "photo", "photos", "picture", "pictures", 
        "image", "images", "video", "videos", "album", "gallery",
        "search", "searching", "query", "queries", "find", "finding", "lookup", "look for",
        "retrieval", "filter", "filters", "sorting", "result", "results",
        "issue", "issues", "problem", "problems", "pain point", "pain points", "failure", "failures", "breakdown",
        "face", "faces", "person", "people", "tag", "tagging", "name", "recognition",
        "date", "dates", "time", "timeline", "year", "month", "chronolog", "exif", "timestamp",
        "place", "places", "location", "locations", "map", "maps", "gps", "geotag",
        "missing", "disappear", "lost", "random", "wrong", "irrelevant", "accuracy", "precision",
        "survey", "respondent", "respondents", "feedback", "review", "reviews", "complaint", "complaints",
        "play store", "reddit", "dataset", "ingested", "scraped", "database",
        "kpi", "metric", "metrics", "success rate", "guardrail", "abandon", "abandonment", "scroll", "scrolling",
        "theme", "themes", "stories", "keywords", "mental model", "paradox", "multi-entity",
        "sentiment", "negative", "positive", "neutral", "frustration", "emotion",
        "solution", "solutions", "recommendation", "recommendations", "disambiguation", "roadmap", "fix", "improve"
    ]

    # Specific quantitative statistics patterns
    STAT_PATTERNS = [
        r"how many",
        r"total (scraped|reviews|items|data|analyzed|surveys|responses|feedback)",
        r"sentiment (percentage|breakdown|distribution|ratio|split)",
        r"top (issue|problem|complaint)",
        r"most common (issue|complaint|problem)",
        r"#1 (issue|problem|complaint)",
        r"number of (reviews|items|survey|respondents|complaints)",
        r"statistics|stats|quantitat",
    ]

    @classmethod
    def route(cls, query: str) -> QueryType:
        """Analyze and route user query."""
        if not query or not query.strip():
            return "OUT_OF_SCOPE"

        q_clean = query.strip()
        q_lower = q_clean.lower()

        # Check if contains any Google Photos domain keywords
        has_domain_keyword = any(kw in q_lower for kw in cls.DOMAIN_KEYWORDS)

        # 1. Check for pure greetings or chit-chat (e.g., "Hey there, hey, how are you?")
        is_greeting = bool(cls.GREETINGS_PATTERN.match(q_clean))
        is_chitchat = bool(cls.CHITCHAT_PATTERN.search(q_clean))

        # If it's a greeting/chit-chat and doesn't ask an explicit domain question
        if (is_greeting or is_chitchat) and not has_domain_keyword:
            return "OUT_OF_SCOPE"

        # If it has zero domain relevance (e.g. general trivia, coding, unrelated questions)
        if not has_domain_keyword:
            return "OUT_OF_SCOPE"

        # 2. Check for Statistical / Quantitative queries
        for p in cls.STAT_PATTERNS:
            if re.search(p, q_lower):
                return "STATS"

        # 3. Targeted Google Photos research inquiries
        return "RAG"
