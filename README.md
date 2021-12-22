# Mambo

This uses pzprjs/pzprv3 as the frontend UI and claspy as the constraint solving library.

## Installation
First run `npm install && grunt dev` in `pzprjs` and then `npm install && grunt dev` in pzprv3.

Next, install `clasp`. On Ubuntu/Debian this can be done with `sudo apt-get install clasp`.

Next, run `pip3 install bottle` in the root directory.

Finally, run `python3 mambo.py` in the root directory and you should be able to navigate to http://localhost:8080 and see the list of puzzle types with solvers.

## Development
Run `grunt watch` in both the `pzprjs` and `pzprv3` directories to setup a watcher that automatically builds whenever you change any of the files in those subdirectories.
