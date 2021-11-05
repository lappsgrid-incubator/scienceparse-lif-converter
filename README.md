# scienceparse-lif-converter

Code to convert the output of [Science Parse](https://github.com/allenai/science-parse) into LIF, either on the command line or with a RESTful service. The conversion code is in `converter.py`, which uses the LIF library in `lif.py`. The other scripts wrap that code to run the converter in some way.

This requires installation of JSON Schema validation and Flask:

```bash
$ pip install jsonschema
$ pip install flask
```

Flask does not need to be installed if you only run the script from the command line.

**Command line usage**:

```bash
$ python3 run.py data/input.json out.lif
```

This takes the example ScienceParse file in the `data` directory and returns a LIF file. There are variations on this to work with standard input and standard output, see `run.py` for details. With `test.py` you can run the converter on a directory, see the module documentation string for details.

**Running a RESTful server**:

Start the server:

```bash
$ python3 app.py
```

This gives access to two URLs:

```bash
$ curl 127.0.0.1:5000
$ curl -X POST -d@data/input.json 127.0.0.1:5000/parse
```
The first returns some metadata and the second a LIF string created from the input file.

