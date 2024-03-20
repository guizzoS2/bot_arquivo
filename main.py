import platform
import subprocess
import ctypes
import getpass
import netifaces
import os
import requests
import socket
import datetime

def forma(tipo="-=", qnt=22):
    print(tipo*qnt)


def cabecalho(msg, qnt=44):
    forma()
    print(msg.center(qnt))
    forma()


def get_system_info():
    system_info = {}
    system_info['Sistema Operacional'] = platform.system() + f" {platform.release()}"
    system_info['Nome do PC'] = platform.node()
    system_info['Versão'] = platform.version()
    system_info['Maquina'] = platform.machine()
    system_info['Processador'] = platform.processor()
    system_info['Arquitetura'] = platform.architecture()[0]
    return system_info


def portas_abertas():
    nenhum = "Nenhuma Porta Aberta"
    output = subprocess.check_output(['netstat', '-ano'])
    linhas = output.decode('latin-1').strip().split('\r\r\n')[4:]
    portas = []
    for linha in linhas:
        partes = linha.split()
        if partes and partes[0] == "TCP" and partes[2] == "LISTENING":
            port = partes[1].split(':')[-1]
            portas.append(port)
    return portas if portas else nenhum


def obter_usu():
    usu_atu = getpass.getuser()
    return usu_atu


def ulti_usu():
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(['quser'])
            linhas = output.decode('latin-1').strip().split('\r\n')
            if len(linhas) > 1:
                ulti_usu = linhas[1].split()[0]
                ulti_usu = ulti_usu[1:]
            else:
                ulti_usu = ""
            return ulti_usu
        except FileNotFoundError:
            # Comando não encontrado no sistema não-Windows
            return ""
    else:
        # Lógica para sistemas não-Windows (substitua pelo que for adequado)
        return ""



def obter_ip():
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ipv4_addresses = addresses[netifaces.AF_INET]
                for addr in ipv4_addresses:
                    ip_address = addr['addr']
                    if not ip_address.startswith('127.'):
                        return ip_address
        return None
    except:
        return None


def obter_mask():
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ipv4_addresses = addresses[netifaces.AF_INET]
                for addr in ipv4_addresses:
                    for key, value in addr.items():
                        if key in ['addr', 'peer', 'mask', 'broadcast']:
                            subnet_mask = value
                            return subnet_mask
        return None
    except:
        return None


def obter_gate():
    try:
        gateways = netifaces.gateways()
        if netifaces.AF_INET in gateways:
            default_gateway = gateways[netifaces.AF_INET][0][0]
            return default_gateway
        return None
    except:
        return None


def obter_mac():
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_LINK in addresses:
                mac_addresses = addresses[netifaces.AF_LINK]
                for addr in mac_addresses:
                    mac_address = addr['addr']
                    return mac_address
        return None
    except:
        return None


def get_disk_memory_usage(disk):
    if platform.system() == "Windows":
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(disk), None, None, ctypes.pointer(free_bytes))
        free_space = free_bytes.value // (1024**3)  # bytes para gigabytes
        return free_space
    else:  # linux
        st = os.statvfs(disk)
        free_space = st.f_bavail * st.f_frsize // (1024**3)  # bytes para gigabytes
        return free_space


def get_disk_max(disk):
    if platform.system() == "Windows":
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(disk), None, ctypes.pointer(total_bytes), None)
        max_space = total_bytes.value / (1024 ** 3)  # bytes para gigabytes
        return "{:.2f}".format(max_space)
    else:  # linux
        st = os.statvfs(disk)
        max_space = st.f_blocks * st.f_frsize / (1024 ** 3)  # bytes para gigabytes
        return "{:.2f}".format(max_space)


def data_instal_img():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(['systeminfo']).decode('utf-8')
            linhas = output.split('\n')
            for linha in linhas:
                if 'Data de Instalação:' in linha:
                    data_install = linha.split(':')[1].strip()
                    return data_install
        else:  # linux
            output = subprocess.check_output(['ls', '-ld', '/']).decode('utf-8')
            data_install = output.split()[5]
            return data_install
    except:
        return None


def obter_particoes():
    if platform.system() == "Windows":
        output = subprocess.check_output(['wmic', 'logicaldisk', 'get', 'DeviceID', '/Value'])
        linhas = output.decode('latin-1').strip().split('\r\r\n')
        particoes = [linha.split('=')[1] for linha in linhas if linha.startswith('DeviceID')]
        return particoes
    else:  # linux
        output = subprocess.check_output(['df']).decode('utf-8')
        linhas = output.strip().split('\n')[1:]
        particoes = [linha.split()[0] for linha in linhas]
        return particoes


def get_ram_total():
    if platform.system() == "Windows":
        output = subprocess.check_output(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory', '/value'])
        linhas = output.decode('latin-1').strip().split('\r\r\n')
        ram_total = int(linhas[0].split('=')[1]) // (1024 ** 2)  # bytes para megabytes
        return ram_total
    else:
        output = subprocess.check_output(['grep', 'MemTotal', '/proc/meminfo']).decode('utf-8')
        ram_total = int(output.split()[1]) // 1024  # kilobytes para megabytes
        return ram_total


def obter_biosV():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(['wmic', 'bios', 'get', 'SMBIOSBIOSVersion']).decode('utf-8')
            bioV = output.strip().split('\n')[1]
            return bioV
        else:  # Linux
            output = subprocess.check_output(['sudo', 'dmidecode', '-s', 'bios-version']).decode('utf-8')
            return output.strip()
    except:
        return None


def obter_data_bios():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(['wmic', 'bios', 'get', 'ReleaseDate']).decode('utf-8')
            data_invertida = output.strip().split('\n')[1]
            data_real = data_invertida[6:8] + "/" + data_invertida[4:6] + '/' + data_invertida[0:4] + " -- " + \
                        data_invertida[8:10] + ":" + data_invertida[10:12]
            return data_real
        else:
            try:
                with open('/sys/class/dmi/id/bios_date', 'r') as f:
                    data_invertida = f.read().strip()
                    data_real = (
                            data_invertida[0:4] + "/" + data_invertida[4:6] + '/' + data_invertida[6:8] +
                            " -- " + data_invertida[9:11] + ":" + data_invertida[11:13]
                    )
                    return data_real
            except IOError as e:
                print(f"Erro ao obter a data da BIOS: {e}")
                return None
    except:
        return None


def enviar_dados_para_servidor(dados):
    url = 'https://exemplo.com/api/endpoint'  # Substitua pela URL do seu servidor
    response = requests.post(url, json=dados)
    if response.status_code == 200:
        print('Dados enviados com sucesso!')
    else:
        print(f'Falha ao enviar os dados. Código de status: {response.status_code}')


def criar_arquivo_com_dados(dados):
    nome_arquivo = 'dados_do_sistema.txt'
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
    with open(nome_arquivo, 'w') as arquivo:
        for chave, valor in dados.items():
            arquivo.write(f"{chave}: {valor}\n")


partitions = obter_particoes()
open_ports = portas_abertas()
domain = socket.getfqdn()
ram_total = get_ram_total()
user_current = obter_usu()
user_last = ulti_usu()
ip_address = obter_ip()
subnet_mask = obter_mask()
default_gateway = obter_gate()
mac_address = obter_mac()
bios_version = obter_biosV()
bios_date = obter_data_bios()
disco = get_disk_memory_usage("C:")
date_time = str(datetime.datetime.now())
dia = date_time[8:10]+ "/" + date_time[5:7]+ "/" + date_time[0:4]
hora = date_time[11:16]
#installed_software = softwares()
# installation_date = data_instal_img()
# license_key = licenca()
# virtual_mem = virtu_memo()
# firewall_status = obter_status_firewall()
system_info = get_system_info()

cabecalho("Informações da Máquina")
for key, value in system_info.items():
    print(f"{key}: {value}")
print("Usuário Atual:", user_current)
print("Último Usuário:", user_last)
print("Versão da BIOS:", bios_version)
print("Data da BIOS:", bios_date)
print("\n")

cabecalho("Especificações")
print("Quantidade de Memória RAM (MB):", ram_total)
print("Partições:", partitions)
for disk in partitions:
    free_space = get_disk_memory_usage(disk)
    print(f"Espaço livre em {disk}: {free_space} GB")
    max_space = get_disk_max(disk)
    print(f"Espaço máximo em {disk}: {max_space} GB")
print("\n")

cabecalho("Rede")
print("Endereço IP:", ip_address)
print("Máscara de Sub-rede:", subnet_mask)
print("Gateway Padrão:", default_gateway)
print("Endereço MAC:", mac_address)
print("Portas Abertas:", open_ports)
print("Domínio:", domain)
print("\n")

dados = {}
for key, value in system_info.items():
    dados[f'{key}'] = f"{value}"

dados_1 = {
    "Usuário Atual": user_current,
    "Último Usuário": user_last,
    "Versão da BIOS": bios_version,
    "Data da BIOS": bios_date,
    "Quantidade de Memória RAM (MB)": ram_total,
    "Partições": partitions}

for disk in partitions:
    free_space = get_disk_memory_usage(disk)
    dados_1[f'Espaço livre em {disk}'] = f"{free_space} GB"
    max_space = get_disk_max(disk)
    dados_1[f"Espaço máximo em {disk}"] = f"{max_space} GB"

dados_2 = {
    "Endereço IP": ip_address,
    "Máscara de Sub-rede": subnet_mask,
    "Gateway Padrão": default_gateway,
    "Endereço MAC": mac_address,
    "Portas Abertas": open_ports,
    "Domínio": domain,
    "Dia de Envio": dia,
    "Hora de Envio": hora}

dados_para_enviar = {**dados, **dados_1, **dados_2}

criar_arquivo_com_dados(dados_para_enviar)

"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡟⠋⢻⣷⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣾⣿⣷⣿⣿⣿⣿⣿⣶⣾⣿⣿⠿⠿⠿⠶⠄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠟⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣆⣤⠿⢶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""