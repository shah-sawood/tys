from csv import DictReader
from tests.models import Category, Choice, Question


# create your helpers below
def add_questions_to_db(filename, category):
    with open(filename) as file:
        counter = 0
        questions = DictReader(file)
        for row in questions:
            question, option = row.get("question"), row.get("option")
            if question:
                counter += 1
                question_obj = Question.objects.create(
                    statement=question,
                    published=True,
                    category=category,
                )
            choice = Choice.objects.create(option=option, question=question_obj)
    return counter
