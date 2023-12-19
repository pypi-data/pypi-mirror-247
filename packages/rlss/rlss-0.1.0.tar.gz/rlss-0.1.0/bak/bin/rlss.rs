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
// void *assign2(int **alignments, float *frequencies, float **travel_time, int n_routes, int n_nodes, int *route_lengths, float *out)

fn main() {
    // 0, 1, 2,  3,  4,  5,  6,  7
    // A, B, C, Ae, Al, Bl, Ce, Cl
    let from_nodes = [0, 0, 1, 3, 4, 5, 5, 6, 7];
    let to_nodes = [3, 4, 5, 6, 5, 1, 7, 2, 2];
    let frequencies = [
        16.0, 6.0, 6.0, INFINITY, INFINITY, INFINITY, INFINITY, INFINITY, INFINITY,
    ];
    let costs = [
        0.0,
        0.0,
        0.0,
        24.01 / 60.0,
        20.01 / 60.0,
        0.0,
        20.01 / 60.0,
        0.0,
        0.0,
    ];
    let demands = [
        10.0, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 350.0, 10.0, -360.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    ];

    let destination_nodes = [1, 2];

    _ = linear_assign(
        &from_nodes,
        &to_nodes,
        &frequencies,
        &costs,
        &destination_nodes,
        &demands,
    );

    println!("OK");
}
