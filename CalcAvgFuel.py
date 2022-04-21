import obd
import time

connection = obd.OBD()

a = 7.718
b = 0.425143707

#b = mpg to kml
#constants


sum = 0
count = 0
kmWithEngineOn = 0
Lastkm = 0

def checkDsitance():
    cmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
    vs = connection.query(cmd).value.magnitude
    return vs

startingDistance = checkDsitance()
#initial destance

def GetCurrFuel():
    cmd = obd.commands.SPEED
    vs = connection.query(cmd).value.magnitude
    #vs = speed


    cmd = obd.commands.SPEED
    MAF = connection.query(cmd).value.magnitude
    # MAF = mass air flow in g/s

    ret = ((vs*a)/MAF)*b
    return ret

def checkIsOn():
    cmd = obd.commands.RPM
    vs = connection.query(cmd).value.magnitude
    if vs>0:
        return True
    else:
        return False


while(True):
    if checkIsOn():
        sum += GetCurrFuel()
        count += 1
        kmWithEngineOn += int(checkDsitance()) - Lastkm
    Lastkm = int(checkDsitance())
    try:
        print(f"FUEL: {(sum/count*kmWithEngineOn/int(checkDsitance()))}")
    except:
        pass
    time.sleep(0.5)










