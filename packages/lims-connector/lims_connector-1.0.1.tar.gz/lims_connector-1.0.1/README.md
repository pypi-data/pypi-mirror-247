# lims_connector
lims_connector is a Python package designed to connect with the CMH (Children's Mercy Hospital) Laboratory Information Management System (LIMS).

## Build and Installation
1. Install the dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the package using the following commands:
 - Install the wheel and twine package by running the following command:
   ```bash
   pip install wheel
   pip install twine
   ```
 - Build the package by executing the setup.py script using the sdist and bdist_wheel commands. Run the following command:
   ```bash
   python setup.py sdist bdist_wheel
   ```
 - Finally, upload the built package to PyPi using twine. Run the following command:
   ```bash
   twine upload dist/*  
   ```

3. Install the Python package using the following commands: <br>
 - Run the following command to install cmh-lims-orm from the local file:
   ```bash
   pip install dist/lims_connector-<version>-py3-none-any.whl
   ```
    Replace <version> with the desired version number. For example:
   ```bash
   pip install dist/lims_connector-1.0.1-py3-none-any.whl
   ```

 - Run the following command to install cmh-lims-orm from PyPi:
   ```bash
   pip install cmh-lims-orm==<version> 
   ```
   Replace <version> with the desired version number. For example:
   ```bash
   pip install cmh-lims-orm==1.0.1
   ```

# Usage:

1. import the `cmhlims` package
   ```bash
   import lims_connector
   ```

2. Set the configuration file by calling the set_config function from the setConfig module:
   ```bash 
   from lims_connector.setConfig import set_config
   set_config('database.yml', "production")
   ```
   Replace 'database.yml' with the path to your configuration file.
   Specify the desired environment (e.g., "production").

3. Connect to the LIMS by calling the connect_to_lims function from the connectToLIMS module:
   ```bash 
   from lims_connector.connectToLIMS import connect_to_lims
   connect_to_lims()
   ```   


Ensure that you have the necessary permissions and valid credentials to access the CMH LIMS.

Note: Prior to running the package, make sure to install it by executing pip install lims_connector.
      The current working directory should also include the file "combined.pem." 
