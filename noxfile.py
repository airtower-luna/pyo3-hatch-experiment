# SPDX-License-Identifier: MIT
# Copyright 2023 Fiona Klute
import nox

nox.options.download_python = 'never'


@nox.session
def lint(session):
    """Lint using Flake8."""
    session.install('flake8')
    session.run('flake8', '--statistics', '.')


@nox.session(python=['3.13'])
def test(session):
    """Run tests, report coverage."""
    session.install('.[tests]')
    session.run('pytest', '-v')
