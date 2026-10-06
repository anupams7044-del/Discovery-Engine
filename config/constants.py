"""
Constants: Issue categories, search queries, relevance keywords.
Refined based on survey data (70+ responses) — ordered by validated frequency.
"""

ISSUE_CATEGORIES = {
    # 🔴 Top issues (validated by survey at 15%+ mention rate)
    "search_accuracy": {
        "display_name": "Search Accuracy",
        "description": "Search returns irrelevant or incorrect results (Survey: ~40% reported)",
    },
    "missing_results": {
        "display_name": "Missing Results",
        "description": "Known photos not appearing in search results (Survey: ~35% reported)",
    },
    "face_recognition": {
        "display_name": "Face Recognition",
        "description": "Issues with facial recognition — confuses two people together (Survey: ~20%)",
    },
    "face_similarity": {
        "display_name": "Face Similarity",
        "description": "Mixes up two people who look similar (Survey: ~18%)",
    },
    "date_time_search": {
        "display_name": "Date/Time Search",
        "description": "Ignores year or month typed, shows recent photos instead (Survey: ~15%)",
    },
    # 🟡 Significant issues (found in scraping + interviews)
    "natural_language": {
        "display_name": "Natural Language Understanding",
        "description": "Cannot understand descriptive/conversational queries",
    },
    "location_search": {
        "display_name": "Location Search",
        "description": "Problems searching by location/place",
    },
    "text_search": {
        "display_name": "Text/OCR Search",
        "description": "OCR/text-in-photo search not working",
    },
    "object_recognition": {
        "display_name": "Object Recognition",
        "description": "Fails to recognize objects/scenes in photos",
    },
    "filter_limitations": {
        "display_name": "Filter Limitations",
        "description": "Insufficient filter/refinement options",
    },
    "memory_retrieval": {
        "display_name": "Memory-Based Retrieval",
        "description": "User remembers context but can't formulate search query",
    },
    "video_search": {
        "display_name": "Video Search",
        "description": "Cannot search within or for specific video content",
    },
    # 🟢 Lower frequency issues
    "speed_performance": {
        "display_name": "Speed/Performance",
        "description": "Search is slow or times out",
    },
    "indexing_delay": {
        "display_name": "Indexing Delay",
        "description": "New photos not indexed or searchable yet",
    },
    "cross_device_sync": {
        "display_name": "Cross-Device Sync",
        "description": "Search results differ across devices",
    },
    "ui_ux_issues": {
        "display_name": "UI/UX Issues",
        "description": "Confusing search interface or interaction patterns",
    },
    "privacy_concerns": {
        "display_name": "Privacy Concerns",
        "description": "Concerns about what data search uses",
    },
    "feature_request": {
        "display_name": "Feature Request",
        "description": "User requesting new search capabilities",
    },
    "other": {
        "display_name": "Other",
        "description": "Doesn't fit any specific category",
    },
}

SEARCH_QUERIES = [
    "Google Photos search not working",
    "Google Photos can't find photo",
    "Google Photos search feature",
    "Google Photos search old photos",
    "Google Photos find photo memory",
    "Google Photos search by description",
    "Google Photos search results missing",
    "Google Photos search improvement",
    "Google Photos search face recognition",
    "Google Photos search by location",
    "Google Photos search by date",
    "Google Photos search text in photos",
]

RELEVANCE_KEYWORDS = [
    "search", "find", "retrieve", "look for", "locate",
    "can't find", "not showing", "missing", "where is",
    "remember", "forgot", "old photo", "memory",
    "filter", "browse", "discover", "recognition",
]

REDDIT_SUBREDDITS = [
    "googlephotos",
    "google",
    "Android",
    "ios",
    "photography",
]
