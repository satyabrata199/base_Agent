from .base_tool import BaseTool

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluates mathematical expressions."

    def run(self, expression: str):
        return eval(expression)