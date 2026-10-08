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

```python
from aria_deps import Dependency, ProjectConfig, install
from aria_deps import providers

RECIPES = (
    Dependency(name="zlib", kind="cmake", ...),
    # ...
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

install(lock_file, work_dir, prefix, source_dir, config=config, profile="runtime")
```

## Layout

All directories are caller-provided; nothing is hardcoded to a repository root.
The dependency work directory follows the build directory, so each
compiler/build-dir gets isolated snapshots, caches and installed libraries.

## Tests

```bash
python -m unittest discover -s tests -t tests -p "test_*.py"
```
