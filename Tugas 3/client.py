import socket


def main():
  host = '127.0.0.1'
  port = 5000

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    client_socket.connect((host, port))
    print(f'Terhubung ke server {host}:{port}')
    print('Ketik pesan dan tekan Enter. Ketik "exit" untuk keluar.\n')

    while True:
      pesan = input('Masukkan pesan: ')
      if not pesan.strip():
        continue

      # Mengirim pesan ke server
      client_socket.sendall(pesan.encode('utf-8'))

      # Jika pesan exit, tidak perlu menunggu balasan dan langsung keluar
      if pesan.lower() == 'exit':
        print('Menutup koneksi...')
        break

      # Menerima balasan dari server
      response = client_socket.recv(1024)
      print(f'Respon dari server: {response.decode("utf-8")}\n')

  except Exception as e:
    print(f'Error: {e}')
  finally:
    client_socket.close()


if __name__ == '__main__':
  main()