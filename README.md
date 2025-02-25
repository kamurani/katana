## Using VScode Jupyter notebooks on Katana compute nodes

##### Preamble 
Running interactive Jupyter notebooks is an increasingly popular way to develop and test software, particularly when working with ML/AI where iterative and quick development is key to testing and refining models, validating training loops, and sanity-checking batching processes for large-scale training. 

In particular, IDE support for Jupyter notebooks such as with VScode is a great way to ease the burden of interacting with notebooks, as they provide features such as: 

* lower latency than browser-based Juyter notebook interfaces
* linting of imported libraries
* GUI-based version control
* debugging
* management of environments (e.g. conda or python `venv` virtual environments)
* marketplace for 3rd party extensions
* AI-assisted code completion
* customisable preferences e.g. syntax highlighting
* remote access management e.g. SSH 

However, some considerations have to be made when trying to integrate VScode with a HPC cluster environment such as Katana, due to the necessary tradeoffs between distributed computing resources necessary for scalability. This tutorial will show you one way of accessing Katana's HPC resources, all from within a single VScode instance - no port forwarding required.

### VScode setup 

To use VScode on Katana compute nodes, we need to set a few things up first. 

##### Submit a job 

In this demonstration, we will use an interactive session and request 1 GPU. 

Our batch file looks something like this: 

`interactive_gpu.pbs` 

```bash
#! /usr/bin/env bash

#PBS -I 
#PBS -l select=1:ncpus=6:ngpus=1:mem=46gb
#PBS -l walltime=4:00:00
#PBS -M YOUR_EMAIL_ADDRESS
#PBS -m ae
#PBS -j oe
```
Submit using 
`qsub /path/to/interactive_gpu.pbs` 

You should then see something like 

```
qsub: waiting for job <JOB_NUMBER>.kman.restech.unsw.edu.au to start
qsub: job <JOB_NUMBER>.kman.restech.unsw.edu.au ready
```
We can confirm that we have GPU access by typing `nvidia-smi`. 

You will need to figure out the `hostname` of the compute node you are currently on for this job. This can be easily obtained by typing

`$ hostname`

In our case, we see `k099`. 

##### SSH

You will need to add a separate `HostName` to your `.ssh` config file for each compute node on katana that you wish to have access to using a single SSH connection from VScode.

Add the following to your `~/.ssh/config` file: 

```
Host katana
  Hostname katana.restech.unsw.edu.au
  User YOUR_USERNAME
```
This should allow you to use a convenient alias to `ssh` into a login node.  

> NOTE: you should already have passwordless access to Katana, if not use `ssh-copy-id user@host`.  If you don't already have a key, use `ssh-keygen`. 


The following one-liner uses the katana login node as a "jump host" from which to login to the specific machine in which the job is running (in this case, k099). 

`ssh -J katana k099`



You can run `nvidia-smi` again to confirm that this is the same node that we have access to with our shell instance given to us when we submitted with `qsub`. 

> NOTE: if using a non-UNSW computer, this may use your local machine's username by default when trying to get into `k099`.  Try `ssh -J katana YOUR_ZID@k099` instead.

Exit and return to your local machine.

> NOTE: when exiting an ssh connection using a jump host, you will exit both levels at the same time, thus typing `hostname` immediately after this should show your local machine's name (not `katana1` or similar). 

We can achieve this command more simply by creating another alias, under a new `HostName` in our config file.  


Your `config` file should look something like this afterward: 

```ssh

# login node on katana.  We will use this as a "jump" host
Host katana
  Hostname katana.restech.unsw.edu.au
  User YOUR_USERNAME

Host k099
  HostName k099
  ProxyJump katana

# Send keepalive packets to prevent SSH disconnecting...
Host *
  ServerAliveInterval 60
```

We can now simply type `ssh k099` to gain access to the compute node. 
> NOTE: this will only work if you have submitted (and are currently running) a job via `qsub` that is on the node specified; in our case k099.  Otherwise, your ssh session will immediately exit. 

As mentioned before, typing `ssh k099` may use your local machine's username for the 2nd (from the katana login node --> the compute node).  If your username on your local machine happens to be the same as your username on katana (such as your zID), then this won't matter.  But to be safe, you can simply define your katana-specific username explicitly:

```ssh
Host k099
  HostName k099
  User YOUR_KATANA_USERNAME
  ProxyJump katana

```




##### Miniconda3 installation 

Sometimes `venv` environments do not automatically show up in VScode's kernel list.  For this reason, I will demonstrate with `conda` environments. 

1. [Download](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) the installer
1. TODO: install instructions

It may be helpful to move your `miniconda3` from your home directory to `$SCRATCH`, although this may result in slower environment solving.  This is because Katana unfortunately only gives users a 15GB quota on their home directory, which can fill up quickly (especially if you use multiple python versions or environments across a handful of projects). 


> NOTE: to use the Grace Hopper (GH200) node, you will need to install the `aarch64` version of conda [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh)



Confirm GPU status 

`watch nvidia-smi` 

##### Connect with VScode

Click on the SSH button in the bottom left corner of a VScode window.  You should see the alias created earlier when prompted to connect to a host. We can then select a folder on the host filesystem to open, and a terminal instance should start.  Confirm by typing `hostname` that we are on the desired compute node (not the login node). You might be prompted to install any software that you don't already have on the remote system in order for the VScode remote connection to work. 

Open a jupyter notebook (`.ipynb` file) and in the top right corner, you should be able to select a python kernel.  VScode will automatically search for python interpreters, such as in your `~/miniconda3/envs/` (or similar) directory. 

> NOTE: you may have to manually install the Jupyter extension in the Extensions tab on VScode.


To test out our notebook, let's try and use the GPU we now have access to. 

```zsh
conda create -n torch-nb

# use --prefix alternatively?
# then add symlink to /envs/ ?

conda activate torch-nb
conda install jupyter 
```

Next, install PyTorch using conda or pip using instructions [here](https://pytorch.org/get-started/locally/) 

Make sure that torch is compiled with CUDA enabled.  To confirm, we can type 
`python -c "import torch; print(torch.version.cuda)"`

To confirm that we are using python from within our newly created environment: `which -a python` 

Now, load this conda environment by selecting it within the VScode notebook interface. 

> NOTE: if a python environment doesn't show up under the kernel list, try Cmd+Shift+P and select `Developer: Reload Window` to cause VScode to scan through valid python interpreters again. 



```python
# Confirm that we can access GPUs
>>> torch.cuda.get_device_name(torch.cuda.current_device())
'NVIDIA H200'
```

# Other stuff
# katana
Useful stuff for using UNSW katana


#### Links 

```zsh
ln -s /srv/scratch/sbf/cam sbf
```

#### Free up space 


```zsh
mv .apptainer $SCRATCH
ln -s $SCRATCH/.apptainer .apptainer
ll .apptainer

mv ~/miniconda3 $SCRATCH
ln -s $SCRATCH/miniconda3 ~/miniconda3
ncdu ~
```
### Reproducibility 


#### Setup

All things I have modified on the system to make Katana usable.


#### ZSH 

Install `oh-my-zsh` 

`.bashrc`:
```bash
# ADDED BY CAM ###
if [[ $- =~ i && $SHLVL == 1 ]]; then
  exec zsh
fi
```

#### Debugging apptainer; show when `~/.bashrc` is sourced

```bash
# For debug 
if [ -t 1 ]; then
        # stdout is a TTY...
        echo "$USER SHELL PROFILE SOURCED."
fi
```


For using VScode notebooks with interactive GPU: 


#### Conda 

##### install miniconda 


move miniconda to `$SCRATCH` and add symlink to home (to prevent disk quota issues)  


Alternatively:

- keep `miniconda3/lib` to home (most commonly accessed directory) and everything else keep as symlink






Local machine `~/.ssh/config`:



