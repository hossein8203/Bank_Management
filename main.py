from functions import create, show_all, search, incr, decr, remove, update

actions = {
    "create": create,
    "show": show_all,
    "search": search,
    "update":update,
    "increase": incr,
    "decrease": decr,
    "remove": remove,
    "exit": ''
}

if __name__ == "__main__":
    while True:
        for index, action in enumerate(actions):
            print(f"{index+1}.{action}".title())

        action = input("Enter Action: ").lower()

        if action not in actions:
            print(f"Action '{action}' not found !")
            continue
        if action == "exit":
            print("GoodBye !")
            break

        actions[action]()
