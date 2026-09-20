import os
import subprocess
import threading
import time
from datetime import datetime
from kitty.fast_data_types import Screen, add_timer, get_boss, wcswidth
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_tab_with_powerline,
)

# ==========================================
# 🎨 TOKYO NIGHT COLOR PALETTE
# ==========================================
C_BG = as_rgb(0x1a1b26)          # Tab bar background (#1a1b26)
C_SURFACE = as_rgb(0x1f2335)     # Pill surface background (#1f2335)
C_FOREGROUND = as_rgb(0xc0caf5)  # Light foreground text (#c0caf5)
C_MUTED = as_rgb(0x565f89)       # Muted gray text (#565f89)
C_BLUE = as_rgb(0x7aa2f7)        # Tokyo Night Blue (#7aa2f7)
C_CYAN = as_rgb(0x7dcfff)        # Tokyo Night Cyan (#7dcfff)
C_GREEN = as_rgb(0x9ece6a)       # Tokyo Night Green (#9ece6a)
C_YELLOW = as_rgb(0xe0af68)      # Tokyo Night Yellow (#e0af68)
C_RED = as_rgb(0xf7768e)         # Tokyo Night Red (#f7768e)
C_MAGENTA = as_rgb(0xbb9af7)     # Tokyo Night Purple (#bb9af7)
C_DARK = as_rgb(0x15161e)        # Tokyo Night Dark (#15161e)

# ==========================================
# 📶 NETWORK STATUS (Async Cache)
# ==========================================
_cached_net_icon = "󰤮"
_cached_net_text = "Offline"
_cached_net_color = C_MUTED
_last_net_check = 0.0
_net_lock = threading.Lock()

def _update_net_info():
    global _cached_net_icon, _cached_net_text, _cached_net_color
    try:
        res = subprocess.run(
            ["nmcli", "-t", "-f", "TYPE,NAME", "con", "show", "--active"],
            capture_output=True,
            text=True,
            timeout=1.0,
        )
        lines = res.stdout.strip().splitlines()
        wifi_ssid = None
        eth_name = None
        for line in lines:
            if ":" in line:
                t, n = line.split(":", 1)
                if t in ("802-11-wireless", "wifi"):
                    wifi_ssid = n
                    break
                elif t in ("802-3-ethernet", "ethernet"):
                    eth_name = n

        with _net_lock:
            if wifi_ssid:
                if len(wifi_ssid) > 14:
                    wifi_ssid = wifi_ssid[:13] + "…"
                _cached_net_icon = "󰤨"
                _cached_net_text = wifi_ssid
                _cached_net_color = C_CYAN
            elif eth_name:
                if len(eth_name) > 14:
                    eth_name = eth_name[:13] + "…"
                _cached_net_icon = "󰈀"
                _cached_net_text = eth_name
                _cached_net_color = C_BLUE
            else:
                _cached_net_icon = "󰤮"
                _cached_net_text = "Offline"
                _cached_net_color = C_MUTED
    except Exception:
        with _net_lock:
            _cached_net_icon = "󰤮"
            _cached_net_text = "Offline"
            _cached_net_color = C_MUTED

def get_network_info():
    global _last_net_check
    now = time.time()
    if now - _last_net_check > 4.0:
        _last_net_check = now
        threading.Thread(target=_update_net_info, daemon=True).start()
    with _net_lock:
        return _cached_net_icon, _cached_net_text, _cached_net_color

# Initial network fetch
_update_net_info()

# ==========================================
# 🔋 BATTERY STATUS (Instant Direct Read)
# ==========================================
def get_battery_info():
    try:
        power_path = "/sys/class/power_supply"
        if not os.path.exists(power_path):
            return None
        bat_dirs = [d for d in os.listdir(power_path) if d.startswith("BAT")]
        if not bat_dirs:
            return None
        bat_dir = os.path.join(power_path, sorted(bat_dirs)[0])

        with open(os.path.join(bat_dir, "capacity"), "r") as f:
            capacity = int(f.read().strip())
        with open(os.path.join(bat_dir, "status"), "r") as f:
            status = f.read().strip()

        if status == "Charging":
            icon = "󰂄"
            color = C_GREEN
        elif status == "Full":
            icon = "󰁹"
            color = C_GREEN
        else:
            if capacity >= 85:
                icon = "󰁹"
                color = C_GREEN
            elif capacity >= 60:
                icon = "󰁾"
                color = C_GREEN
            elif capacity >= 35:
                icon = "󰁼"
                color = C_YELLOW
            elif capacity >= 15:
                icon = "󰁺"
                color = C_YELLOW
            else:
                icon = "󰂃"
                color = C_RED

        return icon, f"{capacity}%", color
    except Exception:
        return None

# ==========================================
# 🔊 AUDIO / VOLUME STATUS (Async Cache)
# ==========================================
_cached_vol_icon = "󰕾"
_cached_vol_text = "--%"
_cached_vol_color = C_MAGENTA
_last_vol_check = 0.0
_vol_lock = threading.Lock()

def _update_vol_info():
    global _cached_vol_icon, _cached_vol_text, _cached_vol_color
    try:
        res = subprocess.run(
            ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
            capture_output=True,
            text=True,
            timeout=0.8,
        )
        parts = res.stdout.strip().split()
        if len(parts) >= 2 and parts[0] == "Volume:":
            vol_val = int(round(float(parts[1]) * 100))
            is_muted = "[MUTED]" in res.stdout
            with _vol_lock:
                if is_muted or vol_val == 0:
                    _cached_vol_icon = "󰝟"
                    _cached_vol_text = "Mute"
                    _cached_vol_color = C_RED
                elif vol_val >= 50:
                    _cached_vol_icon = "󰕾"
                    _cached_vol_text = f"{vol_val}%"
                    _cached_vol_color = C_MAGENTA
                elif vol_val >= 15:
                    _cached_vol_icon = "󰖀"
                    _cached_vol_text = f"{vol_val}%"
                    _cached_vol_color = C_MAGENTA
                else:
                    _cached_vol_icon = "󰕿"
                    _cached_vol_text = f"{vol_val}%"
                    _cached_vol_color = C_YELLOW
    except Exception:
        pass

def get_volume_info():
    global _last_vol_check
    now = time.time()
    if now - _last_vol_check > 1.5:
        _last_vol_check = now
        threading.Thread(target=_update_vol_info, daemon=True).start()
    with _vol_lock:
        return _cached_vol_icon, _cached_vol_text, _cached_vol_color

# Initial volume fetch
_update_vol_info()

# ==========================================
# ⏰ TIME / DATE STATUS
# ==========================================
def get_time_info():
    now = datetime.now()
    return "", now.strftime("%H:%M"), C_BLUE

# ==========================================
# 🔄 AUTO-REFRESH TIMER (Every 2 seconds)
# ==========================================
_timer_initialized = False

def _timer_callback(timer_id):
    boss = get_boss()
    if boss:
        boss.refresh_active_tab_bar()

def _init_timer():
    global _timer_initialized
    if not _timer_initialized:
        _timer_initialized = True
        try:
            add_timer(_timer_callback, 2.0, True)
        except Exception:
            pass

_init_timer()

# ==========================================
# 🖼️ DRAW RIGHT STATUS CAPSULES
# ==========================================
def draw_right_status(draw_data: DrawData, screen: Screen, tab_end: int) -> None:
    default_bg = as_rgb(int(draw_data.default_bg))

    # Gather widget items: (icon, icon_fg, text, text_fg, cap_bg)
    widgets = []

    # 1. Wifi / Network
    net_icon, net_text, net_color = get_network_info()
    widgets.append((net_icon, net_color, net_text, C_FOREGROUND, C_SURFACE))

    # 2. Volume / Audio (Kitty-OS 2.0 Audio Widget)
    vol_icon, vol_text, vol_color = get_volume_info()
    widgets.append((vol_icon, vol_color, vol_text, C_FOREGROUND, C_SURFACE))

    # 3. Battery (if present)
    bat = get_battery_info()
    if bat:
        bat_icon, bat_text, bat_color = bat
        widgets.append((bat_icon, bat_color, bat_text, C_FOREGROUND, C_SURFACE))

    # 3. Time
    time_icon, time_text, time_color = get_time_info()
    # Time pill with Tokyo Blue background for accent
    widgets.append((time_icon, C_DARK, time_text, C_DARK, C_BLUE))

    def calc_width(widget_list):
        # 1 (left ) + icon + 1 (space) + text + 1 (right )
        caps_width = sum(1 + wcswidth(w[0]) + 1 + wcswidth(w[2]) + 1 for w in widget_list)
        spaces_width = len(widget_list)  # (n-1) spaces between + 1 trailing margin
        return caps_width + spaces_width

    # Responsive fallback: drop wifi if space is tight
    while widgets and (screen.columns - calc_width(widgets) <= tab_end + 2):
        if len(widgets) > 1:
            widgets.pop(0)  # Drop leftmost widget (Network first)
        else:
            widgets.clear()
            break

    if not widgets:
        return

    total_width = calc_width(widgets)
    start_x = screen.columns - total_width
    screen.cursor.x = start_x

    for idx, (icon, icon_fg, text, text_fg, cap_bg) in enumerate(widgets):
        # Left round edge
        screen.cursor.bg = default_bg
        screen.cursor.fg = cap_bg
        screen.draw("")

        # Icon
        screen.cursor.bg = cap_bg
        screen.cursor.fg = icon_fg
        screen.draw(f"{icon} ")

        # Text
        screen.cursor.fg = text_fg
        screen.draw(text)

        # Right round edge
        screen.cursor.bg = default_bg
        screen.cursor.fg = cap_bg
        screen.draw("")

        # Space between capsules
        if idx < len(widgets) - 1:
            screen.cursor.bg = default_bg
            screen.draw(" ")

    # Trailing space margin
    screen.cursor.bg = default_bg
    screen.draw(" ")

# ==========================================
# 🎯 MAIN CUSTOM TAB DRAW FUNCTION
# ==========================================
def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_tab_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    end = draw_tab_with_powerline(
        draw_data,
        screen,
        tab,
        before,
        max_tab_length,
        index,
        is_last,
        extra_data,
    )
    if is_last:
        draw_right_status(draw_data, screen, end)
    return end
