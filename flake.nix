{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs = { self, nixpkgs, nixpkgs-python }: 
    let
      system = "x86_64-linux";
      # system = "x86_64-rwin";

      pythonVersion = "3.12.0";


      pkgs = import nixpkgs { inherit system; };
      myPython = nixpkgs-python.packages.${system}.${pythonVersion};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
	  pkgs.python312
	  pkgs.python312Packages.pip
	  pkgs.python312Packages.psycopg
	  pkgs.python312Packages.tkinter
	  pkgs.python312Packages.pymupdf
	  pkgs.python312Packages.python-lsp-server
	  pkgs.python312Packages.ruff
	  pkgs.python312Packages.screeninfo
	  pkgs.python312Packages.pillow
        ];
        shellHook = ''
          python --version
        '';
      };
    };
}