# Python

## Environment

### Creation

```
conda activate base
mamba env create --file=environment.yml
```

### Activate

```
conda activate special-garbanzo
```

### Update

```
conda activate base
mamba env update --file=environment.yml
conda activate special-garbanzo
```

### Deactivate

```
conda deactivate
```

### Delete

```
conda deactivate
conda remove --yes --name=special-garbanzo --all
```
