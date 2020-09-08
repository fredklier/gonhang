import platform
import os
import psutil
import humanfriendly
import time
import subprocess
from gonhang import api
from pathlib import Path
import json
import distro
import socket


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
    # Config file
    cfgFile = f'{Path.home()}/.config/gonhang/config.json'

    def __init__(self):
        if not self.cfgFileExists():
            print('Config file not found, creating....')
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
            print(f'Key not found in {self.cfgFile}: key ====> {key}')
            return None

    @staticmethod
    def getVersion():
        return '0.0.1'


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

        return self.message

    def isToDisplayCpuTemp(self):
        cpuTempOption = self.config.getKey('cpuTempOption')
        if cpuTempOption is None:
            isDisplay = False
        else:
            if cpuTempOption['enabled']:
                isDisplay = True
            else:
                isDisplay = False

        return isDisplay

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
    smiStatus = subprocess.getstatusoutput(smiCommand)[0]
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
        numGPUS = int(self.getOutputCommand('count')[0])
        message = dict()
        if numGPUS > 0:
            gpu_uuid, gpu_name, display_mode, vbios_version, fan_speed, pstate, memory_total, memory_used, memory_free, temperature_gpu, power_management, power_draw, clocks_current_graphics, clocks_current_sm, clocks_current_memory, clocks_current_video, utilization_gpu = self.getOutputCommand(
                'gpu_uuid,gpu_name,display_mode,vbios_version,fan.speed,pstate,memory.total,memory.used,memory.free,temperature.gpu,power.management,power.draw,clocks.current.graphics,clocks.current.sm,clocks.current.memory,clocks.current.video,utilization.gpu'
            )

            message.update(
                {
                    'gpu_uuid': gpu_uuid,
                    'gpu_name': gpu_name,
                    'display_mode': display_mode,
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
        if self.smiStatus == 0:
            return True
        else:
            return False

    def isToDisplayNvidia(self):
        nvidiaOptionConfig = self.config.getKey('nvidiaOption')
        isDisplay = False
        if nvidiaOptionConfig is None:
            isDisplay = False
        else:
            if nvidiaOptionConfig['enabled'] and nvidiaOptionConfig['GpuId'] != '':
                isDisplay = True
            else:
                isDisplay = False

        return isDisplay


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
        isDisplay = False
        if not (netOptionConfig is None):
            if netOptionConfig['enabled'] and (netOptionConfig['interface'] != '') and self.isOnline():
                isDisplay = True
            else:
                isDisplay = False

        return isDisplay
