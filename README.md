# CISC/CMPE 204 Modelling Project: Colour Cubes!!

## Summary

Solving the popular kid's toy that asks you to place coloured cubes in a number of slots so that now side has the same colours.

![cubes](https://i.etsystatic.com/11805630/r/il/50962c/1951375864/il_794xN.1951375864_gxzs.jpg)

## To run things

### Building

```bash
docker build -t cisc204 .
```

### Running

```bash
docker run -it -v $(pwd):/PROJECT cisc204
```

## Structure

### General or provided

* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
  * **IMPORTANT**: You can find the final report in the `documents/final/` folder.



### Custom code

* `run.py`: This is where the whole model is being built and solved
* `viz.py`: Used to visualize solutions for this particular project
* `diceconfigs.py`: The configurations of the actual dice.
