# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\wangke\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\wangke\\Desktop\\698trans'],
             binaries=[],
             datas =[('C:\\Users\\wangke\\Desktop\\698trans\\698APDUConfig.ini',''),('C:\\Users\\wangke\\Desktop\\698trans\\698DataIDConfig.ini',''),('C:\\Users\\wangke\\Desktop\\698trans\\698DataTypeConfig.ini',''),('C:\\Users\\wangke\\Desktop\\698trans\\698ErrIDConfig.ini','')],
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
          console=False , icon='698.ico')
