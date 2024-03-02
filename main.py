import sys

from menu_item import MenuItem
from single_order import SingleOrder

menu: list[MenuItem] = []


def build_menu():
    """build the menu of selections and their prices"""
    global menu

    category = 'Sandwich'
    for selection in (['Chicken', 5.25], ['Beef', 6.25], ['Tofu', 5.75]):
        menu_item = MenuItem(category, selection[0], selection[1])
        menu.append(menu_item)

    category = 'Beverage'
    for selection in (['Small', 1.0], ['Medium', 1.5], ['Large', 2.0]):
        menu_item = MenuItem(category, selection[0], selection[1])
        menu.append(menu_item)

    category = 'Fries'
    for selection in (['Small', 1.0], ['Medium', 1.5], ['Large', 2.0]):
        menu_item = MenuItem(category, selection[0], selection[1])
        menu.append(menu_item)

    category = 'Condiments'
    menu_item = MenuItem(category, 'Ketchup packets', 0.25, 0)
    menu.append(menu_item)


def new_order() -> SingleOrder:
    new_order = SingleOrder()
    # print(f'Order: {new_order}')
    return new_order


def get_fries(order: SingleOrder) -> None:
    if not get_yes_no_answer("Would you like fries?>"):
        return

    # filter the menu for just beverage choices
    filtered_items = filter(lambda item: item.category == 'Fries', menu)
    available_choices = list(filtered_items)

    # create prompt
    prompt = "What size french fries would you like to order: ("
    for available_choice in available_choices:
        prompt += f'{available_choice.name}: ${available_choice.price:.2f}, '
    prompt = prompt.removesuffix(', ')
    prompt += ") ?>"

    # print(f'DEBUG: {prompt=}')
    while True:
        choice = input(prompt)
        if choice is None or len(choice) == 0:
            choice = "unknown"
        abbrev = choice[:1].lower()

        selection = None
        for available_choice in available_choices:
            if available_choice.name[:1].lower() == abbrev:
                selection = available_choice
                break

        if selection is None:
            print(f'{abbrev} is not a valid choice')
        else:
            print(f'{selection.name} is a great choice')
            break

    # Ask customer of they want to super-size their fries from Small to Large
    if selection.name[:1].lower() == 's':
        if get_yes_no_answer('Do you want to super-size to a large?>'):
            abbrev = 'l'
            for available_choice in available_choices:
                if available_choice.name[:1].lower() == abbrev:
                    selection = available_choice

    order.fries_size = selection.name
    order.fries_cost = selection.price

    order.total_cost += selection.price


def get_order():
    order = new_order()
    order.get_sandwich(menu)
    order.get_beverage(menu)
    get_fries(order)
    order.display()


def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'


def get_yes_no_answer(question: str) -> bool:
    while True:
        answer = input(question)
        if answer is None or len(answer) == 0:
            print("please respond with y, n, Yes, yes, No or no")
        else:
            answer = answer.lower()[:1]
            match answer:
                case 'y':
                    return True

                case 'n':
                    return False

                case _:
                    print("please respond with y, n, Yes, yes, No or no")


def get_quantity(question: str, min_value: int = 0, max_value: int = 10) -> int:
    """Prompt for a number between min_value and max_value"""
    question = f'{question} (between {min_value} and {max_value})?>'
    count: int = min_value - 1
    while count < min_value or count > max_value:
        try:
            count = int(input(question))
            if count < min_value or count > max_value:
                print(f'Please enter a number between {min_value} and {max_value}.')
            else:
                return count
        except ValueError:
            print(f'Please enter a value between {min_value} and {max_value}')


if __name__ == '__main__':
    print(f'Combo Menu using Data Classes using python version {get_python_version()}')

    build_menu()
    # print(f'{menu=}')
    get_order()
