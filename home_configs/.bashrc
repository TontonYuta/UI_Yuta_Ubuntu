# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

. "$HOME/.local/bin/env"


# Added by Antigravity CLI installer
export PATH="/home/tontonyuta/.local/bin:$PATH"

# ==============================================================================
# 🚀 YUTA CLI SUITE - CUSTOM ALIASES
# ==============================================================================
alias c='clear'
alias cls='clear'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
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
alias widget='~/.local/bin/conky-toggle.sh'
alias vinyl='desktop-music-player &'
alias cava='~/.local/bin/cava'
alias ports='ss -tulpn'
alias myip='curl -s ifconfig.me && echo ""'
alias mem='free -h'
alias disk='df -h -x tmpfs -x devtmpfs'
alias kitty-help='python3 ~/.local/bin/kitty-help'
alias help-kitty='python3 ~/.local/bin/kitty-help'
alias kitty-os-help='python3 ~/.local/bin/kitty-help'
alias cheatsheet='python3 ~/.local/bin/kitty-help'
# --- Trình đọc & Quản lý Tài Liệu PDF (Tokyo Night) ---
alias pdf='kitty-pdf'
alias pdf-open='kitty-pdf'
alias pdf-view='kitty-pdf-view'
alias pdf-find='kitty-pdf -s'
alias pdf-recent='kitty-pdf -r'

export BROWSER=firefox
export DEFAULT_BROWSER=firefox
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate --all'
export PATH="/home/tontonyuta/.local/bin:$PATH"
