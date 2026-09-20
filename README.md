# 🎨 UI_Yuta - Custom GNOME Desktop & Terminal Suite (Ubuntu 26.04)

**UI_Yuta** là bộ đóng gói giao diện Desktop & cấu hình khởi động, Terminal và tiện ích hệ thống cao cấp dành cho Ubuntu / GNOME Linux, giúp bạn dễ dàng đồng bộ, khôi phục hoặc sao chép toàn bộ không gian làm việc đẹp mắt sang các máy tính khác chỉ với 1 thao tác.

---

## 🌟 Tổng Quan Giao Diện & Tính Năng (Features)

* **Chế độ khởi động mặc định (Boot Mode)**:
  * Khởi động máy ở giao diện dòng lệnh **CLI** (`multi-user.target`).
  * Khi cần sang GUI Desktop: chạy lệnh `gui` (tự động khởi chạy GDM3 và dọn dẹp TTY session).
  * Khi muốn thoát GUI về CLI: chạy lệnh `cli` (hoặc `sudo systemctl stop gdm3`).
* **GTK Theme**: `WhiteSur-Dark` (Phong cách macOS tối tân, thanh lịch và mượt mà)
* **Shell Theme**: `YutaGlass` (Giao diện Shell kính mờ bóng bẩy, hiện đại)
* **Icon Pack**: `candy-icons` & `WhiteSur` (Bộ icon mượt mà, rực rỡ và sắc nét)
* **Con trỏ chuột (Cursor)**: `WhiteSur-cursors` (Phong cách con trỏ macOS cao cấp)
* **Phông chữ (Typography)**:
  * Interface: `Inter 11`
  * Monospace / Code: `JetBrains Mono 10`
  * Vietnamese & Content: `BeVietnam Pro`
  * Apple Typography: `SF Pro Display`, `SF Pro Text`, `SF Pro Rounded`, `SF Mono`
  * UI Fonts: `Roboto`
* **Hiệu ứng & Extensions (GNOME Shell)**:
  * **Blur my Shell**: Hiệu ứng kính mờ (blur) trong suốt thời thượng cho Top Panel, Dash và màn hình khóa
  * **Compiz Windows Effect**: Hiệu ứng Genie / Wobbly Windows chuyển động uyển chuyển
  * **Desktop Cube**: Chuyển đổi Workspace dạng khối hộp 3D xoay vòng
  * **Burn My Windows**: Hiệu ứng đóng/mở cửa sổ nghệ thuật
  * **Coverflow AltTab**: Chuyển đổi ứng dụng dạng 3D coverflow
  * **Vitals**: Giám sát phần cứng (CPU, GPU, RAM, Nhiệt độ, Network) trực tiếp trên Top Bar
  * **Media Controls**: Hiển thị tên bài hát và nút điều khiển media trên Panel
  * **Just Perfection**: Tinh chỉnh và tối ưu hóa chi tiết GNOME Shell
  * **RunCat**: Hoạt họa mèo chạy theo mức tải CPU
  * **Date Menu Formatter**: Tùy biến định dạng đồng hồ hệ thống
* **Terminal & Shell Suite**:
  * **Kitty**: Cấu hình Kitty Terminal hiệu năng cao, hỗ trợ tab bar tùy biến (`tab_bar.py`)
  * **Zsh & Powerlevel10k**: Shell thông minh với gợi ý lệnh (`zsh-autosuggestions`), tô màu (`zsh-syntax-highlighting`), OSC 7 đồng bộ thư mục làm việc và theme Tokyo Night
  * **Tmux Tokyo Night**: Bảng trạng thái hiển thị chi tiết, phím tắt điều hướng nhanh, popup trợ giúp và chế độ sao chép Vim
  * **Fastfetch**: Bảng thông tin hệ thống gọn gàng, đẹp mắt
  * **Conky & Cava**: Widget màn hình hiển thị đồng hồ kính mờ & visualizer sóng nhạc trên terminal
  * **Kịch bản hệ thống**: Lệnh chuyển đổi GUI (`gui`), khởi động nhanh sang Windows (`towin`), trình đọc PDF trên terminal (`kitty-pdf`), chỉnh âm lượng (`kitty-volume`), cheatsheet phím tắt (`kitty-help`)

---

## 📦 Thành Phần Gói `UI_Yuta`

```text
UI_Yuta/
├── README.md               # Hướng dẫn chi tiết
├── install.sh              # Kịch bản tự động cài đặt 1-click & chọn boot mode
├── gnome_settings.dconf    # Toàn bộ cấu hình dconf / GSettings GNOME
├── background              # Tệp hình nền Desktop chuẩn (Qimono Drop)
├── avatar/                 # Ảnh đại diện tài khoản (.face)
├── themes/                 # Thư mục chứa GTK Themes (WhiteSur-Dark) & Shell Theme (YutaGlass)
├── icons/                  # Thư mục chứa Icon Packs (candy-icons, WhiteSur) & Cursors
├── fonts/                  # Bộ phông chữ Inter, JetBrains Mono, BeVietnam Pro, SF Pro, Roboto
├── extensions/             # Toàn bộ GNOME Shell Extensions đã cài đặt và cấu hình
├── scripts/                # Kịch bản tiện ích (gui, reboot-to-windows, kitty-help, v.v.)
├── configs/                # Cấu hình phần mềm (Kitty, Fcitx5, Fastfetch, Conky, Cava)
└── home_configs/           # Cấu hình cá nhân (.bashrc, .zshrc, .p10k.zsh, .tmux, .tmux.conf)
```

---

## 💻 Quản Lý Chế Độ Khởi Động CLI <-> GUI

### Từ giao diện CLI chuyển sang GUI:
```bash
gui
# hoặc
sudo systemctl start gdm3
```

### Từ GUI quay lại CLI:
```bash
cli
# hoặc
sudo systemctl stop gdm3
```

### Chuyển nhanh sang Windows (Dual Boot):
```bash
towin
# hoặc chạy trực tiếp script: reboot-to-windows.sh
```

---

## 🚀 Hướng Dẫn Cài Đặt Sang Máy Mới (Installation)

### 1. Yêu cầu tiền đề (Prerequisites)
```bash
sudo apt update
sudo apt install -y dconf-cli gnome-tweaks gnome-shell-extension-prefs git curl
```

### 2. Tiến hành cài đặt
Clone kho lưu trữ hoặc giải nén gói:

```bash
git clone https://github.com/TontonYuta/UI_Yuta_Ubuntu.git
cd UI_Yuta_Ubuntu
chmod +x install.sh
./install.sh
```

Trong quá trình chạy `install.sh`, kịch bản sẽ hỏi bạn muốn chọn chế độ khởi động mặc định khi bật máy là **CLI (Khuyên dùng)** hay **GUI (Thẳng Desktop)**.

---
*Bản quyền cấu hình & tùy biến bởi Yuta.*
