import base64
import io

import cherrypy
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


def sharlie(n):
    return special.erfinv((n - 1) / n) * np.sqrt(2)


def statistics(x):
    '''return mean, sample std'''
    return x.mean(), np.sqrt(np.sum((x - x.mean()) ** 2) / (len(x) - 1))


def metric(x):
    '''return normalized deviation'''
    mean, sko = statistics(x)
    return np.abs(x - mean) / sko


def borders(x):
    '''return borders for good values'''
    sh = sharlie(len(x))
    s = np.sqrt(np.sum((x - x.mean()) ** 2) / (len(x) - 1))
    m = x.mean()
    return m - sh * s, m + sh * s


def find_bad(x):
    '''return good and bad values in dataset'''
    test = metric(x)
    mask = test > sharlie(len(x))
    bad = x[mask]
    x = x[~mask]
    return x, bad


def plt_to_base64(p):
    '''convert plot to base64 image'''
    b = io.BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return base64.b64encode(b.read()).decode()


def plt_grapg(ax, X, ok, bad):
    '''draw plot graph'''
    border = borders(ok)
    iterator_ok = np.arange(len(X))[np.isin(X, ok)]
    iterator_bad = np.arange(len(X))[np.isin(X, bad)]
    ax.grid(True)
    ax.set_title("Обработка выборки")
    ax.xlabel = "#"
    ax.ylabel = "Значение"
    ax.hlines(border, 0, len(X) - 1, color="r", linestyles="dashed")
    ax.scatter(iterator_ok, ok, label="Хорошие значения")
    ax.scatter(iterator_bad, bad, label="Промахи")
    ax.legend()
    return ax


def calc(x):
    history = []
    x = np.array(x)
    bad = [0]  # do-while loop
    iteration = 0
    fig = plt.figure(figsize=(20, 20))
    ok = x.copy()
    while len(bad) != 0:
        iteration += 1
        ax = fig.add_subplot(3, 3, iteration)
        mean, sko = statistics(ok)
        sh = sharlie(len(ok))
        ok, bad = find_bad(ok)
        ax = plt_grapg(ax, x, ok, bad)
        history.append({"ok": ok.tolist(), "bad": bad.tolist(), "plot": plt_to_base64(ax), "mean": mean, "sko": sko, "sharlie": sh})
    #plt.show()
    return history


class Root(object):
    @cherrypy.expose
    def index(self):
        with open("index.html", 'r', encoding='utf8') as f:
            return f.read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def calc(self):
        data = list(map(float, cherrypy.request.json["data"].splitlines()))
        return calc(data)


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'tools.proxy.on': True,
    })
    cherrypy.quickstart(Root())
