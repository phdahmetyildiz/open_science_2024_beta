# This file is being archived on 15.11.2026 and is not part of the new version.
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.gcc
    pkgs.pkg-config
    pkgs.openssl
    pkgs.zlib
    pkgs.python3
    pkgs.python3Packages.virtualenv
    pkgs.cargo
  ];
}
