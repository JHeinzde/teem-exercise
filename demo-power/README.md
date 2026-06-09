# `demo-power` — assembly demos and container images

> New here? Start with the [root README](../README.md) for the quickstart. This
> document is the deeper reference for the container images and demo programs.

This directory contains:

- A small library of sample AES assembly programs you can run inside the
  TEEM emulator to explore power-trace generation.
- Two `Dockerfile`s for the container images that support the project — a
  RISC-V cross-compilation toolchain and a JupyterLab + PyPy environment.

## Demo AES programs

In case you can't follow the instructions or don't get any working programs by compiling
the AES implementation referenced by this emulator this directory contains mulitiple demo 
programs with different behaviour. We have documented them each with their name and their actual
functionality in this document. 

1. aes-no-delay-first-byte-varies.s This program executes AES ECB where only the first byte of the input varies. It outputs 256 different traces (one for each possible byte value) and contains no counter measures against side channels. The trace recording also only contains the SubBytes operation for the first round and the first byte of the plaintext to make any attack as easy as possible and as simple as possible to understand
2. aes-delay-first-byte-varies.s Exhibits all of the characteristics of the first programm but contains cally to the trace_delay syscall of the emulator. This serves as emulation of the most basic counter measure which can be implemented into AES implementations to make power-based side channel attacks like DPA and CPA harder to excute. 
3. aes-no-delay-custom-plain-text.s This programm can be executed within the emulator but before each run it expects you to provide a plain text of 16 bytes (128 bit) which will be encrypted. This can be used to create your own attack on the AES implementation.

The keys for all of these implementations are set to the same value. 

## Container images

### `riscv-clang` — `Dockerfile`

Self-contained `debian:bookworm-slim` image with clang 17 and the RISC-V ELF
cross-compiler, used to compile the C sources for these demos into the
RISC-V assembly the emulator expects. Full build and usage instructions
live in [`INSTALL_TOOLCHAIN.md`](INSTALL_TOOLCHAIN.md).

Published to GHCR at `ghcr.io/jheinzde/teem-exercise/riscv-clang` by the
`publish-riscv-clang` workflow on every push to `master` that touches the
relevant files.

### `jupyter-env` — `Dockerfile.jupyter`

JupyterLab + PyPy container for working on `Exercise.ipynb` and running the
heavy trace-generation workloads in `headless_main.py`.

#### Build

From the **repo root** (not from inside this folder):

```bash
docker build -f demo-power/Dockerfile.jupyter -t teem-jupyter .
```

The build context must be the repo root because the Dockerfile copies
`requirements.txt` from there.

#### Run

```bash
docker run --rm -it \
  -p 127.0.0.1:8888:8888 \
  -v "$(pwd)":/work \
  --user "$(id -u):$(id -g)" \
  teem-jupyter
```

Then open <http://localhost:8888>. JupyterLab launches with no auth token;
the `127.0.0.1:` prefix on `-p` binds the port to the loopback interface
only, so nothing on your LAN can reach the notebook server. Drop the
prefix only if you know you want remote access — and add an auth token
back if you do.

The `--user` flag matters: without it, JupyterLab runs as root inside the
container and any files saved from notebook cells will land on the host
owned by root.

#### PyPy for trace generation

From inside a notebook cell:

```python
!pypy3 headless_main.py demo/some_program.s
```

PyPy 3 is installed with `python-benedict[yaml]`, `prompt_toolkit`, and
`numpy`. Matplotlib is intentionally not installed under PyPy — plot from
the CPython notebook side instead.

#### Published image

A prebuilt image is published to GHCR by the `publish-jupyter-env` workflow
on every push to `master` that touches `Dockerfile.jupyter` or the repo-root
`requirements.txt`:

```bash
docker pull ghcr.io/jheinzde/teem-exercise/jupyter-env:latest
```
