# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Star_C-Wing.py'],
    pathex=[],
    binaries=[],
    datas=[('menu_background.png', '.'), ('game_background.png', '.'), ('gover_background.png', '.'), ('enemy.png', '.'), ('asteroid.png', '.'), ('ship.png', '.'), ('shoot.wav', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Star_C-Wing',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
