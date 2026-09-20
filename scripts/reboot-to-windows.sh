#!/bin/bash
# Script to reboot directly into Windows

# 1. Tìm tên chính xác của menu Windows trong file cấu hình GRUB
WINDOWS_ENTRY=$(grep -i "windows" /boot/grub/grub.cfg | grep "^menuentry" | head -n 1 | cut -d"'" -f2)

if [ -z "$WINDOWS_ENTRY" ]; then
    echo "Lỗi: Không tìm thấy hệ điều hành Windows trong menu GRUB!"
    exit 1
fi

echo "Đã tìm thấy Windows tại menu: $WINDOWS_ENTRY"
echo "Đang thiết lập khởi động vào Windows và Khởi động lại máy..."

# 2. Báo cho GRUB biết lần khởi động tới hãy boot vào Windows
grub-reboot "$WINDOWS_ENTRY"

# 3. Khởi động lại máy
reboot
