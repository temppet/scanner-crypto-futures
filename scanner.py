#IMPORTACIONES
from binance_f import RequestClient
from binance_f.model import * 
from binance_f.constant.test import *
from binance_f.base.printobject import *

import pandas as pd
import numpy as np
import plotly.express as px
import time
import datetime as dt
import os


#CONEXIÓN CON LA API DE BINANCE
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

#LISTA DE LAS MONEDAS DE FUTUROS
symbols = ['1000SHIBUSDT', '1INCHUSDT', 'AAVEUSDT', 'ADAUSDT', 'AKROUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'ANKRUSDT', 'ATOMUSDT', 'AVAXUSDT', 'AXSUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BLZUSDT', 'BNBUSDT', 'BTCUSDT', 'BTSUSDT', 'BTTUSDT', 'BZRXUSDT', 'CELRUSDT', 'CHRUSDT', 'CHZUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT', 'CVCUSDT', 'DASHUSDT', 'DEFIUSDT', 'DENTUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'EGLDUSDT', 'ENJUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FILUSDT', 'FLMUSDT', 'FTMUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'HNTUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IOSTUSDT', 'IOTAUSDT', 'KAVAUSDT', 'KEEPUSDT', 'KNCUSDT', 'KSMUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LRCUSDT', 'LTCUSDT', 'LUNAUSDT', 'MANAUSDT', 'MATICUSDT', 'MKRUSDT', 'MTLUSDT', 'NEARUSDT', 'NEOUSDT', 'NKNUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT', 'ONTUSDT', 'QTUMUSDT', 'REEFUSDT', 'RENUSDT', 'RLCUSDT', 'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SFPUSDT', 'SKLUSDT', 'SNXUSDT', 'SOLUSDT', 'SRMUSDT', 'STMXUSDT', 'STORJUSDT', 'SUSHIUSDT', 'SXPUSDT', 'THETAUSDT', 'TOMOUSDT', 'TRBUSDT', 'TRXUSDT', 'UNFIUSDT', 'UNIUSDT', 'VETUSDT', 'WAVESUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'YFIIUSDT', 'YFIUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT']


def getCandles(symbols):

	
    #DATAFRAME CON LA INFORMACIÓN
	df = pd.DataFrame(columns= ['Symbol', 'Change', 'Signal', 'Volume'])

    #ARRAYS PARA GUARDAR LA DATA
	coin, change, signal, vol = [], [], [], []

    #RECORRER EL ARRAY DE MONEDAS
	for symbol in symbols:

        #OBTENER LA INFORMACIÓN DE LAS VELAS DE LOS ÚLTIMOS 45 MINUTOS
		candles = request_client.get_candlestick_data(symbol=symbol,interval=CandlestickInterval.MIN1, limit=45)

        #NOMBRE DE LA MONEDA
		sym = symbol[:-4]
        
        #DATOS BASE DE COMPARACIÓN DE PRECIO MÁXIMO Y MÍNIMO
		highPrice = 0
		lowPrice = 99999999999
        
        #RECORRER LAS VELAS DE LA MONEDA
		for candle in candles:
            
            #SI EL PRECIO DE LA VELA ES MAYOR QUE EL ULTIMO PRECIO MAYOR, CAMBIARLO
			if (float(candle.high) > highPrice):
                
				highPrice = float(candle.high)
  
            #SI EL PRECIO DE LA VELA ES MENOR QUE EL ULTIMO PRECIO MENOR, CAMBIARLO
			if (float(candle.low) < lowPrice):
                
				lowPrice = float(candle.low)
        
        #CALCULANDO EL PORCENTAJE DE CAMBIO DEL MAYOR Y EL MENOR CON RESPECTO AL PRECIO ACTUAL
		changeHigh = float(((float(candles[44].close) - float(highPrice)) / float(highPrice)) * 100)
		changeLow = float(((float(candles[44].close) - float(lowPrice)) / float(lowPrice)) * 100)
        
        #ANALIZANDO EL MAYOR CAMBIO Y EL TIPO DE SEÑAL
		changeAbs = 0
		sign = ''
        
		if(abs(changeHigh) > abs(changeLow)):
            
			changeAbs = abs(changeHigh)
			sign = 'LONG'
            
		else:
            
			changeAbs = abs(changeLow)
			sign = 'SHORT'
        
        #OBTENIENDO EL VOLUMEN DE LAS ÚLTIMAS 24 HORAS DE LA MONEDA
		volume = request_client.get_ticker_price_change_statistics(symbol=symbol)[0].quoteVolume
        
        #AGREGAR LOS DATOS A LOS ARRAYS DE DATOS
		coin.append(sym)
		change.append(changeAbs)
		signal.append(sign)
		vol.append(volume)

    #ASIGNAR LOS DATOS AL DATAFRAME
	df['Symbol'] = coin
	df['Change'] = np.array(change).astype(np.float)
	df['Volume'] = np.array(vol).astype(np.float)
	df['Signal'] = sign
    
    #RETORNAR EL DATAFRAME
	return df


def get_moving_symbols(candles_df):

	df1 = candles_df[candles_df['Volume'] >= 100000000]
	df1 = df1[df1['Change'] > 5]

	df2 = candles_df[candles_df['Volume'] < 100000000]
	df2 = df2[df2['Volume'] > 50000000]
	df2 = df2[df2['Change'] > 7]
    
	df3 = candles_df[candles_df['Volume'] < 50000000]
	df3 = df3[df3['Change'] > 10]

	df = [df1, df2, df3]
	df = pd.concat(df)

	return df


def main():

	while(True):

		candles_df = getCandles(symbols)
		candles_df_top = get_moving_symbols(candles_df)

		candles_df = candles_df.sort_values(by=['Change'], ascending = False)
		candles_df = candles_df.head(10)

		candles_df_top = candles_df_top.sort_values(by=['Change'], ascending = False)
  
		print('\nMonedas más movidas')
		print(candles_df)
		print('\nSeñales')
		print(candles_df_top)
		time.sleep(60)


if __name__ == '__main__':
	main()


