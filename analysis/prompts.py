"""
Prompts for AI Analysis Engine: Sentiment, Issue Classification, Theme Extraction.
"""

SENTIMENT_SYSTEM_PROMPT = """
You are an expert NLP researcher analyzing customer reviews and forum posts about Google Photos' search feature.
Analyze the sentiment and emotional state of each review.

Output valid JSON matching this schema:
{
  "results": [
    {
      "item_index": int,
      "label": "positive" | "negative" | "neutral" | "mixed",
      "score": float (-1.0 to 1.0),
      "confidence": float (0.0 to 1.0),
      "emotion": "frustration" | "confusion" | "satisfaction" | "disappointment" | "indifference",
      "intensity": "mild" | "moderate" | "strong"
    }
  ]
}
"""

SENTIMENT_USER_PROMPT = """
Analyze the sentiment of the following {count} user feedback items:

{batch_text}
"""

CLASSIFICATION_SYSTEM_PROMPT = """
You are a senior Product Manager and NLP engineer analyzing user search friction in Google Photos.
Classify user feedback into predefined issue categories, failure points in the user journey, and memory cues.

Output valid JSON matching this schema:
{
  "categories": ["primary_issue", "secondary_issue"],
  "primary_category": "exact_category_name",
  "retrieval_type": "what user was looking for (e.g., 'family photo', 'receipt', 'specific person')",
  "user_memory_cues": ["place", "date", "person", "clothing", "event"],
  "search_failure_point": "query_formulation" | "understanding" | "retrieval" | "ranking" | "refinement",
  "severity": "low" | "medium" | "high" | "critical"
}
"""

CLASSIFICATION_USER_PROMPT = """
Text to analyze:
\"\"\"{text}\"\"\"

Allowed issue categories:
{categories_list}
"""

THEME_SYSTEM_PROMPT = """
You are an AI research analyst. Extract recurring overarching themes across this collection of user complaints about Google Photos search.

Output valid JSON matching this schema:
{
  "themes": [
    {
      "name": "Theme title",
      "description": "Clear explanation of the theme",
      "frequency_estimate": "high" | "medium" | "low",
      "representative_quote": "Direct quote from feedback",
      "user_impact": "How it impacts the user experience"
    }
  ]
}
"""
