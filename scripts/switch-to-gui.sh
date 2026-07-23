#!/usr/bin/env bash
echo "🖼️ Đang chuyển chế độ khởi động mặc định sang GUI (Desktop Mode)..."
sudo systemctl set-default graphical.target
echo "✅ Đã đặt mặc định khởi động vào GUI (graphical.target)."
