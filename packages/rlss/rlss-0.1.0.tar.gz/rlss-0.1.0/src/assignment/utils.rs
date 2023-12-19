use std::f32::INFINITY;

pub fn mat2graph(
    alignments: Vec<Vec<usize>>,
    freqs: Vec<f32>,
    travel_time_mat: Vec<Vec<f32>>,
    demands_mat: Vec<Vec<f32>>,
) -> (Vec<usize>, Vec<usize>, Vec<f32>, Vec<f32>, Vec<f32>) {
    let n_nodes = travel_time_mat.len();
    let n_arcs: usize = alignments.iter().map(|route| (route.len() - 1) * 3).sum();

    let mut from = vec![0usize; n_arcs];
    let mut to = vec![0usize; n_arcs];
    let mut arc_freqs = vec![INFINITY; n_arcs];
    let mut costs = vec![0.0; n_arcs];

    let mut arc_idx = 0usize;
    let mut node_idx = n_nodes;

    for (r, route) in alignments.iter().enumerate() {
        // First stop node (boarding only)
        from[arc_idx] = route[0];
        to[arc_idx] = node_idx;
        arc_freqs[arc_idx] = freqs[r];
        costs[arc_idx] = 0.0;
        arc_idx += 1;
        node_idx += 1;

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
            from[arc_idx] = node_idx - 1;
            to[arc_idx] = node_idx;
            arc_freqs[arc_idx] = INFINITY;
            costs[arc_idx] = travel_time_mat[i][j];
            arc_idx += 1;

            if j != *route.last().unwrap() {
                // Stop node for j - Boarding arc (j_0 -> j_r)
                from[arc_idx] = j;
                to[arc_idx] = node_idx;
                arc_freqs[arc_idx] = freqs[r];
                costs[arc_idx] = 0.0;
                arc_idx += 1;
            }

            // Stop node for j - Alighting arc (j_r -> j_0)
            from[arc_idx] = node_idx;
            to[arc_idx] = j;
            arc_freqs[arc_idx] = INFINITY;
            costs[arc_idx] = 0.0;
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

    return (from, to, arc_freqs, costs, demands);
}

pub fn graph2mat(u: Vec<f32>, mat_size: usize) -> Vec<Vec<f32>> {
    let mut umat = vec![vec![0.0; mat_size]; mat_size];
    let n_graph_nodes = u.len() / (mat_size - 1);

    for i in 0..mat_size {
        for j in (i + 1)..mat_size {
            umat[i][j] = u[(j - 1) * n_graph_nodes + i];
        }
    }

    return umat;
}
