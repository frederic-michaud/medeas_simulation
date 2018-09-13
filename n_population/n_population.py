



def run_simulation_n_pops(n_per_pop: int, nb_pop: int, L: int, theta: float, D: float):
    """Run a simulation for nb_pop with each n individual, splitting at time D, 2D, 3D, ..."""
    with open(file_fake_labs, 'w') as f:
        for i in range(n_per_pop * nb_pop):
            pop = 'pop{}'.format(i // n_per_pop)
            f.write(f'{pop} {pop}{i}\n')

    all_pop_string = nb_pop*(str(n_per_pop) + " ")
    all_split_string = " ".join([f'-ej {D*i} {i} {i+1}' for i in range(1,nb_pop)])
    scrm_command = f'scrm {n_per_pop*nb_pop} {L} -t {theta} -I {nb_pop} {all_pop_string}{all_split_string} --print-model -l -1 -L'
    run_scrm(scrm_command)
    transcode_scrm(n_per_pop * nb_pop)

if SIMULATION_CASE > 3:
    Ls3 = [10000]
    for L in Ls3:
        run_simulation_n_pops(50, SIMULATION_CASE, int(L), 1, 0.5)