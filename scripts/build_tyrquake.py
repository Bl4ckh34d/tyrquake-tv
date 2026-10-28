"""Build pinned TyrQuake with its optional Vulkan backend for ARMv7."""
from pathlib import Path
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ.get("PORT_SOURCES_DIR", str(ROOT / "sources"))).resolve()
NDK_HOME = Path(os.environ.get("ANDROID_NDK_HOME", "C:/tools/android/android-ndk-r27d"))
SOURCE = SOURCES / 'tyrquake'
REVISION = '67db338ff4d27fdbcead61d4e54938d758ae62cb'
NDK = Path(os.environ.get('ANDROID_NDK_HOME', 'C:/tools/android/android-ndk-r27d'))


def main():
    actual = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != REVISION:
        raise SystemExit(f'Expected {REVISION}, found {actual}')
    for name in ['tyrquake-tv.patch']:
        patch = str(ROOT / 'patches' / name)
        applied = subprocess.run(['git', '-C', str(SOURCE), 'apply', '--reverse', '--check', patch],
                                 capture_output=True).returncode == 0
        if not applied:
            subprocess.run(['git', '-C', str(SOURCE), 'apply', '--check', patch], check=True)
            subprocess.run(['git', '-C', str(SOURCE), 'apply', patch], check=True)
    env = os.environ.copy()
    env['PATH'] = 'C:/Program Files/Git/usr/bin;C:/Program Files/Git/bin;' + env['PATH']
    args = [str(NDK / 'prebuilt/windows-x86_64/bin/make.exe'),
            '-f', str(NDK / 'build/core/build-local.mk'),
            'SHELL=C:/Progra~1/Git/bin/sh.exe', 'HOST_OS=cygwin', 'HOST_OS_BASE=windows',
            'NDK_PROJECT_PATH=.', 'APP_BUILD_SCRIPT=Android.mk', 'NDK_APPLICATION_MK=Application.mk',
            'NDK_OUT=' + Path(os.path.relpath(ROOT / 'build/tyrquake-armv7/obj', SOURCE / 'jni')).as_posix(), 'NDK_LIBS_OUT=' + Path(os.path.relpath(ROOT / 'build/tyrquake-armv7/libs', SOURCE / 'jni')).as_posix(),
            'APP_ABI=armeabi-v7a', 'APP_PLATFORM=android-21', 'APP_SHORT_COMMANDS=true',
            'RHI_HAVE_VULKAN=1', 'APP_CFLAGS=-DRHI_HAVE_VULKAN', '-j4', 'installed_modules']
    log = ROOT / 'evidence/tyrquake-build.log'
    log.parent.mkdir(exist_ok=True)
    (ROOT / 'release').mkdir(exist_ok=True)
    with log.open('w', encoding='utf-8') as output:
        process = subprocess.Popen(args, cwd=SOURCE / 'jni', env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace')
        for line in process.stdout:
            output.write(line)
            output.flush()
            if any(word in line for word in ('error:', 'Error ', 'failed', 'Install ', 'SharedLibrary', '***')):
                print(line[:600], end='', flush=True)
        code = process.wait()
    if code:
        raise SystemExit(f'Build failed ({code}); see {log}')
    target = ROOT / 'release/quake_native_libretro_android.so'
    shutil.copyfile(ROOT / 'build/tyrquake-armv7/libs/armeabi-v7a/libretro.so', target)
    subprocess.run([str(NDK / 'toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-strip.exe'),
                    '--strip-unneeded', str(target)], check=True)
    print(f'Built {target} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
