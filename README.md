# scienceparse-lif-converter

Code to convert the output of [Science Parse](https://github.com/allenai/science-parse) into LIF, either on the command line or with a RESTful service. The conversion code is in `converter.py`, which uses the LIF library in `lif.py`. The other scripts wrap that code to run the converter in some way.

**Command line usage**:

```bash
$ python3 run.py input/input.json out.lif
```

This takes the example ScienceParse file in the `input` directory and cretaes a LIF file. There are variations on this to work with standard input and standard output, see `run.py` for details. With `test.py` you can run the converter on a directory, see the documentation string for details.

**Running a RESTfule server**:

This requires Flask to be installed:

```bash
$ pip install flask
```

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

