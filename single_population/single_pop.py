def run_simulation_single_pop(nb_individual: int, L: int, theta: float):
    """Run a simulation for nb_pop with each n individual, splitting at time D, 2D, 3D, ..."""
    with open(file_fake_labs, 'w') as f:
        for i in range(nb_individual):
            pop = 'pop'
            f.write(f'{pop} {pop}{i}\n')


    scrm_command = f'scrm {nb_individual} {L} -t {theta} --print-model -l -1 -L'
    run_scrm(scrm_command)
    transcode_scrm(nb_individual)

if SIMULATION_CASE == 1:
    Ls3 = [4000]
    for L in Ls3:
        run_simulation_single_pop(400, int(L), 1)