import subprocess

# IP-адреса iperf3-сервера. У цій частині роботи сервер піднімаємо вручну, в окремому терміналі.
server_ip = '127.0.0.1'


def client(server_ip):
    """
    Підключається до iperf3-сервера через subprocess та повертає вивід і помилку.

    :param server_ip: Адреса сервера, до якого буде підключатися клієнт
    :return: кортеж (stdout, stderr)
    """
    process = subprocess.Popen(
        ['iperf3', '-c', server_ip, '-i', '1'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(timeout=30)
    return stdout, stderr
