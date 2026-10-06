"""
Unified LLM client supporting OpenAI, Google Gemini, and Local Rule-Based NLP Fallback.
"""
import os
import json
import re
import logging
from typing import Dict, Any, List, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.provider = settings.llm_provider
        self.openai_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.google_key = settings.google_api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

        self.client = None
        self.mode = "local"

        if self.provider == "openai" and self.openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.mode = "openai"
                logger.info(f"Initialized OpenAI client ({settings.llm_model})")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")

        elif (self.provider == "google" or self.google_key) and self.google_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.google_key)
                self.client = genai.GenerativeModel("gemini-2.0-flash")
                self.mode = "google"
                logger.info("Initialized Google Gemini client")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Gemini: {e}")

        if self.mode == "local":
            logger.info("Using Local NLP heuristic engine (no API key configured).")

    def chat(self, system_prompt: str, user_prompt: str, json_mode: bool = True) -> Any:
        """Execute chat completion with automatic fallback."""
        if self.mode == "openai":
            try:
                res = self.client.chat.completions.create(
                    model=settings.llm_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"} if json_mode else None,
                    temperature=0.2,
                )
                content = res.choices[0].message.content
                return json.loads(content) if json_mode else content
            except Exception as e:
                logger.warning(f"OpenAI call failed ({e}), falling back to local NLP heuristics")

        elif self.mode == "google":
            try:
                prompt_combined = f"{system_prompt}\n\nTask:\n{user_prompt}"
                if json_mode:
                    prompt_combined += "\n\nRespond with valid raw JSON only. Do not wrap in markdown quotes."
                res = self.client.generate_content(prompt_combined)
                text = res.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()
                return json.loads(text) if json_mode else text
            except Exception as e:
                logger.warning(f"Google Gemini call failed ({e}), falling back to local NLP heuristics")

        return self._local_fallback(system_prompt, user_prompt, json_mode)

    def _local_fallback(self, system_prompt: str, user_prompt: str, json_mode: bool) -> Any:
        """Heuristic NLP fallback with distinct branches for sentiment, classification, and RAG chat."""
        # 1. Chatbot Synthesis Branch
        if "discovery engine assistant" in system_prompt.lower() or "retrieved user feedback chunks" in user_prompt.lower():
            question_match = re.search(r'User Question:\s*(.*)', user_prompt, re.IGNORECASE)
            question = question_match.group(1).strip() if question_match else "Google Photos Search"
            
            from chatbot.query_router import QueryRouter
            if QueryRouter.route(question) == "OUT_OF_SCOPE":
                return (
                    "I can only assist with Google Photos search research (user feedback, discovery metrics, search failure root causes, strategic themes, and survey findings).\n\n"
                    "Please ask a relevant query or select one of the options at the top of the page."
                )
            
            from chatbot.rag_pipeline import ChatbotRAG
            rag = ChatbotRAG()
            matches = rag.retriever.retrieve(question, top_k=5)
            return rag._synthesize_grounded_answer(question, matches)

        # 2. Sentiment Analysis Branch
        if "sentiment and emotional state" in system_prompt.lower() or "analyze the sentiment" in user_prompt.lower():
            match = re.search(r'"""(.*?)"""', user_prompt, re.DOTALL)
            text_target = match.group(1).lower() if match else user_prompt.lower()

            neg_words = [
                "terrible", "worst", "hate", "awful", "useless", "broken", "fail", "wrong", 
                "random", "doesn't work", "cant find", "can't find", "miss", "lost", "bad", 
                "bug", "confused", "frustrated", "annoying", "garbage", "rubbish", "disappoint", "sucks"
            ]
            pos_words = [
                "love", "great", "best", "good", "amazing", "helpful", "perfect", "easy", 
                "accurate", "finds everything", "awesome", "smooth", "excellent", "fast"
            ]
            
            neg_count = sum(1 for w in neg_words if w in text_target)
            pos_count = sum(1 for w in pos_words if w in text_target)

            if neg_count > pos_count:
                label = "negative"
                score = -0.75
                emotion = "frustration"
                intensity = "strong" if neg_count >= 2 else "moderate"
            elif pos_count > neg_count:
                label = "positive"
                score = 0.75
                emotion = "satisfaction"
                intensity = "moderate"
            elif neg_count > 0 and pos_count > 0:
                label = "mixed"
                score = -0.1
                emotion = "confusion"
                intensity = "moderate"
            else:
                label = "neutral"
                score = 0.0
                emotion = "indifference"
                intensity = "mild"

            return {"label": label, "score": score, "confidence": 0.90, "emotion": emotion, "intensity": intensity}

        # 3. Issue Classification Branch
        match = re.search(r'"""(.*?)"""', user_prompt, re.DOTALL)
        text_target = match.group(1).lower() if match else user_prompt.lower()

        scores = {
            "search_accuracy": 0, "missing_results": 0, "face_recognition": 0,
            "face_similarity": 0, "date_time_search": 0, "location_search": 0,
            "natural_language": 0, "text_search": 0, "video_search": 0, "filter_limitations": 0,
        }

        if any(w in text_target for w in ["random", "wrong photo", "irrelevant", "incorrect", "bad result", "not what i asked", "wrong person", "wrong place"]):
            scores["search_accuracy"] += 5
        if any(w in text_target for w in ["no photos found", "can't find", "cannot find", "missing", "disappeared", "not found", "where is"]):
            scores["missing_results"] += 5
        if any(w in text_target for w in ["face", "facial", "person", "mom and dad", "two people", "faces"]):
            scores["face_recognition"] += 4
        if any(w in text_target for w in ["similar", "mixes up", "mix up", "looks like", "confuses two people"]):
            scores["face_similarity"] += 5
        if any(re.search(r'\b(year|month|date|dated|timeline|chronological|recent|202[0-9]|201[0-9])\b', text_target) for _ in [1]):
            scores["date_time_search"] += 4
        if any(w in text_target for w in ["location", "place", "city", "country", "map", "gps", "travel", "trip", "beach", "goa"]):
            scores["location_search"] += 4
        if any(w in text_target for w in ["simpler words", "different words", "vague", "describe", "story", "description", "words someone said"]):
            scores["natural_language"] += 4
        if any(w in text_target for w in ["ocr", "text in photo", "receipt", "bill", "written", "sign", "words or text"]):
            scores["text_search"] += 5
        if any(w in text_target for w in ["video", "spoken line", "inside video", "audio"]):
            scores["video_search"] += 5
        if any(w in text_target for w in ["albums or people", "album", "filter", "buttons", "manually scroll", "scroll down"]):
            scores["filter_limitations"] += 3

        sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_category, top_score = sorted_categories[0]
        if top_score == 0:
            top_category = "search_accuracy" if "search" in text_target else "missing_results"

        categories = [k for k, v in scores.items() if v > 0] or [top_category]

        if top_category in ("missing_results", "video_search", "text_search"):
            failure_point = "retrieval"
            severity = "critical" if top_category == "missing_results" else "medium"
        elif top_category in ("search_accuracy", "face_similarity"):
            failure_point = "ranking"
            severity = "high"
        elif top_category in ("face_recognition", "date_time_search", "location_search"):
            failure_point = "understanding"
            severity = "high"
        elif top_category == "natural_language":
            failure_point = "query_formulation"
            severity = "medium"
        else:
            failure_point = "refinement"
            severity = "medium"

        memory_cues = []
        if scores["face_recognition"] > 0: memory_cues.append("person")
        if scores["location_search"] > 0: memory_cues.append("place")
        if scores["date_time_search"] > 0: memory_cues.append("date")
        if scores["text_search"] > 0: memory_cues.append("text")

        return {
            "categories": categories,
            "primary_category": top_category,
            "retrieval_type": "Contextual photos",
            "user_memory_cues": memory_cues or ["context"],
            "search_failure_point": failure_point,
            "severity": severity
        }
