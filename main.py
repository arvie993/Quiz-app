import requests
from html import unescape
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

# Fetch questions from Open Trivia DB API
url = "https://opentdb.com/api.php?amount=10&type=boolean"
response = requests.get(url)
response.raise_for_status()
question_data = response.json()["results"]

question_bank = []
for question in question_data:
    # Decode HTML entities in the question text
    question_text = unescape(question["question"])
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)

quiz_ui = QuizInterface(quiz)
