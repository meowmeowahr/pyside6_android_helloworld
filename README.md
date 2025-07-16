# PySide6 Android App Example

This is a simple example Android app written in PySide6.

This example uses a custom deployment script instead of `pyside6-android-deploy` that is included in PySide6.

## Requirements

* Linux (macOS might be compatible, Windows will not work)
* Python 3.11 (fixed version requirement by Buildozer)
* PySide6 **6.9.1** (other versions may be compatible, requires script modifications)
* OpenJDK 17
* uv and dependencies defined in `pyproject.toml`

Additionally, this guide only covers building for **ARM64-v8 devices**.
Other and/or older devices are not covered in this guide, as they require manual cross-compilation of the Qt framework.

## Build Guide

> [!IMPORTANT]
Ensure that all of the above requirements are met.
Even minor version differences will cause issues during the build.

### Create a venv with uv

```console
python3 -m venv .venv
source ./.venv/bin/activate
pip install uv
```

### Install dependencies

```console
uv sync --extra build
```

### Configure

A custom configuration script is provided to prepare Buildozer

```console
python configure.py
```

### Build

```console
buildozer android debug --verbose
```

If the command succeeds, the built APK should end up in `dist/`

## Custom Configurations

The `buildozer.spec` file contains all of the configurations for Buildozer.

> [!WARNING]
All requirements must be defined under `app.requirements`, otherwise, they will not be included in the APK.
An import error will result in the app crashing on launch.

All options for iOS and/or Kivy are not relevant to this guide.
