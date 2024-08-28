import control as ctrl
import matplotlib.pyplot as plt
import math as m

def controler(Kp = 1, Ki = 0, Kd = 0, type = 'P', T = None):
    if type == 'P':
        control = ctrl.TransferFunction([Kp], [1], T)
    elif type == 'PI':
        if T is None:
            control = ctrl.TransferFunction([Kp, Ki], [1, 0])
        else:
            p = ctrl.TransferFunction([Kp], [1], T)
            i = ctrl.TransferFunction([Ki*T, Ki*T], [2, -2], T)
            control = ctrl.parallel(p, i)
    elif type == 'PD':
        if T is None:
            control = ctrl.TransferFunction([Kd, Kp], [1])
        else:
            p = ctrl.TransferFunction([Kp], [1], T)
            d = ctrl.TransferFunction([Kd, -Kd],[T, 0], T)
            control = ctrl.parallel(p, d)
    elif type == 'PID':
        if T is None:
            control = ctrl.TransferFunction([Kd, Kp, Ki],[1, 0])
        else:
           p = ctrl.TransferFunction([Kp], [1], T)
           i = ctrl.TransferFunction([Ki*T, Ki*T], [2, -2], T)
           d = ctrl.TransferFunction([Kd, -Kd],[T, 0], T)
           control = ctrl.parallel(p, i, d) 
    
    return control
        

def firstOrder(K=1, tau=1, T=None):
    system = ctrl.TransferFunction([K], [tau, 1])
    if T is not None:
        system = ctrl.sample_system(system, T, method='zoh')
    return system

def plots(system, control, type):
    open_loop = ctrl.series(system, control)
    closed_loop = ctrl.feedback(open_loop, 1)
    # Plotando o Lugar das Raízes (LGR)
    plt.figure()
    ctrl.root_locus(open_loop)
    plt.title(f'LGR continuo')
    plt.grid(True)

    # Plotando a Resposta ao Degrau
    plt.figure()
    time, response = ctrl.step_response(closed_loop)
    plt.plot(time, response)
    plt.title(f'Resposta ao Degrau continuo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    # Plotando o Diagrama de Bode para o sistema 
    plt.figure()
    ctrl.bode(open_loop, dB=True, Hz=False, deg=True)
    plt.suptitle(f'Diagrama de Bode com Compensador {type}')
    plt.show()

def dynsyn(K = 1, tau = 1, T = None, type = 'P', Kp = 1, Ki = 0, Kd = 0):
    system = firstOrder(K, tau, T)
    control = controler(Kp, Ki, Kd, type, T)
    plots(system, control, type)

# Caso de teste
K = 1
tau = 1
T = 0.5
Kp = 0.5
Ki = 0.2
Kd = 0.1
type = 'PID'
dynsyn(K, tau, T, type, Kp, Ki, Kd)

