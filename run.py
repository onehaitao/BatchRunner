import argparse
import os
import re
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Batch Runner")
    parser.add_argument(
        "-c", "--commands",
        required=True,
        type=str,
        help="commands to be executed"
    )
    parser.add_argument(
        "-p", "--port",
        default=22,
        type=int,
        help="ssh port",
    )
    parser.add_argument(
        "-i", "--hostfile",
        default=None,
        type=str,
        help="servers, defalut local"
    )
    parser.add_argument(
        '-k', '--key',
        default=None,
        type=str,
        help='use passward to login, unsafe and not recommended'
    )
    parser.add_argument(
        "-b", "--background",
        default=False,
        action="store_true",
        help="execute commands in the background"
    )
    return parser.parse_args()


def is_host_format(s):
    format_pattern = r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])+)?"
    if re.fullmatch(format_pattern, s):
        return True
    return False

def get_hosts(hostfile, port):
    hosts = []
    if hostfile is None or not os.path.exists(hostfile):
        return hosts
    hostfile = os.path.abspath(hostfile)

    with open(hostfile, "r", encoding="utf-8") as fr:
        for line in fr:
            line = line.strip()
            if not is_host_format(line):
                print(f"{line} is an invalid item in hostfile!")
                continue
            line = line.split(":")
            if len(line) == 1:
                hosts.append((line[0].strip(), port))
            else:
                hosts.append((line[0].strip(), int(line[1].strip())))
    return hosts

def print_cmd(host, cmd):
    print(f"\n{ 'run on ' + host + ' ':-^40}\n{cmd}\n{'-'*40}\n")

def generate_cmds(cmds, hosts, key):
    ssh_cmds = []
    if not hosts:
        ssh_cmd = cmds
        ssh_cmds.append(ssh_cmd)
    else:
        for host, port in hosts:
            ssh_cmd = f"ssh -p {str(port)} {host} -o StrictHostKeyChecking=no -q '{cmds}'"
            if key:
                ssh_cmd = f"sshpass -p {key} {ssh_cmd}"
            ssh_cmds.append(ssh_cmd)
    return ssh_cmds

def execute_cmds(ssh_cmds, hosts, args):
    for i, ssh_cmd in enumerate(ssh_cmds):
        if args.background:
            ssh_cmd = f"({ssh_cmd}) &"
        print_cmd(hosts[i][0], ssh_cmd)
        subprocess.run(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def main():
    args = parse_args()
    hosts = get_hosts(args.hostfile, args.port)
    print(hosts)
    ssh_cmds = generate_cmds(args.commands, hosts, args.key)
    execute_cmds(ssh_cmds, hosts, args)

if __name__ == "__main__":
    main()
