#Classe che viene utilizzata da Analytics controller per fornire un output strutturato
class ReportSum:
    __nave_code_1 = ""
    __nave_code_2 = ""
    __report = {}

    def __init__(self, nave_1, nave_2, report):
        self.__nave_code_1 = nave_1
        self.__nave_code_2 = nave_2
        self.__report = report

    def getNave_1(self):
        return self.__nave_code_1

    def getNave_2(self):
        return self.__nave_code_2

    def getReport(self):
        return self.__report

