use crate::assignment::utils::{graph2mat, mat2graph};
use priority_queue::PriorityQueue;
use pyo3::prelude::*;
use rayon::prelude::*;
use std::cmp;
use std::collections::{HashMap, VecDeque};
use std::f32::INFINITY;

#[pyfunction]
pub fn linear_assign(
    py: Python<'_>,
    from: Vec<usize>,
    to: Vec<usize>,
    arc_freqs: Vec<f32>,
    costs: Vec<f32>,
    demands: Vec<f32>,
    dsts: Vec<usize>,
) -> (Vec<f32>, Vec<f32>) {
    return py.allow_threads(|| _linear_assign(&from, &to, &arc_freqs, &costs, &demands, &dsts));
}

#[pyfunction]
pub fn mat_linear_assign(
    py: Python<'_>,
    alignments: Vec<Vec<usize>>,
    freqs: Vec<f32>,
    travel_time_mat: Vec<Vec<f32>>,
    demands_mat: Vec<Vec<f32>>,
) -> Vec<Vec<f32>> {
    return py.allow_threads(|| {
        let mat_size = travel_time_mat.len();

        let (from, to, arc_freqs, costs, demands) =
            mat2graph(alignments, freqs, travel_time_mat, demands_mat);

        let dsts = (1..mat_size).collect::<Vec<_>>();
        let (u, _) = _linear_assign(&from, &to, &arc_freqs, &costs, &demands, &dsts);

        return graph2mat(u, mat_size);
    });
}

pub fn _linear_assign(
    from: &[usize],
    to: &[usize],
    arc_freqs: &[f32],
    costs: &[f32],
    demands: &[f32],
    dsts: &[usize],
) -> (Vec<f32>, Vec<f32>) {
    let n_nodes = cmp::max(from.iter().max().unwrap(), to.iter().max().unwrap()) + 1;

    let (us, vs): (Vec<Vec<f32>>, Vec<Vec<f32>>) = (0..dsts.len())
        .into_par_iter()
        .map(|i| {
            _linear_assign_to_dest(
                dsts[i],
                n_nodes,
                from,
                to,
                arc_freqs,
                costs,
                &demands[(i * n_nodes)..((i + 1) * n_nodes)],
            )
        })
        .unzip();

    return (
        us.into_iter().flatten().collect(),
        vs.into_iter().flatten().collect(),
    );
}

fn _linear_assign_to_dest(
    dst: usize,
    n_nodes: usize,
    from: &[usize],
    to: &[usize],
    arc_freqs: &[f32],
    arc_costs: &[f32],
    demands: &[f32],
) -> (Vec<f32>, Vec<f32>) {
    let mut time_from = vec![INFINITY; n_nodes];
    let mut arc_flow = vec![0.0f32; from.len()];
    let mut node_flow = Vec::from(demands);

    let mut node_freqs = vec![0.0f32; n_nodes];
    let mut pq = PriorityQueue::new();
    let mut lq = VecDeque::new();
    let mut arcs_into: HashMap<usize, Vec<usize>> = HashMap::new();

    time_from[dst] = 0.0;

    fn fu(f: f32, u: f32) -> f32 {
        if f.abs() < 1e-8 && u.is_infinite() {
            return 1.0;
        }

        return f * u;
    }

    for arc in 0..from.len() {
        if from[arc] == dst {
            // If the source of arc is the destination, ignore.
            continue;
        }

        let cost = (time_from[to[arc]] + arc_costs[arc]) * 60000.0;
        pq.push(arc, -cost as isize);

        if arcs_into.contains_key(&to[arc]) {
            arcs_into.get_mut(&to[arc]).unwrap().push(arc);
        } else {
            arcs_into.insert(to[arc], vec![arc]);
        }
    }

    while !pq.is_empty() {
        let (arc, priority) = pq.pop().unwrap();

        let i = from[arc];
        let fa = arc_freqs[arc];

        let min_cost = if priority == isize::MIN {
            INFINITY
        } else {
            -(priority as f32) / 60000.0
        };

        if time_from[i] < min_cost {
            continue;
        }

        if arc_freqs[arc].is_infinite() {
            time_from[i] = min_cost;
            node_freqs[i] = fa;
        } else {
            time_from[i] = (fu(node_freqs[i], time_from[i]) + fa * min_cost) / (node_freqs[i] + fa);
            node_freqs[i] += fa;
        }

        lq.push_back(arc);

        if let Some(arcs) = arcs_into.get(&i) {
            for arc in arcs {
                let arc_cost = (time_from[i] + arc_costs[*arc]) * 60000.0;
                let priority = -arc_cost as isize;
                pq.change_priority(arc, priority);
            }
        }
    }

    // Loading
    while !lq.is_empty() {
        let arc = lq.pop_back().unwrap();

        let i = from[arc];
        let j = to[arc];
        let fa = arc_freqs[arc];

        if fa.is_infinite() {
            arc_flow[arc] = node_flow[i];
        } else {
            arc_flow[arc] = fa / node_freqs[i] * node_flow[i];
        }
        node_flow[j] += arc_flow[arc];
    }

    return (time_from, arc_flow);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn linear_assign_spiess1984() {
        // Small network from Spiess and Florian (1984)

        // 0, 1, 2, 3,  4,  5
        // A, B, X, Y, X2, Y3
        let from_nodes = [0, 0, 4, 4, 2, 2, 3, 3, 5, 5];
        let to_nodes = [1, 4, 2, 3, 4, 5, 5, 1, 3, 1];
        let frequencies = [
            1.0 / 6.0,
            1.0 / 6.0,
            INFINITY,
            INFINITY,
            1.0 / 6.0,
            1.0 / 15.0,
            1.0 / 15.0,
            1.0 / 3.0,
            INFINITY,
            INFINITY,
        ];
        let costs = [25.0, 7.0, 0.0, 6.0, 0.0, 4.0, 0.0, 10.0, 0.0, 4.0];
        let demands = [1.0, -1.0, 0.0, 0.0, 0.0, 0.0];
        let destination_nodes = [1usize];

        let (u, v) = _linear_assign(
            &from_nodes,
            &to_nodes,
            &frequencies,
            &costs,
            &demands,
            &destination_nodes,
        );

        let x: Vec<f32> = u.iter().map(|x| *x * 1.0).collect();

        assert_relative_eq!(x[0], 27.75);
        assert_relative_eq!(x[1], 0.0);
        assert_relative_eq!(x[2], 19.071426);
        assert_relative_eq!(x[3], 11.5);
        assert_relative_eq!(x[4], 17.5);
        assert_relative_eq!(x[5], 4.0);

        assert_relative_eq!(v[0], 0.5);
        assert_relative_eq!(v[1], 0.5);
        assert_relative_eq!(v[2], 0.0);
        assert_relative_eq!(v[3], 0.5);
        assert_relative_eq!(v[4], 0.0);
        assert_relative_eq!(v[5], 0.0);
        assert_relative_eq!(v[6], 0.083333336);
        assert_relative_eq!(v[7], 0.4166667);
        assert_relative_eq!(v[8], 0.0);
        assert_relative_eq!(v[9], 0.083333336);
    }

    #[test]
    fn linear_assign_cepeda2006_small() {
        // Small network from Cepada et al. (2006)

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
            10.0, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 10.0, -110.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        ];

        let destination_nodes = [1, 2];
        let (u, v) = _linear_assign(
            &from_nodes,
            &to_nodes,
            &frequencies,
            &costs,
            &demands,
            &destination_nodes,
        );

        let x: Vec<f32> = u.iter().map(|x| *x * 60.0).collect();

        assert_relative_eq!(x[0], 30.01);
        assert_relative_eq!(x[1], 0.0);
        assert_relative_eq!(x[2], INFINITY);
        assert_relative_eq!(x[3], INFINITY);
        assert_relative_eq!(x[4], 20.01);
        assert_relative_eq!(x[5], 0.0);
        assert_relative_eq!(x[6], INFINITY);
        assert_relative_eq!(x[7], INFINITY);
        assert_relative_eq!(x[8], 27.76);
        assert_relative_eq!(x[9], 30.01);
        assert_relative_eq!(x[10], 0.0);
        assert_relative_eq!(x[11], 24.01);
        assert_relative_eq!(x[12], 40.02);
        assert_relative_eq!(x[13], 20.01);
        assert_relative_eq!(x[14], 0.0);
        assert_relative_eq!(x[15], 0.0);

        assert_relative_eq!(v[0], 0.0);
        assert_relative_eq!(v[1], 10.0);
        assert_relative_eq!(v[2], 0.0);
        assert_relative_eq!(v[3], 0.0);
        assert_relative_eq!(v[4], 10.0);
        assert_relative_eq!(v[5], 10.0);
        assert_relative_eq!(v[6], 0.0);
        assert_relative_eq!(v[7], 0.0);
        assert_relative_eq!(v[8], 0.0);
        assert_relative_eq!(v[9], 100.0);
        assert_relative_eq!(v[10], 0.0);
        assert_relative_eq!(v[11], 10.0);
        assert_relative_eq!(v[12], 100.0);
        assert_relative_eq!(v[13], 0.0);
        assert_relative_eq!(v[14], 0.0);
        assert_relative_eq!(v[15], 10.0);
        assert_relative_eq!(v[16], 100.0);
        assert_relative_eq!(v[17], 10.0);
    }
}
