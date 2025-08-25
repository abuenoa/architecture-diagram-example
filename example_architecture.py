# example_architecture.py
# Generic multi-cloud diagram using "Diagrams" (https://diagrams.mingrammer.com/)
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.queue import Kafka
from diagrams.onprem.vcs import Gitlab
from diagrams.onprem.ci import Jenkins

from diagrams.generic.network import Firewall
from diagrams.generic.database import SQL
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage

from diagrams.azure.compute import VM as AzureVM
from diagrams.gcp.compute import ComputeEngine as GCE
from diagrams.onprem.container import Docker

from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server

# Cloudflare CDN lives under diagrams.saas.cdn in most versions.
# Fallback to a generic Internet icon if the CDN module isn't available.
try:
    from diagrams.saas.cdn import Cloudflare as CdnIcon
except Exception:
    from diagrams.generic.network import Internet as CdnIcon  # fallback

with Diagram("reference-architecture", show=False, filename="reference-architecture", direction="LR"):
    users = Users("End Users")
    cdn = CdnIcon("CDN / Edge Cache")
    fw = Firewall("WAF / FW")
    lb = Nginx("Load Balancer")

    with Cluster("Public Cloud A (Azure)"):
        web_vm = AzureVM("Web Node")
        api_vm = AzureVM("API Node")
        cache = Redis("Cache")

    with Cluster("Public Cloud B (GCP)"):
        workers = [GCE("Worker-1"), GCE("Worker-2")]
        queue = Kafka("Event Bus")
        db = SQL("Relational DB")

    with Cluster("CI/CD & Artifacts"):
        scm = Gitlab("Source Control")
        ci = Jenkins("CI Pipeline")
        registry = Storage("Artifact Store")

    with Cluster("Observability"):
        prom = Prometheus("Prometheus")
        graf = Grafana("Grafana")

    artifact_runtime = Docker("Container Runtime")
    batch = Rack("Batch/Jobs")
    bastion = Server("Bastion (restricted)")

    # Flows (generic, no ports/hosts/secrets)
    users >> cdn >> fw >> lb >> web_vm >> api_vm
    api_vm >> Edge(label="read/write") >> cache
    api_vm >> Edge(label="produce") >> queue
    queue >> Edge(label="consume") >> workers
    workers >> Edge(label="persist") >> db

    # CI/CD -> Artifacts -> Runtime
    scm >> ci >> registry
    registry >> Edge(label="deploy") >> [web_vm, api_vm, *workers]

    # Observability
    [web_vm, api_vm, *workers, db] >> prom
    graf << prom

    # Admin paths (no details)
    bastion >> [web_vm, api_vm, *workers, db]

    # Ops
    batch >> workers
    artifact_runtime << registry
