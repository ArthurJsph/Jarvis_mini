import sys
import os
from agent.core import AgentCore

def clear_console():
    """Limpa a tela do terminal para Windows, Linux e Mac."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    print("Jarvis iniciado. Digite 'sair' para encerrar.")
    print("Digite 'ajuda' para ver comandos especiais disponíveis.")

def run_console_chat():
    agent = AgentCore()
    print_welcome_message()

    while True:
        try:
            user_input = input("Você: ").strip()
            if not user_input:
                continue  # Ignora entradas vazias

            if user_input.lower() in ("sair", "exit", "quit"):
                print("Jarvis: Até logo! Foi um prazer ajudar você.")
                break

            if user_input.lower() == "limpar":
                clear_console()
                continue

            if user_input.lower() == "ajuda":
                print("Comandos especiais:")
                print("  sair, exit, quit : encerra o Jarvis")
                print("  limpar           : limpa a tela do terminal")
                print("  ajuda            : exibe essa mensagem de ajuda")
                continue

            response = agent.get_response(user_input)
            print(f"Jarvis: {response}")

        except KeyboardInterrupt:
            print("\nJarvis: Até logo! Encerrando a conversa.")
            break
        except Exception as e:
            print(f"Jarvis: Ocorreu um erro inesperado: {e}")
            # Opcional: log do erro para debug
            # import traceback; traceback.print_exc()

if __name__ == "__main__":
    run_console_chat()
