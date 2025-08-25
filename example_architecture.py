# example_architecture.py
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
from diagrams.onprem.cdn import Cloudflare

with Diagram("reference-architecture", show=False, filename="reference-architecture", direction="LR"):
    users = Users("End Users")
    cdn = Cloudflare("CDN / Edge Cache")
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

    fw = Firewall("WAF / FW")
    artifact_runtime = Docker("Container Runtime")
    batch = Rack("Batch/Jobs")
    bastion = Server("Bastion (restricted)")

    users >> cdn >> fw >> lb >> web_vm >> api_vm
    api_vm >> Edge(label="read/write") >> cache
    api_vm >> Edge(label="produce") >> queue
    queue >> Edge(label="consume") >> workers
    workers >> Edge(label="persist") >> db

    scm >> ci >> registry
    registry >> Edge(label="deploy") >> [web_vm, api_vm, *workers]

    [web_vm, api_vm, *workers, db] >> prom
    graf << prom

    bastion >> [web_vm, api_vm, *workers, db]

    batch >> workers
    artifact_runtime << registry