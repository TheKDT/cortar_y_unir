# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['trans5.py'],
    pathex=[],
    binaries=[
        # Agrega aquí el ejecutable de MeCab y otros binarios necesarios
        ('C:\\MeCab\\bin\\mecab.exe', '.'),
        # Asegúrate de incluir otros archivos binarios necesarios por MeCab aquí
    ],
    datas=[
        ('C:\\MeCab\\etc\\mecabrc', 'etc'),
        # Incluye los diccionarios de MeCab. Ajusta esta línea según sea necesario.
        ('C:\\MeCab\\dic\\', 'dic'),
        ('C:\\Python312\\Lib\\site-packages\\unidic_lite\\dicdir', 'unidic_lite/dicdir'),
        ],
    hiddenimports=[
        'manga_ocr',
        'transformers',
        'unidic_lite',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='trans5',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['pluma.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='trans5',
)