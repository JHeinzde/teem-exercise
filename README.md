# TEEM Power Side-Channel Exercise

This exercise walks you through **power-based side-channel attacks** — Differential
Power Analysis (DPA), Correlation Power Analysis (CPA), and defeating a simple
timing countermeasure — against an AES implementation running on the TEEM CPU
emulator. You work through it entirely in a Jupyter notebook.

**Prerequisite:** a working [Docker](https://docs.docker.com/get-docker/)
installation. Nothing else needs to be installed on your machine.

## Step 1 — Get the two prebuilt images

```sh
docker pull ghcr.io/jheinzde/teem-exercise/jupyter-env:latest
docker pull ghcr.io/jheinzde/teem-exercise/riscv-clang:latest
```

- `jupyter-env` runs JupyterLab (with PyPy) for the exercise notebook.
- `riscv-clang` cross-compiles the AES C code into the RISC-V assembly the emulator runs.

## Step 2 — Launch JupyterLab

From the **repository root**:

```sh
docker run --rm -it \
  -p 127.0.0.1:8888:8888 \
  -v "$(pwd)":/work \
  --user "$(id -u):$(id -g)" \
  ghcr.io/jheinzde/teem-exercise/jupyter-env:latest
```

Then open <http://localhost:8888> and open **`Exercise.ipynb`**.

## Step 3 — Follow the notebook top to bottom

The notebook guides you through everything else: instrumenting the bundled AES
project in `micro-aes-template/`, compiling it with the `riscv-clang` image,
running the emulator to capture power traces, and carrying out the DPA, CPA, and
cross-correlation attacks. Run the cells in order.

## If something breaks

- **Prefer a native toolchain over Docker?** See
  [`demo-power/INSTALL_TOOLCHAIN.md`](demo-power/INSTALL_TOOLCHAIN.md).
- **Emulator reference** (CLI, `config.yml`, compiling C, license/copyright): see
  [`doc/emulator.md`](doc/emulator.md).
- **Can't compile?** `demo-power/` ships prebuilt `.s` programs as a fallback —
  see [`demo-power/README.md`](demo-power/README.md).
