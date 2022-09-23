{
  description = "maplestory cubing averages calculations, C 32-bit version";
  nixConfig.bash-prompt = "\[cubecalc-c-32-dev\]$ ";

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
            clang
            gcc
            tinycc
            mold
          ];
        };
      }
    );
}
