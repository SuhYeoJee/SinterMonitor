def change_ip(adapter_name):
    import subprocess
    try:
        # netsh 명령어를 실행하여 IP 주소 변경
        cmd = f'netsh interface ip set address name="{adapter_name}" static 192.168.0.200 255.255.255.0 192.168.1.1'
        subprocess.run(cmd, shell=True, check=True)
        print("네트워크 인터페이스의 IP 주소가 성공적으로 변경되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")

change_ip('VMware Network Adapter VMnet1')
