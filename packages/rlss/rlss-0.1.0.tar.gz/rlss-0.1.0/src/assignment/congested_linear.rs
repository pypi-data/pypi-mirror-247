use crate::assignment::linear::_linear_assign;
use crate::assignment::utils::{graph2mat, mat2graph};
use pyo3::prelude::*;
use rayon::iter::{IndexedParallelIterator, IntoParallelRefIterator, ParallelIterator};
use std::cmp;
use std::collections::HashMap;
use std::f32::INFINITY;

#[pyfunction]
#[pyo3(signature = (from, to, arc_freqs, costs, demands, dsts, capacity, average_decay_factor=0.01, beta=0.2, tol=0.001, max_iters=1000))]
pub fn linear_congested_assign(
    py: Python<'_>,
    from: Vec<usize>,
    to: Vec<usize>,
    arc_freqs: Vec<f32>,
    costs: Vec<f32>,
    demands: Vec<f32>,
    dsts: Vec<usize>,
    capacity: f32,
    average_decay_factor: f32,
    beta: f32,
    tol: f32,
    max_iters: usize,
) -> (Vec<f32>, Vec<f32>) {
    return py.allow_threads(|| {
        _linear_congested_assign(
            &from,
            &to,
            &arc_freqs,
            &costs,
            &demands,
            &dsts,
            average_decay_factor,
            beta,
            capacity,
            tol,
            max_iters,
        )
    });
}

#[pyfunction]
#[pyo3(signature = (alignments, freqs, travel_time_mat, demands_mat, capacity, average_decay_factor=0.01, beta=0.2, tol=0.001, max_iters=1000))]
pub fn mat_linear_congested_assign(
    py: Python<'_>,
    alignments: Vec<Vec<usize>>,
    freqs: Vec<f32>,
    travel_time_mat: Vec<Vec<f32>>,
    demands_mat: Vec<Vec<f32>>,
    capacity: f32,
    average_decay_factor: f32,
    beta: f32,
    tol: f32,
    max_iters: usize,
) -> Vec<Vec<f32>> {
    return py.allow_threads(|| {
        let mat_size = travel_time_mat.len();

        let (from, to, arc_freqs, costs, demands) =
            mat2graph(alignments, freqs, travel_time_mat, demands_mat);

        let dsts = (1..mat_size).collect::<Vec<_>>();
        let (u, _) = _linear_congested_assign(
            &from,
            &to,
            &arc_freqs,
            &costs,
            &demands,
            &dsts,
            average_decay_factor,
            beta,
            capacity,
            tol,
            max_iters,
        );

        return graph2mat(u, mat_size);
    });
}

fn _linear_congested_assign(
    from: &[usize],
    to: &[usize],
    arc_freqs: &[f32],
    costs: &[f32],
    demands: &[f32],
    dsts: &[usize],
    average_decay_factor: f32,
    beta: f32,
    capacity: f32,
    tol: f32,
    max_iters: usize,
) -> (Vec<f32>, Vec<f32>) {
    let n_nodes = cmp::max(from.iter().max().unwrap(), to.iter().max().unwrap()) + 1;
    let n_arcs = from.len();
    let mut arcs_from: HashMap<usize, Vec<usize>> = HashMap::new();

    for arc in 0..from.len() {
        if arcs_from.contains_key(&from[arc]) {
            arcs_from.get_mut(&from[arc]).unwrap().push(arc);
        } else {
            arcs_from.insert(from[arc], vec![arc]);
        }
    }

    let mut vp: Vec<f32>;
    let mut up: Vec<f32>;
    let mut gap = INFINITY;
    let mut n_iter = 0;

    let (mut u, mut v) = _linear_assign(&from, &to, &arc_freqs, &costs, &demands, &dsts);

    let mut eff_arc_freqs = vec![INFINITY; arc_freqs.len()];
    eff_arc_freqs.clone_from_slice(&arc_freqs);

    println!("Iteration {:5}: gap = {:.10}", n_iter, gap);

    // while gap.abs() > 0.01 {
    while gap > tol {
        eff_arc_freqs = _calc_eff_freqs(&to, &v, &arc_freqs, beta, capacity);
        // println!("{eff_arc_freqs:.2?}");
        (up, vp) = _linear_assign(&from, &to, &eff_arc_freqs, &costs, &demands, &dsts);
        n_iter += 1;

        v = vp
            .par_iter()
            .zip(v.par_iter())
            .map(|(fp, f)| (1.0 - average_decay_factor) * *f + average_decay_factor * *fp)
            .collect();

        u = up;

        gap = _calc_gap(
            &u,
            &v,
            &eff_arc_freqs,
            &costs,
            &dsts,
            n_arcs,
            n_nodes,
            &arcs_from,
            &to,
        );

        println!("Iteration {:5}: gap = {:.10}", n_iter, gap);

        if n_iter == max_iters {
            break;
        }
    }

    return (u, v);
}

fn _calc_gap(
    u: &[f32],
    v: &[f32],
    eff_arc_freqs: &[f32],
    costs: &[f32],
    dsts: &[usize],
    n_arcs: usize,
    n_nodes: usize,
    arcs_from: &HashMap<usize, Vec<usize>>,
    to: &[usize],
) -> f32 {
    let (gap, ttt) = dsts
        .par_iter()
        .enumerate()
        .map(|(i_dst, dst)| {
            let mut gap = 0.0f32;
            let mut ttt = 0.0f32;

            for node in 0..n_nodes {
                if node == *dst {
                    continue;
                }

                if arcs_from.contains_key(&node) {
                    let out = arcs_from
                        .get(&node)
                        .unwrap()
                        .par_iter()
                        .map(|arc| {
                            if v[i_dst * n_arcs + *arc] == 0.0
                                || u[i_dst * n_nodes + to[*arc]].is_infinite()
                                || u[i_dst * n_nodes + node].is_infinite()
                            {
                                return (0.0, 0.0, 0.0);
                            } else {
                                return (
                                    (costs[*arc] + u[i_dst * n_nodes + to[*arc]]
                                        - u[i_dst * n_nodes + node])
                                        * v[i_dst * n_arcs + *arc],
                                    v[i_dst * n_arcs + *arc] / eff_arc_freqs[*arc],
                                    u[i_dst * n_nodes + node] * v[i_dst * n_arcs + *arc],
                                );
                            }
                        })
                        .reduce(
                            || (0.0, 0.0, 0.0),
                            |(a1, b1, c1), (a2, b2, c2)| (a1 + a2, b1.max(b2), c1 + c2),
                        );

                    gap += out.0 + out.1;
                    ttt += out.2;
                }
            }

            return (gap, ttt);
        })
        .reduce(|| (0.0, 0.0), |(a1, b1), (a2, b2)| (a1 + a2, b1 + b2));

    return gap / ttt;
}

fn _calc_eff_freqs(
    to: &[usize],
    arc_flows: &[f32],
    nominal_arc_freqs: &[f32],
    beta: f32,
    capacity: f32,
) -> Vec<f32> {
    let n_arcs = nominal_arc_freqs.len();
    let mut out = vec![INFINITY; n_arcs];

    for arc in 0..n_arcs {
        if nominal_arc_freqs[arc].is_infinite() {
            continue; // non-boarding arcs
        }

        let capacity_per_time = nominal_arc_freqs[arc] * capacity;
        let boarding_flow_into_stop = arc_flows[arc..].iter().step_by(n_arcs).sum::<f32>();
        let onboard_flow_after_stop: f32 = to
            .iter()
            .enumerate()
            .filter(|(_, &v)| v == to[arc])
            .map(|(index, _)| arc_flows[index..].iter().step_by(n_arcs).sum::<f32>())
            .sum::<f32>();

        if onboard_flow_after_stop < capacity_per_time {
            out[arc] = nominal_arc_freqs[arc]
                * (1.0
                    - (boarding_flow_into_stop
                        / (capacity_per_time - onboard_flow_after_stop + boarding_flow_into_stop))
                        .powf(beta));
        } else {
            out[arc] = 0.0;
        }

        if out[arc] < 1.0 / 16.7 {
            out[arc] = 1.0 / 16.7;
        }
    }

    return out;
}
