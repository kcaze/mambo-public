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

## Writing the Python backend solver
To modify the actual solver logic, look in `claspy/solvers/variety/<puzzle>.py`. Each solver derives from the `Base` class in `_base_.py` which has various functions to help with decoding the input from pzpr which comes in the form of a pzpr URL. The two functions that need to be overridden are `_solve()` and `decode()`. The point of `decode()` is to populate `self.board` which contains all the actual input numbers, symbols, etc. and then `_solve()` writes the actual claspy constraints. See `sudoku.py` for a fairly minimal example.

All the actual logic is written in terms of claspy constraints so make sure to read the [claspy README](https://github.com/danyq/claspy). In addition, a `utils.py` file is provided. The main thing of interest there is `require_single_closed_loop_v2()` which takes in two arguments `h` for the horizontal loop segments and `v` for the vertical loop segments and adds constraints to make sure they form a single non self-intersecting loop.

The actual solution object returned will be converted to JSON before being sent back to the pzpr frontend.

## Writing the pzpr frontend
To modify the frontend to handle displaying solutions and allowing any additional input options, look in `pzprjs/src/variety/<puzzle>.py`. The `Solver` field needs to be a Javascript object with a `displayAnswer` function that takes the solution object and uses it to update the board state with the answer.

If you need to update the graphical output, look in the `Graphic` field's `paint` function. You can call `this.vinc()` to create a new layer. It takes three arguments: a layer id, a rendering option (`auto` or `crispEdges`), and a boolean variable called `freeze` (functionality unknown?). The function returns a context object used for drawing and you can see the [candle](https://github.com/sabo2/candle) library for the documentation and source code.

If you need additional input types for your board or cells, look in either the `Board` or `Cell` field. Of note is the ability to add borders to `Board` by setting `hasborder: 1,`.

You can also edit the field `mouseinput_auto` in `MouseEvent` to allow for the inputs of numbers, borders, etc.
