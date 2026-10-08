# Changelog

## 0.1.1

- Carry the selected build configuration through every CMake step and include
  configuration plus caller-supplied CMake options in cache identity.
- Track project hook and helper source changes when reusing installed components.
- Reject unsafe cross-platform archive paths and non-regular members before
  extracting any files; preserve existing files on failure.
- Restore the offline install, upgrade and failed-upgrade rollback regression.
- Add Linux, macOS and Windows package and contract CI, and the MIT license file.
