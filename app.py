import dash
import psutil
from dash import dcc, html
from dash.dependencies import Input, Output

from logger import logger

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="cpu-chart"),
        dcc.Graph(id="memory-chart"),
        dcc.Graph(id="disk-chart"),
        dcc.Graph(id="network-chart"),
        dcc.Interval(
            id="interval-component", interval=5 * 1000, n_intervals=0  # in milliseconds
        ),
    ]
)


def check_cpu_usage(threshold=50):
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > threshold:
        logger.warning(f"High CPU usage detected: {cpu_usage}%")
    else:
        logger.info(f"CPU usage detected: {cpu_usage}%")
    return cpu_usage


def check_memory_usage(threshold=80):
    memory_usage = psutil.virtual_memory().percent
    if memory_usage > threshold:
        logger.warning(f"High memory usage detected: {memory_usage}%")
    else:
        logger.info(f"Memory usage detected: {memory_usage}%")
    return memory_usage


def check_disk_space(path="/", threshold=75):
    disk_usage = psutil.disk_usage(path).percent
    if disk_usage > threshold:
        logger.warning(f"Low disk space detected: {disk_usage}%")
    else:
        logger.info(f"Disk space detected: {disk_usage}%")
    return disk_usage


def check_network_traffic(threshold=100 * 1024 * 1024):
    network_traffic = (
        psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    )
    if network_traffic > threshold:
        logger.warning(f"High network traffic detected: {network_traffic:.2f} MB")
    else:
        logger.info(f"Network traffic detected: {network_traffic:.2f} MB")
    return network_traffic


def run_health_checks():
    cpu_usage = check_cpu_usage()
    memory_usage = check_memory_usage()
    disk_usage = check_disk_space()
    network_traffic = check_network_traffic()
    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
        "network": network_traffic,
    }


def create_pie_chart(labels, values, title):
    return {
        "data": [{"labels": labels, "values": values, "type": "pie"}],
        "layout": {"title": title},
    }


def create_gauge_chart(value, title):
    return {
        "data": [
            {
                "type": "indicator",
                "value": value,
                "title": {"text": title},
                "mode": "gauge+number",
                "gauge": {
                    "axis": {"range": [0, 100]},
                    "steps": [{"range": [0, 100], "color": "lightgray"}],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 100,
                    },
                },
            }
        ],
        "layout": {},
    }


@app.callback(
    Output("cpu-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_cpu_chart(n):
    cpu_usage = run_health_checks()["cpu"]
    return create_pie_chart(
        ["Used", "Unused"], [cpu_usage, 100 - cpu_usage], "CPU Usage"
    )


@app.callback(
    Output("memory-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_memory_chart(n):
    memory_usage = run_health_checks()["memory"]
    return create_pie_chart(
        ["Used", "Unused"], [memory_usage, 100 - memory_usage], "Memory Usage"
    )


@app.callback(
    Output("disk-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_disk_chart(n):
    disk_usage = run_health_checks()["disk"]
    return create_pie_chart(
        ["Used", "Unused"], [disk_usage, 100 - disk_usage], "Disk Space"
    )


@app.callback(
    Output("network-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_network_chart(n):
    network_traffic = run_health_checks()["network"]
    return create_gauge_chart(network_traffic, "Network Traffic")


if __name__ == "__main__":
    app.run_server(debug=True)
