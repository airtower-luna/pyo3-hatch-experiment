# SPDX-License-Identifier: MIT
# Copyright 2023 Fiona Klute
import json
import platform
import shutil
import subprocess
import sysconfig
import tomllib
from functools import cached_property
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from pathlib import Path

CARGO_BIN = shutil.which('cargo')


class CargoBuildHook(BuildHookInterface):
    @cached_property
    def cargo_toml(self):
        with open('Cargo.toml', 'rb') as fh:
            return tomllib.load(fh)

    @cached_property
    def artifact_lib(self):
        return self.cargo_toml['lib']['name'] \
            + sysconfig.get_config_var('EXT_SUFFIX')

    def _find_binlib(self, msg):
        if msg['reason'] != 'compiler-artifact':
            return None
        if msg['target']['name'] != self.cargo_toml['package']['name']:
            return None
        if 'cdylib' not in msg['target']['kind']:
            return None

        match platform.system():
            case 'Windows':
                ending = '.dll'
            case 'Darwin':
                ending = '.dylib'
            case _:
                # Linux, and let's hope anything else is similar enough
                ending = '.so'

        for artifact in msg['filenames']:
            if artifact.endswith(ending):
                return artifact

    def initialize(self, version, build_data):
        cargo = subprocess.run(
            [
                CARGO_BIN, 'build', '--lib', '--release',
                '--message-format=json'
            ],
            stdout=subprocess.PIPE)
        for line in cargo.stdout.splitlines():
            if (binlib := self._find_binlib(json.loads(line))) is not None:
                break

        print(f'copy module {binlib} to {self.artifact_lib}')
        shutil.copyfile(binlib, self.artifact_lib)
        build_data['artifacts'].append(self.artifact_lib)
        build_data['infer_tag'] = True
        build_data['pure_python'] = False

    def clean(self, versions):
        Path(self.artifact_lib).unlink(missing_ok=True)
        subprocess.run([CARGO_BIN, 'clean'])
