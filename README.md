# FireAnalyticsToolbox 

This repo sources Fire2a(.com research group)'s QGIS-Processing-Toolbox plugin: _"FireAnalyticsToolbox"_

User tutorials are at [fire2a/docs](https://fire2a.github.io/docs/)

## Quickstart

### Install
[comprehensive tutorial here](https://fire2a.github.io/docs/docs/qgis/README.html#installation)  
1. Install QGIS
1. Install the custom repo source
1. Install python requirements
1. Install "Fire Analytics Toolbox" plugin  


### Usage options
1. As a window dialog on the [processing toolbox](https://docs.qgis.org/latest/en/docs/user_manual/processing/toolbox.html) interface  
1. As a [model (designer graphic interface)](https://docs.qgis.org/latest/en/docs/user_manual/processing/modeler.html) component  
1. Via [command line interface](https://docs.qgis.org/latest/en/docs/user_manual/processing/standalone) using `$ qgis_process`  
1. Python script, either:  
 - on [QGIS Python console](https://docs.qgis.org/latest/en/docs/user_manual/plugins/python_console.html)  
 - or as a [standalone](https://raw.githubusercontent.com/fdobad/fire-analytics-qgis-processing-toolbox-plugin/main/script_samples/standalone.py) script  

### Development
Fork, clone, symlink `fireanalyticstoolbox` into your qgis-plugins directory, pull requests welcome!  
Also checkout our [algorithms library](https://fire2a.github.io/docs/docs/fire2a-lib.html)

## Structure
- Plugin files at `fireanalyticstoolbox` directory  
  - includes python requirements.txt  
- `script_samples` contains standalone and qgis-console python scripts  
- `pyproject.toml` defines black coding style  
-  requirements.dev.txt lists dev tools  

## Code of Conduct

Everyone interacting in the project's codebases, issue trackers, etc. is expected to follow the [PSF Code of Conduct](https://www.python.org/psf/conduct/).
