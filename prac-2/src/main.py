# Importing other libraries
import os
from time import sleep

# Importing own written functions
from utils import calculate_statistics, calculate_r_threshold_statistics, calculate_q_coef_adaptability
from utils import save_r_threshold, read_r_threshold, save_statistics, read_statistics


def form_statistics_and_show():
    """"""
    train_statistics = calculate_statistics("../input/first_file_statistics.txt")
    line_with_5_keys = ""

    os.system("cls" if os.name == 'nt' else 'clear')

    print("=== Train Statistics ===")
    for i, (key, value) in enumerate(train_statistics.items()):
        line_with_5_keys += f"{key}:{value}, "
        if i % 5 == 0:
            print(line_with_5_keys)
            line_with_5_keys = ""
    sleep(5)
    os.system("cls" if os.name == 'nt' else 'clear')

    save_statistics(train_statistics, "../output/statistics.json")


def calc_r_threshold_and_show():
    """"""
    os.system("cls" if os.name == 'nt' else 'clear')

    train_statistics = read_statistics("../output/statistics.json")
    r_threshold = calculate_r_threshold_statistics(train_statistics)

    print(f"\nR : {r_threshold}")

    sleep(5)
    os.system("cls" if os.name == 'nt' else 'clear')

    save_r_threshold(r_threshold, "../output/r_threshold.txt")


def check_new_text():
    """"""
    train_statistics = read_statistics("../output/statistics.json")
    r_threshold = read_r_threshold("../output/r_threshold.txt")

    os.system("cls" if os.name == 'nt' else 'clear')
    print("|==================|")
    print(f"R : {r_threshold}")
    print("|==================|")

    input_text = input("|========Write your text line========|\n")
    q_coef = calculate_q_coef_adaptability(train_statistics, input_text)

    print("|==================|")
    print(f"Q : {q_coef}")

    if q_coef >= r_threshold:
        print("Your text is adequate")
    elif q_coef < r_threshold:
        print("Your text is inadequate")

    print("|==================|\n")

    sleep(5)
    os.system("cls" if os.name == 'nt' else 'clear')


def main():
    """Main function for executing program."""
    while True:
        print("|============Choose mode============\t|")
        print("|\t1. Form statistics and show\t|")
        print("|\t2. Calculate R Threshold and show\t|")
        print("|\t3. Check your text\t|")
        print("|\t4. Exit\t|")
        print("|===================================\t|")
        mode = input("Selected mode : ")

        match mode:
            case "1": form_statistics_and_show()
            case "2": calc_r_threshold_and_show()
            case "3": check_new_text()
            case "4": return 0


if __name__ == '__main__':
    main()
