import numpy as np
import adi
from sigmf import SigMFFile

# Nombre del archivo donde se guardaran las capturas y la metadata
file_name = 'sample_capture'

# Frecuencia de muestreo
sample_rate = 2.4e6     # Hz
# Frecuencia central
center_freq = 94.6e6    # Hz

# Numero de muestras a capturar
number_of_samples = 102400

# IP de PlutoSDR
sdr = adi.Pluto("ip:192.168.1.36")

# Tipo de ganancia de recepcion
sdr.gain_control_mode_chan0 = 'slow_attack'

sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = number_of_samples

# Captura de muestras
sdr_signal = sdr.rx()/2**14

# Convertir a complex64
sdr_signal = sdr_signal.astype(np.complex64)

# Guardar archivo
sdr_signal.tofile(file_name + '.sigmf-data')

# Crear metadata
meta = SigMFFile(
    data_file = file_name + '.sigmf-data',
    global_info = {
        SigMFFile.DATATYPE_KEY: 'cf32_le',
        SigMFFile.SAMPLE_RATE_KEY: sample_rate,
        SigMFFile.AUTHOR_KEY: 'Author',
        SigMFFile.DESCRIPTION_KEY: 'Captura de transmision FM',
        SigMFFile.VERSION_KEY: '1.0.0'
    }
)

# Crear una capture key en el time index 0
meta.add_capture(0, metadata={
    SigMFFile.FREQUENCY_KEY: center_freq
})

# Comprobar si hay errores y guardar el archivo de metadata
meta.validate()
meta.tofile(file_name + '.sigmf-meta')
