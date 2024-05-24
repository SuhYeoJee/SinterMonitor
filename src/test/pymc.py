import pymcprotocol

#If you use Q series PLC
pymc3e = pymcprotocol.Type3E()
pymc3e.connect("192.168.0.142", 1400)

bitunits_values = pymc3e.batchread_bitunits(headdevice="M46", readsize=1)
print(bitunits_values)