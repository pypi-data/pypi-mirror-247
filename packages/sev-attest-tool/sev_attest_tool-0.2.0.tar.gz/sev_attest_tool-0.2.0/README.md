# sev-attest-tool

This library generates and verifies SEV-SNP attestation reports.

## Python

To build the Python package, run:

```
sudo docker run --rm -v $(pwd):/io --entrypoint "" ghcr.io/pyo3/maturin bash -c 'yum install -f openssl-devel && maturin build --release'
```