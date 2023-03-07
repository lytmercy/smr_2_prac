use std::{time, io::{stdout, Write}};
use crossterm::{event::{read, Event, KeyCode, KeyEvent, KeyEventKind}, Result};


pub fn keys_event_catcher(key_delays: &mut Vec<Vec<f64>>, attempt: u8) -> Result<String> {
    
    let mut input_phrase: String = String::new();
    let mut key_press = time::Instant::now();
    let mut key_num: usize = 0;
    let attempt_num: usize = (attempt-1).try_into().unwrap();

    while let Event::Key(KeyEvent {
        code,
        kind,
        .. }) = read()? {
            if kind == KeyEventKind::Press {
                if key_num == 0 {
                    key_press = time::Instant::now();
                }
                match code {
                    KeyCode::Enter => break,
                    KeyCode::Char(key_char) => {
                        
                        print!("{}", key_char);
                        stdout().flush().unwrap();

                        input_phrase.push(key_char);
                        
                        let key_press_delay: f64 = key_press.elapsed().as_secs_f64();
                        if key_num < key_delays[attempt_num].len() {
                            key_delays[attempt_num][key_num] = key_press_delay;
                            key_num += 1;
                        } else {
                            println!("{} word too long!!<<", input_phrase);
                            break;
                        }
                    },
                    _ => {}
                }
                key_press = time::Instant::now();
            }
    }
    Ok(input_phrase)
}
