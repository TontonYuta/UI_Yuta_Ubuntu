#!/usr/bin/env bash
echo "🖥️ Đang chuyển chế độ khởi động mặc định sang CLI (Text Mode)..."
sudo systemctl set-default multi-user.target
echo "✅ Đã đặt mặc định khởi động vào CLI (multi-user.target)."
echo "💡 Để khởi động giao diện đồ họa GUI khi đang ở CLI, chạy: sudo systemctl start gdm3"
