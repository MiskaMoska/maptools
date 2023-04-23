from matplotlib import pyplot as plt

x = [0.05, 0.0625,	0.07, 0.08,	0.09, 0.1,	0.125	,0.15,	0.2,	0.3,	0.4	,0.5]

y1 = [53.632424,64.364007	,	66.862095, 76.19169,71.144532,73.923018		,69.23273,	60.489421	,35.381086,	2.396125,	0.560795,	0.509814]
y2 = [54.830487,  65.740505	,	78.613306, 78.613306,74.662248, 77.032883	,	79.581953,	77.593678,	81.366301,	82.462401	,82.921234,	82.76829]
y3 = [83.558501]*12
plt.plot(x,y1,label="quantized, ADC clamp")
plt.plot(x,y2,label="quantized, ADC no clamp")
plt.plot(x,y3,label="float model(not quantized)")

plt.xlabel("weight scale factor")
plt.ylabel("TOP3 ACC (%)")
plt.legend()
plt.show()