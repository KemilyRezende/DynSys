import serial
import time

# Configurações da porta serial
arduino_port = "/dev/ttyUSB0"  # Substitua pela porta serial correta (ex: "COM3" no Windows)
baud_rate = 9600
timeout = 1  # Tempo de espera para leitura

# Inicializa a conexão serial
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)
time.sleep(2)  # Aguarda um tempo para que a conexão seja estabelecida

print("Iniciando leitura dos dados...")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Lê a linha enviada pelo Arduino
            print(line)  # Imprime a linha recebida do Arduino
except KeyboardInterrupt:
    print("Encerrando a leitura...")
finally:
    ser.close()  # Fecha a conexão serial
