import platform
import os
import distro
import psutil
import humanfriendly
import time
import subprocess
from gonhang import api
from pathlib import Path
import json


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


class System:
    message = dict()
    distroUtil = DistroUtil()
    platformUtil = PlatFormUtil()

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

        return self.message

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


class Config:
    globalJson = dict()
    # Config file
    cfgFile = f'{Path.home()}/.config/gonhang/config.json'

    def __init__(self):
        if not self.cfgFileExists():
            print('Config file not found, creating....')
            self.createConfigFile()

        self.globalJSON = self.loadGlobalConfig()

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

        return json_object

    def writeGlobalConfig(self):
        # Serializing json
        json_object = json.dumps(self.globalJson, indent=4)
        with open(self.cfgFile, 'w') as outfile:
            outfile.write(json_object)

    def updateConfig(self, data):
        self.globalJson.update(data)
        self.writeGlobalConfig()

    @staticmethod
    def getVersion():
        return '1.8.5'
