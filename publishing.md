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
    :bufdo % s/1.0.0/1.0.1/gc
    :bufdo % s/0.3.11/0.3.12/gc

2. tag

    # show last tags
    git for-each-ref --sort=creatordate --format='%(refname:short) %(creatordate)' refs/tags | tail | column -t
    # create
    git tag -a v1.0.1 -m "upstream fixes to Cell2FireW v1.0.1: neighbour angle and fire2a-lib v0.3.12: deprecation fix"  && git push origin v1.0.1
    # delete if needed
    git tag --delete v1.0.1 && git push --delete origin v1.0.1

## templates

metadata.txt

    changelog
        v1.0.1: upstream fixes to Cell2FireW v1.0.1: neighbour angle and fire2a-lib v0.3.12: deprecation fix

	SAVE BEFORE INSTALL/UPDATE: A dialog asking permission to (pip) install python dependencies (fire2a-lib==0.3.12) will appear

dependencies_handler.txt

    plugin_dependencies = fire2a-lib==0.3.12
    enabled = True

plugins.xml
	<pyqgis_plugin name="Fire Analytics Processing-Toolbox" version="1.0.1" plugin_id="1029384756">

			SAVE BEFORE INSTALL/UPDATE: A dialog asking permission to (pip) install python dependencies (fire2a-lib==0.3.12) will appear]]></about>

		<version>1.0.1</version>

		<update_date>2025-12-03T22:45:00.000000-03:00</update_date>

		<download_url>https://github.com/fire2a/fire-analytics-qgis-processing-toolbox-plugin/releases/download/v1.0.1/fireanalyticstoolbox_v1.0.1.zip</download_url>
