# NVCIM

## Set Up Environments

#### For Linux or WSL
1. Set up environment variable.

```shell
export NVCIM_HOME=/root/directory/of/this/project
```

2. Run the following command to install required packages.

```makefile
make requires
```

3. Run the following command to install python module `maptools`.

```makefile
make maptools
```

#### For Powershell

1. Set up environment variable.

Open Powershell profile file.

```powershell
code $PROFILE
```

Add a new line to the profile file.

```powershell
$Env:NVCIM_HOME = 'c:/root/directory/of/this/project'
```

2. Run the following command to install required pip packages.

```
pip install -U -r requirements.txt
```

Then, install `graphviz` on the client side.

3. Run the following command to install python module `maptools`.

```powershell
python setup.py install
```