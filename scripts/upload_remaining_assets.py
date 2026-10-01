import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import publish_github_release

TAG_NAME = "v6.2"

def main():
    token = publish_github_release.get_token()
    rel = publish_github_release.create_release(TAG_NAME, "", "")
    if not rel or "id" not in rel:
        return
    release_id = rel["id"]
    releases_dir = REPO_ROOT / "releases"
    existing = [a["name"] for a in rel.get("assets", [])]
    
    remaining = [
        "Mi13U_Master_Camera_Combo_5_v6.2_MasterFinal_by_borndead.zip",
        "Mi13U_Camera_5_v6.1_MIUI14_EU_Stable_by_borndead.zip",
        "Mi14U_Master_Camera_Combo_5_v6.2_Full_by_borndead.zip",
        "Mi15_Master_Camera_Combo_5_v6.2_Full_by_borndead.zip",
        "Mi15U_Master_Camera_Combo_5_v6.2_Full_by_borndead.zip",
        "X17U_Master_Camera_Combo_5_v6.2_Full_by_borndead.zip",
    ]
    
    for name in remaining:
        if name in existing:
            continue
        p = releases_dir / name
        if p.exists():
            try:
                publish_github_release.upload_asset(release_id, str(p))
            except Exception as e:
                print(f"Error {name}: {e}")

if __name__ == "__main__":
    main()
