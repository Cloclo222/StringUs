# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\GUI\\STRINGUS_GUI.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\ImageProcessing', 'ImageProcessing'), ('C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\stringus_code_IDE', 'stringus_code_IDE'), ('C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\GUI\\Input', 'Input'), ('.\\StringUS\\GUI\\Output\\', 'Output')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    'C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\LogoStringUS.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='StringUS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\guill\\OneDrive - USherbrooke\\S4GRO\\S4Projet\\StringUS\\StringUSico.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StringUS',
)
