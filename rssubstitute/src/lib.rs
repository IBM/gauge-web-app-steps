use chrono::Utc;
use evalexpr::*;
use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::error::Error;
use uuid::Uuid;

/// Substitutes placeholders in a step parameter with values from environment variables
/// and evaluates mathematical expressions.
/// The environment variables are usually defined in the env/*.properties files in the gauge project
/// or are placed into the context with specific steps.
/// So the same placeholder can be replaced with different values in different environments.
#[pyfunction]
fn substitute(gauge_param: &str, data_store: HashMap<String, String>) -> PyResult<String> {
    // Collect environment variables
    let env_vars: HashMap<_, _> = env::vars().collect();

    let substituted = manual_substitute(gauge_param, &env_vars)
        .and_then(|sub| manual_substitute(&sub, &data_store))
        .and_then(|sub| {
            substitute_expressions('#', &sub, |expr| {
                eval(&expr)
                    .map(|v| v.to_string())
                    .unwrap_or(expr.to_string())
            })
        })
        .and_then(|sub| substitute_expressions('!', &sub, |expr| evaluate_expression(&expr)))
        .unwrap();

    Ok(substituted)
}

fn manual_substitute(
    template: &str,
    vars: &HashMap<String, String>,
) -> Result<String, Box<dyn Error>> {
    let mut result = template.to_string();
    for (key, value) in vars {
        let placeholder = format!("${{{}}}", key);
        result = result.replace(&placeholder, value);
    }
    Ok(result)
}

fn substitute_expressions<F>(
    marker_char: char,
    text: &str,
    evaluator: F,
) -> Result<String, Box<dyn Error>>
where
    F: Fn(String) -> String,
{
    let mut substituted = text.to_string();
    let re = Regex::new(&format!(r"\{}\{{([^}}]+)}}", marker_char))?;

    while let Some(cap) = re.captures(&substituted) {
        let first_match = cap.get(0).unwrap();
        let before = &substituted[..first_match.start()];
        let after = &substituted[first_match.end()..];
        let value = evaluator(cap[1].to_string());
        substituted = format!("{}{}{}", before, value, after);
    }

    Ok(substituted)
}

fn evaluate_expression(expression: &str) -> String {
    match expression.to_lowercase().as_str() {
        "uuid" => Uuid::new_v4().to_string(),
        expr if expr.starts_with("time") => {
            if expr == "time" {
                Utc::now().to_rfc3339()
            } else if expr.starts_with("time:") {
                let format = &expr[5..];
                Utc::now().format(format).to_string()
            } else {
                panic!("unsupported substitute {}", expression)
            }
        }
        _ => panic!("unsupported substitute {}", expression),
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn rssubstitute(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(substitute, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn evaluate_expression_uuid() {
        let result = evaluate_expression("uuid");
        assert_eq!(result.len(), 36); // UUID length
    }

    #[test]
    fn evaluate_expression_time() {
        let result = evaluate_expression("time");
        // Check if the result is a valid ISO 8601 format
        assert!(result.contains('T'));
    }

    #[test]
    fn manual_substitute_hello_world() {
        let mut vars = HashMap::new();
        vars.insert("name".to_string(), "world".to_string());
        let result = manual_substitute("Hello, ${name}!", &vars).unwrap();
        assert_eq!(result, "Hello, world!");
    }

    #[test]
    fn substitute_math_expression() {
        let result = substitute("#{1 + 1}", HashMap::new());
        assert_eq!(
            "2",
            result.unwrap(),
            "expected a result for a math expression"
        );
    }
}
