import psutil
import socket
import subprocess

def get_ip_by_mac(target_mac):
    """
    주어진 MAC 주소와 일치하는 네트워크 인터페이스의 IP 주소를 반환합니다.
    
    매개변수:
    target_mac (str): 확인할 대상 MAC 주소 (예: '00:1A:2B:3C:4D:5E').
    
    반환값:
    tuple: (인터페이스 이름, IP 주소). 일치하는 인터페이스가 없으면 (None, None)을 반환합니다.
    """
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                if addr.address.lower() == target_mac.lower():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            return interface, addr.address
    return None, None

def set_ip_address(interface_name, new_ip):
    """
    주어진 네트워크 인터페이스의 IP 주소를 새로운 IP 주소로 설정합니다.
    
    매개변수:
    interface_name (str): 네트워크 인터페이스 이름 (예: 'Ethernet').
    new_ip (str): 설정할 새로운 IP 주소 (예: '192.168.0.142').
    """
    try:
        # Windows에서 netsh 명령어를 사용하여 IP 주소를 변경합니다.
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface_name, 'static', new_ip, '255.255.255.0'], check=True)
        print(f"인터페이스 {interface_name}의 IP 주소가 {new_ip}(으)로 변경되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"IP 주소 변경에 실패했습니다: {e}")
        return False

def check_and_set_ip(target_mac, target_ip):
    """
    주어진 MAC 주소와 일치하는 네트워크 인터페이스의 IP 주소를 확인하고, 일치하지 않으면 IP 주소를 변경합니다.
    
    매개변수:
    target_mac (str): 확인할 대상 MAC 주소 (예: '00:1A:2B:3C:4D:5E').
    target_ip (str): 설정할 대상 IP 주소 (예: '192.168.0.142').
    """
    interface, current_ip = get_ip_by_mac(target_mac)
    if interface is None:
        print("일치하는 MAC 주소를 찾을 수 없습니다.")
    elif current_ip == target_ip:
        print(f"현재 IP 주소 {current_ip}가 {target_ip}와 일치합니다.")
        return True
    else:
        print(f"현재 IP 주소 {current_ip}가 {target_ip}와 일치하지 않습니다. IP 주소를 변경합니다.")
        return set_ip_address(interface, target_ip)

# 사용 예시:
# 확인할 MAC 주소와 설정할 IP 주소를 지정합니다.
target_mac = '00-50-56-C0-00-08'
target_ip = '192.168.0.142'

# 주어진 MAC 주소와 일치하는 네트워크 인터페이스의 IP 주소를 확인하고, 일치하지 않으면 IP 주소를 변경합니다.
# check_and_set_ip(target_mac, target_ip)


print(get_ip_by_mac(target_mac))