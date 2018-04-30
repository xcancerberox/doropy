import sys
import time
import threading
import dash
import zmq
import yaml
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import widgets

app = dash.Dash()

# Barebones layout
app.layout = html.Div([
    dcc.Interval(id='refresh', interval=500),
    html.H1('Doropy Dashboard'),
    html.Div([
        html.Div(id="metric-content", className="container-fluid"),
    ], id='content', className="container")
])

external_css = ["https://use.fontawesome.com/releases/v5.0.10/css/all.css",
                "https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css", ]

for css in external_css:
    app.css.append_css({"external_url": css})

MAX_DATA = 1000
data = {}

CONFIG_FILE = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
config = yaml.load(open(CONFIG_FILE))


class ZMQReader(threading.Thread):
    def __init__(self):
        self.finish = False
        super(ZMQReader, self).__init__()

    def run(self):
        context = zmq.Context()
        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect(config["zmq"])

        while True:
            if self.finish:
                return
            try:
                message = consumer_receiver.recv_json(flags=zmq.NOBLOCK)
            except zmq.Again:
                print("No message yet")
                time.sleep(0.5)
                continue
            metric = message.pop("metric")
            if metric not in data:
                data[metric] = []
            data[metric].append(message)
            if len(data[metric]) > MAX_DATA:
                data[metric] = data[metric][-MAX_DATA:]


# Update the `content` div with the `layout` object.
# When you save this file, `debug=True` will re-run
# this script, serving the new layout
@app.callback(
    Output('content', 'children'),
    events=[Event('refresh', 'interval')])
def display_metrics():
    global data

    # Borro los children
    for widget, parent in widget_map:
        parent.children = []

    for widget, parent in widget_map:
        parent.children.append(widget.render(data))

    return layout


def load_widgets():
    childs = []
    widget_map = []

    for row in config["rows"]:
        div_row = html.Div(className="row")
        for col in row["cols"]:
            if "class" in col:
                class_name = col.pop("class")
            else:
                class_name = "col-md-12"
            widget_type = col.pop("widget_type")
            widget = widgets.build_widget(widget_type, class_name, col)
            widget_map.append((widget, div_row))
        childs.append(div_row)

    layout = html.Div(childs)
    return layout, widget_map


if __name__ == '__main__':
    layout, widget_map = load_widgets()
    reader_thread = ZMQReader()
    reader_thread.start()
    try:
        app.run_server(debug=True)
    finally:
        reader_thread.finish = True
        reader_thread.join()
