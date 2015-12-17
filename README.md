# qtools

[![Build Status](https://travis-ci.org/YeoLab/qtools.svg)](https://travis-ci.org/YeoLab/qtools)

## What is `qtools`?

qtools has helper functions to submit jobs to compute clusters (PBS on TSCC, SGE on oolite) from within Python

* Free software: BSD license

## Installation

To install this code, clone this github repository and use `pip` to install

    git clone git@github.com:YeoLab/qtools
    cd qtools
    pip install .  # The "." means "install *this*, the folder where I am now"


## Features

### Simple example

Here's an example of a single job where I want to use `hmmscan` to find domains in protein sequences, specifying the walltime and number of processors.

```
import qtools

command = 'bedtools intersect exons.bed placental_conserved_elements.bed'
sub = qtools.Submitter(command, 'intersect')
```

And this will create a submitter script with the default options:

* `walltime="00:30:00"`
* `nodes=1`
* `ppn=1` (processors per node - increase this one first, instead of the numbers of nodes. Max is 16)
* `group="yeo-group"`
* `queue="home-scrm"` (could also be `home-yeo`


This writes a file called `intersect.sh` which looks like this:

```
#!/bin/bash
#PBS -N intersect
#PBS -o intersect.out
#PBS -e intersect.err
#PBS -V
#PBS -l walltime=00:30:00
#PBS -l nodes=1:ppn=1
#PBS -A yeo-group
#PBS -q home

# Go to the directory from which the script was called
cd $PBS_O_WORKDIR
bedtools intersect exons.bed placental_conserved_elements.bed
```

The output is:
```
job ID: 3610818
```

### Array job example

If you have a bunch of independent jobs you want to run, then you can submit
them with one command using `array=True`. Here's an example of calculating average conservation of both constitutive and alternative exons.

```
import os
import glob

import qtools

folder = '/projects/ps-yeolab/obotvinnik/singlecell_pnms'

alt_exons_bedfile = '{}/exon2.bed'.format(folder)
constitutive_bedfile = '{}/constitutive_exons.bed'.format(folder)

bedfiles = alt_exons_bedfile, constitutive_bedfile

commands = []

bw = '/projects/ps-yeolab/genomes/hg19/hg19_phastcons_placental_mammal.bw'

for bedfile in bedfiles:
    basename = os.path.basename(bedfile)

    prefix = basename.split('.bed')[0]

    prefix += '_phastcons_placental_mammal'
    bedout = '{}/{}'.format(folder, prefix + '.bed')
    outtab = '{}/{}'.format(folder, prefix + '.txt')
    command = 'bigWigAverageOverBed {} {} {} -bedOut={}'.format(bw, bedfile, outtab, bedout)
    print command
    commands.append(command)

jobname = 'exonbody_conservation'
qtools.Submitter(commands, jobname, array=True, walltime='2:00:00')
```

Output:
```
running 2 tasks as an array-job.
job ID: 3614584
```

This creates the file `exonbody_conservation.sh` which looks like this:

```
#!/bin/bash
#PBS -N exonbody_conservation
#PBS -o /projects/ps-yeolab/obotvinnik/singlecell_pnms/exonbody_conservation.out
#PBS -e /projects/ps-yeolab/obotvinnik/singlecell_pnms/exonbody_conservation.err
#PBS -V
#PBS -l walltime=2:00:00
#PBS -l nodes=1:ppn=1
#PBS -A yeo-group
#PBS -q home
#PBS -t 1-2

# Go to the directory from which the script was called
cd $PBS_O_WORKDIR
cmd[1]="bigWigAverageOverBed /projects/ps-yeolab/genomes/hg19/hg19_phastcons_placental_mammal.bw /projects/ps-yeolab/obotvinnik/singlecell_pnms/exon2.bed /projects/ps-yeolab/obotvinnik/singlecell_pnms/exon2_phastcons_placental_mammal.txt -bedOut=/projects/ps-yeolab/obotvinnik/singlecell_pnms/exon2_phastcons_placental_mammal.bed"
cmd[2]="bigWigAverageOverBed /projects/ps-yeolab/genomes/hg19/hg19_phastcons_placental_mammal.bw /projects/ps-yeolab/obotvinnik/singlecell_pnms/constitutive_exons.bed /projects/ps-yeolab/obotvinnik/singlecell_pnms/constitutive_exons_phastcons_placental_mammal.txt -bedOut=/projects/ps-yeolab/obotvinnik/singlecell_pnms/constitutive_exons_phastcons_placental_mammal.bed"
eval ${cmd[$PBS_ARRAYID]}
```

### Direct `stdout`/`stderr` to a specific location, and specify queue or number of processors

If you want your `sh`/`stdout`/`stderr` to be sent to a specific location, instead
of to the folder you're currently in by default, then specify them with `sh`,
`out`, and `err`. You can also specify the queue (`home-yeo` vs `home-scrm`) with `queue="home-scrm"`. The default is `home-yeo`.

```
import qtools

jobname = 'run_outrigger_py'
sh = jobname + '.sh'
out = sh + '.out'
err = sh + '.err'

command = 'python /projects/ps-yeolab/obotvinnik/singlecell_pnms/outrigger/outrigger.py'

n_processors = 16
sub = qtools.Submitter([command], 'run_outrigger_py', queue='home-yeo',
                out=out, err=err, sh=sh, walltime='100:00:00', nodes=1,
                ppn=n_processors)
```

Output:
```
job ID: 3884631
```
