# Structure of this folder

```plain
file_storage_security/
├── lambda/ => Lambdas for this challenge
├── templates/ => CloudFormation templates for this challenge
│  └── k8s/ => Manifest files for the kubernetes environment
├── tools/ => Binaries and tools for challenge red-team activities
├── flake.nix => Internal tooling file
└── flake.lock => Internal tooling lockfile
```

# Kubernetes Environment

## Structure
In this challenge, an attacker environment is launched into the existing EKS stack. Here are the steps that are taken by Cloudformation to create the environment:

- Delete any existing infrastrucutre already in the EKS cluster that pertains to this challenge. 
- Create a new namespace to launch challenge pods into.
- Launch all the contents of `./templates/k8s`.

## Development

To develop/test locally:

1. Get a Kubernetes cluster. You can use any cluster, but I recommend the following as it replicates the Tech Day environment:
    - Launch an EKS stack, either through the main CloudFormation template, or launching `infra/eks/amazon-eks-entrypoint-existing-vpc.template.yaml` separately (making sure to pass in the outputs of the main template's `VPCStack`).
2. Create a `cfn-references` secret in the cluster with the following values:
    ```json
    {
        "TOOLSURL": "https://CODEBUCKET.s3.amazonaws.com/PATH/TO/TOOLS/", 
        "PLAYERPASSWORD": "YOUR-DESIRED-PASSWORD-FOR-LOCAL-DEVELOPMENT"
    }
    ```
   - I do this by running: 
    ```bash
    kubectl create secret generic cfn-references --from-literal=TOOLSURL=https://CODEBUCKET.s3.amazonaws.com/PATH/TO/TOOLS/ --from-literal=PLAYERPASSWORD="YOUR-DESIRED-PASSWORD-FOR-LOCAL-DEVELOPMENT" --dry-run=client -o yaml | kubectl apply -f -
    ```
   - Note that this secret will be overwritten in the Tech Day cluster, so you'll have to reset it to your custom value if that happens.
3. During Tech Day, all the manifests in `./templates/k8s` will be launched, so to replicate this behavior, I'd always test deployment using `kubectl apply -f templates/k8s`. But this is really up to you. 
4. Have fun!

To test the Tech Day deployment:

1. The `FSSStack`'s nested `AttackerMachine` template will launch a Lambda Step Function called `DeployAttackerEnvStateMachine`. Find it in the Resources section of the `AttackerMachine` nested template and go to it.
2. Run the state machine.
    - Each activation of the script will delete any existing Kubernetes infrastructure from this challenge and relaunch it. Should take about 2 minutes.
3. Use the `Player` user and `PlayerPassword` main-stack output to login to the attacker machine.
