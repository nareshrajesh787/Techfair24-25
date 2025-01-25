from django.conf import settings
from django.core.cache import cache
from openai import OpenAI
import hashlib
import logging

logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _get_cache_key(self, assignment_id, content_type):
        return f"ai_cache_{assignment_id}_{content_type}"

    def analyze_assignment(self, title, description, uploaded_content, rubric, assignment_id):
        # Generate cache key first
        cache_key = self._get_cache_key(assignment_id, 'analysis')
        cached_response = cache.get(cache_key)

        # Debug logging
        logger.debug(f"Cache key: {cache_key}")
        logger.debug(f"Cache hit: {cached_response is not None}")

        if cached_response:
            logger.info(f"Returning cached analysis for assignment {assignment_id}")
            return cached_response
        """Analyze uploaded assignment against rubric criteria"""

        prompt = f"""
        You are an AI assistant tasked with evaluating a student assignment based on a specific rubric.

        Title: {title}

        Full Assignment Text:
        {uploaded_content}

        Evaluate this assignment based on these rubric criteria:
        {self._format_rubric(rubric)}

        For each criterion:
        1. Analyze how well specific parts of the assignment meet the requirements
        2. Quote relevant examples from the assignment text
        3. Calculate a suggested score based on the max points
        4. Provide specific recommendations for improvement

        Format your response as:
        [Criterion Name]
        Score: [Your Score Reccomendation]/[Max Points]
        Analysis: [Your detailed analysis with specific quotes]
        Recommendations: [Bullet points for improvement]
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            analysis = response.choices[0].message.content
            cache.set(cache_key, analysis, timeout=None)
            logger.info(f"Cached new analysis for assignment {assignment_id}")
            return analysis
        except Exception as e:
            return f"Error analyzing assignment: {str(e)}"

    def _format_rubric(self, rubric):
        formatted = []
        for criterion, details in rubric.items():
            formatted.append(f"""
            {criterion}:
            - Description: {details['description']}
            - Maximum Points: {details['max_points']}
            """)
        return "\n".join(formatted)

    def summarize_reviews(self, reviews, assignment_id):
        """Summarize multiple reviews providing detailed analysis"""

        if len(reviews) < 2:
            return "At least 2 reviews are needed for summarization"

        reviews_content = "|".join([
            f"{review.id}:{review.final_percent}:{review.feedback}"
            for review in reviews
        ])
        reviews_hash = hashlib.md5(reviews_content.encode()).hexdigest()
        cache_key = self._get_cache_key(assignment_id, f'summary_{reviews_hash}')

        cached_response = cache.get(cache_key)
        if cached_response:
            logger.info(f"Using cached review summary for assignment {assignment_id}")
            return cached_response

        try:
            review_texts = [f"Review {i+1}:\nScore: {r.final_percent}%\nFeedback: {r.feedback}"
                          for i, r in enumerate(reviews)]
            reviews_text = "\n\n".join(review_texts)

            scores = [r.final_percent for r in reviews]
            avg_score = sum(scores) / len(scores)
            score_range = max(scores) - min(scores)

            prompt = f"""
            Analyze these {len(reviews)} reviews:
            {reviews_text}

            Statistical Overview:
            - Average Score: {avg_score:.1f}%
            - Score Range: {score_range:.1f}%

            Provide a structured analysis with:
            1. Overall assessment summary (2-3 sentences)
            2. Key strengths mentioned across reviews
            3. Common areas for improvement
            4. Notable differences in reviewer perspectives
            5. Specific actionable recommendations

            Format the response in clearly labeled sections using markdown headers.
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            summary = response.choices[0].message.content

            cache.set(cache_key, summary)
            logger.info(f"Cached new review summary for assignment {assignment_id}")
            return summary

        except Exception as e:
            return f"Error summarizing reviews: {str(e)}"

    def invalidate_cache(self, assignment_id):
        """Invalidate all cached responses for an assignment"""
        # Delete analysis cache
        cache.delete(self._get_cache_key(assignment_id, 'analysis'))
        cache.delete(self._get_cache_key(assignment_id, 'summary'))
        logger.info(f"Invalidated cache for assignment {assignment_id}")
