# SPDX-License-Identifier: MIT
# Copyright 2023 Fiona Klute
import json
import shutil
import subprocess
import sysconfig
import tomllib
from functools import cached_property
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from pathlib import Path


class CargoBuildHook(BuildHookInterface):
    @cached_property
    def cargo_toml(self):
        with open('Cargo.toml', 'rb') as fh:
            return tomllib.load(fh)

    @cached_property
    def artifact_lib(self):
        return self.cargo_toml['lib']['name'] \
            + sysconfig.get_config_var('EXT_SUFFIX')

    def initialize(self, version, build_data):
        cargo = subprocess.run(
            [
                shutil.which('cargo'), 'build', '--lib', '--release',
                '--message-format=json'
            ],
            stdout=subprocess.PIPE)
        for line in cargo.stdout.splitlines():
            msg = json.loads(line)
            if msg['reason'] != 'compiler-artifact':
                continue
            if msg['target']['name'] != self.cargo_toml['package']['name']:
                continue
            if 'cdylib' not in msg['target']['kind']:
                continue
            # This assumes that each target kind produces one file, in
            # the same order.
            assert len(msg['filenames']) == len(msg['target']['kind'])
            idx = msg['target']['kind'].index('cdylib')
            binlib = msg['filenames'][idx]
            break

        print(f'copy module {binlib} to {self.artifact_lib}')
        shutil.copyfile(binlib, self.artifact_lib)
        build_data['artifacts'].append(self.artifact_lib)
        build_data['infer_tag'] = True
        build_data['pure_python'] = False

    def clean(self, versions):
        Path(self.artifact_lib).unlink(missing_ok=True)
        subprocess.run(['cargo', 'clean'])
