from typing import List

regional_manager_weekly_sales = {'rate0': 0,
                                 'rate1': 200,
                                 'rate2': 550,
                                 'rate3': 850,
                                 'rate4': 1100,
                                 }

regular_manager_weekly_sales = {'rate0': 0,
                                'rate1': 300,
                                'rate2': 550,
                                'rate3': 850,
                                'rate4': 1100,
                                }

regional_manager_ticket_prices = {'rate0': 0,
                                  'rate1': 25,
                                  'rate2': 27,
                                  'rate3': 30,
                                  'rate4': 32,
                                  }

regular_manager_ticket_prices = {'rate0': 0,
                                 'rate1': 25,
                                 'rate2': 27,
                                 'rate3': 30,
                                 'rate4': 35,
                                 }

regional_manager_set_salary = 5000
regular_manager_set_salary = 7500


def manager_week_salary(sales_number: List[int], is_regional: bool) -> float:
    if is_regional:
        print('regional manager')
        manager_weekly_sales = regional_manager_weekly_sales
        manager_ticket_prices = regional_manager_ticket_prices
        manager_set_salary = regional_manager_set_salary
    else:
        print('regular manager')
        manager_weekly_sales = regular_manager_weekly_sales
        manager_ticket_prices = regular_manager_ticket_prices
        manager_set_salary = regular_manager_set_salary

    sales_sum = sum(sales_number[:])
    print(f'week sales sum is {sales_sum}')

    if sales_sum > manager_weekly_sales['rate4']:
        return sales_sum * manager_ticket_prices['rate4']
    if sales_sum > manager_weekly_sales['rate3']:
        return sales_sum * manager_ticket_prices['rate3']
    if sales_sum > manager_weekly_sales['rate2']:
        return sales_sum * manager_ticket_prices['rate2']
    if sales_sum > manager_weekly_sales['rate1']:
        return sales_sum * manager_ticket_prices['rate1']
    return manager_set_salary


def agent_week_salary(sales_number: List[int]) -> float:
    return 50


def manager_day_salary(sales_number: List[int]) -> float:
    return 10


def agent_day_salary(sales_number: List[int]) -> float:
    return 5

# -------------------TESTING--------------------------------------------------------------------------------------------
# test_sales_number = [30, 50, 0, 29, 0, 58, 0]
# print(f'week salary is {manager_week_salary(test_sales_number, True)}₽')
# print(f'week salary is {manager_week_salary(test_sales_number, False)}₽')
