import numpy as np
import matplotlib.pyplot as plt

def gera_bitstream(tamanho):
    return np.random.randint(2, size=tamanho)

def gera_sinal_ASK(T, snr, fc, fb_ASK):
    fs = 20 * fc
    t = np.arange(0, T, 1 / fs)
    Nb_ASK = int(fb_ASK * T)
    m_ASK = gera_bitstream(Nb_ASK)
    m_ASKp = np.repeat(m_ASK, int(fs / fb_ASK)) 
    z_ASK = m_ASKp * np.exp(1j * 2 * np.pi * fc * t)
    z_ASK_noise = adiciona_ruido(z_ASK, snr)
    return t, z_ASK, z_ASK_noise, m_ASK

def adiciona_ruido(sinal, snr):
    SNR_dB = snr
    noise_power = 10 ** (-SNR_dB / 10)
    noise_real = np.sqrt(noise_power / 2) * np.random.normal(0, 1, len(sinal))
    noise_imag = np.sqrt(noise_power / 2) * np.random.normal(0, 1, len(sinal))
    return sinal + noise_real + 1j * noise_imag

def intdump(x, factor):
    return x[::factor]

def recupera_sinal_ASK(t, sinal_modulado, fc, fb_ASK, fs):
    m_ASKp_r = sinal_modulado * np.exp(-1j * 2 * np.pi * fc * t)
    n_samp = int(fs / fb_ASK)
    m_ASK_r = intdump(m_ASKp_r, n_samp)
    return m_ASK_r

def calcula_BER(sinal_original, sinal_recuperado):
    bit_errors = np.sum(np.abs(m_ASK - m_ASK_r))
    BER = bit_errors / len(m_ASK)
    error_percentage = BER * 100
    return BER

def plota_sinais_tempo(t, sinal_baseband, sinal_modulado):
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(t, np.real(sinal_baseband))
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude (a.u.)')
    plt.title('Sinal no Domínio do Tempo (Baseband)')
    plt.grid()

    plt.figure(2)
    plt.subplot(2, 1, 1)
    plt.plot(t, np.real(sinal_modulado))
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude (a.u.)')
    plt.title('Sinal no Domínio do Tempo (Modulado)')
    plt.grid()

def plota_espectro(f, espectro_sinal_baseband, espectro_sinal_modulado):
    plt.figure(1)
    plt.subplot(2, 1, 2)
    plt.plot(f, np.real(espectro_sinal_baseband))
    plt.grid()

    plt.figure(2)
    plt.subplot(2, 1, 2)
    plt.plot(f, np.real(espectro_sinal_modulado))
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('PSD (dBV/Hz)')
    plt.title('Espectro de Amplitude do Sinal')
    plt.grid()

if __name__ == "__main__":
    T = 1
    snr = 25
    fc = 13.56e4
    fs = 20 * fc
    fb_ASK = 10e2

    t, sinal_baseband, sinal_modulado, m_ASK = gera_sinal_ASK(T, snr, fc, fb_ASK)
    m_ASK_r = recupera_sinal_ASK(t, sinal_modulado, fc, fb_ASK, fs)
    BER = calcula_BER(m_ASK, m_ASK_r)
    error_percentage = BER * 100

    print("Taxa de Erro de Bit (BER): {:.5f} %")

    df = 20 * 13.56e4 / len(t)
    f = (np.arange(0, len(t)) * df - 20 * 13.56e4 / 2)

    Z_ASKp = np.fft.fftshift(20 * np.log10(np.abs(np.fft.fft(sinal_baseband) + 1e-10)))
    Z_ASK = np.fft.fftshift(20 * np.log10(np.abs(np.fft.fft(sinal_modulado))))


    plota_sinais_tempo(t, sinal_baseband, sinal_modulado)
    plota_espectro(f, Z_ASKp, Z_ASK)
    
    plt.show()
