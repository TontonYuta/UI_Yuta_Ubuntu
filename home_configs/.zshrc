# ==============================================================================
# 🚀 ZSH TERMINAL SUITE - YUTA AESTHETIC EDITION
# ==============================================================================

# 1. Khởi động Powerlevel10k Instant Prompt (Đặt đầu tiên để khởi động tức thì)
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# 2. Hiển thị Thông số khi mở Shell
if [[ -o interactive ]]; then
    if [[ -z "$TMUX" ]]; then
        fastfetch
    else
        # Khi ở trong Tmux hoặc Kitty-OS, hiển thị thông báo mở bảng hướng dẫn
        echo -e "\e[38;2;122;162;247m💡 \e[1;38;2;224;175;104mBảng hướng dẫn Kitty-OS & Tmux:\e[0m \e[38;2;125;207;255mbấm \e[1mSuper+F1\e[0m \e[38;2;125;207;255m(Sway) • \e[1mCtrl+a ?\e[0m \e[38;2;125;207;255m(Tmux) • gõ \e[1mkitty-help\e[0m\e[0m"
    fi
fi

# 3. Kích hoạt Theme Powerlevel10k
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# 4. Kích hoạt ZSH Plugins (Tự động gợi ý lệnh & Tô màu cú pháp siêu tốc)
[[ -f ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
[[ -f ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# ==============================================================================
# 5. ALIASES & TIỆN ÍCH ĐỈNH CAO
# ==============================================================================

# --- Điều hướng & Quản lý File ---
alias c='clear'
alias cls='clear'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# --- Quản trị Hệ Thống & Chế Độ Boot ---
alias update='sudo apt update && sudo apt upgrade -y'
gui() {
    echo -e "\e[38;2;122;162;247m[*] Đang khởi động GDM3 và chuyển sang GUI...\e[0m"
    sudo systemctl start gdm3
    local cur_tty
    cur_tty=$(tty 2>/dev/null)
    if [[ "$cur_tty" =~ ^/dev/tty[0-9]+ ]]; then
        echo -e "\e[38;2;224;175;104m[*] Đang đăng xuất và dọn dẹp phiên TTY ($cur_tty)...\e[0m"
        local sid
        sid=$(cat /proc/self/sessionid 2>/dev/null || echo "$XDG_SESSION_ID")
        if [[ -n "$sid" && "$sid" != "4294967295" ]]; then
            loginctl terminate-session "$sid" 2>/dev/null
        fi
        exit 0
    fi
}
alias cli='sudo systemctl stop gdm3'
alias kitty-os='~/launch-kitty.sh'
alias start-kitty='~/launch-kitty.sh'
alias towin='sudo grub-reboot "Windows Boot Manager (on /dev/nvme0n1p1)" && sudo reboot'
alias customizer='python3 ~/.local/share/system-customizer/main.py &'
alias ports='ss -tulpn'
alias myip='curl -s ifconfig.me && echo ""'
alias mem='free -h'
alias disk='df -h -x tmpfs -x devtmpfs'

# --- Tmux & Bảng Hướng Dẫn Phím Tắt ---
alias kitty-help='python3 ~/.local/bin/kitty-help'
alias help-kitty='python3 ~/.local/bin/kitty-help'
alias kitty-os-help='python3 ~/.local/bin/kitty-help'
alias cheatsheet='python3 ~/.local/bin/kitty-help'
alias tmux-help='python3 ~/.local/bin/kitty-help'
alias help-tmux='python3 ~/.local/bin/kitty-help'

# --- Trình đọc & Quản lý Tài Liệu PDF (Tokyo Night) ---
alias pdf='kitty-pdf'
alias pdf-open='kitty-pdf'
alias pdf-view='kitty-pdf-view'
alias pdf-find='kitty-pdf -s'
alias pdf-recent='kitty-pdf -r'

# --- Trình duyệt mặc định ---
export BROWSER=firefox
export DEFAULT_BROWSER=firefox

# --- Tiện Ích Âm Nhạc & Desktop Widgets ---
alias widget='~/.local/bin/conky-toggle.sh'
alias vinyl='desktop-music-player &'
alias cava='~/.local/bin/cava'
alias volume='kitty-volume'
alias vol='kitty-volume'

# --- Git Shortcuts ---
alias gs='git status'
alias ga='git add'
alias gaa='git add -A'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate --all'

# ==============================================================================
# 6. OSC 7 - TỰ ĐỘNG ĐỒNG BỘ LINK THƯ MỤC CHO KITTY & TMUX
# ==============================================================================
autoload -Uz add-zsh-hook
update_cwd_osc7() {
    printf "\e]7;file://%s%s\e\\" "${HOSTNAME:-$HOST}" "${PWD}"
}
add-zsh-hook chpwd update_cwd_osc7
update_cwd_osc7

# ==============================================================================
# 7. PATH & ENVIRONMENT
# ==============================================================================
[[ -f "$HOME/.local/bin/env" ]] && . "$HOME/.local/bin/env"
export PATH="/home/tontonyuta/.local/bin:$PATH"
