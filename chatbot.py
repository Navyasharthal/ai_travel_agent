from planner_agent import interpret_user_query

def main():
    print("\U0001F4AC Welcome to AI Travel Assistant!")
    while True:
        user_input = input("\U0001F9F3 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Safe travels! Bye!")
            break
        result = interpret_user_query(user_input)
        print("\U0001F916 AI:", result)

if __name__ == "__main__":
    main()


