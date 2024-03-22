# BatchRunner
A simple toolkit to help execute batch operations on cluster servers.

## Setup

Make sure you have [Python](https://www.python.org/downloads/) and [Sshpass](https://pkgs.org/download/sshpass/) (unnecessary if no encryption) installed.


## QuickStart

Run the `run.py`:

```bash
python run.py -i [hostfile] -c [commands]
```

The format of `hostfile`:
```shell
[IP]:[PORT]
```