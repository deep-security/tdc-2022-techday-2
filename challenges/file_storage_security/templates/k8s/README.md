# Adding new manifests
This is **very important**. When you want to add new manifests to the environment, add them to `kustomization.yaml` like so:

```yaml
...
resources:
  - attacker-machine-deployment.yaml
  - log4shell-endpoint-service.yaml
  - MY-NEW-MANIFEST
...
```