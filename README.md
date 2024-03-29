# baseball-hackday

## Setting up a development environment

### Using a virtual environment

Because the web server relies on many third party packages, using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) can help ensure that compatible versions of those packages are installed and do not conflict with other versions of packages that may be installed on the same machine. This is not required, but may help avoid bugs caused by a tangled dependecy tree.

A virtual environment (venv) can be created with the command `python3 -m venv venv`. This creates a directory called `venv` (which is in `.gitignore`). Before it can be used, the virtual environment must be activated using the following command:

Windows

```
venv\Scripts\activate.bat
```

Mac/Unix

```
. venv/bin/activate
```

Once activated, the environment can be deactivated with the shell command `deactivate`.

#### Installing new packages

After the virtual environment has been setup `pip install` will install packages in the virtual environment. A list of package dependencies is kept in `requirements.txt` (checked into git). After installing a new package, update `requirements.txt` by running the script `bin/freeze.sh`.

If you're setting up the repository for the first time, install the packages listed in `requirements.txt` by running the script `bin/install.sh`.

## Rendering the visualization

The model is exposed through a simple webpage that allows the input of parameters to generate a heatmap. This webpage is served from a server implemented using the [Flask framework for Python](https://flask.palletsprojects.com/en/1.1.x/). To start the server, run `python app.py` and navigate to http://localhost:5000 to view the webpage.

## Deployment

The app can be deployed to Azure using VS Code's Azure Extension as documented [here](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli#3---deploy-your-application-code-to-azure).

The script `bin/deploy.sh` can also be used to deploy the app manually. To use the script, first you must [install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
