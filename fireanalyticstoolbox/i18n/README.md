# QGIS QT Translation 

0. tools

    pylupdate5 : busca tr('strings') en el código fuente y genera un archivo .ts
    lrelease : convierte el archivo .ts en un archivo .qm
    sudo apt install pyqt5-dev-tools

1. i18 directory, contains

    es.ts <- es locale typescript file
    es.qm <- es locale q-compiled file

2. a_translation_module.py calls on __init__

    self.plugin_dir = os.path.dirname(__file__)
    locale = QSettings().value('locale/userLocale')[0:2]
    locale_path = os.path.join(
        self.plugin_dir,
        'i18n',
        '{}.qm'.format(locale))
        # 'hola_{}.qm'.format(locale))

    if os.path.exists(locale_path):
        self.translator = QTranslator()
        self.translator.load(locale_path)
        QCoreApplication.installTranslator(self.translator)

3. when used

    class ATraslationClass:
        ...
        def tr(self, message):
            return QCoreApplication.translate('ATraslationClass', message)

4. Prepare, scanning for translation strings. 

    es.ts files can be edited with Qt Linguist, or manually edited.
    pylupdate5 a_translation_module.py -ts i18n/es.ts
    pylupdate5 *.py -ts i18n/es.ts
    
5. Compile translation strings

    lrelease i18n/es.ts -qm i18n/es.qm

    # lrelease i18n/es.ts -qm i18n/hola_es.qm

        
## Other references

    /usr/share/qgis/python/plugins/processing/algs/gdal/GdalAlgorithm.py
    /usr/share/qgis/python/plugins/processing/algs/gdal/GdalAlgorithmDialog.py
    /usr/share/qgis/python/plugins/processing/algs/gdal/GdalAlgorithmProvider.py
