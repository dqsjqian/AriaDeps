# aria-deps

Project-agnostic dependency pipeline for C/C++ projects: resolve locked
dependencies, fetch sources, apply patches, build and transactionally install
them into a prefix.

Extracted from [AriaRead](https://github.com/dqsjqian/AriaRead)'s `tools/build.py`.

## What it does

- **Resolve**: `dependencies.json` lock records (GitHub/sqlite.org/bellard.org
  providers, pluggable) → pinned versions, URLs, SHA256
- **Fetch**: download archives (SHA256-verified) or git clone into editable
  `deps/<name>/` workspaces (user edits are preserved, tracked by content)
- **Build**: per-dependency recipes (`cmake` / `openssl` / `generated` kinds),
  patches applied to disposable snapshots (never touches user sources)
- **Install**: transactional prefix install with manifest, component reuse by
  content identity, rollback on failure
- **Verify**: read-only check that the prefix matches current sources
  (for CMake configure-time validation)

## Usage

Python 3.10 or newer is required. Install the released package into the same
Python environment that runs your build entry point:

```bash
python -m pip install "git+https://github.com/dqsjqian/AriaDeps.git@v0.1.1"
```

```python
from pathlib import Path
from aria_deps import Dependency, ProjectConfig, install
from aria_deps import providers

RECIPES = (
    Dependency(name="example", version="", url="", sha256="",
               license="MIT", license_files=("LICENSE",), root="", kind="cmake"),
)

def configure(recipes, profile, tls_backend):
    # project policy: filter/rewrite recipes per profile
    return recipes

config = ProjectConfig(
    name="myproject",
    recipes=RECIPES,
    configure=configure,
    providers={"sqlite": providers.resolve_sqlite},
    patches_dir=Path("recipes/patches"),
    patch_versions={"foo": {"1.0"}},
)

install(Path("dependencies.json"), Path("build/deps"), Path("build/deps/prefix"),
        Path("deps"), config=config, profile="runtime")
```

The example expects a schema-2 `dependencies.json` declaration with a matching
`example` entry. Normal installs reuse its resolved release, commit and SHA256;
they do not silently upgrade it.

`install(..., build_config="Debug", cmake_options=("-DFEATURE=ON",))` passes the
selected configuration through configure, build and install. Configuration and
extra CMake options are part of component identity, so a Release prefix cannot
be silently reused for Debug. Project hook code and its imported helper module
contents also invalidate affected components when changed.

For configure-time checks, pass the consumer's expected settings explicitly:
`verify(..., build_config="Release", cmake_options=())`. A mismatch fails
without changing the prefix. Omitting either option keeps its recorded value
for compatibility with existing callers. Hooks must be source-readable Python
functions defined in a file; built-ins and dynamically created functions are
rejected with a diagnostic because their implementation cannot be fingerprinted.

## Layout

All directories are caller-provided; nothing is hardcoded to a repository root.
The dependency work directory follows the build directory, so each
compiler/build-dir gets isolated snapshots, caches and installed libraries.

## Tests

```bash
python -m unittest discover -s tests -t tests -p "test_*.py"
```

CI runs the offline suite on Linux, macOS and Windows, with Python 3.10 and
3.13, and checks installation of the distribution. The Windows compiler test
is skipped on non-Windows hosts; install/upgrade/rollback tests run everywhere.
