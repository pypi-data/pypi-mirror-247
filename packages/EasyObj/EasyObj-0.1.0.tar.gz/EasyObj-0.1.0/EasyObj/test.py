from rich import print


class Expect:

    '''
    expect = Expect("Add test")
    expect.toBe(3)
    expect.run(add(1, 2))
    '''

    def __init__(self, testName, showTimes=False) -> None:
        self.TestName = testName
        self.__tobe = "Expect not defined"
        self.__run = "Expect not defined"
        self.__times = 0
        self.showTimes = showTimes

    def __actualRun(self):

        self.__times += 1

        if self.__tobe == self.__run:
            if self.showTimes:
                print(f"{self.TestName} {self.__times} [green]✓[/green]")
            else:
                print(f"{self.TestName} [green]✓[/green]")
        else:
            if self.showTimes:
                print(f"{self.TestName} {self.__times} [red]×[/red]")
            else:
                print(f"{self.TestName} [red]×[/red]")
            print(f" [green]+ {self.__tobe}[/green]")
            print(f" [red]- {self.__run}[/red]")

    def toBe(self, expected):
        self.__tobe = expected

        if self.__run != "Expect not defined":
            self.__actualRun()

    def run(self, actual):
        self.__run = actual

        if self.__tobe != "Expect not defined":
            self.__actualRun()

    def _(self, actual, expected):
        self.__run = actual
        self.__tobe = expected

        self.__actualRun()
