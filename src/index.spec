# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'F:\\auto_add_wechat_friends_py-master'

a = Analysis(['index.py'],
             pathex=['F:\\auto_add_wechat_friends_py-master'],
             binaries=[],
             datas=[(SETUP_DIR+'\\config', 'config'), 
             (SETUP_DIR+'\\data', 'data'), 
             (SETUP_DIR+'\\adb', 'adb'),
             (SETUP_DIR+'\\resources', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='index',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
