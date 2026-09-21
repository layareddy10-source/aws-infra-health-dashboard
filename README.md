# AWS Infra Health Dashboard

A containerized web dashboard that pulls **live EC2 instance status** using AWS's SDK (boto3) — built to automate the kind of infrastructure visibility I used to check manually as an AWS/VMware Windows administrator.

## Why I built this

With 2+ years as an AWS & VMware admin, I wanted my first DevOps project to reflect real infra work, not a generic tutorial app. This dashboard shows instance state, type, availability zone, and uptime — the same checks I used to do by hand in the console, now automated and containerized.

## Architecture

- **App**: Python Flask, serving an HTML dashboard and a JSON API
- **AWS access**: IAM role attached to the EC2 instance (no hardcoded credentials — a real security practice, not just a demo shortcut)
- **Containerized**: Docker, image published to Docker Hub
- *(Coming next: Terraform for infra provisioning, GitHub Actions for CI/CD, Kubernetes deployment, Ansible, and monitoring — see Roadmap below)*

## Endpoints

- `/` — HTML dashboard
- `/api/instances` — JSON list of EC2 instances with state, type, AZ, uptime
- `/health` — health check endpoint (used by orchestrators/load balancers)

## Running it locally

```bash
docker pull ylayareddy/infra-health-dashboard:v1
docker run -d -p 5000:5000 ylayareddy/infra-health-dashboard:v1
```

Requires an IAM role with `AmazonEC2ReadOnlyAccess` attached to the host running the container.

## Tech stack

Python, Flask, boto3, Docker
<img width="951" height="320" alt="image" src="https://github.com/user-attachments/assets/cd5f3112-b5af-4643-9fcb-160b9c3d49e6" />


## Roadmap

- [ ] Terraform to provision the infra (VPC, EKS)
- [ ] CI/CD pipeline via GitHub Actions
- [ ] Kubernetes deployment
- [ ] Ansible for config management (including a Windows EC2 target)
- [ ] Prometheus + Grafana monitoring

## Author

Laya Reddy — AWS & VMware administrator transitioning into DevOps. www.linkedin.com/in/laya-r-172b32403 | https://github.com/layareddy10-source
