"""aria-deps: project-agnostic dependency pipeline for C/C++ projects.

Resolve locked dependencies, fetch sources, apply patches, build and
transactionally install them into a prefix. Each project supplies its own
recipes, providers and policy via ProjectConfig; this package only provides
the mechanism.
"""

from .deps_build import (
    Dependency,
    DependencyError,
    ProjectConfig,
    cache_key,
    init_project,
    install,
    register_provider,
    update_lock,
    verify,
)

__all__ = [
    "Dependency",
    "DependencyError",
    "ProjectConfig",
    "cache_key",
    "init_project",
    "install",
    "register_provider",
    "update_lock",
    "verify",
]
