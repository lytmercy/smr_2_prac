use std::{io, process};

use prac_1_cotuh::*;

mod config;
use config::*;
mod math_ops;
use math_ops::*;
mod keyboard_event;
use keyboard_event::keys_event_catcher;

fn main() {

    // Let the user select an option (train or authentication)    
    let main_status = true;
    while main_status {
        
        print!("{}[2J", 27 as char);
        println!("Select an option for continue (enter the number):");
        println!("|-----------------------------------------------|");
        println!("|             1. Train mode                     |");
        println!("|             2. Authentication mode            |");
        println!("|             3. Exit                           |");
        println!("|-----------------------------------------------|");
        println!("");

        let mut input_text = String::new();
        io::stdin().read_line(&mut input_text).expect("failed to read from line");
        
        let chosen_option: char = input_text.chars().next().unwrap();
        match chosen_option {
            '1' => train_mode(),
            '2' => authentication_mode(),
            '3' => process::exit(0),
            _ => message_to_highlight_selection(),
        }
    }
}


fn train_mode() {

    let code_phrase_config_path: String = "cfg/code_phrase.txt".to_string();
    let num_attempts_config_path: String = "cfg/num_attempts.txt".to_string();
    let reference_delays_config_path: String = "cfg/reference_delays.csv".to_string();

    let mut code_phrase: String = String::new();
    loop {
        // Ask user to enter code phrase for authentication.
        print!("{}[2J", 27 as char);
        println!("Enter code phrase (enter only text):");
        println!("|-------------------------------------|");

        // Define string variable for input text from user.
        let mut input_phrase: String = String::new();
        io::stdin().read_line(&mut input_phrase).expect("failed to read from line");
        input_phrase.pop();
        input_phrase.pop();

        let check_phrase = input_phrase.chars().all(char::is_alphabetic);
        if check_phrase == true {
            message_to_correctness_of(&input_phrase);
            code_phrase = input_phrase;
            write_config(code_phrase_config_path, &code_phrase);
            break;
        } else {
            message_to_incorrectness_of(&input_phrase, "code_phrase".to_string());
            continue;
        }
    }

    let mut num_attempts: u8 = 3;

    loop {
        // Ask user to enter number of attempts for authentication.
        print!("{}[2J", 27 as char);
        println!("Enter number of attempts (enter attempts between 3-5):");
        println!("|----------------------------------------------------|");

        let mut input_attempts: String = String::new();
        io::stdin().read_line(&mut input_attempts).expect("failed to read from line");
        input_attempts.pop();
        input_attempts.pop();

        num_attempts = match input_attempts.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        if [3, 4, 5].contains(&num_attempts) {
            message_to_correctness_of(&input_attempts);
            write_config(num_attempts_config_path, &num_attempts.to_string());
            break;
        } else {
            message_to_incorrectness_of(&input_attempts, "num_attempts".to_string());
            continue;
        }
    }

    // Define size variables for vector with statistics input delay.
    let num_rows: usize = num_attempts.try_into().unwrap();
    let num_cols: usize = code_phrase.len();

    // Define vector for maintains statistics input delay.
    let mut key_press_delays: Vec<Vec<f64>> = vec![vec![0.0; num_cols]; num_rows];

    let mut mode_status: bool = true;
    let mut current_attempt: u8 = 1;
    while mode_status {
        loop {
        
            print!("{}[2J", 27 as char);
            println!("\tTrain mode");
            println!("| ---------------------\t|");
            println!("| Code phrase: {}\t|", code_phrase);
            println!("| Number of attempts: {}\t|", num_attempts);
            println!("| Current attempt: {}\t|", current_attempt);
            println!("| -----Input field-----\t|");
    
            // let input_phrase: String = String::new();

            // Listiner for catch key pressing
            let input_phrase: String = keys_event_catcher(&mut key_press_delays, current_attempt).unwrap();

            println!("\n| ---------------------\t|");

            if input_phrase != code_phrase {
                println!("input {} != code {}!", input_phrase, code_phrase);
                println!(">>phrase not equal!<<");
                sleep_for(2);
                continue;
            } else {
                if current_attempt < num_attempts {
                    
                    let current_press_delays_num: usize= current_attempt.try_into().unwrap();
                    let current_press_delays: &Vec<f64> = &key_press_delays[current_press_delays_num - 1];
                    let student_check_result: bool = student_train_check(current_press_delays);

                    if student_check_result {
                        current_attempt += 1;
                        sleep_for(1);
                        continue;
                    } else {
                        println!(">>Please try again!<<");
                        sleep_for(2);
                        continue;
                    }

                } else {
                    write_references_config(&reference_delays_config_path, &key_press_delays);
                    break;
                }
            }
        }
        mode_status = false;
    }
    println!("\nTrianing was - successfull");
    sleep_for(2)
}


fn authentication_mode() {

    let code_phrase_config_path: String = "cfg/code_phrase.txt".to_string();
    let num_attempts_config_path: String = "cfg/num_attempts.txt".to_string();
    let reference_delays_config_path: String = "cfg/reference_delays.csv".to_string();

    let config: Config = Config::new(code_phrase_config_path, num_attempts_config_path);

    let code_phrase: String = config.code_phrase;
    println!("File code_phrase.txt - have word = {}", &code_phrase);
    
    let num_attempts: u8 = config.num_attempts;
    println!("File num_attempts.txt - have number = {}", &num_attempts);

    let num_rows: usize = num_attempts.try_into().unwrap();
    let num_cols: usize = code_phrase.len();

    let mut standard_key_press_delays: Vec<Vec<f64>> = vec![vec![0.0; num_cols]; num_rows];
    let mut authen_key_press_delays: Vec<Vec<f64>> = vec![vec![0.0; num_cols]; num_rows];

    read_references_config(&reference_delays_config_path, &mut standard_key_press_delays);

    let mut mode_status: bool = true;
    let mut current_attempt: u8 = 1;
    let mut true_attempt: u8 = 0;
    let mut false_attempt: u8 = 0;

    let mut user_mode: bool = true;
    let mut frst_kind_error: f64 = 0.0;
    let mut scnd_kind_error: f64 = 0.0;
    let mut true_student_prob_estm: u8 = 1;

    while mode_status {
        
        loop {
            print!("{}[2J", 27 as char);
            println!("Select an option for continue (enter the number):");
            println!("|-----------------------------------------------|");
            println!("|             1. Legitimate user                |");
            println!("|             2. Illegitimate user              |");
            println!("|-----------------------------------------------|");
            println!("");
    
            let mut input_text = String::new();
            io::stdin().read_line(&mut input_text).expect("failed to read from line");
            
            let chosen_option: char = input_text.chars().next().unwrap();
            match chosen_option {
                '1' => {user_mode = true; break;},
                '2' => {user_mode = false; break;},
                _ => message_to_highlight_selection(),
            }
        }


        loop {
        
            print!("{}[2J", 27 as char);
            println!("\tAuthentication mode");
            println!("| ---------------------\t|");
            println!("| Code phrase: {}\t|", code_phrase);
            println!("| Number of attempts: {}\t|", num_attempts);
            println!("| Current attempt: {}\t|", current_attempt);
            println!("| -----Input field-----\t|");

            // Listiner for catch key pressing
            let input_phrase: String = keys_event_catcher(&mut authen_key_press_delays, current_attempt).unwrap();

            println!("\n| ---------------------\t|");

            if input_phrase != code_phrase {
                println!("input {} != code {}!", input_phrase, code_phrase);
                println!(">>phrase not equal!<<");
                sleep_for(1);
                continue;
            } else {
                if current_attempt < num_attempts {
                    
                    let current_press_delays_num: usize= current_attempt.try_into().unwrap();
                    let current_press_delays: &Vec<f64> = &authen_key_press_delays[current_press_delays_num - 1];
                    let standard_press_delays: &Vec<f64> = &standard_key_press_delays[current_press_delays_num - 1];

                    let fisher_check_result: bool = fisher_check(standard_press_delays, current_press_delays);

                    if fisher_check_result {
                        println!("");
                    } else {
                        println!(">>Fail - attempt is broken<<");
                        println!(">>Please try again!<<");
                        false_attempt += 1;
                        current_attempt += 1;
                        sleep_for(2);
                        continue;
                    }


                    let student_check_result: bool = student_authen_check(standard_press_delays, current_press_delays);

                    if student_check_result {
                        true_attempt += 1;
                        true_student_prob_estm += 1;
                        current_attempt += 1;
                        sleep_for(1);
                        continue;
                    } else {
                        if true_attempt == 0 {
                            println!(">>Please try again!<<");
                            sleep_for(2);
                            continue;
                        } else {
                            println!(">>Fail - attempt is broken<<");
                            println!(">>Please try again!<<");
                            sleep_for(2);
                            false_attempt += 1;
                            current_attempt += 1;    
                            continue;
                        }
                    }
                } else {

                    println!("");
                    println!("| ============================ |");
                    if user_mode {
                        frst_kind_error = first_kind_error(false_attempt, current_attempt);
                        println!("First kind error - {}", frst_kind_error);
                    } else {
                        scnd_kind_error = second_kind_error(true_attempt, current_attempt);
                        println!("Second kind error - {}", frst_kind_error);
                    }
                    println!("| ============================ |");
                    sleep_for(2);

                    let student_prob_legit_user_estm: f64 = true_student_prob_estm as f64 / num_attempts as f64;
                    println!("P-identification - {}", student_prob_legit_user_estm);

                    println!("| ============================ |");
                    sleep_for(2);

                    println!("");
                    if student_prob_legit_user_estm < 0.66 {
                        println!("\nAuthentication - failure");
                    } else if false_attempt == current_attempt {
                        println!("\nAuthentication - failure");
                    } else  if false_attempt > true_attempt {
                        println!("\nAuthentication - failure");
                    } else {
                        println!("");
                    }

                    if user_mode {
                        println!("\nAuthentication - successfull");
                        write_references_config(&reference_delays_config_path, &authen_key_press_delays);
                        break;
                    } else {
                        println!("\nAuthentication - successfull");
                        break;
                    }
                }
            }
        }
        mode_status = false;
    }
    sleep_for(2)
}
