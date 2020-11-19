from app import create_app, db
from app.utils import build_plot
from app.models import User, Answer

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
                User=User,
                Answer=Answer)

@app.context_processor
def make_app_context():
    return dict(image=build_plot(),
                n_answers=Answer.objects.count())