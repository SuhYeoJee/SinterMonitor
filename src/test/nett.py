import subprocess
import re

def find_network_adapter(target_mac_address):
    # Execute PowerShell command to get network adapter information
    powershell_command = f'Get-NetAdapter | Select-Object -Property MacAddress, InterfaceAlias'
    result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)

    # Parse the output to find the matching adapter
    if result.returncode == 0:
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            match = re.match(r'\s*(\S+)\s+(.*)', line)
            if match:
                mac_address = match.group(1)
                interface_alias = match.group(2)
                if mac_address.lower() == target_mac_address.lower():
                    return interface_alias.strip()  # Return interface alias (name)
    return None

# Example usage:
target_mac_address = "00-50-56-C0-00-08"  # Enter the MAC address you want to find here
matching_interface = find_network_adapter(target_mac_address)
if matching_interface:
    print("일치하는 네트워크 인터페이스를 찾았습니다:")
    print(matching_interface)
else:
    print("일치하는 네트워크 인터페이스를 찾을 수 없습니다.")
