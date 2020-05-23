# Pandas as a Pipeline or P.a.a.P

This is an attempt to write pandas code in OO style. I have been fascinated with Dataclasses in python for a while now and decided to make full use of it within this project. 

###### Warning: This code is not meant to be run! The data used to build these pipeline cannot be publicly posted.

I am making this repository public to showcase the style of writing pandas as a pipeline, hopefully someone makes good use of this. 

The idea is simple, use inheritance to make the code D.R.Y, and alongside, utilize the functionality provided by dataclasses. 

I'll still add the instructions to run it! 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

###### This example assumes you have a data directory, which is structured as follows:
```
data
 |
 |- structured
    |
    |- type_a
        |- ALL_TYPE_A_FILES.xlsx
    |
    |- type_b
        |- ALL_TYPE_B_FILES.xls
 |- unstructured
    |
    |- pdf_files
        |- ALL_PDF_FILES.pdf
    |
    |- txt
        |- ALL_TXT_FILES.txt
    |
    |- word_docs 
        |- ALL_WORD_FILES.doc
 |
 |- parsed
    |
    |- type_a
        - Output directory for type_a
    |
    |- type_b
        - Output directory for type_b
    |
    |- txt
        - Output directory for txt
    |
    |- word_docs
        - Output directory for word documents
```

### Installing

As usual, installing python dependencies with pipenv

```bash
asdf local python 3.7.5
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools pipenv
pipenv install
```

Running it:

```
cd ~/paap/
python parser {type_a, type_b, type_c, type_d, unstructured}  --file-path data/structured/{input_dir} --output-path data/parsed/{output_dir} --file-type {json, xls, xlsx, txt, docx}
```



## Contributing

All suggestions are welcome, use a PR! As the sole maintainer of this tiny project, I'll see what I can review and approve!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for detailsContributing