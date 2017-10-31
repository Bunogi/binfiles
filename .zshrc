autoload -U colors && colors

#powerline-daemon -q
PROMPT='%T %~ %? $ '
#. ~/pkgs/powerline/powerline/bindings/zsh/powerline.zsh
#source ~/pkgs/powerlevel9k/powerlevel9k.zsh-theme
#POWERLEVEL9K_PROMPT_ON_NEWLINE=true

setopt promptsubst

alias ls="ls --color=auto -F --si"
alias ll="ls -l"
alias gdb="gdb -q"
alias make="make -j5"
alias poweroff="shutdown -hP 0"

#export CXX=/usr/bin/clang++
#export CC=/usr/bin/clang

ttyctl -f

#export PATH=/home/bunogi/.gem/ruby/2.3.0/bin:/home/bunogi/bin:/home/bunogi/.local/bin:/home/bunogi/cargo/bin:/home/bunogi/go/bin:$PATH
export PAGER=less

zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle :compinstall filename '/home/bunogi/.zshrc'

autoload -Uz compinit
fpath+="~/.zfunc"
compinit
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=100000
SAVEHIST=10000000
# End of lines configured by zsh-newuser-install
#
bindkey "${terminfo[khome]}" beginning-of-line
bindkey "${terminfo[kend]}" end-of-line
bindkey  "${terminfo[kdch1]}"  delete-char
function zle-line-init () { echoti smkx }
		function zle-line-finish () { echoti rmkx }
		zle -N zle-line-init
		zle -N zle-line-finish
