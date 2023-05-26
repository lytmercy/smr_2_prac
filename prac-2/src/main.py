# Importing other libraries
import os
from time import sleep

# Importing own written functions
from utils import calculate_training_statistics, calculate_r_threshold, calculate_q_coef_adaptability
from utils import save_r_threshold, read_r_threshold, save_statistics, read_statistics


def form_statistics_and_show():
    """
    Function for form and show training statistics in console;
    """
    # Calculating training statistics
    train_statistics = calculate_training_statistics("input/first_file_statistics.txt")
    line_with_5_keys = ""

    # Cleaning console
    os.system("cls" if os.name == 'nt' else 'clear')

    # Show training statistics
    print("=== Train Statistics ===")
    for i, (key, value) in enumerate(train_statistics.items()):
        line_with_5_keys += f"{key}:{value}, "
        if i % 5 == 0:
            print(line_with_5_keys)
            line_with_5_keys = ""

    sleep(5)
    os.system("cls" if os.name == 'nt' else 'clear')

    # Saving training statistics
    save_statistics(train_statistics, "output/statistics.json")


def calc_r_threshold_and_show():
    """
    Function for calculating and showing value of R threshold in console;
    """
    os.system("cls" if os.name == 'nt' else 'clear')

    # Reading training statistics from file
    train_statistics = read_statistics("output/statistics.json")
    # Calculating value of R threshold
    r_threshold = calculate_r_threshold(train_statistics)
    # Show value of R threshold
    print(f"\nR : {r_threshold}")

    sleep(5)
    os.system("cls" if os.name == 'nt' else 'clear')

    # Saving value of R threshold
    save_r_threshold(r_threshold, "output/r_threshold.txt")


def check_new_text():
    """
    Function for checking input text that user enter in console;
    """
    # Reading training statistics from file
    train_statistics = read_statistics("output/statistics.json")
    # Reading value of R threshold from file
    r_threshold = read_r_threshold("output/r_threshold.txt")

    # Clearing console
    os.system("cls" if os.name == 'nt' else 'clear')
    # Showing value of R threshold
    print("|==================|")
    print(f"R : {r_threshold}")
    print("|==================|")

    # User enter the text
    input_text = input("|========Write your text line========|\n")
    # Calculating Q coefficient of adaptability
    q_coef = calculate_q_coef_adaptability(train_statistics, input_text)

    # Showing Q coefficient of adaptability
    print("|==================|")
    print(f"Q : {q_coef}")

    # Showing result of checking the text for adequacy
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
