from subprocess import run


SERVICE_STATUS_STOPPED = 0
SERVICE_STATUS_STARTED = 1
SERVICE_STATUS_ERROR = 2

class Service:
    def __init__(self, name):
        self.name = name

    def status(self):
        try:
            process = run(['systemctl', 'status', self.name], capture_output=True)
            output = process.stdout.decode()
            if "Active: active (running)" in output:
                return SERVICE_STATUS_STARTED
            else:
                return SERVICE_STATUS_STOPPED
        except OSError:
            return SERVICE_STATUS_ERROR

    def start(self):
        try:
            process = run(['systemctl', 'start', self.name])
            return process.returncode == 0
        except OSError:
            return False


    def stop(self):
        try:
            process = run(['systemctl', 'stop', self.name])
            return process.returncode == 0
        except OSError:
            return False


class MemoryUsage:
    def __init__(self, total, free, used, cache):
        self.total = total
        self.free = free
        self.used = used
        self.cache = cache


def get_memory():
    try:
        process = run(['top ', '-bn1'], capture_output=True)
        for line in process.stdout.decode():
            if "Mem :" in line:
                i = line.index(':')
                line = line[i+1:]

                i = line.index(' total,')
                total = float(line[:i])
                i += len(' total,')
                line = line[i+1:]

                i = line.index(' free,')
                free = float(line[:i])
                i += len(' free,')
                line = line[i+1:]

                i = line.index(' used,')
                used = float(line[:i])
                i += len(' used,')
                line = line[i+1:]

                i = line.index(' buff')
                cache = float(line[:i])

                return MemoryUsage(total, free, used, cache)
    except OSError as error:
        print(error)

    return None

