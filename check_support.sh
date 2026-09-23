#!/system/bin/sh
# ==============================================================================
# Xiaomi Master Camera Combo - Automated Diagnostic & Compatibility Tool
# Author: borndead
# Usage:
#   In Termux: su -c "sh /sdcard/check_support.sh"
#   Via ADB:   adb shell "su -c sh /sdcard/check_support.sh"
# ==============================================================================

# ANSI Color Codes
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

REPORT_FILE="/sdcard/Download/Mi_Camera_Diagnostic_Report.txt"
mkdir -p /sdcard/Download 2>/dev/null

log_both() {
    echo -e "$1"
    # strip ANSI codes for text report
    echo -e "$1" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" >> "$REPORT_FILE"
}

# Reset report
echo "=== Xiaomi Master Camera Combo Diagnostic Report ===" > "$REPORT_FILE"
echo "Generated at: $(date)" >> "$REPORT_FILE"
echo "----------------------------------------------------" >> "$REPORT_FILE"

log_both "${CYAN}======================================================${NC}"
log_both "${CYAN}  📸 Xiaomi Master Camera Combo - Hardware Diagnostics ${NC}"
log_both "${CYAN}  Author: borndead                                     ${NC}"
log_both "${CYAN}======================================================${NC}"

# 1. Device Information
DEV_MODEL=$(getprop ro.product.model)
DEV_NAME=$(getprop ro.product.device)
DEV_BRAND=$(getprop ro.product.brand)
BUILD_ID=$(getprop ro.build.display.id)
ANDROID_VER=$(getprop ro.build.version.release)
SDK_API=$(getprop ro.build.version.sdk)
SOC_NAME=$(getprop ro.soc.model 2>/dev/null || getprop ro.board.platform)

log_both "\n${BLUE}[1. Сведения об устройстве / Device Info]${NC}"
log_both "  • Model:        $DEV_BRAND $DEV_MODEL ($DEV_NAME)"
log_both "  • Firmware/ROM: $BUILD_ID"
log_both "  • Android OS:   $ANDROID_VER (API $SDK_API)"
log_both "  • SoC Platform: $SOC_NAME"

case "$DEV_NAME" in
    ishtar)
        log_both "  • Target:       ${GREEN}Xiaomi 13 Ultra (Confirmed)${NC}" ;;
    aurora)
        log_both "  • Target:       ${GREEN}Xiaomi 14 Ultra (Confirmed)${NC}" ;;
    dada)
        log_both "  • Target:       ${GREEN}Xiaomi 15 (Confirmed)${NC}" ;;
    haotian)
        log_both "  • Target:       ${GREEN}Xiaomi 15 Pro (Confirmed)${NC}" ;;
    xuanyuan)
        log_both "  • Target:       ${GREEN}Xiaomi 15 Ultra (Confirmed)${NC}" ;;
    nezha)
        log_both "  • Target:       ${GREEN}Xiaomi 17 Ultra (Confirmed)${NC}" ;;
    *)
        log_both "  • Target:       ${YELLOW}Non-standard / Generic Flagship ($DEV_NAME)${NC}" ;;
esac

# 2. Root & Environment Check
log_both "\n${BLUE}[2. Проверка окружения Root / Environment]${NC}"
CURRENT_UID=$(id -u 2>/dev/null || echo 999)
if [ "$CURRENT_UID" -eq 0 ]; then
    log_both "  • Root Access:  ${GREEN}[PASS] Running with ROOT (UID 0)${NC}"
else
    log_both "  • Root Access:  ${YELLOW}[WARN] Not running as root. Some checks may be limited.${NC}"
fi

SELINUX=$(getenforce 2>/dev/null || echo "Unknown")
log_both "  • SELinux Mode: $SELINUX"

# Check Magisk / KSU / APatch module directory and conflicts
MOD_FOUND="false"
CONFLICT_MODS=""
for mpath in /data/adb/modules /data/adb/ksu/modules /data/adb/ap/modules; do
    if [ -d "$mpath" ]; then
        FOUND_NAMES=$(ls "$mpath" 2>/dev/null | grep -iE "camera|master|combo|borndead|imaging" | tr '\n' ' ')
        if [ -n "$FOUND_NAMES" ]; then
            log_both "  • Module State: ${GREEN}[PASS] Detected in $mpath: $FOUND_NAMES${NC}"
            MOD_FOUND="true"
            CAM_COUNT=$(ls "$mpath" 2>/dev/null | grep -iE "camera|master|combo|borndead|imaging" | wc -l)
            if [ "$CAM_COUNT" -gt 1 ]; then
                CONFLICT_MODS=$(ls "$mpath" 2>/dev/null | grep -iE "camera|master|combo|borndead|imaging" | tr '\n' ' ')
            fi
        fi
    fi
done
if [ "$MOD_FOUND" = "false" ]; then
    log_both "  • Module State: ${YELLOW}[INFO] Module directory not detected or non-root inspection.${NC}"
fi

if [ -n "$CONFLICT_MODS" ]; then
    log_both "  • ${RED}[WARNING] Multiple camera modules detected: $CONFLICT_MODS${NC}"
    log_both "    ${RED}Conflicting modules cause black screen, crashes, or stale icon! Delete older modules and reboot.${NC}"
fi

# Check for stale user camera updates in /data/app
if [ -d /data/app ]; then
    STALE_APP=$(find /data/app -maxdepth 2 -name "*com.android.camera*" 2>/dev/null)
    if [ -n "$STALE_APP" ]; then
        log_both "  • ${YELLOW}[WARN] Stale Camera update detected in /data/app: $STALE_APP${NC}"
        log_both "    ${YELLOW}Go to Settings -> Apps -> Camera -> 'Uninstall updates' & 'Clear all data'.${NC}"
    fi
fi

# 3. Qualcomm CamX & System Properties Check
log_both "\n${BLUE}[3. Системные параметры CamX & Engine Properties]${NC}"

# Check Max RAW Sizes (50M/200M unlock)
MAX_RAW=$(getprop persist.vendor.camera.maxRAWSizes)
if [ "$MAX_RAW" = "55" ]; then
    log_both "  • FullRes RAW Buffer:   ${GREEN}[PASS] persist.vendor.camera.maxRAWSizes = 55 (50M/200M Unlocked)${NC}"
else
    log_both "  • FullRes RAW Buffer:   ${RED}[FAIL] maxRAWSizes = '$MAX_RAW' (Expected: 55)${NC}"
fi

# Check DCG Hardware HDR
DCG_EN=$(getprop persist.vendor.camera.dcg.enable)
if [ "$DCG_EN" = "1" ]; then
    log_both "  • Hardware DCG HDR:     ${GREEN}[PASS] persist.vendor.camera.dcg.enable = 1 (Active)${NC}"
else
    log_both "  • Hardware DCG HDR:     ${RED}[FAIL] dcg.enable = '$DCG_EN' (Expected: 1)${NC}"
fi

# Check Sensor HDR
SENSOR_HDR=$(getprop persist.vendor.camera.sensor.hdr)
if [ "$SENSOR_HDR" = "1" ]; then
    log_both "  • Sensor HDR:           ${GREEN}[PASS] persist.vendor.camera.sensor.hdr = 1 (Active)${NC}"
else
    log_both "  • Sensor HDR:           ${YELLOW}[WARN] sensor.hdr = '$SENSOR_HDR'${NC}"
fi

# Check AISP Noise Reduction Bypass
AISP_BYPASS=$(getprop persist.vendor.camera.arcsoft.aisp_algo_nr.bypass)
if [ "$AISP_BYPASS" = "1" ]; then
    log_both "  • AISP NR Bypass:       ${GREEN}[PASS] aisp_algo_nr.bypass = 1 (Clean video textures)${NC}"
else
    log_both "  • AISP NR Bypass:       ${YELLOW}[INFO] aisp_algo_nr.bypass = '$AISP_BYPASS'${NC}"
fi

# Check Video Bitrate Factor
BITRATE=$(getprop persist.vendor.camera.video.bitrate.factor)
if [ "$BITRATE" = "1.5" ]; then
    log_both "  • Video Bitrate Factor: ${GREEN}[PASS] video.bitrate.factor = 1.5 (+50% bitrate)${NC}"
else
    log_both "  • Video Bitrate Factor: ${YELLOW}[INFO] video.bitrate.factor = '$BITRATE'${NC}"
fi

# 4. AUX Package Whitelist Check (GCam Access)
log_both "\n${BLUE}[4. Проверка белого списка сторонних камер / AUX Whitelist]${NC}"
AUX_LIST=$(getprop vendor.camera.aux.packagelist)
if [ -n "$AUX_LIST" ]; then
    log_both "  • AUX Packagelist:      ${GREEN}[PASS] Active${NC}"
    
    # Check key GCam packages
    for pkg in "com.agc.cam" "com.samsung.android.scan3d" "com.google.android.GoogleCamera" "com.android.mgc" "org.codeaurora.snapcam"; do
        if echo "$AUX_LIST" | grep -q "$pkg"; then
            log_both "    - $pkg: ${GREEN}[OK] Whitelisted${NC}"
        else
            log_both "    - $pkg: ${YELLOW}[MISSING]${NC}"
        fi
    done
    
    # Verify stock camera is excluded to prevent SAT arbitration freeze
    if echo "$AUX_LIST" | grep -q "com.android.camera"; then
        log_both "  • SAT Protection:       ${RED}[WARN] com.android.camera is in AUX list (May cause preview freeze!)${NC}"
    else
        log_both "  • SAT Protection:       ${GREEN}[PASS] com.android.camera excluded (Logical SAT protected)${NC}"
    fi
else
    log_both "  • AUX Packagelist:      ${RED}[FAIL] Property is empty! Third-party cameras won't see AUX lenses.${NC}"
fi

# 5. Chromatix & Binaries Verification
log_both "\n${BLUE}[5. Проверка файлов калибровок / Chromatix Status]${NC}"
TUNED_FILES=$(find /odm/etc/camera /vendor/etc/camera 2>/dev/null | grep -iE "tuned|sensormodule" | grep -i "$DEV_NAME" | head -n 4)
if [ -n "$TUNED_FILES" ]; then
    log_both "  • Chromatix Binaries:   ${GREEN}[PASS] Sensor profiles mounted:${NC}"
    for f in $TUNED_FILES; do
        log_both "    - $(basename "$f")"
    done
else
    log_both "  • Chromatix Binaries:   ${YELLOW}[INFO] Default system partition profiles active.${NC}"
fi

# 6. AI Neural Engine & Smart Features
log_both "\n${BLUE}[6. Проверка нейросетевых функций ИИ / AI Neural Engine Status]${NC}"
AISP_EN=$(getprop persist.vendor.camera.aisp)
if [ "$AISP_EN" = "1" ]; then
    log_both "  • Xiaomi AISP Hardware: ${GREEN}[PASS] persist.vendor.camera.aisp = 1 (Active on NPU)${NC}"
else
    log_both "  • Xiaomi AISP Hardware: ${YELLOW}[INFO] aisp = '$AISP_EN' (Stock or default)${NC}"
fi

AINR_EN=$(getprop persist.vendor.camera.sensor.ainr)
if [ "$AINR_EN" = "1" ]; then
    log_both "  • AI Noise Reduction:   ${GREEN}[PASS] persist.vendor.camera.sensor.ainr = 1 (Hexagon DSP)${NC}"
else
    log_both "  • AI Noise Reduction:   ${YELLOW}[INFO] sensor.ainr = '$AINR_EN'${NC}"
fi

CYBER_EN=$(getprop persist.vendor.camera.cyberfocus.enable)
if [ "$CYBER_EN" = "1" ]; then
    log_both "  • CyberFocus 2.0 AI:    ${GREEN}[PASS] cyberfocus.enable = 1 (Real-time tracking)${NC}"
else
    log_both "  • CyberFocus 2.0 AI:    ${YELLOW}[INFO] cyberfocus.enable = '$CYBER_EN'${NC}"
fi

AI_EDITOR_EN=$(getprop persist.sys.miui.gallery.ai_editor)
if [ "$AI_EDITOR_EN" = "1" ]; then
    log_both "  • HyperAI GenAI Studio: ${GREEN}[PASS] gallery.ai_editor = 1 (Eraser Pro & Expansion active)${NC}"
else
    log_both "  • HyperAI GenAI Studio: ${YELLOW}[INFO] gallery.ai_editor = '$AI_EDITOR_EN'${NC}"
fi

AI_DIR_EN=$(getprop persist.vendor.camera.ai.director)
if [ "$AI_DIR_EN" = "1" ]; then
    log_both "  • AI Director HUD:      ${GREEN}[PASS] camera.ai.director = 1 (Viewfinder coach active)${NC}"
else
    log_both "  • AI Director HUD:      ${YELLOW}[INFO] camera.ai.director = '$AI_DIR_EN'${NC}"
fi

# 7. Overall Verdict
log_both "\n${CYAN}======================================================${NC}"
if [ "$MAX_RAW" = "55" ] && [ "$DCG_EN" = "1" ] && [ -n "$AUX_LIST" ]; then
    log_both "${GREEN}  🎉 ВЕРДИКТ: ВСЕ СИСТЕМНЫЕ ТВЫКИ АКТИВНЫ И РАБОТАЮТ!${NC}"
    log_both "${GREEN}     All Master Camera tweaks are fully operational!${NC}"
else
    log_both "${YELLOW}  ⚠️ ВЕРДИКТ: НЕКОТОРЫЕ ПАРАМЕТРЫ НЕ АКТИВИРОВАНЫ.${NC}"
    log_both "${YELLOW}     Убедитесь, что модуль включен в Magisk/KSU и выполните перезагрузку.${NC}"
fi
log_both "${CYAN}======================================================${NC}"
log_both "📄 Отчёт сохранён в: ${GREEN}$REPORT_FILE${NC}\n"
