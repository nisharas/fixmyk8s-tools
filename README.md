# 🩺 FixMyK8s-Tools

**FixMyK8s-Tools** is a suite of CLI plugins for `kubectl` that helps developers and DevOps engineers manage the complexity of Kubernetes manifests. 

Rather than just telling you what is wrong, these tools are designed to **heal** your configurations and provide **educational feedback** in your terminal.

---

## 🛠 Available Tools

| Tool | Status | Purpose |
| :--- | :--- | :--- |
| [**kubectl-lint**](./lint) | ✅ Stable | Auto-heals syntax, indentation, and formatting. |
| **kubectl-doctor** | 🏗 In-Dev | Audits Selector-to-Label connections and missing Secrets. |
| **kubectl-cost-check**| 💡 Planned | Predicts resource costs based on requests/limits. |

---
## 🛠 Tool 1: kubectl-lint

kubectl-lint is not just a linter; it’s an auto-healer. It uses a dual-engine approach (Pattern Matching + YAML Standardizing) to fix manifests that are too broken for standard tools to even open.

✨ Smart Features

Universal Keyword Detection: Automatically detects missing colons on any Kubernetes keyword (even Custom Resources!).

The "Space-Injection" Engine: Fixes image:nginx into image: nginx instantly.

Structure Normalization: Converts illegal tabs and messy indentations into the K8s-standard 2-space format.

Visual Diff Report: Shows you exactly what was fixed in green (added) and red (removed) before saving.
---

## 🚀 Getting Started (Installing kubectl-lint)

You don't need Python or any dependencies to use these tools. Simply download the pre-compiled binary for your system.

### **Quick Install (Linux/macOS)**
```bash
# 1. Download the latest binary
curl -LO https://github.com/nisharas/fixmyk8s-tools/releases/download/v1.0.0/kubectl-lint

# 2. Make it executable
chmod +x kubectl-lint

# 3. Move it to your PATH
sudo mv kubectl-lint /usr/local/bin/

# 4. Use it immediately
kubectl lint my-dev-pod.yaml
