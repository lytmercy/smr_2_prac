use std::{error::Error, thread::sleep, time, fs, iter::Enumerate};

mod math_ops;
use math_ops::*;

pub fn sleep_for(seconds: u64) {
    let secs_for_sleep = time::Duration::from_secs(seconds);
    let now = time::Instant::now();

    sleep(secs_for_sleep);

    assert!(now.elapsed() >= secs_for_sleep);
}


pub fn message_to_highlight_selection() {
    println!("Please choose the option!\n");
    sleep_for(1);
}


pub fn message_to_correctness_of(message_string: &String) {
    println!("");
    println!("{} is correct!", message_string);
    sleep_for(1);
}


pub fn message_to_incorrectness_of(message_string: &String, type_of_message: String) {
    println!("");
    println!("{} has incorrect format!", message_string);

    match type_of_message.as_str() {
        "code_phrase" => 
        println!("Please write only text (without numbers and other characters)!"),
        "num_attempts" => 
        println!("Please write correct number (between 3 - 5)!"),
        &_ => 
        println!("Please write in correct form!")
    }

    sleep_for(2);
}

pub fn write_references_config(file_path: &String, press_delays: &Vec<Vec<f64>>) -> Result<(), Box<dyn Error>> {
    
    let mut wtr = csv::Writer::from_path(file_path)?;

    let num_cols = press_delays[0].len();

    wtr.write_record(&vec!["0.0"; num_cols])?;

    for row in press_delays {
        let string_row: Vec<String> = row.iter().map(|&e| e.to_string()).collect();
        wtr.write_record(&string_row)?;
    }
    wtr.flush()?;
    println!("reference delay - saved successful");
    Ok(())
}


struct Float(f64);

impl<'a> From<&'a str> for Float {
    #[inline]
    fn from(s: &'a str) ->  Self {
        Float(s.parse::<f64>().unwrap_or(0.0).to_owned())
    }
}


pub fn read_references_config(file_path: &String, press_delays: &mut Vec<Vec<f64>>) -> Result<(), Box<dyn Error>> {

    let mut rdr = csv::ReaderBuilder::new()
        .delimiter(b',')
        .from_path(file_path)?;
    let mut key_num: usize = 0;
    let mut attempt_num: usize = 0;
        
    for result in rdr.records() {
        
        let record = result?;
        let record_len: usize = record.len();
        for delay in record.iter() {
            press_delays[attempt_num][key_num] = delay.trim().parse().unwrap();
            
            if key_num < record_len {
                key_num += 1;
            } else {
                key_num = 0;
                break;
            }
        }
        println!("{:?}", press_delays[attempt_num]);
        key_num = 0;
        attempt_num += 1;
    }
    Ok(())
}


pub fn write_config(file_path: String, content: &String) -> Result<(), Box<dyn Error>> {

    let content = fs::write(&file_path, content)
    .expect("Something went wrong reading the file");
    println!("file {} - saved successful", file_path);
    sleep_for(2);
    Ok(())
}


pub fn read_config(file_path: String) -> Result<String, Box<dyn Error>> {

    let content: String = fs::read_to_string(file_path)
                            .expect("Something went wrong reading the file");
    Ok(content)
}


pub fn student_train_check(y_array: &Vec<f64>) -> bool {

    let n: u8 = y_array.len().try_into().unwrap();
    let freedom: u8 = n - 1;
    let significance: f64 = 0.05;
    let student_table_rt: f64 = get_table_value("student".to_string(), freedom, 0, significance);
    for y_element in y_array.iter() {
        
        let y_dash: Vec<f64> = get_y_dash(&y_array, *y_element);
        let y_dash_n: u8 = y_dash.len().try_into().unwrap();
        let student_rt: f64 = student_ratio(y_element, &y_dash, &y_dash_n);
                
        if student_rt <= student_table_rt {
            continue;
        } else {
            println!("Student's ratio check - failure");
            return false;
        }
        
    }
    println!("Student's ratio check - successfully");
    true
}


pub fn student_authen_check(y_standard: &Vec<f64>, y_authen: &Vec<f64>) -> bool {

    let n: u8 = y_standard.len().try_into().unwrap();
    let student_rt: f64 = authen_student_ratio(y_standard, y_authen);
    
    let p: f64 = 0.95;
    
    let freedom: u8 = n - 1;
    let significance: f64 = 1.0 - p;
    let student_table_rt: f64 = get_table_value("student".to_string(), freedom, 0, significance);

    if student_rt <= student_table_rt {
        println!("Student's ratio check - successfully");
        true    
    } else {
        println!("Student's ratio check - failure");
        false
    }

}


pub fn fisher_check(y_standard: &Vec<f64>, y_authen: &Vec<f64>) -> bool {

    let n: u8 = y_standard.len().try_into().unwrap();
    let fisher_rt: f64 = fisher_ratio(y_standard, y_authen);

    let freedom: u8 = n - 1;
    let significance: f64 = 0.05;
    let fisher_table_rt: f64 = get_table_value("fisher".to_string(), freedom, freedom, significance);

    if fisher_rt <= fisher_table_rt {
        println!("Fisher's ratio check - successfully");
        true    
    } else {
        println!("Fisher's ratio check - failure");
        false
    }

}

