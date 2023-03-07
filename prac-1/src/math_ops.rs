

pub fn get_y_dash(y_array: &Vec<f64>, y_element: f64) -> Vec<f64>{
    
    let mut y_dash: Vec<f64> = y_array.clone();

    y_dash.retain(|&x| x != y_element);
    y_dash = y_dash.iter().map(|y: &f64| y/y_element).collect();
    y_dash
}


pub fn math_expectation(y_array: &Vec<f64>, n: &u8) -> f64 {
    
    y_array.iter().sum::<f64>() / *n as f64
}


pub fn dispersion(y_array: &Vec<f64>, n: &u8) -> f64{

    let math_expt: f64 = math_expectation(y_array, n);
    let y_dash_sub_math_expt: Vec<f64> = y_array.iter().map(|y: &f64| (y - math_expt).powi(2)).collect();
    let sum_with_sub_math_expt: f64 = y_dash_sub_math_expt.iter().sum();
    sum_with_sub_math_expt / (*n - 1) as f64
}


pub fn root_mean_square_deviation(y_array: &Vec<f64>, n: &u8) -> f64 {

    dispersion(y_array, n).sqrt()
}

// ToDo:: Continue write use this function!! <<<<
pub fn authen_rms_deviation(y_standard: &Vec<f64>, y_authen: &Vec<f64>) -> f64 {

    let n: u8 = y_standard.len().try_into().unwrap();
    
    let standard_dispersion: f64 = dispersion(&y_standard, &n);
    let authen_dispersion: f64 = dispersion(&y_authen, &n);

    let numerator: f64 = (standard_dispersion + authen_dispersion) * (n as f64 - 1.0);
    let denominator: f64 = 2.0 * n as f64 - 1.0;

    let result: f64 = numerator / denominator;

    result.sqrt() 
}


pub fn authen_student_ratio(y_standard: &Vec<f64>, y_authen: &Vec<f64>) -> f64 {

    let n_standard: u8 = y_standard.len().try_into().unwrap();

    let standard_math_expt: f64 = math_expectation(y_standard, &n_standard);
    let authen_math_expt: f64 = math_expectation(y_authen, &n_standard);

    let std_authen_math_expt_sub: f64 = standard_math_expt - authen_math_expt;

    let authen_rms_dev: f64 = authen_rms_deviation(y_standard, y_authen);    

    std_authen_math_expt_sub.abs() / (authen_rms_dev * (2.0 / n_standard as f64).sqrt())
}


pub fn student_ratio(y_element: &f64, y_array: &Vec<f64>, n: &u8 ) -> f64 {
    
    let y_sub_math_expt: f64 = y_element - math_expectation(y_array, n);
    let sub_devision_msd: f64 = y_sub_math_expt / root_mean_square_deviation(y_array, n);
    sub_devision_msd.abs()
}


pub fn fisher_ratio(y_standard: &Vec<f64>, y_authen: &Vec<f64>) -> f64 {

    let n_standard: u8 = y_standard.len().try_into().unwrap();
    let standard_dispersion: f64 = dispersion(y_standard, &n_standard);

    let authen_dispersion: f64 = dispersion(y_authen, &n_standard);

    let max_dispersion: f64 = standard_dispersion.max(authen_dispersion);
    let min_dispersion: f64 = standard_dispersion.min(authen_dispersion);

    max_dispersion / min_dispersion
}


pub fn first_kind_error(failure_attempts: u8, all_attempts: u8) -> f64 {

    failure_attempts as f64 / all_attempts as f64
}


pub fn second_kind_error(seccessfully_attempts: u8, all_attempts: u8) -> f64 {

    seccessfully_attempts as f64 / all_attempts as f64
}


pub fn get_table_value (ratio: String, freedom_1: u8, freedom_2: u8, significance: f64) -> f64 {

    let signific: usize = if significance == 0.10 {0} else
                          if significance == 0.05 {1} else
                          if significance == 0.01 {2} else {1};

    if ratio == "student" {
        let student_table: [[f64; 20]; 3] = [
            [6.31, 2.92, 2.35, 2.13, 2.01, 1.94, 1.89, 1.86, 1.83, 1.81,
             1.80, 1.78, 1.77, 1.76, 1.75, 1.75, 1.74, 1.73, 1.73, 1.73],
            [12.70, 4.30, 3.18, 2.78, 2.57, 2.45, 2.36, 2.31, 2.26, 2.23,
             2.2, 2.18, 2.16, 2.14, 2.13, 2.12, 2.11, 2.10, 2.09, 2.09],
            [63.70, 9.92, 5.84, 4.60, 4.03, 3.71, 3.50, 3.36, 3.25, 3.17,
             3.11, 3.05, 3.01, 2.98, 2.95, 2.92, 2.90, 2.88, 2.86, 2.85]];
        
        student_table[signific][freedom_1 as usize]
    } else if ratio == "fisher" {

        let freedom_1: usize = if freedom_1 < 4 {0 as usize} else
                               if freedom_1 >= 4 && freedom_1 < 7 {0 as usize} else
                               if freedom_1 >= 7 && freedom_1 < 10 {1 as usize} else
                               if freedom_1 >= 10 && freedom_1 < 16 {2 as usize} else
                               {3 as usize};

        let freedom_2: usize = if freedom_2 < 10 {freedom_2 as usize} else
                               if freedom_2 >= 10 && freedom_2 < 12 {9 as usize} else
                               if freedom_2 >= 12 && freedom_2 < 14 {10 as usize} else
                               if freedom_2 >= 14 && freedom_2 < 16 {11 as usize} else
                               if freedom_2 >= 16 && freedom_2 < 18 {12 as usize} else 
                               {13 as usize};

        let fisher_table: [[[f64; 14]; 4]; 2] = [
            [[0.0; 14], [0.0; 14], [0.0; 14], [0.0; 14]],
            [[225.0, 19.25, 9.12, 6.39, 5.19, 4.53, 4.12, 3.84, 3.63, 3.48, 3.26, 3.11, 3.01, 2.93],
             [237.0, 19.36, 8.88, 6.09, 4.88, 4.21, 3.79, 3.50, 3.29, 3.14, 2.92, 2.77, 2.66, 2.58],
             [242.0, 19.39, 8.78, 5.96, 4.74, 4.06, 3.63, 3.34, 3.13, 2.97, 2.76, 2.60, 2.49, 2.41],
             [246.0, 19.43, 8.69, 5.84, 4.60, 3.92, 3.49, 3.20, 2.98, 2.82, 2.60, 2.44, 2.33, 2.25]]
        ];
        
        fisher_table[signific][freedom_1][freedom_2]
    } else {0.0}

}



