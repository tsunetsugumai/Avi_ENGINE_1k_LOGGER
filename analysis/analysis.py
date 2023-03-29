#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
from tqdm import tqdm
import math

def main(source,target):
    with open(source) as fr:
        reader = csv.reader(fr)
        with open(target, 'w', encoding='utf_8_sig',newline="") as fw:
             writer = csv.writer(fw)
             writer.writerow(['書き込み待ちデータ数','データ取得開始時','データ取得終了時','推力[N]','圧力1[Pa]','圧力2[Pa]','圧力3[Pa]','圧力4[Pa]','高域温度1','高域温度2','低域温度1','低域温度2','低域温度3'])
             for row in tqdm(reader):
                # 1行ずつ読み込み
                writer.writerow([row[0],row[1],row[2],str(bin2Thrust(int(row[3]))),str(bin2dataPressure(int(row[5]))),str(bin2dataPressure(int(row[6]))),str(bin2dataPressure(int(row[7]))),str(bin2dataPressure(int(row[8]))),str(bin2dataTempHigh(int(row[11]))),str(bin2dataTempHigh(int(row[12]))),str(bin2dataTempLow(int(row[13]))),str(bin2dataTempLow(int(row[14]))),str(bin2dataTempLow(int(row[15])))])
            
    

def bin2ADCvoltage(binary):
    return 5.1 * float(binary) / 4096

'''
理論値
250lbf = 1112.06 N について，5.1* 20 * 1e-3 V の出力が得られる
'''
def bin2Thrust(binary):
    sensorOutputVoltage = bin2ADCvoltage(binary)/47.0
    return 1112.06 * sensorOutputVoltage / (5.1 * 20.0 * 1e-3) # N

'''
実験値
ADCの値 x に対して，力 y[N] は，y = 0.5952 * x - 20.177
'''
def bin2ThrustTest(binary):
    return 0.5952 * binary - 20.177


def bin2dataPressure(binary):
    sensorOutputVoltage = 2.0 * bin2ADCvoltage(binary)
    return sensorOutputVoltage * 1e6 # Nm^-2

def bin2dataTempHigh(binary):
    R = 10000
    return bin2dataTemp(binary,R)

def bin2dataTempLow(binary):
    R = 1000
    return bin2dataTemp(binary,R)

def bin2dataTemp(binary,R):
    if(binary == 0):
        return -273
    Voltage = bin2ADCvoltage(binary)
    return 1/(1/(25+273)+math.log(((Voltage/(5.1-Voltage))*R)/10000)/4126)-273


if __name__ == "__main__":
    args = sys.argv
    main(args[1],args[2])