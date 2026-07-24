# ==============================================================================
# 1. CÁC LỆNH IN RA MÀN HÌNH (Phải đặt TRÊN Instant Prompt của P10k)
# ==============================================================================

# Chỉ hiển thị Fastfetch và Câu chào khi KHÔNG ở trong Tmux
if [[ -z "$TMUX" ]]; then
    fastfetch

    # Chọn ngẫu nhiên một câu chào lầy lội
    QUOTES=(
        "Dừng code bug nữa sếp ơi, em mệt lắm rồi! 🦖"
        "Nhớ uống nước và commit code thường xuyên nhé! 💧"
        "Lại một ngày nữa fix bug do chính mình tạo ra... 🤡"
        "Hệ thống đã sẵn sàng! 🚀"
        "Trời đánh tránh bữa code! Bắt đầu vào việc thôi! 💻"
    )
    RANDOM_QUOTE=${QUOTES[$RANDOM % ${#QUOTES[@]} ]}
    
    BATTERY=$(acpi 2>/dev/null | awk '{print $4}' | tr -d ',' || echo "100%")
    LOAD=$(cut -d' ' -f1 /proc/loadavg)

    # In ra khủng long màu xanh lá
    echo -e "\e[38;5;118m"
    echo "                __"
    echo "               / _)"
    echo "        _.----._/ /   $RANDOM_QUOTE"
    echo "       /         /    "
    echo "  __/ (  | (  |      CPU Load: $LOAD | Pin: $BATTERY"
    echo " /__.-'|_|--|_|     "
    echo -e "\e[0m"
fi

# ==============================================================================
# 2. KHỞI ĐỘNG POWERLEVEL10K INSTANT PROMPT
# ==============================================================================
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ==============================================================================
# 3. CẤU HÌNH GIAO DIỆN & PLUGINS
# ==============================================================================
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# Kích hoạt Plugins ZSH siêu tốc
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# ==============================================================================
# 4. ALIASES / PHÍM TẮT
# ==============================================================================
# Chuyển nhanh sang Windows bằng định danh chuỗi chuẩn xác của GRUB
alias towin='sudo grub-reboot "Windows Boot Manager (on /dev/nvme0n1p1)" && sudo reboot'
