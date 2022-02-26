conda create --prefix ./env python=3.7 -y
source activate ./env
pip install -r requirements.txt
conda env export > conda.yaml
# to run this shell script use command -> bash ini_setup.sh