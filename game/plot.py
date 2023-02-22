import matplotlib.pyplot as pyplot
from IPython import display

pyplot.ion()

def plot(scores, mean):
    display.clear_output(wait=True)
    display.display(pyplot.gcf())
    pyplot.clf()
    pyplot.title('Training...')
    pyplot.xlabel('Number of Games')
    pyplot.ylabel('Score')
    pyplot.plot(scores)
    pyplot.plot(mean)
    pyplot.ylim(ymin=0)
    pyplot.text(len(scores)-1, scores[-1], str(scores[-1]))
    pyplot.text(len(mean)-1, mean[-1], str(mean[-1]))
    pyplot.show(block=False)
    pyplot.pause(.1)