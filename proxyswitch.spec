# -*- mode: python -*-

from mastermind.version import VERSION

block_cipher = None

a = Analysis(['proxyswitch.py'],
             pathex=['/Users/arnau/kitchen/ustwo/mastermind'],
             binaries=None,
             datas=None,
             hiddenimports=[],
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
          name="proxyswitch-{}".format(VERSION),
          debug=False,
          strip=False,
          upx=True,
          console=True )
