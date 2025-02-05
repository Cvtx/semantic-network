{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs = { self , nixpkgs ,... }: let
    pkgs = import <nixpkgs> {};
    # system should match the system you are running on
    system = "x86_64-linux";
    # system = "x86_64-darwin";
    python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
      dash-cytoscape = pyfinal.callPackage ./dash-cytoscape { };
    };
  };
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in pkgs.mkShell {
      packages = [
        (python.withPackages (python-pkgs: [          
          python-pkgs.ipython
          python-pkgs.dash
          python-pkgs.dash-cytoscape
          python-pkgs.tabulate
        ]))
      ];
      shellHook = ''
        echo `${pkgs.python3}/bin/python --version`
        python semanticnetwork.py
      '';
    };
  };
}
