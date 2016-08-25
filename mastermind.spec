# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files


a = Analysis(['mastermind.py'],
             pathex=['.'],
             binaries=None,
             datas=collect_data_files("mitmproxy.onboarding") +
                   [('./mastermind/scripts/*.py', 'scripts')],
             hiddenimports=['mastermind.handlers', 'mastermind.driver'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None)

pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name="mastermind",
          debug=False,
          strip=False,
          upx=True,
          console=True)
