import argparse
import base64
import io
import random
import uuid

import matplotlib.pyplot as plt

from app.models import Answer

parser = argparse.ArgumentParser(
    description="Generate fake answers"
)
parser.add_argument(
    "--number", "-n",
    required=True,
    help="Number of fake answers to generate",
    type=int
)

def get_answers_values():
    all_answers = Answer.get_all_answers()
    x = list(all_answers.keys())
    y = list(all_answers.values()) #height
    return x, y

def gen_randomic_answers(number_of_answers):
    for _ in range(number_of_answers):
        fake_answer_id = "FAKE_answer-"+uuid.uuid4().hex
        fake_user_id = "FAKE_user-"+uuid.uuid4().hex
        answer = Answer(
            _id=fake_answer_id,
            answer_1=random.choice([True, False]),
            answer_2=random.choice([True, False]),
            answer_3=random.choice([True, False]),
            answer_4=random.choice([True, False]),
            answer_5=random.choice([True, False]),
            answer_6=random.choice([True, False]),
            answer_7=random.choice([True, False]),
            answer_8=random.choice([True, False]),
            answer_9=random.choice([True, False]),
            answer_10=random.choice([True, False]),
            answer_11=random.choice([True, False]),
            user_id=fake_user_id
        )
        answer.save()
    print(f"Generate {number_of_answers} fake answers!")