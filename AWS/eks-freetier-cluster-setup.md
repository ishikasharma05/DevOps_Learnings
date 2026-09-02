# AWS EKS Cluster Setup — `august-2026-eks-cluster`

A hands-on walkthrough of provisioning an Amazon EKS cluster from the AWS Console, hitting a real Free Tier node-launch failure, and resolving it end-to-end via the AWS CLI and `kubectl`. Built as part of an ongoing cloud/DevOps learning portfolio, with Helm + Argo CD set up as the next milestone.

---

## 📌 Project Summary

| | |
|---|---|
| **Cluster name** | `august-2026-eks-cluster` |
| **Region** | `ap-south-1` |
| **Kubernetes version** | `1.36` |
| **Cluster type** | AWS Managed EKS (EKS Auto Mode **off** — custom configuration) |
| **Node group** | Self-managed, standard (not Fargate) |
| **Final worker instance type** | `t3.micro` (Free Tier eligible) |

---

## 🧭 Architecture at a Glance

```
IAM (eks-role, worker-node-role)
        │
        ▼
EKS Control Plane (august-2026-eks-cluster)
        │
        ▼
Node Group (EC2 Auto Scaling Group)
        │
        ▼
Worker Node (t3.micro, AL2023 x86_64)
        │
        ▼
kubectl  →  Deployments / Services
        │
        ▼
Argo CD + Helm (next phase)
```

---

## ✅ Checklist

- [x] IAM role for EKS cluster (`es-role`)
- [x] IAM role for worker node group (`worker-node*`)
- [x] AWS CLI installed and configured
- [x] IAM user credentials (Access Key + Secret Key)
- [x] `kubectl` installed
- [x] `kubectl` installed on Ubuntu server
- [x] `aws configure` run on Ubuntu server (Access Key + Secret Key)
- [x] GitHub repo ready (for automated deployment via Argo CD)
- [x] Helm installation planned on Ubuntu
- [x] Verified AWS CLI connectivity (`aws s3 ls`)

---

## 🛠️ Step 1 — Prerequisites

1. **IAM setup**
   - Created an IAM role for the EKS control plane: `es-role`
   - Created a separate IAM role for the worker node group: `worker-node*`
   - Generated IAM user credentials (Access Key + Secret Key) for CLI access
2. **Local/Ubuntu machine setup**
   - Installed the AWS CLI
   - Installed `kubectl`
   - Ran `aws configure` and supplied the Access Key + Secret Key
   - Verified connectivity with `aws s3 ls`

---

## 🛠️ Step 2 — Create the EKS Cluster (AWS Console)

**Configuration used:**
- IAM role: `es-role`
- Cluster configuration: **Standard** (Custom configuration, **EKS Auto Mode off**)
- Cluster authentication mode: **EKS API and ConfigMap**
- Networking: Default VPC, with all subnets attached to an Internet Gateway (IGW)
- Cluster endpoint access: **Public and private**
- Control plane logging: **API server**
- Add-ons: left at default (no additions/removals)
- Reviewed and created the cluster

---

## 🛠️ Step 3 — Create the Node Group (AWS Console — first attempt)

**Configuration used:**
- Node group name: `august-2026-worker-node-grp`
- Node IAM role: `worker-node*`
- Tag: `name: august-2026-worker-node`
- Instance type: `t3.large`
- Scaling configuration: min `1` / desired `1` / max `1`

This node group **failed to launch**, surfacing the error documented below.

---

## 🚨 The Error

```
AsgInstanceLaunchFailures

Could not launch On-Demand Instances. InvalidParameterCombination -
The specified instance type is not eligible for Free Tier.
For a list of Free Tier instance types, run 'describe-instance-types'
with the filter 'free-tier-eligible=true'. Launching EC2 instance failed.
```

**Root cause:** the node group was configured with `t3.large`, which is **not** a Free Tier eligible instance type on this account. The Auto Scaling Group could not launch the EC2 worker instance, so the node group creation failed — while the EKS control plane itself remained `ACTIVE`.

---

## 🩹 Troubleshooting & Resolution (AWS CLI)

### 1. Confirm the cluster is still intact
```bash
aws eks list-clusters
aws eks describe-cluster \
  --name august-2026-eks-cluster \
  --query "cluster.status"
```
Result: `"ACTIVE"` — the control plane was healthy; only the node group had failed.

### 2. Delete the failed node group
The broken node group (using `t3.large`) was deleted, confirmed via:
```bash
eksctl get cluster
```

### 3. Identify Free Tier eligible instance types for the account
```bash
aws ec2 describe-instance-types \
  --filters Name=free-tier-eligible,Values=true \
  --query "InstanceTypes[].InstanceType" \
  --output text
```
Returned: `t3.micro`, `t3.small`, `t4g.micro`, `t4g.small`

> ⚠️ Don't assume `t2.micro` or `t3.micro` is eligible just because older tutorials say so — Free Tier eligibility is account- and region-specific and has changed over time.

### 4. Recreate the node group with an eligible instance type
```bash
aws eks create-nodegroup \
  --cluster-name august-2026-eks-cluster \
  --nodegroup-name august-2026-free-tier-node \
  --node-role arn:aws:iam::<account-id>:role/august-2026-worker-role-1 \
  --subnets subnet-xxxxxxxxxxxxxxxxx subnet-xxxxxxxxxxxxxxxxx subnet-xxxxxxxxxxxxxxxxx \
  --instance-types t3.micro \
  --scaling-config minSize=1,maxSize=1,desiredSize=1 \
  --disk-size 20 \
  --ami-type AL2023_x86_64_STANDARD \
  --capacity-type ON_DEMAND
```

Change made: `t3.large ❌  →  t3.micro ✅`

### 5. Monitor node group creation
```bash
aws eks describe-nodegroup \
  --cluster-name august-2026-eks-cluster \
  --nodegroup-name august-2026-free-tier-node \
  --query "nodegroup.{Status:status,InstanceTypes:instanceTypes,Desired:scalingConfig.desiredSize}" \
  --output table
```
Status moved from `CREATING` → `ACTIVE`.

### 6. Connect `kubectl` to the cluster

Running `kubectl get nodes` immediately after this failed with:
```
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```
This meant `kubectl` had no kubeconfig context pointing at the EKS cluster, so it defaulted to `localhost:8080`. Fixed with:
```bash
aws eks update-kubeconfig \
  --region ap-south-1 \
  --name august-2026-eks-cluster
```
Verified:
```bash
kubectl config current-context
kubectl get nodes
```

**Result:**
```
NAME                                          STATUS   ROLES    AGE   VERSION
ip-172-31-44-38.ap-south-1.compute.internal   Ready    <none>   3m2s  v1.36.2-eks-254016e
```

The worker node successfully joined the cluster. ✅

---

## 🚀 Deploying Workloads

```bash
kubectl create -f deployment.yml
kubectl create -f services.yml
```

---

## 💰 Free Tier Notes

- The final node group uses `t3.micro`, confirmed by the account as `free-tier-eligible=true`.
- **Free Tier eligibility on the EC2 instance does not cover every related resource.** The EKS control plane itself, along with NAT gateways, load balancers, EBS volumes, and public IPv4 addresses, can incur separate charges even when the worker node is Free Tier eligible.

---

## 📍 Current Status

| Component | Status |
|---|---|
| EKS Control Plane | ✅ ACTIVE |
| Node Group (`t3.micro`) | ✅ ACTIVE |
| Kubernetes Node | ✅ Ready |
| `kubectl` connectivity | ✅ Configured |

---

## 🔜 Next Steps

- Install Helm on the Ubuntu server
- Set up Argo CD for GitOps-based automated deployment from GitHub
- Explore self-hosted vs. AWS-managed trade-offs for future iterations

---

## 🗒️ Notes on Approach

This cluster was built as a **custom configuration** (EKS Auto Mode off) via the AWS Console for the control plane, with the node group and kubeconfig work done through the AWS CLI — giving hands-on exposure to both the console workflow and the CLI/`kubectl` debugging process, including a real Free Tier instance-type failure and its resolution.
