import logging
from transformers import pipeline

class CoachService:
    def __init__(self):
        # Using roberta model from hugging face for sentiment analysis which as output :
        # 'negative', 'neutral', 'positive'
        try:
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1 # Using -1 for cpu
            )
        except Exception as e:
            logging.error(f"Failed to load sentiment model: {e}")
            self.sentiment_model = None

        # I have used keywords to detect objections for simplicity. In a production system, 
        # this could be replaced with a more sophisticated approach (example: fine-tuned NLP model).
        self.objection_map = {
            "price": ["price", "expensive", "cost", "too much", "dollars", "pricing"],
            "budget": ["budget", "afford", "finance", "money"],
            "competitor": ["competitor", "using someone else", "alternative", "switch"],
            "authority": ["talk to my boss", "manager", "decision maker"]
        }

    def analyze_sentiment(self, text: str) -> str:
        """Returns the sentiment label: positive, neutral, or negative."""
        if not self.sentiment_model:
            return "neutral"
        
        # truncating text to 512 tokens to stay with in modle limits
        result = self.sentiment_model(text[:512])[0]
        return result['label'].lower()

    def is_coachable(self, text: str, sentiment: str, speaker: str) -> bool:
        """
        Logic to flag a segment for review. 
        A moment is coachable if:
        1. It contains a sales objection.
        2. The Agent (Speaker 0) has a negative sentiment.
        """
        text_lower = text.lower()
        
        has_objection = any(
            any(kw in text_lower for kw in keywords) 
            for keywords in self.objection_map.values()
        )

        # additional logic: If the agent is negative, its always a coaching moment
        is_agent_negative = (speaker == "Speaker 0" and sentiment == "negative")

        return has_objection or is_agent_negative