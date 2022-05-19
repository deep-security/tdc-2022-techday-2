{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.rain.url = "path:/home/alex/.dotfiles/pkgs/rain";
  inputs.rain.inputs.nixpkgs.follows = "nixpkgs";

  inputs.flake-compat = {
    url = "github:edolstra/flake-compat";
    flake = false;
  };

  outputs = { self, nixpkgs, flake-utils, rain, ... }:
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
            rain.packages.${system}.default

            # shell development
            shellcheck

            # python development
            python39
            black
            mypy
            pyright
          ];
        };
      });
}

