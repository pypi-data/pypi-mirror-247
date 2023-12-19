extern crate queues;

// use ndarray::{array, Array, Array1, Array2};
use priority_queue::PriorityQueue;
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

    let n_arcs = arc_frequencies.len();
    let n_dest = destination_nodes.len();

    let mut us = vec![INFINITY; (n_dest * n_nodes) as usize];
    let mut vs = vec![0.0f32; (n_dest * n_arcs) as usize];

    for i in 0..destination_nodes.len() {
        let (u, v) = linear_assign_to_dest(
            destination_nodes[i],
            from_nodes,
            to_nodes,
            arc_frequencies,
            costs,
            &demands[(i * n_nodes)..((i + 1) * n_nodes)],
        );

        us[(i * n_nodes)..((i + 1) * n_nodes)].copy_from_slice(&u);
        vs[(i * n_arcs)..((i + 1) * n_arcs)].copy_from_slice(&v);
    }

    return (us, vs);
}

fn linear_assign_to_dest(
    destination_node: usize,
    from_nodes: &[usize],
    to_nodes: &[usize],
    arc_frequencies: &[f32],
    costs: &[f32],
    demands: &[f32],
) -> (Vec<f32>, Vec<f32>) {
    let n_nodes = max(
        from_nodes.iter().max().unwrap(),
        to_nodes.iter().max().unwrap(),
    ) + 1;
    let mut u = vec![INFINITY; n_nodes];
    let mut node_frequencies = vec![0.0; n_nodes];

    // for dst in 0..n_nodes {
    u[destination_node] = 0.0;

    let mut pq = PriorityQueue::new();
    let mut loading_q = VecDeque::new();
    let mut arcs_by_target_node: HashMap<usize, Vec<usize>> = HashMap::new();

    for i in 0..from_nodes.len() {
        let arc_cost = (u[to_nodes[i]] + costs[i]) * 60000.0;
        // println!(
        //     "[{}->{}] Arc: {}, Cost: {}, u: {}, cost: {}, freq: {}, dst: {}",
        //     from_nodes[i],
        //     to_nodes[i],
        //     i,
        //     arc_cost,
        //     u[to_nodes[i]],
        //     costs[i],
        //     arc_frequencies[i],
        //     destination_node
        // );
        pq.push(i, -arc_cost as isize);

        if arcs_by_target_node.contains_key(&to_nodes[i]) {
            arcs_by_target_node.get_mut(&to_nodes[i]).unwrap().push(i);
        } else {
            arcs_by_target_node.insert(to_nodes[i], vec![i]);
        }
    }

    // println!("-----");

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
            // println!("");
            // println!("[{}->{}] Arc: {} NO", from_nodes[arc], to_nodes[arc], arc);

            continue;
        }

        // println!("");
        // println!(
        //     "[{}->{}] Arc: {}, Cost:{}, f_min_cost: {}",
        //     from_nodes[arc], to_nodes[arc], arc, min_cost, f_min_cost
        // );

        if fa.is_infinite() {
            u[i] = f_min_cost;
            node_frequencies[i] = fa;
            // println!("> Update node {}: u={}, f={}", i, u[i], node_frequencies[i]);
        } else {
            u[i] = (fu(node_frequencies[i], u[i]) + fa * f_min_cost) / (node_frequencies[i] + fa);
            node_frequencies[i] = node_frequencies[i] + fa;
            // println!("> Update node {}: u={}, f={}", i, u[i], node_frequencies[i]);
        }

        loading_q.push_back(arc);

        // change priority
        if let Some(arcs) = arcs_by_target_node.get(&i) {
            for arc in arcs {
                let arc_cost = (u[i] + costs[*arc]) * 60000.0;
                pq.change_priority(arc, -arc_cost as isize);
                // println!(
                //     "> Update [{}->{}]: {}",
                //     from_nodes[*arc],
                //     to_nodes[*arc],
                //     arc_cost / 60000.0
                // );
            }
        }
    }

    // println!("\nu = {:?}", u);

    // Loading
    let mut arc_flows = vec![0.0; to_nodes.len()];
    let mut node_flows = Vec::from(demands);

    for i in 0..from_nodes.len() {
        let arc_cost = (u[to_nodes[i]] + costs[i]) * 60000.0;
        // println!(
        //     "[{}->{}] Arc: {}, Cost: {}, u: {}, cost: {}, freq: {}, dst: {}",
        //     from_nodes[i],
        //     to_nodes[i],
        //     i,
        //     arc_cost,
        //     u[to_nodes[i]],
        //     costs[i],
        //     arc_frequencies[i],
        //     destination_node
        // );
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

        // println!(
        //     "[{}->{}] flow={} | {} {} {} | {} {} {} {} {} {}",
        //     i,
        //     j,
        //     arc_flows[arc],
        //     fa,
        //     node_frequencies[i],
        //     node_flows[i],
        //     node_flows[0],
        //     node_flows[4],
        //     node_flows[2],
        //     node_flows[5],
        //     node_flows[3],
        //     node_flows[1]
        // );

        // println!("{:?}", arc_flows);
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

fn congested_assign(
    from_nodes: &[usize],
    to_nodes: &[usize],
    frequencies: &[f32],
    costs: &[f32],
    demands: &[f32],
    average_decay_factor: f32,
    beta: f32,
    bus_capacity: f32,
) -> (Vec<f32>, Vec<f32>) {
    let (u, mut v) = linear_assign(
        &from_nodes,
        &to_nodes,
        &frequencies,
        &costs,
        &[1, 2],
        &demands,
    );

    let mut arc_frequencies = vec![INFINITY; frequencies.len()];
    arc_frequencies.clone_from_slice(&frequencies);

    let x: Vec<f32> = u.iter().map(|x| x * 60.0).collect();
    println!("f_a = {:?}", arc_frequencies);
    println!("costs = {:?}", costs);
    println!("demands = {:?}", demands);
    println!("v = {:?}", v);
    println!("u = {:?}", x);

    let mut up = vec![0.0; 0];
    let mut vp: Vec<f32>;

    for _ in 1..70 {
        arc_frequencies = calc_effective_frequencies(
            &to_nodes,
            &arc_frequencies,
            &v,
            &frequencies,
            beta,
            bus_capacity,
        );

        (up, vp) = linear_assign(
            &from_nodes,
            &to_nodes,
            &arc_frequencies,
            &costs,
            &[1, 2],
            &demands,
        );

        v = Vec::from_iter(
            zip(vp, v).map(|(fp, f)| (1.0 - average_decay_factor) * f + average_decay_factor * fp),
        );
        // let x = Vec::from_iter(up.into_iter().map(|x| x * 60.0));

        // println!(
        //     "\n===============\n Iteration {}\n===============\nf_a = {:?}\nfn_a = {:?}\nv = {:?}\nu = {:?}",
        //     i, arc_frequencies, frequencies, v, x
        // );
    }

    up = Vec::from_iter(up.into_iter().map(|x| x * 60.0));

    return (up, v);
}

//     // 0, 1, 2,  3,  5,  6,  4,  7
//     // A, B, C, Ae, Al, Bl, Ce, Cl

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

    congested_assign(
        &from_nodes,
        &to_nodes,
        &frequencies,
        &costs,
        &demands,
        0.02,
        0.2,
        20.0,
    );

    let (u, mut v) = linear_assign(
        &from_nodes,
        &to_nodes,
        &frequencies,
        &costs,
        &[1, 2],
        &demands,
    );

    let mut arc_frequencies = vec![INFINITY; frequencies.len()];
    arc_frequencies.clone_from_slice(&frequencies);

    const BETA: f32 = 0.2;
    const BUS_CAPACITY: f32 = 20.0;

    let x: Vec<f32> = u.iter().map(|x| x * 60.0).collect();
    println!("f_a = {:?}", arc_frequencies);
    println!("v = {:?}", v);
    println!("u = {:?}", x);

    for i in 1..70 {
        arc_frequencies = calc_effective_frequencies(
            &to_nodes,
            &arc_frequencies,
            &v,
            &frequencies,
            BETA,
            BUS_CAPACITY,
        );

        let (up, vp) = linear_assign(
            &from_nodes,
            &to_nodes,
            &arc_frequencies,
            &costs,
            &[1, 2],
            &demands,
        );

        v = Vec::from_iter(zip(vp, v).map(|(fp, f)| (1.0 - 0.02) * f + 0.02 * fp));
        let x = Vec::from_iter(up.into_iter().map(|x| x * 60.0));

        println!(
        "\n===============\n Iteration {}\n===============\nf_a = {:?}\nfn_a = {:?}\nv = {:?}\nu = {:?}",
        i, arc_frequencies, frequencies, v, x
    );
    }
}
