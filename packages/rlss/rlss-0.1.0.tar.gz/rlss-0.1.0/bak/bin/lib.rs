use pyo3::prelude::*;
extern crate queues;

// use ndarray::{array, Array, Array1, Array2};
use priority_queue::PriorityQueue;
use rayon::prelude::*;
use std::cmp::max;
use std::collections::{HashMap, VecDeque};
use std::f32::INFINITY;
use std::iter::zip;

fn fu(f: f32, u: f32) -> f32 {
    if f.abs() < 1e-8 && u.is_infinite() {
        return 1.0;
    }

    return f * u;
}

fn linear_assign(
    from_nodes: &[usize],
    to_nodes: &[usize],
    arc_frequencies: &[f32],
    costs: &[f32],
    destination_nodes: &[usize],
    demands: &[f32],
) -> (Vec<f32>, Vec<f32>) {
    let n_nodes = max(
        from_nodes.iter().max().unwrap(),
        to_nodes.iter().max().unwrap(),
    ) + 1;

    let (us, vs): (Vec<Vec<f32>>, Vec<Vec<f32>>) = (0..destination_nodes.len())
        .into_par_iter()
        .map(|i| {
            linear_assign_to_dest(
                destination_nodes[i],
                from_nodes,
                to_nodes,
                arc_frequencies,
                costs,
                &demands[(i * n_nodes)..((i + 1) * n_nodes)],
                n_nodes,
            )
        })
        .unzip();

    // us[(i * n_nodes)..((i + 1) * n_nodes)].copy_from_slice(&u);
    // vs[(i * n_arcs)..((i + 1) * n_arcs)].copy_from_slice(&v);
    return (
        us.into_iter().flatten().collect(),
        vs.into_iter().flatten().collect(),
    );
}

fn linear_assign_to_dest(
    destination_node: usize,
    from_nodes: &[usize],
    to_nodes: &[usize],
    arc_frequencies: &[f32],
    costs: &[f32],
    demands: &[f32],
    n_nodes: usize,
) -> (Vec<f32>, Vec<f32>) {
    let mut u = vec![INFINITY; n_nodes];
    let mut arc_flows = vec![0.0; to_nodes.len()];

    u[destination_node] = 0.0;

    let mut node_frequencies = vec![0.0; n_nodes];
    let mut pq = PriorityQueue::new();
    let mut loading_q = VecDeque::new();
    let mut arcs_by_target_node: HashMap<usize, Vec<usize>> = HashMap::new();

    for i in 0..from_nodes.len() {
        let arc_cost = (u[to_nodes[i]] + costs[i]) * 60000.0;
        pq.push(i, -arc_cost as isize);

        if arcs_by_target_node.contains_key(&to_nodes[i]) {
            arcs_by_target_node.get_mut(&to_nodes[i]).unwrap().push(i);
        } else {
            arcs_by_target_node.insert(to_nodes[i], vec![i]);
        }
    }

    while !pq.is_empty() {
        let (arc, min_cost) = pq.pop().unwrap();

        let i = from_nodes[arc];
        let fa = arc_frequencies[arc];

        let f_min_cost = if min_cost == isize::MIN {
            INFINITY
        } else {
            -(min_cost as f32) / 60000.0
        };

        if u[i] < f_min_cost {
            continue;
        }

        if fa.is_infinite() {
            u[i] = f_min_cost;
            node_frequencies[i] = fa;
        } else {
            u[i] = (fu(node_frequencies[i], u[i]) + fa * f_min_cost) / (node_frequencies[i] + fa);
            node_frequencies[i] = node_frequencies[i] + fa;
        }

        loading_q.push_back(arc);

        if let Some(arcs) = arcs_by_target_node.get(&i) {
            for arc in arcs {
                let arc_cost = (u[i] + costs[*arc]) * 60000.0;
                pq.change_priority(arc, -arc_cost as isize);
            }
        }
    }

    // Loading
    let mut arc_flows = vec![0.0; to_nodes.len()];
    let mut node_flows = Vec::from(demands);

    for i in 0..from_nodes.len() {
        let arc_cost = (u[to_nodes[i]] + costs[i]) * 60000.0;
        pq.push(i, -arc_cost as isize);
    }

    while !loading_q.is_empty() {
        let arc = loading_q.pop_back().unwrap();

        let i = from_nodes[arc];
        let j = to_nodes[arc];
        let fa = arc_frequencies[arc];

        if fa.is_infinite() {
            arc_flows[arc] = node_flows[i];
        } else {
            arc_flows[arc] = fa / node_frequencies[i] * node_flows[i];
        }
        node_flows[j] += arc_flows[arc];
    }

    return (u, arc_flows);
}

fn calc_effective_frequencies(
    to_nodes: &[usize],
    arc_frequencies: &[f32],
    arc_flows: &[f32],
    nominal_arc_frequencies: &[f32],
    beta: f32,
    bus_capacity: f32,
) -> Vec<f32> {
    let n_arcs = nominal_arc_frequencies.len();
    let n_dest = arc_frequencies.len() / n_arcs;

    let mut effective_frequencies = vec![INFINITY; n_arcs];

    for arc in 0..n_arcs {
        if nominal_arc_frequencies[arc].is_infinite() {
            continue; // non-boarding arcs
        }

        let capacity_per_hour = nominal_arc_frequencies[arc] * bus_capacity;

        let boarding_flow_into_stop = arc_flows[arc..].iter().step_by(n_arcs).sum::<f32>();
        let onboard_flow_after_stop: f32 = to_nodes
            .iter()
            .enumerate()
            .filter(|(_, &v)| v == to_nodes[arc])
            .map(|(index, _)| arc_flows[index..].iter().step_by(n_arcs).sum::<f32>())
            .sum::<f32>();

        for dst in 0..n_dest {
            if onboard_flow_after_stop < capacity_per_hour {
                effective_frequencies[arc + dst * n_arcs] = nominal_arc_frequencies[arc]
                    * (1.0
                        - (boarding_flow_into_stop
                            / (capacity_per_hour - onboard_flow_after_stop
                                + boarding_flow_into_stop))
                            .powf(beta))
            } else {
                effective_frequencies[arc + dst * n_arcs] = 0.0;
            }

            if effective_frequencies[arc + dst * n_arcs] < 1.0 / 16.7 {
                effective_frequencies[arc + dst * n_arcs] = 1.0 / 16.7;
            }
        }
    }

    return effective_frequencies;
}

fn main() {}

// fn main() {
//     // 0, 1, 2, 3,  4,  5
//     // A, B, X, Y, X2, Y3
//     let from_nodes = [0, 0, 4, 4, 2, 2, 3, 3, 5, 5];
//     let to_nodes = [1, 4, 2, 3, 4, 5, 5, 1, 3, 1];
//     let frequencies = [
//         1.0 / 6.0,
//         1.0 / 6.0,
//         INFINITY,
//         INFINITY,
//         1.0 / 6.0,
//         1.0 / 15.0,
//         1.0 / 15.0,
//         1.0 / 3.0,
//         INFINITY,
//         INFINITY,
//     ];
//     let costs = [25.0, 7.0, 0.0, 6.0, 0.0, 4.0, 0.0, 10.0, 0.0, 4.0];
//     let demands = [1.0, -1.0, 0.0, 0.0, 0.0, 0.0];

//     _ = linear_assign(&from_nodes, &to_nodes, &frequencies, &costs, 1, &demands);
// }

// void *assign2(int **alignments, float *frequencies, float **travel_time, int n_routes, int n_nodes, int *route_lengths, float *out)

#[pyfunction]
fn congested_assign_allow_threads(
    py: Python<'_>,
    alignments: Vec<Vec<usize>>,
    frequencies: Vec<f32>,
    travel_time: Vec<Vec<f32>>,
    demands_mat: Vec<Vec<f32>>,
    average_decay_factor: f32,
    beta: f32,
    bus_capacity: f32,
    n_iters: usize,
) -> Vec<Vec<f32>> {
    return py.allow_threads(|| {
        congested_assign(
            alignments,
            frequencies,
            travel_time,
            demands_mat,
            average_decay_factor,
            beta,
            bus_capacity,
            n_iters,
        )
    });
}

#[pyfunction]
fn congested_assign(
    alignments: Vec<Vec<usize>>,
    frequencies: Vec<f32>,
    travel_time: Vec<Vec<f32>>,
    demands_mat: Vec<Vec<f32>>,
    average_decay_factor: f32,
    beta: f32,
    bus_capacity: f32,
    n_iters: usize,
) -> Vec<Vec<f32>> {
    // let n_routes = alignments.len();
    let n_nodes = travel_time.len();
    // let n_nodes_e = n_nodes * 3;
    let n_arcs: usize = alignments.iter().map(|route| (route.len() - 1) * 3).sum();

    let mut from_nodes = vec![0usize; n_arcs];
    let mut to_nodes = vec![0usize; n_arcs];
    let mut arc_frequencies = vec![INFINITY; n_arcs];
    let mut costs = vec![0.0; n_arcs];

    let mut arc_idx = 0usize;
    let mut node_idx = n_nodes;
    // let mut arcs: Vec<(usize, usize, f32, f32)> = vec![];

    for (r, route) in alignments.iter().enumerate() {
        // First stop node (boarding only)
        from_nodes[arc_idx] = route[0];
        to_nodes[arc_idx] = node_idx;
        arc_frequencies[arc_idx] = frequencies[r];
        costs[arc_idx] = 0.0;
        // arcs.push((route[0], node_idx, frequencies[r], 0.0));
        node_idx += 1;
        arc_idx += 1;

        for idx in 0..(route.len() - 1) {
            let i = route[idx];
            let j = route[idx + 1];

            // ==================================== //
            //                                      //
            // +···········+          +-----------+ //
            // · i_0 (  i) ·          | j_0 (  j) | //
            // +···········+          +-----------+ //
            //     ·   ^                  |   ^     //
            //     ·   ·                  |   |     //
            //     v   ·                  v   |     //
            // +-----------+          +-----------+ //
            // | i_r (  0) |  ------> | j_r ( +1) | //
            // +-----------+          +-----------+ //
            //                                      //
            // ==================================== //

            // Intermediate arcs (i_r -> j_r)
            from_nodes[arc_idx] = node_idx - 1;
            to_nodes[arc_idx] = node_idx;
            arc_frequencies[arc_idx] = INFINITY;
            costs[arc_idx] = travel_time[i][j] / 60.0;
            // arcs.push((node_idx - 1, node_idx, INFINITY, travel_time[i][j]));
            arc_idx += 1;

            if j != *route.last().unwrap() {
                // Stop node for j - Boarding arc (j_0 -> j_r)
                from_nodes[arc_idx] = j;
                to_nodes[arc_idx] = node_idx;
                arc_frequencies[arc_idx] = frequencies[r];
                costs[arc_idx] = 0.0;
                // arcs.push((j, node_idx, frequencies[r], 0.0));
                arc_idx += 1;
            }

            // Stop node for j - Alighting arc (j_r -> j_0)
            from_nodes[arc_idx] = node_idx;
            to_nodes[arc_idx] = j;
            arc_frequencies[arc_idx] = INFINITY;
            costs[arc_idx] = 0.0;
            // arcs.push((node_idx, j, INFINITY, 0.0));
            arc_idx += 1;

            node_idx += 1;
        }
    }

    let mut demands = vec![0.0; node_idx * (n_nodes - 1)];
    for dst in 1..n_nodes {
        for node in 0..n_nodes {
            if node == dst {
                continue;
            }

            demands[(dst - 1) * node_idx + node] = demands_mat[node][dst];
            demands[(dst - 1) * node_idx + dst] -= demands_mat[node][dst];
        }
    }

    // println!("from_nodes = {:?}", from_nodes);
    // println!("to_nodes = {:?}", to_nodes);
    // println!("frequencies = {:?}", arc_frequencies);
    // println!("costs = {:?}", costs);

    // let (u, _) = _congested_assign(
    //     &[0, 0, 1, 3, 4, 5, 5, 6, 7],
    //     &[3, 4, 5, 6, 5, 1, 7, 2, 2],
    //     &[
    //         16.0, 6.0, 6.0, INFINITY, INFINITY, INFINITY, INFINITY, INFINITY, INFINITY,
    //     ],
    //     &[
    //         0.0,
    //         0.0,
    //         0.0,
    //         24.01 / 60.0,
    //         20.01 / 60.0,
    //         0.0,
    //         20.01 / 60.0,
    //         0.0,
    //         0.0,
    //     ],
    //     &[
    //         10.0, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 350.0, 10.0, -360.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    //     ],
    //     &[1, 2],
    //     average_decay_factor,
    //     beta,
    //     bus_capacity,
    // );

    let (u, _) = _congested_assign(
        &from_nodes,
        &to_nodes,
        &arc_frequencies,
        &costs,
        &demands,
        &(1..n_nodes).collect::<Vec<usize>>(),
        average_decay_factor,
        beta,
        bus_capacity,
        n_iters,
    );

    // println!("ulen = {} | node_idx = {}", u.len(), node_idx);
    let mut out: Vec<Vec<f32>> = vec![vec![0.0; n_nodes]; n_nodes];
    for i in 0..n_nodes {
        for j in 1..n_nodes {
            out[i][j] = u[(j - 1) * node_idx + i];
        }
    }

    return out;
}

fn _congested_assign(
    from_nodes: &[usize],
    to_nodes: &[usize],
    frequencies: &[f32],
    costs: &[f32],
    demands: &[f32],
    destination_nodes: &[usize],
    average_decay_factor: f32,
    beta: f32,
    bus_capacity: f32,
    n_iters: usize,
) -> (Vec<f32>, Vec<f32>) {
    let (u, mut v) = linear_assign(
        &from_nodes,
        &to_nodes,
        &frequencies,
        &costs,
        &destination_nodes,
        &demands,
    );

    let mut arc_frequencies = vec![INFINITY; frequencies.len()];
    arc_frequencies.clone_from_slice(&frequencies);

    let mut up = vec![0.0f32; u.len()];

    for _ in 1..n_iters {
        arc_frequencies = calc_effective_frequencies(
            &to_nodes,
            &arc_frequencies,
            &v,
            &frequencies,
            beta,
            bus_capacity,
        );

        let out = linear_assign(
            &from_nodes,
            &to_nodes,
            &arc_frequencies,
            &costs,
            &destination_nodes,
            &demands,
        );

        up = out.0;

        v = out
            .1
            .par_iter()
            .zip(v.par_iter())
            .map(|(fp, f)| (1.0 - average_decay_factor) * f + average_decay_factor * fp)
            .collect();

        // v = Vec::from_iter(
        //     zip(out.1, v)
        //         .map(|(fp, f)| (1.0 - average_decay_factor) * f + average_decay_factor * fp),
        // );
    }

    up = Vec::from_iter(up.into_iter().map(|x| x * 60.0));

    return (up, v);
}

/// A Python module implemented in Rust.
#[pymodule]
fn rlss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(congested_assign_allow_threads, m)?)?;
    m.add_function(wrap_pyfunction!(congested_assign, m)?)?;
    Ok(())
}
