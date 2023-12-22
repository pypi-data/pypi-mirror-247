import subprocess

TYPES = {
    "returnCode": 0,
    "stdoutValue": 1,
}

class test:
    def __init__(self, shouldBe, type):
        self.shouldBe = shouldBe
        self.type = type

    def checkStdout(self, pipe):
        if not self.type == 1:
            return

        for line in pipe.communicate():
            print(line.decode())

class tester:
    def __init__(self, execPath):
        self.execPath = execPath
        self.tests = []

    def run(self):
        return subprocess.Popen([self.execPath], stdout=subprocess.PIPE)

    def test(self):
        output = self.run()
        for test in self.tests:
            test.checkStdout(output)
