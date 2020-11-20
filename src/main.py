from app import create_app, db
from app.utils import build_plot
from app.models import User, Answer

# THINGS TO DO
# ADD CAPTHA IN TO CONFIRM REQUEST RESET PASSWORD
# CHANGE THE RENDER OF GRAPHIC TO CLIENT SIDE
#

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