import io
import json
import random
import pandas as pd
from botocore.vendored import requests
import statistics as stat
import numpy as np

def lambda_handler(event, context):
    # TODO implement
    mov_time_window = int(event['mov_time_window'])
    # mov_time_window = 20
    closing_price_series = event['closing_price_series']

    Signal = []
    MoveAvg = []
    for i in range(0, len(closing_price_series)):
        if (i >= mov_time_window):
            Total = 0;
            for j in range(mov_time_window, -1, -1):
                Total = Total + closing_price_series[i - j]
            MoveAvg.append(Total / mov_time_window)
    # print(Total/20, file=sys.stderr)
    for i in range(len(MoveAvg)):
        if (i > 0):
            if (closing_price_series[i+mov_time_window] - MoveAvg[i] > 0 and closing_price_series[i+mov_time_window-1] - MoveAvg[i - 1] <= 0 ):
                Signal.append(('Buy',i+mov_time_window,closing_price_series[i+mov_time_window]))
            elif (closing_price_series[i+mov_time_window] - MoveAvg[i] < 0 and closing_price_series[i+mov_time_window-1] - MoveAvg[i - 1] >= 0 ):
                Signal.append(('Sell',i+mov_time_window,closing_price_series[i+mov_time_window]))

    data = {'mov':MoveAvg, 'signal': Signal }
    res = json.dumps(data)
    return res