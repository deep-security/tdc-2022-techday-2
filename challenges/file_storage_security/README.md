# Structure of this folder

```plain
file_storage_security/
├── templates/ => Templates for this challenge
├── lambda/ => Lambdas for this challenge
├── scripts/ => Development scripts
├── flake.nix => Internal tooling file
└── flake.lock => Internal tooling lockfile
```

# Scripts
All under `scripts/`:
- `package-lambda.sh`: package the code in a lambda folder into a `.zip`, ready for consumption by Lambda. Run inside the directory of the function you wish to package, calling `../../scripts/package-lambda.sh`.
- `vend.sh`: deploy the latest upstream commit hash for the current branch to Vending Machine. Can run anywhere.

# How to add a new lambda function

I swear this is going to make the CloudFormation easier to reason about, but can be a PITA when you make a new function. Tradeoffs.

> TODO: Automate this.

1. Copy an existing lambda folder and rename it to your liking.
2. Delete the existing `.zip` file in the folder.
3. Edit code and alter `requirements.txt `as needed. Just leave requirements.txt empty if there are no dependencies.
4. Once function is finished, `cd` into the folder and run `./package.sh`. 
5. Edit `templates/entrypoint.template.yaml`: 
    1. Include a parameter that points to the zip file. Follow the form of the function code already there.
    2. Add that parameter as a parameter to the `FSSMainStack` resource. For example `MyCode: !Ref MyCode`.
    3. Add that parameter as a `!Ref` under `Objects` in the `CopyZips` resource
6. Edit `templates/main.template.yaml`:
    1. Add a parameter under `Parameters` that has the same name as you defined in step 5. Set `Default: ""` and `Type: String`.
    2. Add the function to the template, following the form of other functions currently in the template.
7. Commit/sync/move on with your life. You did it!
