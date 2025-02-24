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
ln -s
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



