import requests

def get_external_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    external_ip = data['ip']
    return external_ip

# Пример использования
external_ip = get_external_ip()
print("Внешний IP-адрес:", external_ip)
