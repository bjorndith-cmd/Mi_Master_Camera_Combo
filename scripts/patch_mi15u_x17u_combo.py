import os, shutil, zipfile

stg = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Combo_Staging'
payload = r'C:\Users\ASTA\OneDrive\Antigravity\Clean_Camera_Payload_Staging'

# Update priv-app and permissions in staging
shutil.rmtree(os.path.join(stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload, 'system', 'priv-app'), os.path.join(stg, 'system', 'priv-app'))
shutil.copy2(os.path.join(payload, 'system', 'etc', 'permissions', 'privapp-permissions-camera.xml'), os.path.join(stg, 'system', 'etc', 'permissions', 'privapp-permissions-camera.xml'))

# Update customize.sh to add oat/.replace
cust_p = os.path.join(stg, 'customize.sh')
with open(cust_p, 'r', encoding='utf-8') as f:
    c = f.read()

old_oat = 'touch "$target_dir/oat/.nomedia"'
new_oat = 'touch "$target_dir/oat/.replace"\n    touch "$target_dir/oat/.nomedia"\n    touch "$target_dir/.replace"'
c = c.replace(old_oat, new_oat)
with open(cust_p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

# Repackage v5.1 and v5.0
z_51 = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip'
z_50 = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.0_by_borndead.zip'
with zipfile.ZipFile(z_51, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(stg):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, stg).replace('\\', '/')
            zf.write(full_p, rel_p)

shutil.copy2(z_51, z_50)
repo_rel = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\releases'
shutil.copy2(z_51, os.path.join(repo_rel, os.path.basename(z_51)))
shutil.copy2(z_50, os.path.join(repo_rel, os.path.basename(z_50)))
print('Patched and repackaged Mi15U_X17U combo.')
