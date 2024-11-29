class ParamEnum:
    def __init__(self):
        #default val
        self.__amplitude = 100
        self.__lrl = 60
        self.__pulse_width = 0.4
        self.__threshold = 66
        self.__arp = 320
        self.__vrp = 320
        self.__url = 120        
        self.__msr = 120
        self.__activity_threshold = 1.1 # Med
        self.__response_factor = 8
        self.__reaction_time = 10
        self.__recovery_time = 30  # sec = 5 min
        
    def getAmplitude(self):
        return self.__amplitude if self.__amplitude != 0 else 0

    def getLowerRateLimit(self):
        return self.__lrl
    
    def getPulseWidth(self):
        return self.__pulse_width
    
    def getthresholf(self):
        return self.__threshold
    
    def getARP(self):
        return self.__arp
    def getVRP(self):
        return self.__vrp
    def getUpperRateLimit(self):
        return self.__url
    def getMSR(self):
        return self.__msr
    def getActivityThreshold(self):
        if self.__activity_threshold - 1.13 < 0.01:
            return 'V-L'
        elif self.__activity_threshold - 1.25 < 0.01:
            return 'L'
        elif self.__activity_threshold - 1.4 < 0.01:
            return 'M-L'
        elif self.__activity_threshold - 1.6 < 0.01:
            return 'M'
        elif self.__activity_threshold == 2:
            return 'M-H'
        elif self.__activity_threshold - 2.4 < 0.01:
            return 'H'
        elif self.__activity_threshold == 3:
            return 'V-H'
        return 0    
    def getResponseFactor(self):
        return self.__response_factor
    def getReactionTime(self):
        return self.__reaction_time
    def getRecoveryTime(self):
        return round(self.__recovery_time / 60)

    #set amp
    def setAmplitude(self, val):
        if str(val).casefold() == 'off'.casefold():
            self.__amplitude = 0
            return
        if self.__is_num(val):
            num = round(float(val), 1)
            if num <= 5.0 and num >= 0.1:
                self.__amplitude = num
            elif round(float(val), 1) == 0:
                self.__amplitude = 0
            else:
                raise IndexError
        else:
            raise TypeError
        
    #set lrl
    def setLowerRateLimit(self, val):
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if round(float(val)) <= 90 and round(float(val)) >= 50:
                self.__lrl = round(float(val))
            elif (num <= 50 and num >= 30) or (num <= 175 and num >= 90):
                self.__lrl = num
            else:
                raise IndexError
        else:
            raise TypeError
    
    #set p_w    
    def setPulseWidth(self, val):
        if self.__is_num(val):
            if 0 <= round(float(val)) <= 50:
                self.__pulse_width = round(float(val))
            else:
                raise IndexError
        else:
            raise TypeError

    #set threshold
    def setThreshold(self,val):
        if self.__is_num(val):
            self.__threshold = val
        else:
            raise IndexError
        
    #set arp
    def setARP(self, val):
        if self.__is_num(val):
            if 150 <= int(round(float(val), -1)) <= 500:
                self.__arp = int(round(float(val), -1))
            else:
                raise IndexError
        else:
            raise TypeError   
    
    #set vrp
    def setVRP(self, val):
        if self.__is_num(val):
            if 150 <= int(round(float(val), -1)) <= 500:
                self.__vrp = int(round(float(val), -1))
            else:
                raise IndexError
        else:
            raise TypeError
    
    #set url
    def setUpperRateLimit(self, val):
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if 50 <= num <= 175 and num >= self.__lrl:
                self.__url = num
            else:
                raise IndexError
        else:
            raise TypeError
        
    #set msr
    def setMaximumSensorRate(self, val):
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if 50 <= num <= 175 and num >= self.__lrl:
                self.__msr = num
            else:
                raise IndexError
        else:
            raise TypeError
        
    #setActivityThreshold
    def setActivityThreshold(self, val):
        self.__activity_threshold = float(val)

    #set spf
    def setResponseFactor(self, val):
        if self.__is_num(val):
            if 1 <= round(float(val)) <= 16:
                self.__response_factor = round(float(val))
            else:
                raise IndexError
        else:
            raise TypeError

    #set reaction time
    def setReactionTime(self, val):
        if self.__is_num(val):
            num = 10 * round(float(val) / 10)
            if 10 <= num <= 50:
                self.__reaction_time = num
            else:
                raise IndexError
        else:
            raise TypeError

    #set recovery time 
    def setRecoveryTime(self, val):
        if self.__is_num(val):
            if 2 <= round(float(val)) <= 16:
                self.__recovery_time = round(float(val)) * 60
            else:
                raise IndexError
        else:
            raise TypeError

    def __is_num(self, s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True
