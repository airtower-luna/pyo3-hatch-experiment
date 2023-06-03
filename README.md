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

* I haven't checked if the way the hook calls Cargo will work on
  non-Linux platforms.
* The hook makes some assumptions about the artifacts produced by
  Cargo, specifically that the artifacts produced for the lib build
  will be one per `crate-type` and listed in the same order as the
  types in the `filenames` field of the `compiler-artifact` message.
* The hook assumes that the working directory of `hatchling` is also
  where the Rust package exists (with `Cargo.toml`, etc.).
* Using custom build targets may need some extra care depending on
  whether the hook should or shouldn't run. The hook class itself
  doesn't check the target.
