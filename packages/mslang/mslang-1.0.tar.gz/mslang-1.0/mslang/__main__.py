import inspect

class MyInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, code):
        lines = code.split('\n')
        for line in lines:
            self.execute(line)

    def execute(self, line):
        if line.startswith("퉷"):
            self.print_output(line)
        elif line.startswith("정신집중"):
            self.store_variable(line)
        elif line.startswith("어떻게"):
            pass
        elif line.startswith("이 코드냐ㅋㅋ"):
            exit()
        elif line.startswith("빙글빙글돌아가는"):
            self.repeat(line)
        elif line.startswith(".--. .-.. ..- ..."):
            self.add(line)
        elif line.startswith("변수는 제거해야되"):
            self.subtract(line)
        elif line.startswith("변수독재정치코드"):
            self.set_value(line)
        else:
            print(f"뭔 코드냐 ㅋㅋ - {line}")

    def print_output(self, line):
        _, output = line.split("퉷 ")
        variable_name = output.strip('()')
        if variable_name in self.variables:
            print(self.variables[variable_name])
        else:
            print(f"뭔 변수냐 ㅋㅋ - {variable_name}")

    def store_variable(self, line):
        _, assignment = line.split("정신집중 ")
        variable, value = assignment.split(" = ")
        self.variables[variable] = value

    def repeat(self, line):
        _, rest = line.split("빙글빙글돌아가는 ")
        count, code_to_repeat = rest.split(" ", 1)
        count = int(count)
        for _ in range(count):
            self.run(code_to_repeat)

    def add(self, line):
        _, rest = line.split(".--. .-.. ..- ... ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            current_value = self.variables[variable]
            try:
                current_value = int(current_value)
                value = int(value)
                result = current_value + value
            except ValueError:
                result = current_value + value

            self.variables[variable] = result
        else:
            print(f"{variable}이 뭐냐ㅋㅋ")

    def subtract(self, line):
        _, rest = line.split("변수는 제거해야되 ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            current_value = self.variables[variable]
            try:
                current_value = int(current_value)
                value = int(value)
                result = current_value - value
                self.variables[variable] = result
            except ValueError:
                print(f"그게 되겠냐 ㅋㅋ")
        else:
            print(f"{variable}이 뭐냐ㅋㅋ.")

    def set_value(self, line):
        _, rest = line.split("변수독재정치코드 ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            self.variables[variable] = value
        else:
            print(f"{variable}이 뭐냐ㅋㅋ")

def run_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
        interpreter = MyInterpreter()

        if "어떻게" not in code:
            print("이게 무슨 세찐찐이랭이냐")
            return

        if "뭔소리냐ㅋㅋ" not in code:
            print("이게 무슨 세찐찐이랭이냐")
            return

        interpreter.run(code)
