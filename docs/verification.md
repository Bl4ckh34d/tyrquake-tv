# Follow-up verification — 2026-10-29

The repository's build script completed on Windows with NDK r27d using the pinned shared sources. Python scripts parse, and source patches pass both a forward check against a temporary pristine upstream index and a reverse check against the working source. Original game data, saves, screenshots and binaries are excluded from publication.

Build: `quake_native_libretro_android.so`, 641,352 bytes, SHA-256 `3d3caaecf49d1ae0eb8abca25452da2c90ed5d1abae4ef3267ef11dff1f068a8`.

The byte-identical installed build passed gameplay save/move/fire/load, reset/load, fast-forward and Close Content. Physical Xbox A confirms menus and jumps; B cancels menus and swims down. L2 is reserved, L3/R3 use tvquick.sav.

These are bounded checks on Android 11 ARMv7. They do not establish whole-campaign performance or subjective physical-controller feel. Earlier records below describe their own historical builds.

---

# Publication verification � 2026-10-28

The checked-in build recipe passed on Windows with Python/Git and NDK r27d, targeting ARMv7 API 21. Python scripts parse successfully. All patches pass forward checks against the pinned upstream index and reverse checks against the patched working tree.

Build: `quake_native_libretro_android.so`, 641208 bytes, SHA256 `5d288ff358a66d0ca656555a9eacaaad3fa8c0fdcca61b83c7d0e8a20a6c1204`. This identifies this verification build; paths and timestamps can affect rebuild hashes. Original game files, player saves and generated output are not included in Git.

Recovered source patch set builds successfully. This rebuilt binary has not received a fresh live gameplay test. Earlier gameplay measurements describe the previously installed build. Production core unchanged.
