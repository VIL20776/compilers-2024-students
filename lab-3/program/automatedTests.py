import os
import subprocess
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init()

# Define the test specifications and content for each test file
test_cases = [
    ("Cree un programa que reserve una sala de conferencias.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
LISTAR
"""),
    ("Cree un programa que cancele una reserva de sala de conferencias.", """RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
CANCELAR room2 PARA 12/12/2024 DE 12:00 A 13:00
LISTAR
"""),
    ("Experimente con varias reservas y cancelaciones en un mismo programa.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
RESERVAR MEETINGROOM room3 PARA 12/12/2024 DE 14:00 A 15:00 POR Alice DESCRIPCION "Client meeting"
CANCELAR room2 PARA 12/12/2024 DE 12:00 A 13:00
LISTAR
"""),
    ("Modifique el DSL para incluir el nombre del solicitante de la reserva.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
LISTAR
"""),
    ("Agregue manejo de errores para detectar fechas u horas inválidas.", """RESERVAR MEETINGROOM room3 PARA 32/12/2024 DE 10:00 A 11:00 POR Alice DESCRIPCION "Client meeting"  # Invalid date
RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 25:00 A 26:00 POR John DESCRIPCION "Project meeting"  # Invalid time
LISTAR
"""),
    ("Cree un programa que incluya reservas solapadas y verifique su manejo (para validar reservaciones traslapadas, use un listener de ANTLR en Python; el listener llevará la cuenta de las reservaciones y validará cada nueva reservación en contra de las existentes).", """RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 10:00 A 11:00 POR Jane DESCRIPCION "Training session"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 10:30 A 11:30 POR Frank DESCRIPCION "Strategy meeting"  # Overlapping reservation
LISTAR
"""),
    ("Extienda el DSL para soportar descripciones de eventos.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
LISTAR
"""),
    ("Agregue validaciones adicionales como restricciones de tiempo de uso máximo.", """RESERVAR MEETINGROOM room3 PARA 12/12/2024 DE 08:00 A 18:00 POR Grace DESCRIPCION "All-day workshop"  # Exceeds maximum allowed time
LISTAR
"""),
    ("Implemente una funcionalidad para listar las reservas existentes.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
RESERVAR MEETINGROOM room3 PARA 12/12/2024 DE 14:00 A 15:00 POR Alice DESCRIPCION "Client meeting"
LISTAR
"""),
    ("Cree un programa que utilice todas las características extendidas del DSL.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
RESERVAR MEETINGROOM room3 PARA 12/12/2024 DE 14:00 A 15:00 POR Alice DESCRIPCION "Client meeting"
LISTAR
"""),
    ("Añada soporte para diferentes tipos de salas (por ejemplo, sala de juntas, sala de capacitación).", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
RESERVAR MEETINGROOM room3 PARA 12/12/2024 DE 14:00 A 15:00 POR Alice DESCRIPCION "Client meeting"
RESERVAR BOARDROOM room4 PARA 13/12/2024 DE 09:00 A 10:00 POR Bob DESCRIPCION "Board meeting"
RESERVAR TRAININGROOM room5 PARA 13/12/2024 DE 11:00 A 12:00 POR Carol DESCRIPCION "Workshop"
LISTAR
"""),
    ("Implemente un sistema de notificaciones para reservas próximas.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
# Notifications will be handled based on the upcoming reservations
LISTAR
"""),
    ("Extienda el DSL para permitir la reprogramación de reservas.", """RESERVAR BOARDROOM room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Project meeting"
REPROGRAMAR room1 PARA 12/12/2024 DE 10:00 A 11:00 POR John DESCRIPCION "Rescheduled project meeting"
LISTAR
"""),
    ("Cree un programa que reprograme una reserva existente y valide el cambio (para validar reservaciones traslapadas, use un listener de ANTLR en Python que ya creó en una actividad anterior; el listener llevará la cuenta de las reservaciones y validará cada nueva reservación en contra de las existentes).", """RESERVAR TRAININGROOM room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Training session"
REPROGRAMAR room2 PARA 12/12/2024 DE 12:00 A 13:00 POR Jane DESCRIPCION "Rescheduled training session"
LISTAR
""")
]

# Create the tests directory if it doesn't exist
if not os.path.exists('tests'):
    os.makedirs('tests')

# Create files, run DriverConfroom.py with each file, and capture the output
for i, (description, content) in enumerate(test_cases, 1):
    file_path = f"tests/{i}.txt"
    with open(file_path, "w") as file:
        file.write(content)

    # Run the DriverConfroom.py script
    command = f"python3 DriverConfroom.py {file_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Get the current timestamp and environment details
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = f"OS: {os.name}, Timestamp: {timestamp}"

    # Print the test specification, file content, and result with colors
    print(Fore.CYAN + f"Test {i}: {description}" + Style.RESET_ALL)
    print(Fore.YELLOW + "File Content:" + Style.RESET_ALL)
    print(content)
    print(Fore.GREEN + "Execution Result:" + Style.RESET_ALL)
    print(result.stdout)
    print(result.stderr)
    print(Fore.MAGENTA + "Environment Info:" + Style.RESET_ALL)
    print(os_info)
    print("\n" + "="*80 + "\n")

# for i in range(1, len(test_cases) + 1):
#     os.remove(f"tests/{i}.txt")

print("Tests executed and results captured successfully.")
