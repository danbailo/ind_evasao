from app import create_app, db
from app.models import Answer, User
from app.utils import gen_randomic_answers, get_answers_values

# THINGS TO DO
# ADD CAPTHA IN TO CONFIRM REQUEST RESET PASSWORD
# CHANGE THE RENDER OF GRAPHIC TO CLIENT SIDE
#

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
                User=User,
                Answer=Answer,
                gen_randomic_answers=gen_randomic_answers)

@app.context_processor
def make_app_context():
    return dict(n_answers=Answer.objects.count(),
                answers_values=get_answers_values())
