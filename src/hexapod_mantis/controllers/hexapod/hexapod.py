# mantis.py
# Controlador del hexápodo Mantis para Webots
# Gait trípode clásico (fémur levanta, tibia toca piso)

from controller import Robot
import math

# -------------------------
# CONFIGURACIÓN GENERAL
# -------------------------
TIME_STEP = 32
FREQ = 1.0         # frecuencia del gait
PHASE = [0, math.pi]  # trípode A / B

# -------------------------
# OFFSETS (postura base)
# -------------------------
# Orden por pata: A (coxa), B (femur), C (tibia)
# Patas: 1A,1B,1C, 2A,2B,2C ... 6C
d = [
    0.0, -0.7,  2.4,   # pata 1
    0.0, -0.7,  2.4,   # pata 2
    0.0, -0.7,  2.4,   # pata 3
    0.0, -0.7,  2.4,   # pata 4
    0.0, -0.7,  2.4,   # pata 5
    0.0, -0.7,  2.4    # pata 6
]

# -------------------------
# AMPLITUDES (MOVIMIENTO)
# -------------------------
aA = 0.25    # coxa
aB = -0.20   # femur (INVERTIDO → levanta)
aC = -0.10   # tibia (INVERTIDO → baja)

# -------------------------
# MAPEO DE PATAS A TRÍPODES
# -------------------------
# Trípode A: patas 1,3,5
# Trípode B: patas 2,4,6
tripod = [
    0,  # pata 1
    1,  # pata 2
    0,  # pata 3
    1,  # pata 4
    0,  # pata 5
    1   # pata 6
]

# -------------------------
# MAIN
# -------------------------
def main():
    robot = Robot()
    time_step = int(robot.getBasicTimeStep())

    # -------------------------
    # CARGAR MOTORES
    # -------------------------
    motors = []
    for i in range(1, 7):
        for j in ['A', 'B', 'C']:
            name = f"joint_{i}{j}"
            m = robot.getDevice(name)
            if m is None:
                print(f"ERROR: motor {name} no encontrado")
                return
            m.setPosition(float('inf'))
            m.setVelocity(2.0)
            motors.append(m)

    # -------------------------
    # POSTURA INICIAL (PATAS ABAJO)
    # -------------------------
    for i in range(18):
        motors[i].setPosition(d[i])

    t = 0.0

    # -------------------------
    # LOOP PRINCIPAL
    # -------------------------
    while robot.step(time_step) != -1:
        t += time_step / 1000.0

        for leg in range(6):
            phase = PHASE[tripod[leg]]
            s = math.sin(2 * math.pi * FREQ * t + phase)

            idx = leg * 3

            # Coxa → adelante / atrás
            motors[idx + 0].setPosition(d[idx + 0] + aA * s)

            # Femur → levanta la pata
            motors[idx + 1].setPosition(d[idx + 1] + aB * s)

            # Tibia → baja para tocar el piso
            motors[idx + 2].setPosition(d[idx + 2] + aC * s)

# -------------------------
# EJECUCIÓN
# -------------------------
if __name__ == "__main__":
    main()