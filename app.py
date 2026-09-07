from flask import Flask, jsonify, render_template_string
import boto3
import os
from datetime import datetime, timezone

app = Flask(__name__)
ec2 = boto3.client(
    "ec2",
    region_name=os.environ.get("AWS_REGION", "ap-southeast-2")
)

def get_instances():
    instances = []
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            name = "unnamed"
            for tag in inst.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
            launch_time = inst["LaunchTime"]
            uptime = datetime.now(timezone.utc) - launch_time
            instances.append({
                "name": name,
                "id": inst["InstanceId"],
                "type": inst["InstanceType"],
                "state": inst["State"]["Name"],
                "az": inst["Placement"]["AvailabilityZone"],
                "uptime_hours": round(uptime.total_seconds() / 3600, 1)
            })
    return instances

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Infra Health Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0d1117; color: #e6edf3; padding: 30px; }
        h1 { color: #58a6ff; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #30363d; padding: 10px; text-align: left; }
        th { background: #161b22; }
        .running { color: #3fb950; font-weight: bold; }
        .stopped { color: #f85149; font-weight: bold; }
    </style>
</head>
<body>
    <h1>AWS Infra Health Dashboard</h1>
    <p>Live EC2 instance status, pulled via IAM role — no hardcoded credentials.</p>
    <table>
        <tr><th>Name</th><th>Instance ID</th><th>Type</th><th>State</th><th>AZ</th><th>Uptime (hrs)</th></tr>
        {% for i in instances %}
        <tr>
            <td>{{ i.name }}</td>
            <td>{{ i.id }}</td>
            <td>{{ i.type }}</td>
            <td class="{{ i.state }}">{{ i.state }}</td>
            <td>{{ i.az }}</td>
            <td>{{ i.uptime_hours }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def dashboard():
    instances = get_instances()
    return render_template_string(DASHBOARD_HTML, instances=instances)

@app.route("/api/instances")
def api_instances():
    return jsonify(get_instances())

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
