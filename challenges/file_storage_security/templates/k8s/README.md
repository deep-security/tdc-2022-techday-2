# How to deploy
The Tech Day template is expecting a `main.yaml` with all the kubernetes resources inside it. We generate this using kustomize.

To generate `main.yaml` after a change to any of the manifest files, run:

```shell
kubectl kustomize $PATH_TO_TEMPLATES/k8s > $PATH_TO_TEMPLATES/k8s/main.yaml
```

## Adding new manifests
When you want to add new manifests to the environment, add them to `kustomization.yaml` like so:

```yaml
...
resources:
  - attacker-machine-deployment.yaml
  - log4shell-endpoint-service.yaml
  - MY-NEW-MANIFEST
...
```