# -*- mode: python -*-

block_cipher = None


a = Analysis(['ExoPlanet.py'],
             pathex=['C:\\Users\\Jerry\\Projects\\exoplanet'],
             binaries=[],
             datas=[
                 ('README.md', '.'),
                 ('COPYING.txt', '.'),
                 ('Info/Images/*.png', 'Info/Images/'),
                 ('Info/Images/appicon.ico', 'Info/Images/'),
                 ('Info/Parameters/*.json', 'Info/Parameters/'),
                 ('Info/Styles/fonts/Catamaran/*', 'Info/Styles/fonts/Catamaran/'),
                 ('Info/Styles/fonts/Cutive_Mono/*', 'Info/Styles/fonts/Cutive_Mono/'),
                 ('Info/Styles/fonts/Merriweather/*', 'Info/Styles/fonts/Merriweather/'),
                 ('Info/Styles/fonts/Montserrat/*', 'Info/Styles/fonts/Montserrat/'),
                 ('Info/Styles/fonts/Roboto_Slab/*', 'Info/Styles/fonts/Roboto_Slab/'),
                 ('Info/Styles/fonts/Work_Sans/*', 'Info/Styles/fonts/Work_Sans/'),
                 ('Info/Styles/AppStyles.qss', 'Info/Styles/'),
             ],
             hiddenimports=[],
             hookspath=['PyInstaller-Hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ExoPlanet',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='Info\\Images\\appicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ExoPlanet')
