# cmhlims_orm
cmhlims_orm is a Python package designed to interact with the CMH (Children's Mercy Hospital) Laboratory Information Management System (LIMS). It provides functionalities to connect to the LIMS, retrieve analysis data, fetch analysis files, and retrieve sample names.

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
   pip install dist/cmh_lims_orm-<version>-py3-none-any.whl
   ```
    Replace <version> with the desired version number. For example:
   ```bash
   pip install dist/cmh_lims_orm-1.0.17-py3-none-any.whl
   ```

 - Run the following command to install cmh-lims-orm from PyPi:
   ```bash
   pip install cmh-lims-orm==<version> 
   ```
   Replace <version> with the desired version number. For example:
   ```bash
   pip install cmh-lims-orm==1.0.17
   ```

# Usage:

1. import the `cmhlims` package
   ```bash
   import cmhlims
   ```

2. Set the configuration file by calling the set_config function from the setConfig module:
   ```bash 
   from cmhlims.setConfig import set_config
   set_config('database.yml', "production")
   ```
   Replace 'database.yml' with the path to your configuration file.
   Specify the desired environment (e.g., "production").

3. Connect to the LIMS by calling the connect_to_lims function from the connectToLIMS module:
   ```bash 
   from cmhlims.connectToLIMS import connect_to_lims
   connect_to_lims()
   ```   
4. Retrieve analysis data by calling the get_analyses function from the getAnalysis module:
   ```bash
   from cmhlims.getAnalysis import get_analysis
   get_analysis(["cmh000514"], "GRCh38")
   ```   
   Pass a list of analysis IDs as the first argument (e.g., ["cmh000514"]).
   Pass a list of genome build versions as the second argument (e.g., ["GRCh38"]).

5. Fetch analysis files by calling the get_analysis_files function from the getAnalysisFiles module:
   ```bash
   from cmhlims.getAnalysisFiles import get_analysis_files
   get_analysis_files(["2287"])
   ```
   Pass a list of analysis file IDs as the argument (e.g., ["2287"]).

6. Retrieve sample names by calling the get_sample_names function from the getSampleNames module:
   ```bash
   from cmhlims.getSampleNames import get_sample_names
   get_sample_names()
   ```   

Ensure that you have the necessary permissions and valid credentials to access the CMH LIMS.

Note: Prior to running the package, make sure to install it by executing pip install cmhlims.
      The current working directory should also include the file "combined.pem." 
