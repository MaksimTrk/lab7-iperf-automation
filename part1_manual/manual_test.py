from client import client, server_ip
from parser import parser

if __name__ == '__main__':
    result, error = client(server_ip)

    if error:
        print("ПОМИЛКА ПІДКЛЮЧЕННЯ:")
        print(error)
    else:
        result_list = parser(result)
        print(f"Отримано {len(result_list)} інтервалів передачі.\n")
        print("Інтервали, що відповідають умові Transfer > 2 MBytes та Bitrate > 20 Mbits/sec:")
        found = False
        for value in result_list:
            if value['Transfer'] > 2 and value['Bitrate'] > 20:
                print(value)
                found = True
        if not found:
            print("Жоден інтервал не відповідає умові.")
