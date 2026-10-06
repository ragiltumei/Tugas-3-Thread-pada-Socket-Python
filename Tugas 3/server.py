import socket
import threading
import time


class ClientThread(threading.Thread):

  def __init__(self, client_socket, client_address):
    super().__init__()
    self.client_socket = client_socket
    self.client_address = client_address

  def run(self):
    print(
        f"[{threading.current_thread().name}] Koneksi baru dari"
        f" {self.client_address}"
    )

    try:
      while True:
        # Membaca pesan dari client
        data = self.client_socket.recv(1024)
        if not data:
          break

        message = data.decode('utf-8').strip()

        # Menampilkan nama thread dan pesan client sesuai format
        print(
            f"({threading.current_thread().name}): pesan dari client"
            f" ({message})"
        )

        # Jika client mengirimkan "exit", hentikan loop dan tutup koneksi
        if message.lower() == 'exit':
          break

        # Mengirimkan balasan kembali ke client
        response = f'Server menerima: {message}'
        self.client_socket.sendall(response.encode('utf-8'))

        time.sleep(0.1)  # Simulasi jeda eksekusi kecil
    except Exception as e:
      print(f"[{threading.current_thread().name}] Error: {e}")
    finally:
      self.client_socket.close()
      print(
        f"[{threading.current_thread().name}] Koneksi dengan"
        f" {self.client_address} ditutup."
      )


def main():
  host = '127.0.0.1'
  port = 5000

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Memungkinkan reuse address jika server di-restart cepat
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((host, port))
  server_socket.listen(5)

  print(f'Server Multithreading berjalan di {host}:{port}...')

  try:
    while True:
      client_socket, client_address = server_socket.accept()
      # Membuat objek thread baru untuk setiap client
      new_thread = ClientThread(client_socket, client_address)
      # Memanggil start() untuk menjalankan thread secara asinkron
      new_thread.start()
  except KeyboardInterrupt:
    print('\nServer dihentikan.')
  finally:
    server_socket.close()


if __name__ == '__main__':
  main()