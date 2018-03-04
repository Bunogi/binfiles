autoload -U colors && colors

PROMPT='$(zsh_prompt)'

function zsh_prompt() {
    echo '%F{red}%T%f | %F{yellow}%m%f | %F{green}%B%~%f%b'
    echo -n '%(?.%K{green}.%K{red}) '
    echo '%k %B%(!.%F{red}root #%f.$)%b: '
}

setopt promptsubst

alias ls="ls --color=auto -F --si"
alias ll="ls -l"
alias gdb="gdb -q"
alias make="make -j5"
alias poweroff="shutdown -hP 0"

ttyctl -f

export PAGER=less

zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle :compinstall filename '/home/bunogi/.zshrc'

autoload -Uz compinit
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=100000
SAVEHIST=10000000
# End of lines configured by zsh-newuser-install

bindkey "${terminfo[khome]}" beginning-of-line
bindkey "${terminfo[kend]}" end-of-line
bindkey  "${terminfo[kdch1]}"  delete-char

if [[ -n ${terminfo[smkx]} ]] && [[ -n ${terminfo[rmkx]} ]]; then
    function zle-line-init () { echoti smkx }
    function zle-line-finish () { echoti rmkx }

    zle -N zle-line-init
    zle -N zle-line-finish
fi
