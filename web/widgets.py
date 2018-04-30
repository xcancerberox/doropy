import dash_html_components as html
import dash_core_components as dcc
import datetime


def format_timestamp(epoch):
    return datetime.datetime.fromtimestamp(epoch).isoformat()


class Widget(object):
    def __init__(self, class_name, metric):
        self.class_name = class_name
        self.metric = metric

    def _get_current_value(self, data):
        if self.metric not in data:
            return None
        return data[self.metric] and data[self.metric][-1]


class H1Widget(Widget):
    def render(self, data):
        value = self._get_current_value(data)
        if value:
            return html.H1(str(value["value"]) + " " + format_timestamp(value["timestamp"]),
                           className=self.class_name)
        else:
            return html.H1("Sin datos", className=self.class_name)


class CardWidget(Widget):
    def __init__(self, class_name, metric, title, icon, format="{0}"):
        super(CardWidget, self).__init__(class_name, metric)
        self.title = title
        self.icon = icon
        self.format = format

    def render(self, data):
        value = self._get_current_value(data)
        if not value:
            value = {"value": 0}
        return html.Div(className="%s" % self.class_name, children=[
            html.Div(className="card", children=[
                html.Div(className="card-header", children=[
                    self.title,
                    html.I(className="fa-2x float-right %s" % self.icon)
                ]),
                html.Div(className="card-body", children=[
                    html.H4(self.format.format(value["value"]), className="card-title"),
                ])
            ])
        ])


class GraphWidget(Widget):
    def __init__(self, class_name, metric, title):
        super(GraphWidget, self).__init__(class_name, metric)
        self.title = title

    def render(self, data):
        if self.metric not in data:
            values = []
        else:
            values = data[self.metric]
        ret = dcc.Graph(id="graph-" + self.metric)
        ret.figure = {
            "data": [{
                "x": [datetime.datetime.fromtimestamp(x["timestamp"]) for x in values],
                "y": [x["value"] for x in values]
            }],
            'layout': {
                    'title': self.title
            }
        }
        return html.Div(ret, className=self.class_name)


def build_widget(widget_type, class_name, kargs):
    widget_class = globals()["%sWidget" % widget_type]
    return widget_class(class_name=class_name, **kargs)
