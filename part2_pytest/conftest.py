import time
import paramiko
import subprocess
import pytest

# Дані серверу для підключення по SSH та піднімання iperf3-сервера.
# У цій роботі як "сервер" використовується той самий комп'ютер (localhost) —
# підключення відбувається по справжньому SSH-протоколу, так само, як і до
# окремої віддаленої машини.
server_ip = '127.0.0.1'
username = 'iperftest'
password = 'iperftest123'


@pytest.fixture(scope='function')
def server():
    """
    Підключається до сервера по SSH (бібліотека paramiko), запускає на ньому
    iperf3-сервер у фоновому режимі. Після виконання теста закриває SSH-з'єднання
    та завершує процес iperf3-сервера (teardown через yield).

    :return: повідомлення про помилку підключення, якщо вона виникла, інакше None
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    error = None
    try:
        ssh.connect(server_ip, username=username, password=password, timeout=5)
        ssh.exec_command('pkill iperf3; sleep 0.5; nohup iperf3 -s > /tmp/iperf3_server.log 2>&1 &')
        time.sleep(1)
    except Exception as exc:
        error = str(exc)

    yield error

    if error is None:
        ssh.exec_command('pkill iperf3')
        ssh.close()


@pytest.fixture(scope='function')
def client(server):
    """
    Підключається до iperf3-сервера через subprocess. Якщо фікстура server
    повернула помилку (не вдалось підняти сервер по SSH) — одразу повертає цю
    помилку, не намагаючись підключитись.

    :param server: викликає фікстуру server (піднімає iperf3-сервер по SSH)
    :return: кортеж (stdout, stderr) для подальшого аналізу у тесті
    """
    if server:
        return None, server

    process = subprocess.Popen(
        ['iperf3', '-c', server_ip, '-i', '1', '-b', '50M'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(timeout=30)
    return stdout, stderr
