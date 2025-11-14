from fastapi import APIRouter
from app.models import AskRequest, AskResponse
from app.data_loader import DataLoader
from app.question_parser import QuestionParser
from app.rule_engine import RuleEngine

router = APIRouter()

data_loader = DataLoader()
messages = data_loader.load_messages()
print("LOADED MESSAGES TYPE:", type(messages))
print("LOADED MESSAGES EXAMPLE:", messages[:5])

question_parser = QuestionParser(messages)
rule_engine = RuleEngine(messages)


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    parsed = question_parser.parse(request.question)
    answer = rule_engine.answer_question(parsed)

    return AskResponse(answer=answer)
