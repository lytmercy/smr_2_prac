use prac_1_cotuh::*;

pub struct Config {
    pub code_phrase: String,
    pub num_attempts: u8,
}

impl Config {
    pub fn new(code_phrase_path: String,
           num_attempts_path: String) -> Config {
        
        let code_phrase: String = read_config(code_phrase_path).unwrap();
        let num_attempts: u8 = read_config(num_attempts_path).unwrap().trim().parse().unwrap();

        Config { code_phrase, num_attempts}
    }
}