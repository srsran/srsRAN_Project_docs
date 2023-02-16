# srsGNB_docs
Documentation relating to srsGNB.

# Local Installation 

The docs require following Sphinx extensions:
- sphinxcontrib-seqdiag
- sphinxcontrib-blockdiag

On Ubuntu, they can be installed with:
```
sudo apt install python-pip
pip install -r requirements.txt
```

Once dependencies are installed,

```
git clone https://github.com/srsRAN/srsGNB_docs.git
cd srsGNB_docs/srsgnb_docs
make html
```

Then load the compiled doc in your browser
```
firefox build/html/index.html
google-chrome build/html/index.html
```

To enable live build previews when editing documentation install the following extension: 
- sphinx-autobuild 

This can be installed from the requirements file. 
```
pip install -r requirements.txt
```

To build the docs first run from /srsgnb_docs/source
```
sphinx-build -b html . _build
```

Then run the following command from the docs main folder
```
sphinx-autobuild srsgnb_docs/source/ srsgnb_docs/source/_build/html
```
This will start a server at http://127.0.0.1:8000 which can be viewed in your browser, any changes to the docs will be shown here once saved. 