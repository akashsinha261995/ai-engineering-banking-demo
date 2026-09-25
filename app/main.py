from agent import CustomerAgent
from logging_config import setup_logging

def main():
    setup_logging()

    agent = CustomerAgent()

    print("Customer AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        token = input("Enter access token: ").strip()

        answer = agent.run(
            user_input,
            token
        )

        #answer = agent.run(user_input)

        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    main()