import platform
import os
import psutil
import humanfriendly
import time
from gonhang import api
from gonhang import version
from pathlib import Path
import json
import distro
import socket
from telnetlib import Telnet
import requests
import urllib.request
import subprocess
import gettext

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('gonhang', localedir, fallback=True)
_ = translate.gettext


class Temperature:

    @staticmethod
    def celtokel(C):  # Celsius para Kelvin
        K = (C + 273.15)
        return '{K:.2f}'.format(K=K)

    @staticmethod
    def celtofah(C):  # Celsius para Fahrenheit
        F = (C * 1.8 + 32)
        return '{F:.2f}'.format(F=F)

    @staticmethod
    def keltocel(K):  # Kelvin para Celsius
        C = (K - 273.15)
        return '{C:.2f}'.format(C=C)

    @staticmethod
    def keltofah(K):  # Kelvin para Fahrenheit
        F = (K * 1.8 - 459.7)
        return '{F:.2f}'.format(F=F)

    @staticmethod
    def fahtocel(F):  # Fahrenheit para Celsius
        C = ((F - 32) / 1.8)
        return '{C:.2f}'.format(C=C)

    @staticmethod
    def fahtokel(F):  # Fahrenheit para Kelvin
        K = ((F - 32) / 1.8 + 273)
        return '{K:.2f}'.format(K=K)


class VirtualMachine:
    @staticmethod
    def getStatus():
        outCmd = subprocess.getoutput('systemd-detect-virt')
        if 'none' in outCmd:
            return False
        else:
            return True


# The Keys to store in Config
class KeysSkeleton:
    cpuTempOption = dict(
        {
            'cpuTempOption': {
                'index': 0,
                'subIndex': 0,
                'enabled': False
            }
        }
    )

    positionOption = dict(
        {
            'positionOption': {
                'index': 0,
                'value': 'Left'
            }
        }
    )

    nvidiaOption = dict(
        {
            'nvidiaOption': {
                'GpuId': '',
                'enabled': False
            }
        }
    )

    netOption = dict(
        {
            'netOption': {
                'interface': '',
                'enabled': False
            }
        }
    )

    storTempsOption = dict(
        {
            'storTempsOption': {
                'devices': list(),
                'enabled': False
            }
        }
    )

    partitionsOption = dict(
        {
            'partitionsOption': {
                'partitions': list(),
                'enabled': False
            }
        }
    )

    weatherOption = dict(
        {
            'weatherOption': {
                'lat': '',
                'lon': '',
                'apiKey': '',
                'updateTime': 30,
                'validated': False,
                'enabled': False

            }
        }
    )


class PlatFormUtil:
    plat = platform.uname()

    def getRelease(self):
        return self.plat.release

    def getNode(self):
        return self.plat.node

    def getMachine(self):
        return self.plat.machine


class DistroUtil:
    distrosDir = f'{os.path.dirname(__file__)}/images/distros'

    @staticmethod
    def getDistroStr():
        distroStr = f"{distro.name()} {distro.version()}"
        if not distro.codename() == '':
            distroStr = f"{distroStr} {distro.codename()}"

        return distroStr

    def getDistroIcon(self):
        iconFile = f'{self.distrosDir}/{distro.id()}.png'
        if os.path.isfile(iconFile):
            return iconFile
        else:
            return f'{self.distrosDir}/generic.png'


class Config:
    globalJson = dict()
    version = version.Version()
    # Config file
    cfgFile = f'{Path.home()}/.config/gonhang/config.json'

    def __init__(self):
        if not self.cfgFileExists():
            print(_('Config file not found, creating....'))
            self.createConfigFile()

        self.loadGlobalConfig()

    def createConfigFile(self):
        if not os.path.isdir(os.path.dirname(self.cfgFile)):
            os.makedirs(os.path.dirname(self.cfgFile))

        self.writeGlobalConfig()

    def cfgFileExists(self):
        if os.path.isfile(self.cfgFile):
            return True
        else:
            return False

    def loadGlobalConfig(self):
        self.globalJson.clear()
        with open(self.cfgFile, 'r') as openfile:
            json_object = json.load(openfile)

        self.updateConfig(json_object)

    def writeGlobalConfig(self):
        # Serializing json
        json_object = json.dumps(self.globalJson, indent=4)
        with open(self.cfgFile, 'w') as outfile:
            outfile.write(json_object)

    def updateConfig(self, data):
        self.globalJson.update(data)
        self.writeGlobalConfig()

    def getKey(self, key):
        try:
            return self.globalJson[key]
        except KeyError:
            # print(f'Key not found in {self.cfgFile}: key ====> {key}')
            return None

    def getVersion(self):
        return self.version.getVersion()


class System:
    message = dict()
    distroUtil = DistroUtil()
    platformUtil = PlatFormUtil()
    config = Config()

    def getMessage(self):
        self.message.clear()
        # ---------------------------------------------------------------------------------
        # Update distro Info
        # ---------------------------------------------------------------------------------
        self.message['distroIcon'] = self.distroUtil.getDistroIcon()
        self.message['distroStr'] = self.distroUtil.getDistroStr()
        self.message['release'] = self.platformUtil.getRelease()
        self.message['node'] = self.platformUtil.getNode()
        self.message['machine'] = self.platformUtil.getMachine()

        cpuFreq = psutil.cpu_freq()
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.message['cpuFreqCurrent'] = '{:.0f}'.format(cpuFreq.current)
        self.message['cpuFreqMax'] = '{:.0f}'.format(cpuFreq.max)

        ramUsed = ram.total - ram.available

        self.message['ramUsed'] = '{}'.format(humanfriendly.format_size(ramUsed, binary=True))
        self.message['ramTotal'] = '{}'.format(humanfriendly.format_size(ram.total, binary=True))

        self.message['swapUsed'] = '{}'.format(humanfriendly.format_size(swap.used, binary=True))
        self.message['swapTotal'] = '{}'.format(humanfriendly.format_size(swap.total, binary=True))

        self.message['cpuProgressBar'] = psutil.cpu_percent(percpu=False)
        self.message['ramProgressBar'] = ram.percent
        self.message['swapProgressBar'] = swap.percent

        # Get boot time
        btDays, btHours, btMinutes, btSeconds = self.getUptime()
        self.message['btDays'] = btDays
        self.message['btHours'] = btHours
        self.message['btMinutes'] = btMinutes
        self.message['btSeconds'] = btSeconds

        if self.isToDisplayCpuTemp():
            cpuTempOption = self.config.getKey('cpuTempOption')
            cpuSensors = psutil.sensors_temperatures()
            for index, sensor in enumerate(cpuSensors):
                for subIndex, shwtemp in enumerate(cpuSensors[sensor]):
                    if index == int(cpuTempOption['index']) and subIndex == int(cpuTempOption['subIndex']):
                        self.message['cpuTempProgressBar'] = int(shwtemp.current)
                        self.message['cpuCurrentTempLabel'] = '{:.1f}'.format(shwtemp.current)
                        self.message['cpuTempLabel'] = shwtemp.label

        return self.message

    def isToDisplayCpuTemp(self):
        if VirtualMachine.getStatus():
            return False
        cpuTempOption = self.config.getKey('cpuTempOption')
        if cpuTempOption is None:
            return False
        else:
            if cpuTempOption['enabled']:
                return True
            else:
                return False

    @staticmethod
    def getUptime():
        bootTime = time.time() - psutil.boot_time()
        days = bootTime // (24 * 3600)
        bootTime = bootTime % (24 * 3600)
        hours = bootTime // 3600
        bootTime %= 3600
        minutes = bootTime // 60
        bootTime %= 60
        seconds = bootTime
        return [int(days), int(hours), int(minutes), int(seconds)]

    @staticmethod
    def getCpuModelName():
        output = subprocess.getoutput('cat /proc/cpuinfo')
        # regex = re.compile(r'[\t]')
        # output = regex.sub('', output)
        modelName = ''
        output = api.StringUtil.removeString(r'[\t]', output)
        lines = output.split('\n')
        for line in lines:
            if 'model name:' in line:
                modelName = api.StringUtil.removeString(r'model name: ', line)
                break

        return modelName


class Nvidia:
    config = Config()
    smiCommand = 'nvidia-smi'
    # , nounits
    smiSuffixCommand = '--format=csv,noheader'
    smiStatus = 1
    nvidiaEntity = dict()

    def __init__(self):
        if self.getSmiStatus():
            count, DriverVersion = self.getOutputCommand('count,driver_version')
            self.nvidiaEntity.update(
                {
                    'count': int(count),
                    'driver_version': DriverVersion,
                    'gpus': self.getGPUsInfo()
                }
            )

    def getNumberGPUs(self):
        if self.getSmiStatus():
            return int(self.getOutputCommand('count')[0])
        else:
            return 0

    def getGPUsInfo(self):

        message = dict()
        if self.getNumberGPUs() > 0:
            gpu_uuid, gpu_name, display_mode, driver_version, vbios_version, fan_speed, pstate, memory_total, memory_used, memory_free, temperature_gpu, power_management, power_draw, clocks_current_graphics, clocks_current_sm, clocks_current_memory, clocks_current_video, utilization_gpu = self.getOutputCommand(
                'gpu_uuid,gpu_name,display_mode,driver_version,vbios_version,fan.speed,pstate,memory.total,memory.used,memory.free,temperature.gpu,power.management,power.draw,clocks.current.graphics,clocks.current.sm,clocks.current.memory,clocks.current.video,utilization.gpu'
            )

            message.update(
                {
                    'gpu_uuid': gpu_uuid,
                    'gpu_name': gpu_name,
                    'display_mode': display_mode,
                    'driver_version': driver_version,
                    'vbios_version': vbios_version,
                    'fan_speed': fan_speed,
                    'pstate': pstate,
                    'memory_total': memory_total,
                    'memory_used': memory_used,
                    'memory_free': memory_free,
                    'temperature_gpu': float(temperature_gpu),
                    'temperature_gpu_high': 70.0,
                    'temperature_gpu_critical': 85.0,  # 40% above
                    'temperature_scale': 'C',
                    'power_management': power_management,
                    'power_draw': power_draw,
                    'clocks_current_graphics': clocks_current_graphics,
                    'clocks_current_sm': clocks_current_sm,
                    'clocks_current_memory': clocks_current_memory,
                    'clocks_current_video': clocks_current_video,
                    'utilization_gpu': utilization_gpu
                }
            )

        return message

    def getOutputCommand(self, queryList):
        return subprocess.getoutput(f"{self.smiCommand} --id=0 --query-gpu={queryList} {self.smiSuffixCommand}").split(
            ',')

    def getSmiStatus(self):
        self.smiStatus = self.runCommand(f'which {self.smiCommand}')[0]
        if self.smiStatus == 0:
            return True
        else:
            return False

    def isToDisplayNvidia(self):
        nvidiaOptionConfig = self.config.getKey('nvidiaOption')
        if nvidiaOptionConfig is None:
            return False
        else:
            if nvidiaOptionConfig['enabled'] and nvidiaOptionConfig['GpuId'] != '':
                return True
            else:
                return False

    @staticmethod
    def runCommand(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        std_out, std_err = proc.communicate()
        return proc.returncode, std_out, std_err


class Net:
    config = Config()
    message = dict()

    def __init__(self):
        pass

    @staticmethod
    def getIOCounters(interface):
        return psutil.net_io_counters(pernic=True)[interface]

    def getMessage(self):
        netOptionConfig = self.config.getKey('netOption')
        if netOptionConfig['enabled'] and (netOptionConfig['interface'] != '') and self.isOnline():
            return self.message

    @staticmethod
    def isOnline():
        try:
            socket.create_connection(("8.8.8.8", 53))
            return True
        except OSError:
            return False

    def isToDisplayNet(self):
        netOptionConfig = self.config.getKey('netOption')
        if netOptionConfig is None:
            return False

        if netOptionConfig['enabled'] and (netOptionConfig['interface'] != '') and self.isOnline():
            return True
        else:
            return False


class StorTemps:
    config = Config()
    message = list()
    keys = KeysSkeleton()

    def getMessage(self):
        self.message.clear()
        storTempsConfig = self.config.getKey('storTempsOption')
        for device in storTempsConfig['devices']:
            self.message.append(self.findDataFromDevice(device['device'], device['label']))

        return self.message

    def findDataFromDevice(self, device, label):
        deviceArray = list()
        # print(f'finding data from [{device}] with label [{label}]')
        sensors = psutil.sensors_temperatures()
        for i, sensor in enumerate(sensors):
            # print(f'index {i} sensor {sensor}')
            if (sensor == device) and (sensors[sensor][i].label == label):
                deviceArray.append({
                    'device': device,
                    'label': label,
                    'temperature': sensors[sensor][i].current
                })

        # maybe hddtemp
        if self.hddtempIsOk():
            with Telnet('127.0.0.1', 7634) as tn:
                lines = tn.read_all().decode('utf-8')

            if lines != '':
                data = lines
                # remove first char
                data = data[1:]
                # remove the last char
                data = ''.join([data[i] for i in range(len(data)) if i != len(data) - 1])
                # replace double || by one |
                data = data.replace('||', '|')
                # convert to array
                data = data.split('|')
                dataLen = len(data)
                forLenght = int(dataLen / 4)

                newarray = self.chunkIt(data, forLenght)
                for na in newarray:
                    if (device == na[0]) and (label == na[1]):
                        deviceArray.append({
                            'device': na[0],
                            'label': na[1],
                            'temperature': na[2]
                        })

        # print(deviceArray)
        return deviceArray

    @staticmethod
    def hddtempIsOk():
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ('127.0.0.1', 7634)
        result_of_check = a_socket.connect_ex(location)
        a_socket.close()
        if result_of_check == 0:
            return True
        else:
            return False

    @staticmethod
    def chunkIt(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    def isToDisplay(self):
        storTempsOptionConfig = self.config.getKey('storTempsOption')
        if storTempsOptionConfig is None:
            return False

        if storTempsOptionConfig['enabled'] and (len(storTempsOptionConfig['devices']) > 0):
            return True
        else:
            return False


class Partitions:
    config = Config()
    message = list()
    keys = KeysSkeleton()

    def getMessage(self):
        self.message.clear()
        partitionsOptionConfig = self.config.getKey('partitionsOption')
        for partition in partitionsOptionConfig['partitions']:
            usage = psutil.disk_usage(partition['mountpoint'])
            # print(partition)
            # print(usage)
            self.message.append(
                {
                    'partition': partition['partition'],
                    'mountpoint': partition['mountpoint'],
                    'fstype': partition['fstype'],
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            )

        return self.message

    def isToDisplay(self):
        partitionsOptionConfig = self.config.getKey('partitionsOption')
        if partitionsOptionConfig is None:
            return False

        if partitionsOptionConfig['enabled'] and (len(partitionsOptionConfig['partitions']) > 0):
            return True
        else:
            return False


class Weather:
    config = Config()
    temperature = Temperature()
    net = Net()
    url = ''
    iconUrlPrefix = 'https://openweathermap.org/img/wn/'
    iconUrlSuffix = '@2x.png'
    message = dict()
    keysSkeleton = KeysSkeleton()

    def updateUrl(self, lat, lon, apiKey):
        self.url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}'

    def getMessage(self):
        self.loadConfig()
        # print(self.keysSkeleton.weatherOption)
        self.message.clear()
        self.message['statusCode'] = 0
        validated = False
        if self.net.isOnline():
            # print(f"self.url ===> {self.url}")
            res = requests.get(self.url)
            if res.status_code == 200:
                tempJson = json.loads(res.text)
                # print(tempJson)
                self.message['temp'] = int(float(self.temperature.keltocel(tempJson['main']['temp'])))
                self.message['humidity'] = f"{tempJson['main']['humidity']}%"
                self.message['pressure'] = f"{tempJson['main']['pressure']}hPa"
                self.message['visibility'] = '{:.1f}Km'.format(int(tempJson['visibility']) / 1000)
                self.message['wind'] = '{} m/s {}'.format(
                    tempJson['wind']['speed'],
                    self.degToCompass(tempJson['wind']['deg'])
                )
                self.message['name'] = tempJson['name']
                self.message['statusCode'] = 200
                self.message['statusText'] = f'http code {res.status_code} OK!'
                self.message['icon'] = tempJson['weather'][0]['icon']
                self.message['country'] = ''
                if self.message['name'] == '':
                    self.message['statusCode'] = 0
                    self.message['statusText'] = f'Error: Latitude and Longitude not found!'
                else:
                    self.message['country'] = tempJson['sys']['country']
                    validated = True

            else:
                self.message['statusText'] = f'ERROR: http code {res.status_code}!'
        else:
            self.message['statusText'] = 'ERROR: You are offline?'

        self.message['validated'] = validated
        return self.message

    def loadConfig(self):
        weatherOptionConfig = self.config.getKey('weatherOption')
        lat = ''
        lon = ''
        updateTime = 30
        apiKey = ''
        enabled = False
        validated = False
        if not (weatherOptionConfig is None):
            lat = weatherOptionConfig['lat']
            lon = weatherOptionConfig['lon']
            updateTime = weatherOptionConfig['updateTime']
            apiKey = weatherOptionConfig['apiKey']
            validated = weatherOptionConfig['validated']
            enabled = weatherOptionConfig['enabled']

        self.updateUrl(lat, lon, apiKey)
        self.updateWeatherOption(lat, lon, updateTime, apiKey, validated, enabled)

    def isToDisplay(self):
        self.loadConfig()
        if self.keysSkeleton.weatherOption['weatherOption']['enabled'] and \
                self.keysSkeleton.weatherOption['weatherOption']['validated']:
            return True
        else:
            return False

    def getIcon(self, iconStr):
        if self.net.isOnline():
            with urllib.request.urlopen(f"{self.iconUrlPrefix}{iconStr}{self.iconUrlSuffix}") as response:
                return response.read()

    @staticmethod
    def degToCompass(num):
        val = int((num / 22.5) + .5)
        arr = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        return arr[(val % 16)]

    def updateWeatherOption(self, lat, lon, updateTime, apiKey, validated, enabled):
        self.keysSkeleton.weatherOption.clear()
        self.keysSkeleton.weatherOption.update(
            {
                'weatherOption': {
                    'lat': lat,
                    'lon': lon,
                    'updateTime': updateTime,
                    'apiKey': apiKey,
                    'validated': validated,
                    'enabled': enabled

                }
            }
        )
