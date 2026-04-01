#!/usr/bin/env pybricks-micropython

#o codigo a seguir utiliza a versao 2.0.0 do pybricks
#pip install pybricks==2.0.0

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# Inicializa o EV3
ev3 = EV3Brick()

# Configura o motor da garra (Porta A)
motor_garra = Motor(Port.A)

# Configura o motor do cotovelo (Porta B, anti-horário para subir)
motor_cotovelo = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configura o motor da base (Porta C, anti-horário para afastar do sensor)
motor_base = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limita velocidade e aceleração para movimentos mais suaves
motor_cotovelo.control.limits(speed=60, acceleration=120)
motor_base.control.limits(speed=60, acceleration=120)

# Sensor de toque atua como fim de curso da base (Porta S1)
sensor_toque_base = TouchSensor(Port.S1)

# Sensor de cor detecta a posição inicial do cotovelo (Porta S3)
sensor_cor_cotovelo = ColorSensor(Port.S3)

# Inicializa o cotovelo: desce, sobe até ver a viga branca e zera o ângulo
motor_cotovelo.run_time(-30, 1000)
motor_cotovelo.run(15)
while sensor_cor_cotovelo.reflection() < 32:
    wait(10)
motor_cotovelo.reset_angle(0)
motor_cotovelo.hold()

# Inicializa a base: gira até pressionar o sensor e zera o ângulo
motor_base.run(-60)
while not sensor_toque_base.pressed():
    wait(10)
motor_base.reset_angle(0)
motor_base.hold()

# Inicializa a garra: fecha até travar, zera o ângulo e abre 90 graus
motor_garra.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
motor_garra.reset_angle(0)
motor_garra.run_target(200, -90)


def robo_pegar(posicao):
    # Gira para a posição, abaixa, fecha a garra e levanta
    motor_base.run_target(60, posicao)
    motor_cotovelo.run_target(60, -40)
    motor_garra.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    motor_cotovelo.run_target(60, 0)


def robo_soltar(posicao):
    # Gira para a posição, abaixa, abre a garra e levanta
    motor_base.run_target(60, posicao)
    motor_cotovelo.run_target(60, -40)
    motor_garra.run_target(200, -90)
    motor_cotovelo.run_target(60, 0)


# Bipes de inicialização concluída
for i in range(3):
    ev3.speaker.beep()
    wait(100)

# Posições de destino da base
ESQUERDA = 160
CENTRO = 100
DIREITA = 40

# Loop principal: move os objetos ciclicamente entre Esquerda, Centro e Direita
while True:
    robo_pegar(ESQUERDA)
    robo_soltar(CENTRO)

    robo_pegar(DIREITA)
    robo_soltar(ESQUERDA)

    robo_pegar(CENTRO)
    robo_soltar(DIREITA)
