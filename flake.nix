{
  description = "personal maplestory cubing averages calculations";
  nixConfig.bash-prompt = "\[cubecalc-dev\]$ ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-compat, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      with nixpkgs.legacyPackages.${system}; {
        devShell = mkShell {
          buildInputs = [
            python310
          ] ++ (with python310Packages; [
            numpy
          ]);
        };
      }
    );
}
