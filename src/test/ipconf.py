import psutil

def find_adapter_by_mac(mac_address):
    for name, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.address.lower() == mac_address.lower():
                return name, address.address
    return None, None

# MAC 주소를 인자로 전달받아서 일치하는 네트워크 어댑터 찾기
def find_adapter_with_mac(mac_address):
    adapter_name, adapter_mac = find_adapter_by_mac(mac_address)
    if adapter_name:
        print("일치하는 네트워크 어댑터를 찾았습니다:")
        print("어댑터 이름:", adapter_name)
        print("MAC 주소:", adapter_mac)
    else:
        print("일치하는 네트워크 어댑터를 찾을 수 없습니다.")

# 예시: MAC 주소를 인자로 전달하여 해당 MAC 주소와 일치하는 네트워크 어댑터 찾기
target_mac_address =  "00-E0-4C-36-08-EA"
find_adapter_with_mac(target_mac_address)
