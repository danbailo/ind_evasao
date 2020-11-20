import base64
import matplotlib.pyplot as plt
import io
from app.models import Answer

def get_answers_values():
    all_answers = Answer.get_all_answers()
    x = list(all_answers.keys())
    y = list(all_answers.values()) #height
    return x, y