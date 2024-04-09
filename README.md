# BatchRunner
A simple toolkit to help execute batch operations on cluster servers.

## Requirements

* [Python](https://www.python.org/downloads/) >= 2.7 
* [sshpass](https://pkgs.org/download/sshpass/) (unnecessary if no encryption)

## Usage

Start a cluster task
```
python run.py -c <COMMANDS> -p <PORT> -i <HOSTFILE> -k <KEY> -o <OUTPUT> -b -q
```
* `-c --commands`: Commands to be executed among all cluster servers, such as `pkill -f python`.

* `-p --port`: Default port of ssh services on cluster servers, default is `22`.

* `-i --hostfile`: IP file of cluster servers that commands will be executed on. The format of `hostfile` can refered [here](./hostfile) (`[IP]:[PORT]` per line). Default value is `localhost`.

* `-k --key`: Login passward for cluster servers. This action is unsafe and not recommended. [Sshpass](https://pkgs.org/download/sshpass/) is required here.

* `-o --output`: Path to save log info, default print to screen.

* `-b --background`：Execute commands in the background, defalut is `False` (blocking mode).

* `-q --quiet`: If set true, no log info produced, default is `False`.

Use `--help` flag to see more parameter options.

## QuickStart

1. Kill all python programs on all cluster servers in the background.
```bash
python run.py -i hostfile -c 'pkill -f python' -b
```
***Note***: `run.py` is also a python program, maybe killed by itself.

2. Show date of all cluster servers on screen.
```bash
python run.py -i hostfile -c 'date'
```

3. Record system information of all cluster servers in a file.
```bash
python run.py -i hostfile -c 'uname -a' -o './log/info.txt'
```

You can try more in practice.