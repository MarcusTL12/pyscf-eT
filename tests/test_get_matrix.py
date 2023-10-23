from pyscf_eT import get_matrix

def test_get_matrix():
    m = get_matrix.get_matrix("eta_pq_tilde", "testdata/test.out")
    print(m)
