# CISC/CMPE 204 Modelling Project: Colour Cubes!!

## Summary

Coming soon...

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

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

### Custom code

* `run.py`: This is where the whole model is being built and solved
* `viz.py`: Used to visualize solutions for this particular project
