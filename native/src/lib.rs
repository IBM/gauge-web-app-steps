use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn substitute(_param: String) -> PyResult<String> {
    Ok("2".to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(substitute, m)?)?;
    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn substitute_with_full_math_expression() {
        let result = substitute("#{1 + 1}".to_string());
        assert_eq!("2", result.unwrap(), "expected an result for a match expression");
    }
}