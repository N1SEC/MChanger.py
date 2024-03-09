"""
@Author: n1sec
"""
#!/usr/bin/python3

import sys, signal, time, argparse, subprocess
from colorama import init, Fore, Back, Style

def handler(sig, frame):
    print(Fore.YELLOW + "\n[!] Process interrupted..." + Style.RESET_ALL)
    sys.exit(1)

def mac_changer(mac, interface):
    print(Fore.GREEN + "\n[*] Changing MAC address....." + Style.RESET_ALL)
    time.sleep(2)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])
    ifconfig_output = subprocess.check_output(["ifconfig"]).decode("utf-8")
    new_mac = ifconfig_output.split()[17]
    print(Fore.GREEN + f"[*] New MAC: {new_mac}\n" + Style.RESET_ALL)
    
def restart_mac(restart):
    print(Fore.CYAN + "\n[+] Resetting MAC address..." + Style.RESET_ALL)
    time.sleep(2)
    subprocess.call(["ifconfig", restart, "down"])
    ethtool_output  = subprocess.check_output(["ethtool", "-P", restart]).decode("utf-8")
    mac_address = ethtool_output.split()[2]
    subprocess.call(["ifconfig", restart, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", restart, "up"])
    print(Fore.CYAN + f"[*] Default MAC: {mac_address}\n" + Style.RESET_ALL)

def main():
    signal.signal(signal.SIGINT, handler)
    parser = argparse.ArgumentParser(description="Script to modify the MAC address of localhost.")
    parser.add_argument("-i", "--interface", nargs="?", help="indicate the network interface.")
    parser.add_argument("-m", "--mac", nargs="?", help="indicate the MAC address.")
    parser.add_argument("-r", "--restart", nargs="?", help="Restores the default MAC address of localhost.")
    args = parser.parse_args()
    
    if args.mac and args.interface:
        mac_changer(args.mac, args.interface)
    
    elif args.restart:
        restart_mac(args.restart)
        
    else:
        parser.print_help()
        sys.exit()

if __name__=="__main__":
    main()
