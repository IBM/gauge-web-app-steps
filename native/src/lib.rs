use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn substitute(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(substitute, m)?)?;
    Ok(())
}
