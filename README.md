### VScode setup 

To setup VScode on Katana compute nodes, we need to set a few things up first. 

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

You will need to add a separate 

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






##### Miniconda3 installation 

Sometimes `venv` environments do not automatically show up in VScode's kernel list.  For this reason, I will demonstrate with `conda` environments. 

[Download](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) the installer 




> NOTE: to use the Grace Hopper (GH200) node, you will need to install the `aarch64` version of conda [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh)



Confirm GPU status 

`watch nvidia-smi` 


```python
# Confirm that we can access GPUs
torch.cuda.get_device_name(torch.cuda.current_device())
# 
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



