import zipfile
import os
import shutil

zips = [
    r'releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15_Master_Camera_Combo_v5.0_by_borndead.zip'
]

old_dada = '    dada)\n        DEVICE_NAME="Xiaomi 15"\n        DEV_PROFILE="dada"\n        ZOOM_GRID="0.6:1.0:3.2"'
new_dada = '    dada)\n        DEVICE_NAME="Xiaomi 15"\n        DEV_PROFILE="dada"\n        # On Xiaomi 15 (dada), stock HAL supports 50M remosaic only on main sensor (1.0x).\n        # Forcing 0.6x and 3.2x breaks stock camera due to missing Chi-CDK remosaic graph nodes.\n        ZOOM_GRID="1.0"'

for zp in zips:
    if not os.path.exists(zp):
        print('Not found:', zp)
        continue
    tmp_zp = zp + '.tmp.zip'
    with zipfile.ZipFile(zp, 'r') as zin, zipfile.ZipFile(tmp_zp, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'customize.sh':
                text = data.decode('utf-8', errors='ignore')
                if old_dada in text:
                    text = text.replace(old_dada, new_dada)
                    print('Patched customize.sh in', zp)
                else:
                    print('old_dada not found in', zp)
                data = text.encode('utf-8')
            zout.writestr(item, data)
    shutil.move(tmp_zp, zp)
    print('Updated', zp, 'Size:', os.path.getsize(zp))
