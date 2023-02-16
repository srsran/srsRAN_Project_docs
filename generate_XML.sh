# Script to clone srsGNB and generate most up-to-date version of Doxygen XML files

# Clone srsGNB (private) from GitLab
git clone git@gitlab.com:softwareradiosystems/srsgnb.git srsgnb

# Create folder for doxygen files
mkdir -p docs/source/.doxygen/xml

# Build Doxygen XML files from srsGNB (no need to build srsGNB application)
cd srsgnb 
mkdir build
cd build
cmake ../
cd docs
make doxygen

# Copy to relevant location in Docs source folder
mv xml/* ../../../docs/source/.doxygen/xml