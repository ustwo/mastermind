# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(['mastermind.py'],
             pathex=['.'],
             binaries=None,
             datas=collect_data_files("mitmproxy.onboarding") +
                   [('./mastermind/scripts/*.py', 'scripts')],
             hiddenimports=['mastermind.handlers', 'mastermind.driver'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name="mastermind",
          debug=False,
          strip=False,
          upx=True,
          console=True )
