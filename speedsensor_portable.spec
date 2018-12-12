# -*- mode: python -*-

block_cipher = None

app_name = 'SpeedSensor'


a = Analysis(['src\\main.py'],
     pathex=['C:\\Users\\Admin\\Desktop\\SpeedSensorCompile'],
     binaries=None,
     datas=None,
     hiddenimports=[],
     hookspath=None,
     runtime_hooks=None,
     excludes=None,
     cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
     cipher=block_cipher)

exe = EXE(pyz,
  a.scripts,
  a.binaries,
  a.zipfiles,
  a.datas,
  name=app_name,
  debug=False,
  strip=False,
  upx=True,
  console=False)