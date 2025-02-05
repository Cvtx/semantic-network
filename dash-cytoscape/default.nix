{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  pkgs
}:

buildPythonPackage rec {
  pname = "dash_cytoscape";
  version = "1.0.2";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-phAZ0hhNY6KztcBtBW07hnoEIjpnTMPHz5AKVhqaWao=";
  };

  # do not run tests
  doCheck = false;

  # specific to buildPythonPackage, see its reference
  nativeBuildInputs = [ setuptools wheel ];
  propagatedBuildInputs = [ pkgs.python3Packages.dash ];
}
