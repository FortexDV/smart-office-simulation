# simulador_smart_office.py
# Gera 7 dias de dados a cada 15 minutos para sensores de temperatura, luminosidade e ocupacao.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate(start_dt, end_dt, freq_minutes=15):
    timestamps = pd.date_range(start=start_dt, end=end_dt, freq=f'{freq_minutes}T')
    rows = []
    sensor_map = {
        'temp_': 'temperature_c',
        'lux_': 'luminosity_lux',
        'occ_': 'occupancy'
    }
    for ts in timestamps:
        hour = ts.hour
        # temperatura base: 22C dia, 19C noite, com ruído
        if 7 <= hour < 19:
            base_temp = 23 + 2*np.sin((hour-7)/12*np.pi)
        else:
            base_temp = 19 + 1.5*np.cos((hour)/24*2*np.pi)
        temp = round(np.random.normal(base_temp, 0.6), 2)
        # luminosidade: 0 durante noite, pico durante dia, com variação
        if 6 <= hour < 19:
            lux_base = max(200, 800 * np.sin((hour-6)/13*np.pi))
            lux = int(max(100, np.random.normal(lux_base, 80)))
        else:
            lux = int(np.random.normal(5, 2))
            if lux < 0:
                lux = 0
        # ocupacao: probabilidade maior em horário comercial dias úteis
        weekday = ts.weekday()
        if weekday < 5 and 8 <= hour < 18:
            occ_prob = 0.6
        elif weekday < 5 and (7 <= hour < 8 or 18 <= hour < 20):
            occ_prob = 0.2
        else:
            occ_prob = 0.05
        occupancy = 1 if np.random.rand() < occ_prob else 0

        rows.append({
            'timestamp': ts.isoformat(),
            'sensor_id': 'temp_1',
            'sensor_type': 'temperature',
            'value': temp
        })
        rows.append({
            'timestamp': ts.isoformat(),
            'sensor_id': 'lux_1',
            'sensor_type': 'luminosity',
            'value': lux
        })
        rows.append({
            'timestamp': ts.isoformat(),
            'sensor_id': 'occ_1',
            'sensor_type': 'occupancy',
            'value': occupancy
        })
    df = pd.DataFrame(rows)
    return df

if __name__ == '__main__':
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7) - timedelta(minutes=15)
    df = simulate(start, end)
    df.to_csv('smart_office_data.csv', index=False)
    print('Arquivo smart_office_data.csv gerado com', len(df), 'linhas.')