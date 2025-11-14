import re

class QuestionParser:
    def __init__(self, messages):
        self.user_names = self._extract_names(messages)
        print("Loaded user names:", self.user_names)


    def _extract_names(self, messages):
        names = set()
        for m in messages:
            if isinstance(m, dict) and m.get("user_name"):
                names.add(m["user_name"])
        return list(names)

    def _find_user(self, question):
        for name in self.user_names:
            if name.lower() in question.lower():
                return name
        return None

    def _detect_intent(self, question):
        q = question.lower()

        if "how many" in q or "number of" in q:
            return "count"

        if "when" in q or "date" in q or "trip" in q:
            return "date"

        if "favorite" in q or "restaurants" in q or "likes" in q:
            return "preference"

        if "where" in q or "going to" in q or "travel" in q:
            return "location"

        return "unknown"

    def parse(self, question):
        return {
            "raw_question": question,
            "user": self._find_user(question),
            "intent": self._detect_intent(question)
        }
