// SPDX-License-Identifier: MIT
// Copyright 2023 Fiona Klute
use pyo3::prelude::*;

#[pyfunction]
pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[pymodule]
fn pyo3_example(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
