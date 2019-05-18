# AI-Apache-Server-Intrusion-Detection-and-Avoidance

Decision tree based AI model that detects malicious actions on the network and adds them to a blacklist. This model utilizes the [classification and regression trees (CART)](https://en.wikipedia.org/wiki/Predictive_analytics#Classification_and_regression_trees_.28CART.29), utilizing the Gini Index as the measure of impurity. The model has an accuracy of 94.5%.

---

The program utilizes python3.6 to run the model. The python libraries needed are as follows:

- [Pandas](https://pandas.pydata.org/)
- [TensorFlow](https://www.tensorflow.org/install/pip)
- [numpy](https://www.numpy.org/)
- [Requests](https://pypi.org/project/requests/)

---

Also needed is an API-key for the [IPInfoDB](https://ipinfodb.com/) API. This can be obtained [here](https://ipinfodb.com/register).

---

## Installation Instructions

1. Clone or download this repo to a folder on the machine of your web server.

2. Copy the `ip-blacklist.conf` file to the configuration directory of your server:
   For Apache2 web servers: `/etc/apache2/`
   For HTTPD web servers: `/etc/httpd/`

3. Include the `ip-blacklist.conf` file in the main `.conf` file, whose location is specified in step 2.
   Apache2 conf: `apache2.conf`
   HTTPD conf: `httpd.conf`

4. Enable the combined log format for access logs located within the main `.conf` file in your system. More detailed instructions can be found [here](https://httpd.apache.org/docs/2.4/logs.html) on how to enable this log format.

5. Edit the `main.py` file (located in the folder of the cloned repo) and include the path of the following files your your system:
   ⋅⋅* Access Log File: e.g. `accessLogPath = '/var/log/apache2/access_log'`
   ⋅⋅* CSV file for the blacklist (Entire working directory of the `/files/iplist.csv` file) : e.g. `ipBlackListCsv = "/your_directory/files/iplist.csv"`
   ⋅⋅* Key for the IPInfoDB API. e.g. `ipDBkey = "1234567891011121314151617181920"`
   ⋅⋅* Location of the `ip-blacklist.conf` file placed in step 2. e.g. `ipBlackListConf = "/etc/apache2/ip-blacklist.conf"`

6. Edit the `script1.sh` file in the cloned repo and replace the `python3.6 main.py` command to include the entire location path for the `main.py` file. For example the new line will be `python3.6 /your_directory/main.py`.
   Also edit the `: > ACCESSLOGPATH` line to include the path for the access log of your system. For example the command would be ': > /var/log/httpd/access_log'.
   The last line `service httpd restart` is set up for httpd server by default. If you use an apache server, replace this line with the restart command for the apache server.

7. The initial set up is now complete. You can schedule the running of the `script1.sh` file through the use of the cron scheduler. To learn more about the cron scheduler click [here](https://en.wikipedia.org/wiki/Cron).
