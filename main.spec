# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['UI\\'],
             binaries=[],
             datas =[('698APDUConfig.ini',''),('698DataIDConfig.ini',''),('698DataTypeConfig.ini',''),('698ErrIDConfig.ini','')],
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
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='UI\\698.ico')
