import base64
import matplotlib.pyplot as plt
import io
from app.models import Answer

def build_plot():
    # colors = ['red', 'green', 'blue', 'purple', 'darkorange', 'brown', 'yellow', 'gray', 'cyan', 'olive', 'chocolate']
    all_answers = Answer.get_all_answers()

    img = io.BytesIO()

    x = list(all_answers.keys())
    y = list(all_answers.values()) #height
    plt.figure(figsize=(12, 8))
    bar_list = plt.bar(x,y, zorder=3, color="purple", width=0.5)
    plt.grid(axis="both")
    # for i, color in enumerate(colors):
        # bar_list[i].set_color(color)    
    plt.xticks(fontsize=15)
    max_y_value = max(y)
    int_yticks = list(range(0, max_y_value+1))
    plt.yticks(int_yticks, fontsize=15)
    plt.xlabel("Respostas", fontsize=15)
    plt.ylabel("Quantidade", fontsize=15)    
    plt.savefig(img, format='jpg')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url
