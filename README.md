# Mambo

This uses pzprjs/pzprv3 as the frontend UI and claspy as the constraint solving library.

## Installation
Make sure you have `grunt` installed with `sudo npm install -g grunt`.

Next, in the `pzprjs` directory run `npm install && grunt dev` and then in the `pzprv3` directory run `npm install && grunt dev`.

Next, install `clasp`. On Ubuntu/Debian this can be done with `sudo apt-get install clasp`.

Next, run `pip3 install bottle` in the root directory.

Finally, run `python3 mambo.py` in the root directory and you should be able to navigate to http://localhost:8080 and see the list of puzzle types with solvers.

## Development
Run `grunt watch` in both the `pzprjs` and `pzprv3` directories to setup a watcher that automatically builds whenever you change any of the files in those subdirectories.

## Creating new solvers
Run `scripts/create_new_puzzle` and follow the script's instructions to set up a new solver. You can select an existing solver as a template.

After running this script, there are two files that you will want to edit. The Python solver file lives in `claspy/solvers/variety/<puzzle>.py` and the Javascript pzpr file lives in `pzprjs/src/variety/<puzzle>.js`.
