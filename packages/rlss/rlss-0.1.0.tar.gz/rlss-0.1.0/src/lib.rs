#[macro_use]
extern crate approx;

mod assignment;

use pyo3::prelude::*;

#[pymodule]
fn rlss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(assignment::linear_assign, m)?)?;
    m.add_function(wrap_pyfunction!(assignment::mat_linear_assign, m)?)?;
    m.add_function(wrap_pyfunction!(assignment::linear_congested_assign, m)?)?;
    m.add_function(wrap_pyfunction!(
        assignment::mat_linear_congested_assign,
        m
    )?)?;
    Ok(())
}
