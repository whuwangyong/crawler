This script is used crawl infomation from iffershow.com, and write data into MYSQL database at thesame time.
There is another way to save data: generate sql statement and save them in insert.sql, and then import them into MYSQL with source command.
If you don't want to use database, just delete the related code.


(1) infomation comes from: http://www.ioffershow.com:8000/

(2) install python setup tools and pip:
wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
python setup.py build
sudo python setup.py install
sudo apt-get install python-pip

(3) install beautifulsoup:
first, uncompress the .tar.gz file;
then,
python setup.py build
sudo python setup.py install

(4) install pymysql(https://github.com/PyMySQL/PyMySQL)
sudo pip install pymysql
or
sudo pip3 install pymysql

(5)RUNNING
python3 getoffershow.py

