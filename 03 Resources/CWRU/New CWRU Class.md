# Creating A New Class

1. Create a virtual environment:
```shell
$ uv venv
```
2. Install spartan:
	```shell
$ (cd spartan; uv init --bare)
	```
3. Install requirements:
	```shell
$ uv pip install -r ../spartan/requirements.txt
	```
4. Copy `nbgrader_conf.py` from another project
