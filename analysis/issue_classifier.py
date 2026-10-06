"""
Issue classifier categorizing feedback into survey-aligned issue taxonomy.
"""
from analysis.llm_client import LLMClient
from analysis.prompts import CLASSIFICATION_SYSTEM_PROMPT, CLASSIFICATION_USER_PROMPT
from config.constants import ISSUE_CATEGORIES
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class IssueClassifier:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.categories_str = "\n".join(
            f"- {k}: {v['description']}" for k, v in ISSUE_CATEGORIES.items()
        )

    def classify(self, text: str) -> Dict:
        """Classify a single feedback text into issue categories."""
        try:
            res = self.llm.chat(
                system_prompt=CLASSIFICATION_SYSTEM_PROMPT,
                user_prompt=CLASSIFICATION_USER_PROMPT.format(
                    text=text,
                    categories_list=self.categories_str,
                ),
                json_mode=True,
            )
            if isinstance(res, dict) and "primary_category" in res:
                return res
        except Exception as e:
            logger.warning(f"Issue classification error: {e}")

        # Fallback response
        return {
            "categories": ["search_accuracy"],
            "primary_category": "search_accuracy",
            "retrieval_type": "Contextual photos",
            "user_memory_cues": ["date", "place"],
            "search_failure_point": "retrieval",
            "severity": "medium",
        }
