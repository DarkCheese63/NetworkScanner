import nmap
import ipaddress
import time
import pyfiglet
from rich.console import Console
import random



scan_modes = { "stealth": "-sS", "aggressive": "-A", "fast": "-F", "os": "-O", "ping": "-sn", "version": "-sV", "default": "", "pingsubnet": "-sn", "noping": "-sL" }

screams = ["ahhhh", "ahhhhhhhh", "ahhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "ahhhhhhhhhhhhhhhhhhhhhhhhh", "ahhhhhhhhhhhhhhh", "ahhhhhhhhhh"]


def banner():
    console = Console()

    console.print("=" * 110 + "\n")

    # display the name of the project
    name = pyfiglet.figlet_format("Auto  Nmap", font="epic")
    console.print(f"[bold cyan]{name}[/bold cyan]")

    # display the options
    console.print(f"\n[bold]Please choose one of the following options:[/bold]")

    console.print("\n[italic]Stealth: Performs a SYN scan which starts the TCP handshake but doesnt finish it, making it harder to detect.[/italic]")
    console.print("\n[italic]Aggresive: Combines OS detection (-O), service versioning (-sV), script scanning (-sC), and traceroute.[/italic]")
    console.print("\n[italic]Fast: Scans only the top 100 most common ports.[/italic]")
    console.print("\n[italic]Version: Checks open ports to determine exactly what software and version is running.[/italic]")
    console.print("\n[italic]OS: Attempts to identify the target's operating system.[/italic]")
    console.print("\n[italic]Ping: Only checks if the host is alive, does not scan any ports.[/italic]")
    console.print("\n[italic]UDP: Specifically scans for UDP services like DNS, DHCP, or SNMP.[/italic]")

    console.print("\n[bold]Below are ping scans to discover active IP addresses on a network:[/bold]")
    console.print("\n[italic]PingSubnet: performs a ping scan on the subnet to list all live hosts.[/italic]")
    console.print("\n[italic]NoPing: lists all IP addresses in the subnet without pinging them.[/italic]")

    
    
    console.print("=" * 110 + "\n")



# helper module to check if the first input is a valid ip address
def is_valid_ip(ip_string):
    
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False
    

# helper module to scan ports
def scan(ip_address, flag, option):
    nm = nmap.PortScanner()
    
    if not flag:
        option = "default"
        flag = scan_modes.get(option.lower())
        print(f"Uknown option performing default scan")

    
        
    
    print(f"Starting {option} scan on IP: {ip_address}")
    nm.scan(ip_address, arguments=flag)



    print(f"\n--- Results for {ip_address} ---")

    if option == "pingsubnet" or option == "noping":
        hosts_list = nm.all_hosts()
        print(f"Found {len(hosts_list)} hosts:")
        for host in hosts_list:
            print(host)
        return
    
    # Print OS info if available
    if 'osmatch' in nm[ip_address] and len(nm[ip_address]['osmatch']) > 0:
        best_guess = nm[ip_address]['osmatch'][0] # Take the top result
        print(f"Probable OS: {best_guess['name']} ({best_guess['accuracy']}%)")
    
    # Print Version info (includes port info)
    if option == "version":
        for proto in nm[ip_address].all_protocols():
            for port in nm[ip_address][proto]:
                p_data = nm[ip_address][proto][port]
                print(f"Port {port}: {p_data['state']} | {p_data['name']} {p_data['product']} {p_data['version']}")

    # print Port info
    else:
        for proto in nm[ip_address].all_protocols():
                for port in nm[ip_address][proto]:
                    p_data = nm[ip_address][proto][port]
                    print(f"Port {port}: {p_data['state']}")


def end():
    choice = input ("Would you like to scan another host? ")
    if choice.lower() == "yes" or choice.lower() == "y":
        return True
    elif choice.lower() == "no" or choice.lower() == "n":
        print("Thank you for using AutoNmap!")
        return False
    else:
        print("you should have picked an option")
        time.sleep(1)
        while True:
            num = random.randint(0,5)
            print(screams[num])


def main():
    banner()

    # scan options 
    # stealth(-sS), aggressive(-A), fast(-F), version(-sV), os(-O), ping(-sn), udp(-sU)
    while True:
        scan_option = input ("Enter the chosen scan: ")

        flag = scan_modes.get(scan_option.lower())

        if scan_option == "pingsubnet":
            ip_address = input("Please input IP (ex: 192.168.1.0): ")
            if ip_address == "":
                ip_address = "192.168.1.0"
            if is_valid_ip(ip_address):
                subnet = input("Please input subnet: ")
                if subnet == "":
                    subnet = "24"
                new_ip = ip_address + "/" + subnet
                scan(new_ip, flag, scan_option)
                if end():
                    continue
                else:
                    break
            else:
                print("you must input a valid ip (ex: 192.168.1.0)")

        elif scan_option == "noping":
            ip_address = input("Please input IP (ex: 192.168.1.0): ")
            if ip_address == "":
                ip_address = "192.168.1.0"
            if is_valid_ip(ip_address):
                subnet = input("Please input subnet: ")
                new_ip = ip_address + "/" + subnet
                scan(new_ip, flag, scan_option)
                if end():
                    continue
                else:
                    break
            else:
                print("you must input a valid ip (ex: 192.168.1.0)")

        ip_address = input("Please input IP (ex: 192.168.1.0): ")

        # check if local host
        if ip_address.lower() == "localhost" or ip_address == "":
            ip_address = "127.0.0.1"
        
        if is_valid_ip(ip_address):
            scan(ip_address, flag, scan_option)
            if end():
                continue
            else:
                break
        else:
            print("IP address format incorrect try again.")

if __name__ == "__main__":
    main()