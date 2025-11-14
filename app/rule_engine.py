import re

class RuleEngine:
    def __init__(self, messages):
        self.messages = messages

    def _get_user_messages(self, user):
        return [m["message"] for m in self.messages if m["user_name"] == user]

    # ---------------- RULES ---------------- #

    def _answer_count(self, user_msgs):
        patterns = [
            r"(\d+)\s+cars?",
            r"owns\s+(\d+)",
            r"has\s+(\d+)",
        ]

        for msg in user_msgs:
            for pattern in patterns:
                match = re.search(pattern, msg, re.IGNORECASE)
                if match:
                    return match.group(1)

        return "Unknown"

    def _answer_date(self, user_msgs):
        patterns = [
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}",
            r"\bnext\s+(week|month|year)\b",
            r"\b\d{1,2}/\d{1,2}/\d{4}\b"
        ]

        for msg in user_msgs:
            for p in patterns:
                match = re.search(p, msg, re.IGNORECASE)
                if match:
                    return match.group(0)

        return "Date not found"

    def _answer_preference(self, user_msgs):
        patterns = [
            r"favorite restaurants? are (.*)",
            r"eats at (.*)",
            r"loves (.*)"
        ]

        for msg in user_msgs:
            for p in patterns:
                match = re.search(p, msg, re.IGNORECASE)
                if match:
                    return match.group(1)
        return "No preferences found"

    def _answer_location(self, user_msgs):
        patterns = [
            r"going to ([A-Za-z\s]+)",
            r"travelling to ([A-Za-z\s]+)",
            r"trip to ([A-Za-z\s]+)",
        ]

        for msg in user_msgs:
            for p in patterns:
                match = re.search(p, msg, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        return "Location not found"

    # ---------------- MASTER LOGIC ---------------- #

    def answer_question(self, parsed):
        user = parsed["user"]
        intent = parsed["intent"]

        if user is None:
            return "Could not identify the user in the question."

        user_msgs = self._get_user_messages(user)

        if not user_msgs:
            return f"No messages found for {user}."

        if intent == "count":
            value = self._answer_count(user_msgs)
            return f"{user} has {value} cars."

        if intent == "date":
            value = self._answer_date(user_msgs)
            return f"{user}'s trip is planned for {value}."

        if intent == "preference":
            value = self._answer_preference(user_msgs)
            return f"{user}'s favorite restaurants are {value}."

        if intent == "location":
            value = self._answer_location(user_msgs)
            return f"{user} is going to {value}."

        return "I could not understand the question."
