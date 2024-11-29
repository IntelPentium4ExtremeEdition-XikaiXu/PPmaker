class ParameterManager:
    def __init__(self):
        self.__lrl = 60
        self.__url = 120
        self.__msr = 120
        self.__fixed_av_delay = 150
        self.__atrial_amplitude = 5
        self.__ventricular_amplitude = 5
        self.__atrial_pulse_width = 1
        self.__ventricular_pulse_width = 1
        self.__atrial_sensitivity = 0.1
        self.__ventricular_sensitivity = 0.1
        self.__arp = 250
        self.__vrp = 320
        self.__pvarp = 250
        self.__hysteresis = 0
        self.__rate_smoothing = 0
        self.__activity_threshold = 1.6 # Med
        self.__reaction_time = 30
        self.__response_factor = 8
        self.__recovery_time = 300  # sec = 5 min

    def getLowerRateLimit(self):
        return self.__lrl

    def getUpperRateLimit(self):
        return self.__url

    def getMaximumSensorRate(self):
        return self.__msr

    def getFixedAVDelay(self):
        return self.__fixed_av_delay

    def getAtrialAmplitude(self):
        return self.__atrial_amplitude if self.__atrial_amplitude != 0 else 0

    def getVentricularAmplitude(self):
        return self.__ventricular_amplitude if self.__ventricular_amplitude != 0 else 0

    def getAtrialPulseWidth(self):
        return self.__atrial_pulse_width

    def getVentricularPulseWidth(self):
        return self.__ventricular_pulse_width

    def getAtrialSensitivity(self):
        return self.__atrial_sensitivity

    def getVentricularSensitivity(self):
        return self.__ventricular_sensitivity

    def getARP(self):
        return self.__arp

    def getVRP(self):
        return self.__vrp

    def getPVARP(self):
        return self.__pvarp

    def getHysteresis(self):
        return self.__hysteresis if self.__hysteresis != 0 else 0

    def getRateSmoothing(self):
        return self.__rate_smoothing

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

    def getReactionTime(self):
        return self.__reaction_time

    def getResponseFactor(self):
        return self.__response_factor

    def getRecoveryTime(self):
        return round(self.__recovery_time / 60)

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

    def setUpperRateLimit(self, val):
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if 50 <= num <= 175 and num >= self.__lrl:
                self.__url = num
            else:
                raise IndexError
        else:
            raise TypeError

    def setMaximumSensorRate(self, val):
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if 50 <= num <= 175 and num >= self.__lrl:
                self.__msr = num
            else:
                raise IndexError
        else:
            raise TypeError

    def setFixedAVDelay(self, val):
        if self.__is_num(val):
            if 70 <= val <= 300:
                self.__fixed_av_delay = val
            else:
                raise IndexError
        else:
            raise TypeError

    def setAtrialAmplitude(self, val):
        if str(val).casefold() == 'off'.casefold():
            self.__atrial_amplitude = 0
            return
        if self.__is_num(val):
            num = round(float(val), 1)
            if num <= 5.0 and num >= 0.1:
                self.__atrial_amplitude = num
            elif round(float(val), 1) == 0:
                self.__atrial_amplitude = 0
            else:
                raise IndexError
        else:
            raise TypeError

    def setVentricularAmplitude(self, val):
        if str(val).casefold() == 'off'.casefold():
            self.__ventricular_amplitude = 0
            return
        if self.__is_num(val):
            num = round(float(val), 1)
            if num <= 5.0 and num >= 0.1:
                self.__ventricular_amplitude = num
            elif round(float(val), 1) == 0:
                self.__ventricular_amplitude = 0
            else:
                raise IndexError
        else:
            raise TypeError

    def setAtrialPulseWidth(self, val):
        if self.__is_num(val):
            if 1 <= round(float(val)) <= 30:
                self.__atrial_pulse_width = round(float(val))
            else:
                raise IndexError
        else:
            raise TypeError

    def setVentricularPulseWidth(self, val):
        if self.__is_num(val):
            if 1 <= round(float(val)) <= 30:
                self.__ventricular_pulse_width = round(float(val))
            else:
                raise IndexError
        else:
            raise TypeError

    def setAtrialSensitivity(self, val):
        if self.__is_num(val):
            if 0 <= round(float(val), 1) <= 5.0:
                self.__atrial_sensitivity = round(float(val), 1)
            else:
                raise IndexError
        else:
            raise TypeError

    def setVentricularSensitivity(self, val):
        if self.__is_num(val):
            if 0 <= round(float(val), 1) <= 5.0:
                self.__ventricular_sensitivity = round(float(val), 1)
            else:
                raise IndexError
        else:
            raise TypeError

    def setARP(self, val):
        if self.__is_num(val):
            if 150 <= int(round(float(val), -1)) <= 500:
                self.__arp = int(round(float(val), -1))
            else:
                raise IndexError
        else:
            raise TypeError

    def setVRP(self, val):
        if self.__is_num(val):
            if 150 <= int(round(float(val), -1)) <= 500:
                self.__vrp = int(round(float(val), -1))
            else:
                raise IndexError
        else:
            raise TypeError

    def setPVARP(self, val):
        if self.__is_num(val):
            if 150 <= int(round(float(val), -1)) <= 500:
                self.__pvarp = int(round(float(val), -1))
            else:
                raise IndexError
        else:
            raise TypeError

    def setHysteresis(self, val):
        if str(val).casefold() == 'off'.casefold():
            self.__hysteresis = 0
            return
        if self.__is_num(val):
            num = 5 * round(float(val) / 5)
            if 50 <= round(float(val)) <= 90 or (30 <= num <= 50) or (90 <= num <= 175):
                self.__hysteresis = num
            elif round(float(val)) == 0:
                self.__hysteresis = 0
            else:
                raise IndexError
        else:
            raise TypeError

    def setRateSmoothing(self, val):
        self.__rate_smoothing = round(float(val))

    def setActivityThreshold(self, val):
        self.__activity_threshold = float(val)

    def setReactionTime(self, val):
        if self.__is_num(val):
            num = 10 * round(float(val) / 10)
            if 10 <= num <= 50:
                self.__reaction_time = num
            else:
                raise IndexError
        else:
            raise TypeError

    def setResponseFactor(self, val):
        if self.__is_num(val):
            if 1 <= round(float(val)) <= 16:
                self.__response_factor = round(float(val))
            else:
                raise IndexError
        else:
            raise TypeError

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
