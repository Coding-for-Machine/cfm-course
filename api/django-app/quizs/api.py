from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from utils.auth import JWTBearer
from .models import Answer, Question, QuestionAttempt

router = Router()

class QuestionAnswerSchema(Schema):
    question_id: int
    answer_id: int

@router.post("/question/answer", auth=JWTBearer())
def submit_question_answer(request, payload: QuestionAnswerSchema):
    user = request.user
    question = get_object_or_404(Question, id=payload.question_id)
    answer = get_object_or_404(Answer, id=payload.answer_id, question=question)

    is_correct = answer.is_correct

    # Saqlash yoki yangilash
    attempt, _ = QuestionAttempt.objects.update_or_create(
        user=user,
        question=question,
        defaults={
            "selected_answer": answer,
            "is_correct": is_correct
        }
    )

    return {
        "is_correct": is_correct,
    }
