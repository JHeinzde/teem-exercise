# `demo-power` — assembly demos and container images

> New here? Start with the [root README](../README.md) for the quickstart. This
> document is the deeper reference for the container images and demo programs.

This directory contains:

- A small library of sample AES assembly programs you can run inside the
  TEEM emulator to explore power-trace generation.
- Two Dockerfiles for the container images that support the project — a
  RISC-V cross-compilation toolchain and a JupyterLab + PyPy environment.

## Demo AES programs

If you can't follow the instructions, or compiling the provided AES template
doesn't produce a working program, this directory contains
several demo programs with different behaviour. Each is documented below by name
and function.

1. `aes-no-delay-first-byte-varies.s` — Runs AES ECB where only the first byte of
   the input varies, producing 256 traces (one per possible byte value). It has no
   countermeasures against side channels. To keep the attack as easy as possible to
   follow, the trace recording covers only the SubBytes operation of the first
   round on the first plaintext byte.
2. `aes-delay-first-byte-varies.s` — Same as the first program, but adds calls to
   the emulator's `trace_delay` syscall. This emulates the most basic countermeasure
   an AES implementation can use to make power-based side-channel attacks like DPA
   and CPA harder to execute.
3. `aes-no-delay-custom-plain-text.s` — Runs in the emulator, but before each run it
   expects you to provide a 16-byte (128-bit) plaintext to encrypt. Use this to build
   your own attack on the AES implementation.

The key is the same for all three programs.

## Container images

### `riscv-clang` — `Dockerfile`

Self-contained `debian:bookworm-slim` image with clang 17 and the RISC-V ELF
cross-compiler, used to compile the C sources for these demos into the
RISC-V assembly the emulator expects. Full build and usage instructions
live in [`INSTALL_TOOLCHAIN.md`](INSTALL_TOOLCHAIN.md).

Published to GHCR at `ghcr.io/jheinzde/teem-exercise/riscv-clang`.

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
only, so the JupyterLab is only reachable from your machine. Drop the
prefix only if you know you want remote access — and add an auth token
back if you do. Cases where this might be required are uses of colima, rancher
Desktop which might be used on MacOS and Windows. 

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

A prebuilt image is published to GHCR.

```bash
docker pull ghcr.io/jheinzde/teem-exercise/jupyter-env:latest
```
