from binance.client import Client
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import time
import datetime as dt

client = Client('6kHqRwsLMjkbboMcIHw1TuUF8HbjMEOdhYYnPrNjMW4Ns8ObG4u6DWARpyPitNhZ', 'G3ZLw4chFydbmEziM3IBp2CPxFsVOsNE1fzsrNrgcUDwKfCnZU4CmeVBf28KnNth')

symbols = ['1INCHUSDT', 'AAVEUSDT', 'ADAUSDT', 'AKROUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'ANKRUSDT', 'ATOMUSDT', 'AVAXUSDT', 'AXSUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BLZUSDT', 'BNBUSDT', 'BTCUSDT', 'BTSUSDT', 'BTTUSDT', 'BZRXUSDT', 'CELRUSDT', 'CHRUSDT', 'CHZUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT', 'CVCUSDT', 'DASHUSDT', 'DENTUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'EGLDUSDT', 'ENJUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FILUSDT', 'FLMUSDT', 'FTMUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'HNTUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IOSTUSDT', 'IOTAUSDT', 'KAVAUSDT', 'KEEPUSDT', 'KNCUSDT', 'KSMUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LRCUSDT', 'LTCUSDT', 'LUNAUSDT', 'MANAUSDT', 'MATICUSDT', 'MKRUSDT', 'MTLUSDT', 'NEARUSDT', 'NEOUSDT', 'NKNUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT', 'ONTUSDT', 'QTUMUSDT', 'REEFUSDT', 'RENUSDT', 'RLCUSDT', 'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SFPUSDT', 'SKLUSDT', 'SNXUSDT', 'SOLUSDT', 'SRMUSDT', 'STMXUSDT', 'STORJUSDT', 'SUSHIUSDT', 'SXPUSDT', 'THETAUSDT', 'TOMOUSDT', 'TRBUSDT', 'TRXUSDT', 'UNFIUSDT', 'UNIUSDT', 'VETUSDT', 'WAVESUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'YFIIUSDT', 'YFIUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT']


def getCandles(symbols):

	df = pd.DataFrame(columns= ['Symbol', 'Open_time', 'Open', 'Close', 'Change', 'Volume', 'Close_time'])

	coin, opentime, lopen, lclose, change, vol, closetime = [], [], [], [], [], [], []

	for symbol in symbols:

		candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "30 minutes ago UTC")
		volume = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=1)[0][5]

		coin.append(symbol)
		opentime.append(dt.datetime.fromtimestamp(candles[0][0] / 1e3))
		lopen.append(candles[0][1])
		lclose.append(candles[0][4])
		change.append(abs(((float(candles[29][4]) / float(candles[0][1])) - 1) * 100))
		vol.append(volume)
		closetime.append(dt.datetime.fromtimestamp(candles[0][6] / 1e3))

		coin.append(symbol)
		opentime.append(dt.datetime.fromtimestamp(candles[29][0] / 1e3))
		lopen.append(candles[29][1])
		lclose.append(candles[29][4])
		change.append(abs(((float(candles[29][4]) / float(candles[0][1])) - 1) * 100))
		vol.append(volume)
		closetime.append(dt.datetime.fromtimestamp(candles[29][6] / 1e3))

	df['Symbol'] = coin
	df['Open_time'] = opentime
	df['Open'] = np.array(lopen).astype(np.float)
	df['Close'] = np.array(lclose).astype(np.float)
	df['Change'] = np.array(change).astype(np.float)
	df['Volume'] = np.array(vol).astype(np.float)
	df['Close_time'] = closetime
	return df


def get_moving_symbols(candles_df):

	df1 = candles_df[candles_df['Volume'] >= 1e+07]
	df1 = df1[df1['Change'] > 5]

	df2 = candles_df[candles_df['Volume'] < 1e+07]
	df2 = df2[df2['Change'] > 7]

	df = [df1, df2]
	df = pd.concat(df)

	return df


def main():

	while(True):

		candles_df = getCandles(symbols)
		candles_df = get_moving_symbols(candles_df)
		print(candles_df)
		time.sleep(60)


if __name__ == '__main__':
	main()


