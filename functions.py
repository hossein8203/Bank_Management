import tinydb

db = tinydb.TinyDB("customers.json")
query = tinydb.Query()


# actions

def create():
    customer = {
        "national_code": '',
        "name": '',
        "family": '',
        "phone": '',
    }

    flag = True

    for index, item in enumerate(customer):
        customer[item] = input(f"type {item}: ".title()).lower()
        if len(customer[item]) == 0:
            print(f"field '{item}' can't be empty !".title())
            index -= 1
            continue
        if item == "national_code":
            ncode_exist = db.search(query.national_code == customer["national_code"])
            if len(ncode_exist) != 0:
                print(f"customer '{customer[item]}' already exists !".title())
                flag = False
                break

    if flag:
        customer.update({"balance": 0})
        db.insert(customer)
        print(
            f"costumer {customer['name']} {customer['family']}"
            f" {customer['national_code']} successfully created !".title()
        )


def show_customer(customer):
    return (
        f"name: {customer['name']} | family: {customer['family']} | "
        f"national code: {customer['national_code']} | phone: {customer['phone']} | "
        f"balance: {customer['balance']}".title()
    )


def show_all():
    all_customers = db.all()

    if len(all_customers) == 0:
        print("there is no customer yet !".title())
        return

    for index, customer in enumerate(all_customers):
        print(f"{index + 1}.{show_customer(customer)}")
        print("-" * 50)


def search(is_return=False):
    while True:
        searched_national_code = input("type national code : ".title()).lower()
        if searched_national_code == "exit":
            return [], None
        try:
            searched_national_code = int(searched_national_code)
        except Exception:
            print("invalid input !".title())
            return [], None

        if searched_national_code == 0:
            print("invalid input !".title())
        else:
            break

    searched_national_code = str(searched_national_code)
    searched_customer = db.search(query.national_code == searched_national_code)
    if len(searched_customer) == 0:
        print(f"customer '{searched_national_code}' not found !".title())
        return [], searched_national_code

    if is_return:
        return searched_customer, searched_national_code
    else:
        print(show_customer(searched_customer[0]))
        return [], searched_national_code


def update():
    to_update_customer, to_update_ncode = search(True)

    if len(to_update_customer) == 0:
        return
    else:
        to_update_customer = to_update_customer[0]

    show_customer(to_update_customer)
    to_update_fields = ["name", "family", "phone", "exit"]
    while True:
        to_update_field = input(f"enter field {to_update_fields}: ".title()).lower()
        if to_update_field not in to_update_fields:
            print(f"field '{to_update_field}' not found !".title())
            to_update_field = input(f"enter field {to_update_fields}: ".title()).lower()
        elif to_update_field == "exit":
            return
        else:
            break

    while True:
        to_update_val = input(f"type new '{to_update_field}': ".title()).lower()
        if len(to_update_val) == 0:
            print(f"'{to_update_field}' can't be empty !".title())
            to_update_val = input(f"type new '{to_update_field}': ".title()).lower()
        elif to_update_val == "exit":
            return
        else:
            break

    db.update({to_update_field: to_update_val}, query.national_code == to_update_ncode)


def incr():
    to_increase_customer, to_increase_ncode = search(True)
    if len(to_increase_customer) == 0:
        return
    else:
        to_increase_customer = to_increase_customer[0]

    print(show_customer(to_increase_customer))

    increase_val = int(input("enter amount : ".title()))
    while increase_val < 0:
        print("invalid input !")
        increase_val = int(input("enter amount : ".title()))

    to_increase_customer["balance"] += increase_val
    db.update({"balance": to_increase_customer["balance"]}, query.national_code == to_increase_ncode)
    print(f"{to_increase_ncode} balance successfully updated !")
    print(show_customer(to_increase_customer))


def decr():
    to_decrease_customer, to_decrease_ncode = search(True)
    if len(to_decrease_customer) == 0:
        return
    else:
        to_decrease_customer = to_decrease_customer[0]

    print(show_customer(to_decrease_customer))

    decrease_val = int(input("enter amount : ".title()))
    while decrease_val < 0:
        print("invalid input !")
        decrease_val = int(input("enter amount : ".title()))

    if decrease_val <= to_decrease_customer["balance"]:
        to_decrease_customer["balance"] -= decrease_val
        db.update({"balance": to_decrease_customer["balance"]}, query.national_code == to_decrease_ncode)
        print(f"{to_decrease_ncode} balance successfully updated !".title())
        print(show_customer(to_decrease_customer))
    else:
        print("not enough balance !".title())


def remove():
    to_remove_customer, to_remove_ncode = search(True)
    if len(to_remove_customer) == 0:
        return
    else:
        to_remove_customer = to_remove_customer[0]

    confirm = input(f"do you want to delete '{show_customer(to_remove_customer)}' ?(Y/n) :".title()).lower()

    if confirm == "y" or confirm == "yes":
        db.remove(query.national_code == to_remove_ncode)
        print(f"customer {to_remove_ncode} successfully deleted !".title())
    else:
        print(f"customer {to_remove_ncode} was not deleted !".title())
