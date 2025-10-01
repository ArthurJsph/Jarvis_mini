import datetime
import random

class PluginManager:
    def __init__(self):
        self.jokes = [
            "Por que o computador foi ao médico? Porque estava com um vírus!",
            "Qual é o computador favorito dos matemáticos? O Excel!",
            "Por que o programador confunde Halloween com Natal? Porque OCT 31 == DEC 25.",
            "O que é que um bit disse para o outro? Você me completa."
        ]
        self.commands = {
            "data_atual": self.get_current_datetime,
            "piada": self.tell_joke,
            "previsao_tempo": self.get_weather,
            "ajuda": self.list_commands,
            "hora": self.get_current_time,
            "saudacao": self.say_hello
        }

    def execute_command(self, command, params=None):
        func = self.commands.get(command)
        if func:
            return func(params)
        else:
            return f"Ops! Comando '{command}' desconhecido. Use 'ajuda' para ver os comandos disponíveis."

    def get_current_datetime(self, params=None):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def get_current_time(self, params=None):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def tell_joke(self, params=None):
        return random.choice(self.jokes)

    def get_weather(self, params=None):
        location = params.get("location") if params else None
        if not location:
            return "Por favor, informe a localização para a previsão do tempo."
        return f"A previsão do tempo para {location} é: céu parcialmente nublado, 25°C."

    def list_commands(self, params=None):
        cmds = ", ".join(sorted(self.commands.keys()))
        return f"Comandos disponíveis: {cmds}"

    def say_hello(self, params=None):
        return "Olá! Como posso ajudar você hoje?"
