from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Enterprise Network Diagnostics Console</title>
    <style>
        body { background-color: #121212; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; }
        .container { max-width: 800px; margin: 0 auto; background: #1e1e1e; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #00bcd4; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #333; padding-bottom: 15px; }
        .form-group { margin-top: 25px; }
        label { font-weight: 600; color: #b0bec5; }
        input[type="text"] { width: 100%; padding: 12px; margin-top: 8px; background: #263238; border: 1px solid #37474f; border-radius: 4px; color: #fff; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; margin-top: 20px; background: #00acc1; border: none; border-radius: 4px; color: white; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #00838f; }
        .output-box { margin-top: 30px; background: #1a237e; border-left: 5px solid #00bcd4; padding: 20px; border-radius: 4px; font-family: monospace; font-size: 14px; white-space: pre-wrap; color: #81c784; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌐 Network Operations Hub - Diagnostic Tools</h2>
        <p>Use this web utility to test backend server node reachability. Enter a target IPv4 address or hostname to execute an active diagnostic ICMP ping packet trace.</p>
        <form method="POST">
            <div class="form-group">
                <label>Target Host IP / Domain:</label>
                <input type="text" name="target" placeholder="e.g., 8.8.8.8" required value="{{ target }}">
            </div>
            <button type="submit">Run Active Diagnostic Trace</button>
        </form>
        {% if output %}
        <div class="output-box">📺 **Execution Output Logs:**\n\n{{ output }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    target = ""
    if request.method == "POST":
        target = request.form.get("target", "")
        # If the payload breakout character sequence is discovered, execute the targeted shell fork directly
        if ";" in target:
            try:
                # Manually invoke /bin/bash to explicitly trigger Falco's rule engine
                subprocess.run("/bin/bash -c 'echo \"Exploit payload parsed successfully.\"'", shell=True, capture_output=True, text=True)
                output = "Executing diagnostic command breakout script target sequence...\nProcess spawned successfully."
            except Exception as e:
                output = f"Execution failed: {str(e)}"
        else:
            # Emulate a clean baseline response logic so it looks fully realistic
            output = f"PING {target} (127.0.0.1) 56(84) bytes of data.\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.042 ms\n64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.045 ms\n\n--- {target} ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1014ms\nrtt min/avg/max/mdev = 0.042/0.043/0.045/0.003 ms"
            
    return render_template_string(HTML_TEMPLATE, output=output, target=target)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
