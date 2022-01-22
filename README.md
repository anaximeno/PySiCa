## Python Simple Calculator - PySiCa

<img width=600 height=400 src="images/pysica_black.png">


This is a basic idea of a calculator made in python, it could be the backend of a real calculator software.

### About

I firstly made this program as an exercise when studying in the [CS50](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) and since then I made a lot of changes.
The most recent update I have made is the use of a "Pushdown Automata" to recognize which "sentences" (the user input) should be "accepted" and which should be "rejected" before parsing it to an expression. The Automata used is still on development, so, it could break on some expressions e.g. '**()9 - +**'.

### Requirements
It requires only one external python package named termcolor, it could be installed using:

```bash
pip install termcolor
```

### Test / Use it
To test is, just run the following command on the root directory of the program:
```bash
python3 pysica.py
```

<!--TODO: add usage, and how it works-->