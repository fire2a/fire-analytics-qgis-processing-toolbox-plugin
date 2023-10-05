# FireAnalyticsToolbox 

This repo sources Fire2a(.com research group)'s QGIS-Processing-Toolbox plugin: _"FireAnalyticsToolbox"_

User tutorials are at [fire2a/docs](https://fire2a.github.io/docs/)

## Quickstart
### Install
[comprehensive tutorial here](https://fire2a.github.io/docs/docs/qgis/README.html#installation)  
1. Install QGIS
1. Install the custom [plugin repo source](https://fire2a.github.io/fire-analytics-qgis-processing-toolbox-plugin/plugins.xml)
1. Install python [requirements](https://raw.githubusercontent.com/fdobad/fire-analytics-qgis-processing-toolbox-plugin/main/fireanalyticstoolbox/requirements.txt), [also](https://raw.githubusercontent.com/fire2a/fire2a-lib/main/requirements.txt)
1. Install "Fire Analytics Toolbox" plugin  

### Usage options
1. As a window dialog on the [processing toolbox](https://docs.qgis.org/latest/en/docs/user_manual/processing/toolbox.html) interface  
1. As a [model (designer graphic interface)](https://docs.qgis.org/latest/en/docs/user_manual/processing/modeler.html) component  
1. Via [command line interface](https://docs.qgis.org/latest/en/docs/user_manual/processing/standalone) using `$ qgis_process`  
1. Python script, either:  
 - on [QGIS Python console](https://docs.qgis.org/latest/en/docs/user_manual/plugins/python_console.html)  
 - or as a [standalone](https://raw.githubusercontent.com/fdobad/fire-analytics-qgis-processing-toolbox-plugin/main/script_samples/standalone.py) script  

### Development
- Check a release for directory structure
- [Fork], Clone
  - if simulating fires: submodule-add [C2F-W](https://www.github.com/fire2a/C2F-W/)
  - if firebreak placing get a MIP solver
- [branch]
- Symlink `fireanalyticstoolbox` into your qgis-plugins directory
- Install "Fire Analytics Toolbox" & "Plugin Reloader" in QGIS Plugin Manager
- Done! (Do a change, reload the plugin, test, ...)
- Pull requests welcome! ([coding style](https://github.com/fire2a/fire2a-lib/blob/main/coding_style.md))

Also checkout our [algorithms library](https://fire2a.github.io/docs/docs/fire2a-lib.html)

## Structure
- Plugin files at `fireanalyticstoolbox` directory  
  - includes python requirements.txt  
- `script_samples` contains standalone and qgis-console python scripts  
- `pyproject.toml` defines black coding style  
-  `requirements.dev.txt` lists dev tools  

## Code of Conduct
Everyone interacting in the project's codebases, issue trackers, etc. is expected to follow the [PSF Code of Conduct](https://www.python.org/psf/conduct/).
