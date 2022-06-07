{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.flake-compat = {
    url = "github:edolstra/flake-compat";
    flake = false;
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            # required packages
            awscli2
            gh
            python39Packages.pip
            zip

            # cloudformation development
            python39Packages.cfn-lint

            # shell development
            shellcheck

            # node development
            nodejs-slim-14_x
            (yarn.override {
              nodejs = nodejs-slim-14_x;
            })

            # python development
            python39
            black
            mypy
            pyright
          ];
        };
      });
}

