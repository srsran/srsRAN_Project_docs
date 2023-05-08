# srsRAN Project Docs
The srsRAN Project documentation.

# Local Installation 

The docs require multiple sphinx extensions.

On Ubuntu, they can be installed with:
```
sudo apt install python3-pip python3-sphinx
pip install -r requirements.txt
```

Once all dependencies are installed, you can download and build the docs with the following commands: 

```
git clone https://github.com/srsran/srsran_project_docs.git
cd srsran_project_docs/docs
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
pip3 install -r requirements.txt
```

To build the docs first run from /docs/source
```
sphinx-build -b html . .build
```

Then run the following command from the docs main folder
```
sphinx-autobuild docs/source/ docs/source/.build/html
```
This will start a server at http://127.0.0.1:8000 which can be viewed in your browser, any changes to the docs will be shown here once saved. 
