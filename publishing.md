# publishing

## tl;dr
bump to beta, tag to release a beta, test in windows, remove beta, merge pull, tag final

## how to
1. bump versions by modifying the following files (templates at the end):

    fireanalyticstoolbox/metadata.txt
        - includes changelog
        - don't change version is changed in the release action
    fireanalyticstoolbox/dependencies_handler.txt
        - make sure it matches the version of fire2a-lib https://pypi.org/project/fire2a-lib/
    qgis-plugin-server/plugins.xml
        - do only on final release to all users
        - make sure the release is not draft

    vim fireanalyticstoolbox/metadata.txt fireanalyticstoolbox/dependencies_handler.txt qgis-plugin-server/plugins.xml
    :bufdo % s/0.7.0/0.8.0/gc
    :bufdo % s/0.3.10/0.3.11/gc

2. tag

    git tag -n2 | tail # show last tags
    git tag -a v0.9.0-beta -m "spanish + C2FWv0.4.1"  && git push origin v0.9.0-beta
    git tag --delete v0.9.0-beta && git push --delete origin v0.9.0-beta

## templates

metadata.txt

    changelog
        v0.8.0: 

	SAVE BEFORE INSTALL/UPDATE: A dialog asking permission to (pip) install python dependencies (fire2a-lib==0.3.10) will appear

dependencies_handler.txt

	plugin_dependencies = fire2a-lib==0.3.10
    enabled = True

plugins.xml

	<pyqgis_plugin name="Fire Analytics Processing-Toolbox" version="0.8.0" plugin_id="1029384756">

			SAVE BEFORE INSTALL/UPDATE: A dialog asking permission to (pip) install python dependencies (fire2a-lib==0.3.10) will appear]]></about>

		<version>0.8.0</version>

		<update_date>2024-07-03T06:06:06.066666+06:00</update_date>

		<download_url>https://github.com/fire2a/fire-analytics-qgis-processing-toolbox-plugin/releases/download/v0.8.0/fireanalyticstoolbox_v0.8.0.zip</download_url>
