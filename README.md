# TyrQuake TV

A small patch set and reproducible build recipe for TyrQuake on 32-bit ARM Android TV. Original Quake PAK data is required.

## Scope

Replaces misaligned 32-bit lightmap reads with memcpy in ARM NEON and SSE remainder paths; escapes spaces in save comments so the existing token-based loader can read them; uses the TyrQuake TV library name to isolate overrides.

This repository contains the integration sources, patches and build/profile files. Upstream engines and dependencies are fetched at the exact revisions in `dependencies.json`; original commercial game data is not included.

## Build

The verified build host is Windows with Python 3.10+, Git for Windows at `C:/Program Files/Git` (short shell path `C:/Progra~1/Git/bin/sh.exe`) and Android NDK r27d. Use a checkout path without spaces. Set `ANDROID_NDK_HOME` if the NDK is not at `C:/tools/android/android-ndk-r27d`.

```powershell
python scripts/fetch_sources.py
python scripts/build_tyrquake.py
```

Output: `release/quake_native_libretro_android.so` (ARMv7, Android API 21). `PORT_SOURCES_DIR` optionally points to an existing dependency directory to share downloads between builds. Fetch refuses unexpected existing revisions/origins instead of resetting them. Remove only disposable `build/` output when a clean rebuild is needed.

## Install and configure

Install the core through RetroArch's Android core installation interface. The tested package is `com.retroarch.ra32`; its `com.retroarch.browser.debug.CoreSideloadActivity` accepts a `LIBRETRO` string pointing to a readable core file. Other RetroArch packages may differ.

Keep original game data on USB. Keep saves in a writable directory. `config/` contains the tested content-specific override/remap/options examples; adjust Android paths and content filenames to your installation. See [setup details](docs/setup.md). Do not replace the global RetroArch configuration. Xbox labels here refer to the tested Android Xbox mapping; other controller profiles can differ.

## Verification and limits

E1M1/E1M2 movement and shooting, save/load after process restart and resume passed. E1M2 software/threaded sample about 59 FPS; comparison runs were not deterministic replays. Xbox A jump and corrected vertical look were verified using injected controller events.

The optional Vulkan backend is compiled in, but software rendering was faster on the tested Mali-G52 TV. Not all combat scenes hold 60 FPS. Native save/load tested; controller quicksave/quickload shortcuts are not claimed as verified.

These are bounded historical gameplay checks on one Android 11 ARMv7/Mali-G52 TV. Physical controller feel and speaker quality were not independently measured. See `docs/verification.md` for publication-time build checks.

## Licensing and credits

New integration code, build scripts and documentation in this repository are provided under GPL-2.0-or-later. Patches retain the applicable upstream file licenses. See `LICENSE` and `licenses/` for upstream notices. Dependencies retain their own licenses; review them before distributing a linked binary. Game names identify compatibility and do not imply endorsement.
