import numpy as np
import matplotlib.pyplot as plt
import math as math

def gerar_bitstream(tamanho):
    return np.random.randint(2, size=tamanho)

def rect_pulse(bits, n_samp):
    output_signal = np.ones(len(bits)*n_samp)
    for i, bit in enumerate(bits):
        output_signal[i*n_samp:(i+1)*n_samp] = bit
    return output_signal

def plotar_sinal_modulado(t, modulated_signal):
    plt.plot(t, modulated_signal)
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    plt.title('Sinal Modulado')
    plt.grid(True)
    plt.show()

def plot(pulse):
    # Plote o pulso retangular
    plt.plot(pulse)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.title('Pulso Retangular')
    plt.grid(True)
    plt.show()

# simular comportamento de um sistema NFC, adicionando ruído e recuperando o sinal

if __name__ == '__main__':
    # Initial parameters
    fc =  13.56e4
    fs = 20 * fc + 1
    T = 1 
    snr = 20

    # Time vector for signal generations
    t = np.arange(0, (T-1/fs), 1/fs)
    
    # Generate ASK message signal
    fb_ASK = 10e2 # bit rate (bits/sec)
    Nb_ASK = fb_ASK * T # number of bits
    m_ASK = gerar_bitstream(int(Nb_ASK)) # generate bit sequence
    m_ASKp = rect_pulse(m_ASK, int(fs/fb_ASK)) # generate pulse sequence
    
    plot(m_ASKp*np.cos(2*np.pi*fc*t))

    # Array para o pulso retangular
    #pulse = m_ASK * (t < Nb_ASK)

    #plotar_pulso(t, m_ASKp)