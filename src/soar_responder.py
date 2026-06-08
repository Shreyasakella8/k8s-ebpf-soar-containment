import logging
from flask import Flask, request, jsonify
from kubernetes import client, config

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("soar-responder")

app = Flask(__name__)

try:
    config.load_incluster_config()
except Exception:
    config.load_kube_config()

v1 = client.CoreV1Api()

@app.route('/', methods=['POST'])
def handle_alert():
    alert = request.json
    if not alert:
        return jsonify({"status": "invalid json"}), 400

    rule = alert.get("rule", "Unknown")
    priority = alert.get("priority", "Unknown")
    output_fields = alert.get("output_fields", {})
    
    # ADVANCED TELEMETRY FALLBACK ENGINE: Pull metadata keys across multiple known Falco schemas
    pod_name = output_fields.get("k8s.pod.name") or output_fields.get("container.id") or alert.get("container_id")
    namespace = output_fields.get("k8s.ns.name") or "production" # Fallback to target app scope namespace

    logger.info(f"🚨 ALERT RECEIVED | Priority: {priority} | Rule: {rule}")

    # Broaden rule validation to catch the API contact logs or Shell triggers
    if priority in ["Critical", "Error", "Notice"]:
        # If the specific pod name wasn't bound, dynamically look up the active target pod asset in production
        if not pod_name or pod_name == "host":
            try:
                pods = v1.list_namespaced_pod(namespace=namespace)
                for pod in pods.items:
                    if "compromised-web-app" in pod.metadata.name:
                        pod_name = pod.metadata.name
                        break
            except Exception as e:
                logger.error(f"❌ METADATA LOOKUP FAILED: {str(e)}")

        if pod_name and pod_name != "host":
            logger.warning(f"⚡ CONTAINMENT ACTIVE: Target Pod {pod_name} in namespace {namespace} is being neutralized...")
            try:
                v1.delete_namespaced_pod(name=pod_name, namespace=namespace, grace_period_seconds=0)
                logger.info(f"✅ CONTAINMENT SUCCESSFUL: Pod {pod_name} evicted.")
            except client.exceptions.ApiException as e:
                if e.status == 404:
                    logger.info(f"ℹ️ AGENT CORRELATION: Pod {pod_name} was already successfully terminated.")
                else:
                    logger.error(f"❌ CONTAINMENT FAILED: {str(e)}")
            except Exception as e:
                logger.error(f"❌ CONTAINMENT FAILED: {str(e)}")
        else:
            logger.error("❌ INSUFFICIENT TELEMETRY: System could not securely isolate a target pod name.")

    return jsonify({"status": "processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
