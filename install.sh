#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "✨ Đang cài đặt giao diện UI_Yuta sang máy mới..."

# Tạo các thư mục đích
mkdir -p ~/.themes ~/.icons ~/.local/share/fonts ~/.local/share/gnome-shell/extensions ~/.config ~/.local/bin ~/.config/fcitx5 ~/.config/kitty ~/.config/fcitx5 ~/.config/kitty

# 1. Khôi phục Themes & Icons
echo "🎨 Đang khôi phục Themes & Icons..."
[ -d "$SCRIPT_DIR/themes" ] && cp -r "$SCRIPT_DIR/themes"/* ~/.themes/ 2>/dev/null || true
[ -d "$SCRIPT_DIR/icons" ] && cp -r "$SCRIPT_DIR/icons"/* ~/.icons/ 2>/dev/null || true

# 2. Khôi phục Fonts
echo "🔤 Đang khôi phục Fonts & cập nhật font cache..."
[ -d "$SCRIPT_DIR/fonts" ] && cp -r "$SCRIPT_DIR/fonts"/* ~/.local/share/fonts/ 2>/dev/null || true
fc-cache -f >/dev/null 2>&1 || true

# 3. Khôi phục Cấu hình (Terminal, Shell, Fcitx5)
echo "🔧 Đang khôi phục Terminal, Shell & Fcitx5..."
[ -d "$SCRIPT_DIR/configs/fcitx5" ] && cp -r "$SCRIPT_DIR/configs/fcitx5"/* ~/.config/fcitx5/ 2>/dev/null || true
[ -d "$SCRIPT_DIR/configs/kitty" ] && cp -r "$SCRIPT_DIR/configs/kitty"/* ~/.config/kitty/ 2>/dev/null || true
[ -d "$SCRIPT_DIR/home_configs" ] && cp -ra "$SCRIPT_DIR/home_configs"/. ~/ 2>/dev/null || true

# 4. Khôi phục Avatar (nếu có)
echo "👤 Đang khôi phục Avatar..."
[ -f "$SCRIPT_DIR/avatar/.face" ] && cp "$SCRIPT_DIR/avatar/.face" ~/.face || true
[ -f "$SCRIPT_DIR/avatar/.face" ] && sudo cp "$SCRIPT_DIR/avatar/.face" /var/lib/AccountsService/icons/$USER 2>/dev/null || true

# 5. Khôi phục Extensions
echo "🧩 Đang khôi phục GNOME Extensions..."
[ -d "$SCRIPT_DIR/extensions" ] && cp -r "$SCRIPT_DIR/extensions"/* ~/.local/share/gnome-shell/extensions/ 2>/dev/null || true

# 6. Khôi phục Hình nền
echo "🖼️ Đang khôi phục Hình nền..."
[ -f "$SCRIPT_DIR/background" ] && cp "$SCRIPT_DIR/background" ~/.config/background || true

# 7. Nạp cấu hình GSettings / dconf
if command -v dconf >/dev/null 2>&1; then
    echo "⚙️ Đang nạp dconf settings..."
    dconf load /org/gnome/ < "$SCRIPT_DIR/gnome_settings.dconf"
else
    echo "⚠️ Cảnh báo: 'dconf' chưa được cài đặt. Hãy cài đặt dconf-cli bằng: sudo apt install dconf-cli"
fi

# 8. Sao chép kịch bản chuyển đổi CLI <-> GUI vào ~/.local/bin
echo "🛠️ Đang cài đặt công cụ chuyển đổi CLI <-> GUI..."
[ -d "$SCRIPT_DIR/scripts" ] && cp "$SCRIPT_DIR/scripts"/*.sh ~/.local/bin/ 2>/dev/null || true

# Reload GNOME Shell Extensions list
echo "🔄 Bật các extensions..."
if command -v gnome-extensions >/dev/null 2>&1; then
    for ext in $(ls ~/.local/share/gnome-shell/extensions/); do
        gnome-extensions enable "$ext" 2>/dev/null || true
    done
fi

echo ""
echo "--------------------------------------------------------"
echo "🖥️ Cấu hình Chế độ khởi động (Boot Target Mode):"
echo "1) Mặc định boot vào CLI (Cần chạy 'sudo systemctl start gdm3' để lên GUI)"
echo "2) Mặc định boot vào GUI thẳng Desktop"
read -p "Lựa chọn chế độ boot mặc định (1 hoặc 2, mặc định là 1): " boot_choice

if [ "$boot_choice" = "2" ]; then
    echo "⚙️ Đang đặt mặc định boot vào GUI (graphical.target)..."
    sudo systemctl set-default graphical.target || true
else
    echo "⚙️ Đang đặt mặc định boot vào CLI (multi-user.target)..."
    sudo systemctl set-default multi-user.target || true
fi

echo "--------------------------------------------------------"
echo "✅ Hoàn tất! Vui lòng Đăng xuất (Log out) hoặc khởi động lại máy để áp dụng trọn vẹn."
