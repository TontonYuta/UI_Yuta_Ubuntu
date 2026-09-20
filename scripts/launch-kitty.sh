#!/usr/bin/env bash
# ==============================================================================
# 🐱 KITTY-OS 2.0 LAUNCHER (DIRECT DRM / WAYLAND SWAY TILING)
# ==============================================================================

# Thiết lập môi trường Wayland & XDG
export XDG_SESSION_TYPE=wayland
export XDG_CURRENT_DESKTOP=sway
export GDK_BACKEND=wayland
export QT_QPA_PLATFORM=wayland
export CLUTTER_BACKEND=wayland
export MOZ_ENABLE_WAYLAND=1
export _JAVA_AWT_WM_NONREPARENTING=1
export ELECTRON_OZONE_PLATFORM_HINT=wayland
export BROWSER=firefox
export DEFAULT_BROWSER=firefox

# Kiểm tra Sway (Khuyên dùng cho Kitty-OS 2.0 đa nhiệm 70/30)
if command -v sway &> /dev/null; then
    echo -e "\e[34m[*] Đang khởi chạy Kitty-OS 2.0 (Sway Tiling Desktop)...\e[0m"
    exec sway
elif command -v cage &> /dev/null; then
    echo -e "\e[33m[*] Sway chưa khả dụng, fallback về Cage Kiosk...\e[0m"
    exec cage -s -- kitty --start-as=fullscreen
else
    echo -e "\e[31m[!] Không tìm thấy Sway hoặc Cage.\e[0m"
    exit 1
fi
