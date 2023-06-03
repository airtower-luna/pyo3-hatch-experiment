# SPDX-License-Identifier: MIT
# Copyright 2023 Fiona Klute
import pyo3_example


def test_pyo3_example():
    assert pyo3_example.add(2, 3) == 5
