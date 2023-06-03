# pyo3-hatch-experiment

This is an experiment in combining pyo3 and hatch, instead of using
[`maturin`](https://www.maturin.rs/) or
[setuptools-rust](https://setuptools-rust.readthedocs.io/en/latest/). Cargo
gets called via a [custom build
hook](https://hatch.pypa.io/latest/plugins/build-hook/custom/)
implemented in [`cargo_build.py`](cargo_build.py). The hook is
configured in [`pyproject.toml`](pyproject.toml) to run only for the
`wheel` target, because there's no point in building the library for a
source distribution.

## What's experimental?

* The hook assumes that the working directory of `hatchling` is also
  where the Rust package exists (with `Cargo.toml`, etc.).
* Using custom build targets may need some extra care depending on
  whether the hook should or shouldn't run. The hook class itself
  doesn't check the target.
