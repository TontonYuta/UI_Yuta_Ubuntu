# 🎨 UI_Yuta - Custom GNOME Desktop & Boot Mode Suite

**UI_Yuta** là bộ đóng gói giao diện Desktop & cấu hình khởi động dành cho Ubuntu / GNOME Linux, giúp bạn dễ dàng khôi phục hoặc sao chép toàn bộ không gian làm việc đẹp mắt sang các máy tính khác chỉ với 1 thao tác.

---

## 🌟 Tổng Quan Giao Diện & Tính Năng (Features)

* **Chế độ khởi động mặc định (Boot Mode)**:
  * Khởi động máy ở giao diện dòng lệnh **CLI** (`multi-user.target`).
  * Khi cần sang GUI Desktop: chạy lệnh `sudo systemctl start gdm3`.
  * Khi muốn thoát GUI về CLI: chạy `sudo systemctl stop gdm3`.
* **GTK Theme**: `Sweet-Dark-v40` (Phong cách Dark Neon cá tính, hiện đại)
* **Icon Pack**: `candy-icons` (Bộ icon mượt mà, nhiều màu sắc rực rỡ)
* **Con trỏ chuột (Cursor)**: `WhiteSur-cursors` (Phong cách con trỏ macOS cao cấp)
* **Phông chữ (Typography)**:
  * Interface: `Inter 11`
  * Monospace / Code: `JetBrains Mono 10`
  * System Fonts: `SF Pro Display` & `SF Pro Text` (Apple Fonts)
* **Dock / Taskbar**:
  * Đặt ở đáy màn hình (Bottom Position)
  * Thiết kế trong suốt (Floating Transparent Dock)
* **Hiệu ứng & Extensions (GNOME Shell)**:
  * **Compiz Windows Effect**: Hiệu ứng Genie / Wobbly Windows khi thu nhỏ/phóng to cửa sổ
  * **Desktop Cube**: Chuyển đổi Workspace dạng khối 3D
  * **Burn My Windows**: Hiệu ứng đóng/mở cửa sổ
  * **Coverflow AltTab**: Chuyển đổi cửa sổ 3D
  * **Just Perfection & Quick Settings Tweaks**: Tối ưu thanh hệ thống gọn gàng

---

## 📦 Thành Phần Gói `UI_Yuta`

```text
UI_Yuta/
├── README.md               # Hướng dẫn chi tiết
├── install.sh              # Kịch bản tự động cài đặt 1-click & chọn boot mode
├── gnome_settings.dconf    # Toàn bộ cấu hình dconf / GSettings GNOME
├── background              # Tệp hình nền Desktop chuẩn
├── themes/                 # Thư mục chứa GTK Themes (Sweet-Dark, WhiteSur...)
├── icons/                  # Thư mục chứa Icon Packs & Cursors
├── fonts/                  # Bộ phông chữ SF Pro, Inter, JetBrains Mono
├── extensions/             # Toàn bộ GNOME Shell Extensions đã cài đặt
└── scripts/                # Kịch bản chuyển đổi CLI <-> GUI nhanh (switch-to-cli / switch-to-gui)
```

---

## 💻 Quản Lý Chế Độ Khởi Động CLI <-> GUI

### Từ giao diện CLI chuyển sang GUI:
```bash
sudo systemctl start gdm3
```

### Từ GUI quay lại CLI:
```bash
sudo systemctl stop gdm3
```

### Đổi chế độ boot mặc định khi bật máy:
* **Khởi động thẳng vào CLI**: `switch-to-cli.sh` (hoặc `sudo systemctl set-default multi-user.target`)
* **Khởi động thẳng vào GUI**: `switch-to-gui.sh` (hoặc `sudo systemctl set-default graphical.target`)

---

## 🚀 Hướng Dẫn Cài Đặt Sang Máy Mới (Installation)

### 1. Yêu cầu tiền đề (Prerequisites)
```bash
sudo apt update
sudo apt install -y dconf-cli gnome-tweaks gnome-shell-extension-prefs
```

### 2. Tiến hành cài đặt
Sao chép tệp `UI_Yuta.tar.gz` sang máy mới và mở Terminal chạy:

```bash
# Giải nén gói
tar -xzf UI_Yuta.tar.gz

# Chạy kịch bản cài đặt tự động
cd UI_Yuta
chmod +x install.sh
./install.sh
```

Trong quá trình chạy `install.sh`, kịch bản sẽ hỏi bạn muốn chọn chế độ khởi động mặc định khi bật máy là **CLI (Khuyên dùng)** hay **GUI (Thẳng Desktop)**.

---
*Tạo bởi Yuta - Nền tảng GNOME Customization Suite.*
