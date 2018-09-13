
def run_simulation_three_pops(n1: int, n2: int, n3: int, L: int, theta: float, D: float, D1: float):
    with open(file_fake_labs, 'w') as f:
        for i in range(n1+n2+n3):
            if i < n1:
                pop = 'PAP'
            elif i < n2:
                pop = 'BRI'
            else:
                pop = 'CHI'
            f.write(f'{pop}  {pop}{i}\n')

    with open('res3.txt', 'a') as f:
        f.write(str(L))
    scrm_command = f'scrm {n1+n2+n3} {L} -t {theta} -I 3 {n1} {n2} {n3} -ej {D} 2 1 -ej {D1} 3 2'
    run_scrm(scrm_command)
    transcode_scrm(n1+n2)



if SIMULATION_CASE == 3:
    Ls3 = [10000]
    for L in Ls3:
        run_simulation_three_pops(50, 100, 150, int(L), 1, 0.2, 0.1)