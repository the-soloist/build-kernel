#!/usr/bin/env bash
# set -x

function pause() {
    read -n 1 -p "Press any key to continue..." INP
}

tty_size=($(stty size))
tty_width=${tty_size[1]}
# echo $(($tty_width - 100))

pane_number=$(tmux list-panes | wc -l)

if [[ $pane_number -lt 3 ]]; then
    tmux split -h -l $(($tty_width - 90)) # 2
    tmux select-pane -t 0
    tmux split -v # 1
fi

kill -9 $(pgrep qemu-system)
kill -9 $(pgrep gdb)

# make
tmux send-keys -t 1 "./start.sh" Enter
# pause
tmux send-keys -t 2 "./debug.sh" Enter
