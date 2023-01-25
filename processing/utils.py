import matplotlib.pyplot as plt


def create_graph_image(title, label_x, label_y, area, attribute, image_name):
    fig, axis = plt.subplots(nrows=1, ncols=1)
    axis.bar(area, attribute)
    axis.set_title(title)
    axis.set_xlabel(label_x)
    axis.set_ylabel(label_y)
    plt.xticks(rotation=90)
    plt.tight_layout()
    fig.savefig(image_name)

