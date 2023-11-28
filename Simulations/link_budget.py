import numpy as np

# Prx is the received power at the output of the receive antenna
# Grx is the gain of the receive antenna
# Lrx is the losses in the cabling in the receiver
# Ptx is the power transmitted
# Gtx is the gain of the transmitted antenna
# Ltx is the losses in the cabling in the transmitter
# Lfree is the free space loss

def calculate_transmission_power_in_dbW(Ptx_dBm):
    Ptx_W = np.power(10, Ptx_dBm/10) * 0.001
    Ptx_dBW = 10 * np.log10(Ptx_W)
    return Ptx_dBW

def calculate_loss(distance, frequency):
    c = 3e8  
    lambda_ = c / frequency  

    free_space_loss = 20 * np.log10(4 * np.pi * distance / lambda_)
    path_loss = 20 * np.log10(distance)  

    total_loss = free_space_loss + path_loss
    return total_loss

def calculate_link_budget(Ptx, distance, frequency, sensitivity, sigma):
    Prx = calculate_transmission_power_in_dbW(Ptx) - calculate_loss(distance, frequency)
    free_space = calculate_transmission_power_in_dBm(Prx)
    log_distance_model = calculate_log_distance_model(free_space, distance, 1, 6)
    log_normal_model = calculate_log_normal_mode(log_distance_model, sigma) 
    result = log_normal_model - sensitivity
    return result

def calculate_log_distance_model(free_space, d, d0, n):
    log_distance_model = free_space + 10 * n * np.log10(d/d0)
    return log_distance_model

def calculate_transmission_power_in_dBm(Ptx_dBW):
    Ptx_W = np.power(10, Ptx_dBW/10)
    Ptx_dBm = 10 * np.log10(Ptx_W/0.001)
    return Ptx_dBm

def calculate_log_normal_mode(free_space_loss, sigma):
    log_normal_model = free_space_loss + sigma * np.random.randn()
    return log_normal_model

if __name__ == "__main__":
    #thread 1Mbps
    #sensitivity = -95dBm
    #transmission_power = 8dBm
    #distance = 10m
    transmission_power = input("Transmission Power (dBm): ")
    sensitivity = input("Sensitivity (dBm): ")
    frequency = input("Frequency (GHz): ")
    distance = input("Distance (m): ")
    sigma = input("Sigma: ")
    
    # Calcula o orçamento do link
    result = calculate_link_budget(int(transmission_power), int(distance), float(frequency) * 1e9, int(sensitivity), int(sigma))
    
    print("RESULT: ", result)
