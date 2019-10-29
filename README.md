# medeas_simulation
This pipeline aim at reproducing all the figures and related data that are present in the draft. 

It requires first to have first run the 1000 genome pipeline in the same folder with three different scenario (no prunning/ plink pruning and random pruning).
The location of this simulation should then be the `config.yaml` file. 

to run it on a slurm cluster, the following command can be use:

`snakemake -j 10 --cluster-config cluster.json --cluster "sbatch -p {cluster.partition} --mem={cluster.mem} -t {cluster.time} -A {cluster.account} --cpus-per-task={cluster.cpus} --job-name={cluster.name} --error={cluster.error} --output={cluster.output}"`
