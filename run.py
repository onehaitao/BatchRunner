import argparse
import os
import re
import subprocess
import sys

py_version = sys.version_info.major

assert py_version == 3 or (py_version == 2 and sys.version_info.minor >= 7), \
    "Require Python >= 2.7, rather than Python {}.{}".format(py_version, sys.version_info.minor)

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
        "-k", "--key",
        default=None,
        type=str,
        help="use passward to login, unsafe and not recommended"
    )
    parser.add_argument(
        "-b", "--background",
        default=False,
        action="store_true",
        help="execute commands in the background"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        type=str,
        help="path to save log info, default print to screen"
    )
    parser.add_argument(
        "-q", "--quiet",
        default=False,
        action="store_true",
        help="if set true, no log info produced"
    )
    return parser.parse_args()


def is_host_format(s):
    format_pattern = r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])+)?$"
    if re.match(format_pattern, s):
        return True
    return False

def get_hosts(hostfile, port):
    hosts = []
    if hostfile is None or not os.path.exists(hostfile):
        return hosts
    hostfile = os.path.abspath(hostfile)

    with open(hostfile, "r") as fr:
        for line in fr:
            line = line.strip()
            if not is_host_format(line):
                print("{} is an invalid item in hostfile!".format(line))
                continue
            line = line.split(":")
            if len(line) == 1:
                hosts.append((line[0].strip(), port))
            else:
                hosts.append((line[0].strip(), int(line[1].strip())))
    return hosts

def print_cmd(host, cmd, fh=None):
    cmd_info = "\n{:-^50}\n{}\n{}\n".format(" run on " + host + " ", cmd, "-"*50)
    print(cmd_info)
    if fh:
        fh.write(cmd_info + "\n")
        fh.flush()

def generate_cmds(cmds, hosts, args):
    ssh_cmds = []
    if not hosts:
        ssh_cmd = cmds
        ssh_cmds.append(ssh_cmd)
        hosts.append(("localhost", args.port))
    else:
        for host, port in hosts:
            ssh_cmd = "ssh -p {} {} -o StrictHostKeyChecking=no -q '{}'".format(str(port), host, cmds)
            if args.key:
                ssh_cmd = "sshpass -p '{}' {}".format(args.key, ssh_cmd)
            ssh_cmds.append(ssh_cmd)
    return ssh_cmds

def execute_cmds(ssh_cmds, hosts, args):
    if args.output and not args.quiet:
        filedir = os.path.dirname(os.path.abspath(args.output))
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        fh = open(args.output, "w")
    else:
        fh = None
    for i, ssh_cmd in enumerate(ssh_cmds):
        if args.background:
            ssh_cmd = "({}) &".format(ssh_cmd)
        print_cmd(hosts[i][0], ssh_cmd, fh)
        if args.quiet:
            stdout = subprocess.PIPE
            stderr = subprocess.STDOUT
        else:
            stdout = fh
            stderr = fh
        proc = subprocess.Popen(ssh_cmd, shell=True, stdout=stdout, stderr=stderr)
        proc.wait()

    if fh:
        fh.close()

def main():
    args = parse_args()
    hosts = get_hosts(args.hostfile, args.port)
    ssh_cmds = generate_cmds(args.commands, hosts, args)
    execute_cmds(ssh_cmds, hosts, args)

if __name__ == "__main__":
    main()
