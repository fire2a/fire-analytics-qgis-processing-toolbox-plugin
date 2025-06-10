<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es">
<context>
    <name>BaseContext</name>
    <message>
        <location filename="../algorithm_deprecated.py" line="79"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <translation>Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
</context>
<context>
    <name>BetweennessCentralityMetric</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1514"/>
        <source>Use default sampling ratio</source>
        <translation>Usar la ratio de sampleo por defecto</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1522"/>
        <source>K samples to estimate betweenness.
 Not set and disabled default sampling checkbox means all nodes are used: very slow!
 Trade-off between accuracy and running time.</source>
        <translation>K muestras para estimar la centralidad de intermediación.
	No fijado y deshabilitada la casilla de muestreo por defecto significa que se usan todos los nodos: ¡muy lento!
	Es un dilema entre precisión y tiempo de ejecución.</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1537"/>
        <source>Random number generator seed for sampling. Used if K is not set.</source>
        <translation>Semilla del generador de números aleatorios para el muestreo. Se usa si K no está configurado.</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1557"/>
        <source>Output raster</source>
        <translation type="obsolete">Raster de salida</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1493"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1557"/>
        <source>Output raster</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster de salida</translation>
    </message>
</context>
<context>
    <name>BurnProbabilityMetric</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1327"/>
        <source>Burn probabilty raster is the mean of all simulations&lt;br&gt;
            It&apos;s the same as using the &apos;Fire Scar&apos; algorithm, skipping output for scars and polygons, leaving only the &apos;Burn Probability&apos; output enabled&lt;br&gt;
            From a simulation results directory, select the &apos;Grids&apos; directory and choose any of the &apos;ForestGrid&apos; files
            </source>
        <translation>El raster de probabilidad de quema (BP) es la media de todas las simulaciones&lt;br&gt;
		    Es lo mismo que usar el algoritmo 'Fire Scar', omitiendo la salida de cicatrices y polígonos, dejando solo la salida de 'Burn Probability' habilitada&lt;br&gt;
	    </translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1259"/>
        <source>burn probability</source>
        <translation type="unfinished">probabilidad de quema</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1259"/>
        <source>Output raster</source>
        <translation type="obsolete">Raster de salida</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1238"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1259"/>
        <source>Output raster</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster de salida</translation>
    </message>
</context>
<context>
    <name>ClusterizeAlgorithm</name>
    <message>
        <location filename="../algorithm_clusterize.py" line="88"/>
        <source>to clusterize</source>
        <translation>para agrupar</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="99"/>
        <source>Raster Configuration Matrix (use same order than input rasters)</source>
        <translation>Matriz de configuración de raster (usar el mismo orden que los rasters de entrada)</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="108"/>
        <source>Distance threshold [adjusted observations]</source>
        <translation>Umbral de distancia [observaciones ajustadas]</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="122"/>
        <source>Total clusters</source>
        <translation>Total de grupos</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="134"/>
        <source>Minimum surface [pixels]</source>
        <translation type="unfinished">Superficie mínima [píxeles]</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="88"/>
        <source>Input rasters</source>
        <translation type="unfinished">Rasters de entrada</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="183"/>
        <source>Output raster</source>
        <translation type="unfinished">Raster de salida</translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="190"/>
        <source>Output polygons</source>
        <translation type="unfinished">Polígonos de salida</translation>
    </message>
</context>
<context>
    <name>DownStreamProtectionValueMetric</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1711"/>
        <source>Protection Value Raster (get values &amp; geotransform)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1732"/>
        <source>Output raster</source>
        <translation type="obsolete">Raster de salida</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1742"/>
        <source>Maximum number of threads to use simultaneously</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1930"/>
        <source>This Metric mixes a user defined proteccion value raster with the fire spread history of each simulation (the Propagation Digraph). Using the fact that the value of a pixel should also include the values of downstream pixels (or succesors in its fire propagation tree); In the sense that protecting that pixel also protects where the fire would have gone if not protected&lt;br&gt;
            &lt;a href=&quot;https://doi.org/10.1016/j.cor.2021.105252&quot;&gt;https://doi.org/10.1016/j.cor.2021.105252&lt;/a&gt;&lt;br&gt;
            &lt;b&gt;To run:&lt;/b&gt;&lt;br&gt;
            1. Select a protection value raster 
                - Any number type works
                - NODATA is mapped to 0 value
                - In a relative sense, negative numbers mean you want them burned / unprotected
            2. First generate the Propagation Digraph Algorithm that generates the messages.pickle file &lt;i&gt;(skip showing them if they are too many simulations and periods)&lt;/i&gt; by default along side the original messages.csv files
            3. Select the messages.pickle file
            &lt;b&gt;Advanced options:&lt;/b&gt;&lt;br&gt;
            - &lt;b&gt;Threads&lt;/b&gt; Maximum number of threads to use simultaneously. Does not work on Windows! (use linux for serious parallelization)
            For retaining &lt;i&gt;protection value compatibility&lt;/i&gt; use:
            - &lt;b&gt;No Burn Fill&lt;/b&gt; Include original protection values where no fire was seen (default true)
            - &lt;b&gt;Scaling&lt;/b&gt; Scale every pixel by burn count (default true); or all pixels by number of simulations (false)
            For &lt;i&gt;fraction of times pixels were burned&lt;/i&gt; use the false options, even with burn probability as the protection value
            </source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1732"/>
        <source>Output raster</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster de salida</translation>
    </message>
</context>
<context>
    <name>FileLikeFeedback</name>
    <message>
        <location filename="../algorithm_clusterize.py" line="330"/>
        <source>Polygonize Multiple Rasters</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="333"/>
        <source>Utils</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_clusterize.py" line="351"/>
        <source> &lt;h1&gt; Automatic clustering of different rasters &lt;/h1&gt;
        &lt;h2&gt; Overview &lt;/h2&gt;
        A scikit-learn pipeline that:
        1. Handles nodata with &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html&quot;&gt;SimpleImputer&lt;/a&gt;
        2. Scales data with &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html&quot;&gt;StandardScaler&lt;/a&gt;, &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html&quot;&gt;RobustScaler&lt;/a&gt; which removes outliers or &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html&quot;&gt;OneHotEncoder&lt;/a&gt; for categorical data like fuel models.
        3. Rescales all observations to [0, 1], then multiplies a prioritization (weight) to each raster.
        4. Clusterizes the map using the &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html&quot;&gt;Agglomerative&lt;/a&gt; clustering algorithm.
        &lt;h2&gt; Usage &lt;/h2&gt;
        1. Select the rasters: notice you can drag &amp; drop to &lt;i&gt;reorder&lt;/i&gt; them.
        2. Optionally fill the matrix &lt;i&gt;in the same order&lt;/i&gt; than the selected rasters, with
        - scaling_strategy = [&quot;standard&quot;, &quot;robust&quot;, &quot;onehot&quot;] (default is &quot;standard&quot;)
        - no_data_strategy = [&quot;mean&quot;, &quot;median&quot;, &quot;most_frequent&quot;, &quot;constant&quot;] (default is &quot;mean&quot;)
        - fill_value = any number (only for &quot;constant&quot; no_data_strategy) (default is 0)
        - weight = any number (default is 1)
        &lt;b&gt;Categorical rasters (like fuel models) should use &quot;onehot&quot; and &quot;most_frequent&quot;&lt;/b&gt;
        &lt;br&gt;
        3. Experiment with the distance threshold until you get the desired number of clusters. Less distance (until 0) yields more clusters and processing time.
        4. Fine tune the output, ensuring clusters have a minimum number of pixels using the advanced parameter -that invokes GDAL&apos;s: &lt;a href=&quot;https://gdal.org/en/latest/programs/gdal_sieve.html#gdal-sieve&quot;&gt;gdal_sieve&lt;/a&gt;
        5. Outputs: The output polygon layer has the attribute &apos;number of pixels&apos;. The raster layer can be skipped.
        6. Data debug: There&apos;s an additional option to raise a (mat)plot(lib) window with original &amp; rescaled data distributions, clustering sizes history &amp; histogram labels. Available outside QGIS, by executing the shown command adding the &apos;--plots&apos; flag in the terminal (OSGeo4WShell).

        &lt;br&gt;
        &lt;i&gt;Both agglomerative and sieve connectivity is done with 4 neighbors because the fire simulator can cross diagonals&lt;i/&gt;

        In depth instructions can be found &lt;a href=&quot;https://fire2a.github.io/fire2a-lib/fire2a/agglomerative_clustering.html&quot;&gt;here&lt;/a&gt;
        </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>FireSimulatorAlgorithm</name>
    <message>
        <location filename="../algorithm_simulator.py" line="206"/>
        <source>==================
LANDSCAPE SECTION

Surface fuel model</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="289"/>
        <source>
Firebreaks raster (1=firebreak)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="309"/>
        <source>Generation mode</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="354"/>
        <source>
================
WEATHER SECTION

source mode</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="438"/>
        <source>
================
OUTPUTS SECTION

options (click &apos;...&apos; button on the right)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="733"/>
        <source>Single weather file scenario requires a file!</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="747"/>
        <source>Multiple weathers requires a directory with Weather[0-9]*.csv files!</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="946"/>
        <source>Cell2 Fire Simulator</source>
        <translation>Simulador de incendio por celdas</translation>
    </message>
    <message>
        <location filename="../algorithm_simulator.py" line="975"/>
        <source>
            See documentation:
            &lt;a href=https://fire2a.github.io/docs/qgis-toolbox/algo_simulator.html&gt;This dialog&lt;/a&gt;
            &lt;a href=https://fire2a.github.io/docs/Cell2FireW&gt;Cell2FireW&lt;/a&gt;
            &lt;font color=&quot;red&quot;&gt;Warning: GeoTiff(.tif) support (in development) limited to only reading the fuels layer!&lt;/font&gt; If planning to use more layers, transform them to AIIGrid(.asc) format!
            &lt;font color=&quot;orange&quot;&gt;Warning: Kitral cbh and cbd rasters must use nodata -9999&lt;/font&gt;
            </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>FireToolboxAlgorithm</name>
    <message>
        <location filename="../fireanalyticstoolbox_algorithm.py" line="67"/>
        <source>Input layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../fireanalyticstoolbox_algorithm.py" line="76"/>
        <source>Output layer</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>FireToolboxProvider</name>
    <message>
        <location filename="../fireanalyticstoolbox_provider.py" line="113"/>
        <source>Fire Analytics</source>
        <translation>Analíticas de incendios</translation>
    </message>
</context>
<context>
    <name>IgnitionPointsFromLogFileSIMPP</name>
    <message>
        <location filename="../algorithm_deprecated.py" line="99"/>
        <source>Output ignition point(s) layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_deprecated.py" line="188"/>
        <source>zdeprecated</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_deprecated.py" line="197"/>
        <source>Ignition Points From LogFile</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>IgnitionPointsSIMPP</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="123"/>
        <source>Output ignition point(s) layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="199"/>
        <source>Simulator Post Processing</source>
        <translation type="unfinished">Post procesamiento de simulaciones</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="208"/>
        <source>Ignition Points</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="105"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
</context>
<context>
    <name>InstanceDownloader</name>
    <message>
        <location filename="../algorithm_instance_downloader.py" line="63"/>
        <source>Select the instances to download</source>
        <translation>Seleccione las instancias a descargar</translation>
    </message>
    <message>
        <location filename="../algorithm_instance_downloader.py" line="136"/>
        <source>Instance Downloader</source>
        <translation>Descargador de instancias</translation>
    </message>
    <message>
        <location filename="../algorithm_instance_downloader.py" line="71"/>
        <source>optional</source>
        <translation>opcional</translation>
    </message>
    <message>
        <location filename="../algorithm_instance_downloader.py" line="71"/>
        <source>- leave empty for using selected filename and temporary path
- if current project is saved its path will be used
- else use absolute filenaming (.zip extension is suggested)
- or relative filenaming for users home directory (or default qgis launch path)

After downloading, the file will be unzipped and opened in the file browser
</source>
        <translation>- dejar vacío para usar el nombre de archivo seleccionado en ruta temporal
- si el proyecto actual está guardado se usará su ruta
- de lo contrario usar un nombre de archivo absoluto (.zip es sugerido)
- o un nombre de archivo relativo al directorio personal del usuario (o ruta de inicio por defecto de qgis)</translation>
    </message>
    <message>
        <location filename="../algorithm_instance_downloader.py" line="71"/>
        <source>Output file</source>
        <translation type="unfinished">Archivo de salida</translation>
    </message>
</context>
<context>
    <name>MatchAIIGrid</name>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="52"/>
        <source>Raster to modify</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="60"/>
        <source>Raster to match to</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="69"/>
        <source>CLI arguments</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="78"/>
        <source>Matched raster</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="193"/>
        <source>Match AII Grids</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="196"/>
        <source>Utils</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_match_aiigrids.py" line="211"/>
        <source>Simplifies using gdal translate to &lt;b&gt;clip extent, then resize and replace geotransform&lt;/b&gt; to match an ascii raster into another&lt;br&gt;&lt;br&gt;
            useful cli_args: -r {nearest,bilinear,cubic,cubicspline,lanczos,average,mode} (default nearest)&lt;br&gt;&lt;br&gt;
            not implemented: dealing with CRSs or nodatas.
            </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>MessagesSIMPP</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="586"/>
        <source>Output propagation digraph layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="594"/>
        <source>Output pickled messages file (needed by BC or DPV metrics, defaults to results/Messages/messages.pickle)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="712"/>
        <source>Simulator Post Processing</source>
        <translation type="unfinished">Post procesamiento de simulaciones</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="721"/>
        <source>Propagation DiGraph</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="730"/>
        <source>Warning: Uncheck &apos;Open output file after running algorithm&apos; if the graph is too big or your computer too slow.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="565"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
</context>
<context>
    <name>MeteoAlgo</name>
    <message>
        <location filename="../algorithm_meteo.py" line="66"/>
        <source>Quantile of daily maximum temperature</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="77"/>
        <source>Start Hour</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="86"/>
        <source>Step resolution in minutes (time between rows) - Not implemented yet</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="96"/>
        <source>Lenght of each scenario (number of rows) - Implementing hourly weather scenarios only.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="106"/>
        <source>Number of scenarios to generate</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="117"/>
        <source>Output folder</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="204"/>
        <source>Meteo Kitral</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_meteo.py" line="207"/>
        <source>Utils</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>MultiObjectiveRasterKnapsackAlgorithm</name>
    <message>
        <location filename="../algorithm_knapsack.py" line="655"/>
        <source>Input rasters</source>
        <translation type="unfinished">Rasters de entrada</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="666"/>
        <source>Raster Configuration Matrix (use same order than input rasters)</source>
        <translation type="unfinished">Matriz de configuración de raster (usar el mismo orden que los rasters de entrada)</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="676"/>
        <source>Raster Knapsack Output layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="845"/>
        <source>Multi Objective Raster Knapsack</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="848"/>
        <source>Decision Optimization</source>
        <translation>Optimizador de decisiones</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="863"/>
        <source>Optimizes a multi objective knapsack problem using layers as values and/or weights, returns a layer with the selected pixels.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="874"/>
        <source>&lt;b&gt;1.&lt;/b&gt; Select a list of rasters to be used as values (to maximize or minimize) or weights (to be capacity constrained).
            (drag to reorder the rasters to match the matrix)

            &lt;b&gt;2.&lt;/b&gt; Complete the matrix datasheet in the same order as 1.:
            &lt;b&gt;- value_rescaling&lt;/b&gt;: minmax, onehot, standard, robust or pass for no rescaling.
                &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMax.html&quot;&gt;MinMax&lt;/a&gt; is default if only a value_weight is provided.
                &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html&quot;&gt;OneHotEncoder&lt;/a&gt; is for categorical data, e.g., fuel models.
                MinMax and OneHot outputs into [0,1] range, &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html&quot;&gt;Standard Scaler&lt;/a&gt; (x - &amp;mu;) / &amp;sigma; and &lt;a href=&quot;https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html&quot;&gt;Robust Scaler&lt;/a&gt; (same without outliers) not
            &lt;b&gt;- value_weight&lt;/b&gt;: Any real number, although 0 doesn&apos;t make sense, &lt;i&gt;negative values are for minimizing instead of maximizing&lt;/i&gt;
            &lt;b&gt;- capacity_sense&lt;/b&gt;, whether &lt;i&gt;at most or at least&lt;/i&gt;, use any of: &quot;&amp;lt;=, &amp;le;, le, ub&quot; or &quot;&amp;gt;=, &amp;ge;, ge, lb&quot;, respectively.
            &lt;b&gt;- capacity_ratio&lt;/b&gt;: A real number, inside (-1,1). Internally it&apos;s multiplied by the &lt;i&gt;sum of all weights of that layer&lt;/i&gt;. E.g., 0.5 selects (at most or at least) half of the pixels, if all weights (values of that raster) are equal.
            &lt;b&gt;3. [speed-up]&lt;/b&gt; Stop visually debugging your calculations by disabling the plots option in Advanced Parameters (writing the plots can take a while).

            A new raster with selected, not selected and undecided pixels will be created. The undecided pixels means the solver failed to terminate fully; modifying solver options can mitigate this issue.

            The classical knapsack problem is NP-hard, so a MIP solver engine is used to find &quot;nearly&quot; the optimal solution (**), because -often- is asymptotically hard to prove the optimal value. So a default gap of 0.5% and a timelimit of 5 minutes cuts off the solver run. The user can experiment with these parameters to trade-off between accuracy, speed and instance size(*). On Windows closing the blank terminal window will abort the run!

            By using Pyomo, several MIP solvers can be used: CBC, GLPK, Gurobi, CPLEX or Ipopt; If they&apos;re accessible through the system PATH, else the executable file can be selected by the user. Installation of solvers is up to the user.

            Although windows version is bundled with CBC unsigned binaries, so their users may face a &quot;Windows protected your PC&quot; warning, please avoid pressing the &quot;Don&apos;t run&quot; button, follow the &quot;More info&quot; link, scroll then press &quot;Run anyway&quot;. Nevertheless windows cbc does not support multithreading, so ignore that warning (or switch to Linux).

            (*): Complexity can be reduced greatly by rescaling and/or rounding values into integers, or even better coarsing the raster resolution (see gdal translate resolution).
            (**): There are specialized knapsack algorithms that solve in polynomial time, but not for every data type combination; hence using a MIP solver is the most flexible approach.

            </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>PARasterKnapsackAlgorithm</name>
    <message>
        <location filename="../algorithm_knapsack.py" line="920"/>
        <source>Protected area layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="929"/>
        <source>Strategy for the protected pixels</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="942"/>
        <source>Values layer (if blank 1&apos;s will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="951"/>
        <source>Weights layer (if blank 1&apos;s will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="960"/>
        <source>Capacity ratio (1 = weight.sum)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="973"/>
        <source>Raster Knapsack Output layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="1213"/>
        <source>Raster Knapsack with Protected Area</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="1216"/>
        <source>Decision Optimization</source>
        <translation type="unfinished">Optimizador de decisiones</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="1231"/>
        <source>Optimizes the knapsack problem by incorporating protected area (pixels) that the algorithm cannot select.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="1242"/>
        <source>Optimizes the knapsack problem by incorporating protected area (pixels) that the algorithm cannot select. 

                &lt;b&gt;1. Select the protected pixels layer:&lt;/b&gt; 
                This must be a raster fully populated with 0s and 1s. Pixels with a value of 1 will be treated as protected, while those with a value of 0 will be considered non-protected.

                It is crucial that the raster contains no missing values and only binary values (0 and 1) to ensure the algorithm functions correctly.
                
                &lt;b&gt;2. Choose the strategy to apply to protected pixels:&lt;/b&gt;
                Two strategies are available:

                Strategy 1 – Make protected pixels unselectable:
                This strategy excludes pixels classified as protected from selection and solves the knapsack problem using only non-protected pixels.

                Strategy 2 – Reselection prioritizing pixels neighboring the protected area:
                This strategy involves first solving the classic knapsack problem using the provided value and weight layers. Pixels selected outside the protected area are retained, while those selected within the protected area are re-optimized by relocating them toward its border.
            </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>PolyTreatmentAlgorithm</name>
    <message>
        <location filename="../algorithm_treatment.py" line="757"/>
        <source>Input Polygons Layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="765"/>
        <source>Attribute table field name for {self.IN_TRT}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="779"/>
        <source>Attribute table field name for {field_value} [0s if not provided]</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="792"/>
        <source>Treatments table (fid,treatment,value,value/m2,cost,cost/m2)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="801"/>
        <source>Total Area</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="813"/>
        <source>Total Budget</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="1028"/>
        <source>Polygon Treatment</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="829"/>
        <source>Set invalid geometry check to GeometrySkipInvalid (more options clicking the wrench on the input poly layer)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="1031"/>
        <source>Decision Optimization</source>
        <translation type="unfinished">Optimizador de decisiones</translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="1047"/>
        <source>&lt;b&gt;Objetive:&lt;/b&gt; Maximize the changed value of the treated polygons&lt;br&gt; 
            &lt;b&gt;Decisions:&lt;/b&gt; Which treatment to apply to each polygon (or no change)&lt;br&gt;
            &lt;b&gt;Contraints:&lt;/b&gt;&lt;br&gt;
            (a) fixed+area costs less than budget&lt;br&gt;
            (b) treated area less than total area&lt;br&gt; 
            &lt;b&gt;Inputs:&lt;/b&gt;&lt;br&gt;
            (i) A polygon layer with &lt;b&gt;current&lt;/b&gt; attributes: [fid],&lt;b&gt;treatment, value, value/m2&lt;/b&gt;&lt;br&gt;
            (ii) A .csv table defining &lt;b&gt;target&lt;/b&gt; treatments: &lt;b&gt;fid, treatment, value, value/m2, cost, cost/m2&lt;/b&gt; (use these column names)&lt;br&gt;
            - fid is the feature id of each polygon so it&apos;s given in the attribute table, but must be specified in the .csv table&lt;br&gt;
            - current &amp; target treatment are just strings, but each polygon needs at least one feasible treatment (one row)&lt;br&gt;
            - current &amp; target values[/m2] weight towards the objective when no change (keep current) or a target treatment is recommended&lt;br&gt;
            (iii) &lt;b&gt;Budget&lt;/b&gt; (same units than costs)&lt;br&gt;
            (iv) &lt;b&gt;Area&lt;/b&gt; (same units than the geometry of the polygons)&lt;br&gt;
            &lt;br&gt;
            &lt;br&gt;
            sample: &lt;a href=&apos;</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>PolygonKnapsackAlgorithm</name>
    <message>
        <location filename="../algorithm_knapsack.py" line="71"/>
        <source>Input Polygons Layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="79"/>
        <source>Attribute table field name for VALUE (if blank 1&apos;s will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="92"/>
        <source>Attribute table field name for WEIGHT (if blank polygon&apos;s area will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="105"/>
        <source>Capacity ratio (1 = weight.sum)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="117"/>
        <source>Polygon Knapsack Output Layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="119"/>
        <source>Set invalid geometry check to GeometrySkipInvalid (more options clicking the wrench on the input poly layer)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="299"/>
        <source>Polygon Knapsack</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="302"/>
        <source>Decision Optimization</source>
        <translation type="unfinished">Optimizador de decisiones</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="317"/>
        <source>Optimizes the classical knapsack problem using polygons with values and/or weights attributes, returns a polygon layer with the selected polygons.</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>PostSimulationAlgorithm</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="515"/>
        <source>Bundle</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="533"/>
        <source>This algorithm attempts to load everything from a simulation results directory, in a convenient but slower than selecting one of the following algorithms in the &lt;b&gt;PostProcessing group&lt;/b&gt;. Check each one for more details.

            Although &lt;b&gt;Propagation Directed Graph&lt;/b&gt; output is fundamental to risk metrics such as DPV and BC: &lt;b&gt;Warning: Enabling it here can hang-up your system&lt;/b&gt;, around 300.000 arrows is manageable for a regular laptop&lt;br&gt;
            Be safe by counting them first: Go to results/Messages folder:&lt;br&gt;
             - using bash $ wc -l Messages*csv&lt;br&gt;
             - using PowerShell &gt; Get-Content Messages*.csv | Measure-Object -Line&lt;br&gt;
            To process but not display them, use Propagation DiGraph algorithm directly, unchecking &apos;Open output file after running algorithm&apos;&lt;br&gt;&lt;br&gt;
            &lt;i&gt;The visualization alternative is &lt;b&gt;Propagation Fire Scars&lt;/b&gt;. Or even &lt;b&gt;Final Fire Scar&lt;/b&gt;, recommended for very large simulations&lt;/i&gt;
            </source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="225"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
</context>
<context>
    <name>RasterKnapsackAlgorithm</name>
    <message>
        <location filename="../algorithm_knapsack.py" line="340"/>
        <source>Values layer (if blank 1&apos;s will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="349"/>
        <source>Weights layer (if blank 1&apos;s will be used)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="358"/>
        <source>Capacity ratio (1 = weight.sum)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="371"/>
        <source>Raster Knapsack Output layer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="555"/>
        <source>Raster Knapsack</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="558"/>
        <source>Decision Optimization</source>
        <translation type="unfinished">Optimizador de decisiones</translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="573"/>
        <source>Optimizes the classical knapsack problem using layers as values and/or weights, returns a layer with the selected pixels.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_knapsack.py" line="584"/>
        <source>By selecting a Values layer and/or a Weights layer, and setting the bound on the total capacity, a layer that maximizes the sum of the values of the selected pixels is created.

            A new raster (default .gpkg) will show selected pixels in red and non-selected green (values 1, 0 and no-data=-1).

            The capacity constraint is set up by choosing a ratio (between 0 and 1), that multiplies the sum of all weights (except no-data). Hence 1 selects all pixels that aren&apos;t no-data in both layers.

            This raster knapsack problem is NP-hard, so a MIP solver engine is used to find &quot;nearly&quot; the optimal solution (**), because -often- is asymptotically hard to prove the optimal value. So a default gap of 0.5% and a timelimit of 5 minutes cuts off the solver run. The user can experiment with these parameters to trade-off between accuracy, speed and instance size(*). On Windows closing the blank terminal window will abort the run!

            By using Pyomo, several MIP solvers can be used: CBC, GLPK, Gurobi, CPLEX or Ipopt; If they&apos;re accessible through the system PATH, else the executable file can be selected by the user. Installation of solvers is up to the user.

            Although windows version is bundled with CBC unsigned binaries, so their users may face a &quot;Windows protected your PC&quot; warning, please avoid pressing the &quot;Don&apos;t run&quot; button, follow the &quot;More info&quot; link, scroll then press &quot;Run anyway&quot;. Nevertheless windows cbc does not support multithreading, so ignore that warning (or switch to Linux).

            (*): Complexity can be reduced greatly by rescaling and/or rounding values into integers, or even better coarsing the raster resolution (see gdal translate resolution).
            (**): There are specialized knapsack algorithms that solve in polynomial time, but not for every data type combination; hence using a MIP solver is the most flexible approach.

            ----

            USE CASE:

            If you want to determine where to allocate fuel treatments throughout the landscape to protect a specific value that is affected by both the fire and the fuel treatments, use the following:

                - Values: Downstream Protection Value layer calculated with the respective value that you want to protect.

                - Weights: The layer, that contains the value that you want to protect and that is affected also by the fuel treatments (e.g., animal habitat).
            If you want to determine where to allocate fuel treatments through out the landscape to protect and specific value that is affected by both, the fire and the fuel treatments use: 
            </source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>RasterTreatmentAlgorithm</name>
    <message>
        <location filename="../algorithm_treatment.py" line="488"/>
        <source>Raster layer for {raster}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="498"/>
        <source>Treatments Matrix (csv)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="507"/>
        <source>Total Area</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="518"/>
        <source>Total Budget</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="682"/>
        <source>Raster Treatment</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="701"/>
        <source>&lt;b&gt;Objetive:&lt;/b&gt; Maximize the changed value of the treated raster&lt;br&gt; 
            &lt;b&gt;Decisions:&lt;/b&gt; Which treatment to apply to each pixel (or no change)&lt;br&gt;
            &lt;b&gt;Contraints:&lt;/b&gt;&lt;br&gt;
            (a) treat cost * pixel area less than budget&lt;br&gt;
            (b) treated area less than total area&lt;br&gt; 
            &lt;b&gt;Inputs:&lt;/b&gt;&lt;br&gt;
            (i) A .csv squared-table of &lt;b&gt;treatment transformation costs(/m2)&lt;/b&gt; (defines index encoding)&lt;br&gt;
            (ii) A raster layer with &lt;b&gt;current treatments&lt;/b&gt; index values (encoded: 0..number of treatments-1)&lt;br&gt;
            (iii) A raster layer with &lt;b&gt;current values&lt;/b&gt;&lt;br&gt;
            (iv) A multiband raster layer with &lt;b&gt;target values&lt;/b&gt; (number of treatments == number of bands)&lt;br&gt;
            (vi) &lt;b&gt;Budget&lt;/b&gt; (same units than costs)&lt;br&gt;
            (vii) &lt;b&gt;Area&lt;/b&gt; (same units than pixel size of the raster)&lt;br&gt;
            &lt;br&gt;
            - consistency between rasters is up to the user&lt;br&gt;
            - rasters &quot;must be saved to disk (for layers to have a publicSource != )&quot;&lt;br&gt;
            - raster no data == -1 &lt;br&gt;
            &lt;br&gt;
            sample: &lt;a href=&apos;</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>RasterTreatmentTeamAlgorithm</name>
    <message>
        <location filename="../algorithm_treatment.py" line="81"/>
        <source>Raster layer for {raster}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="91"/>
        <source>Treatments transformation costs (csv)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="100"/>
        <source>Total Area</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="111"/>
        <source>Total Budget</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="123"/>
        <source>Treatment areas &amp; budget (csv)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="134"/>
        <source>Teams on_cost, area, budget and abilities (csv)</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="145"/>
        <source>Raster tReatment</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="148"/>
        <source>Raster tEam</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="405"/>
        <source>Raster Treatment Team</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_treatment.py" line="424"/>
        <source>&lt;b&gt;Objetive:&lt;/b&gt; Maximize the changed value of the treated raster&lt;br&gt; 
            &lt;b&gt;Decisions:&lt;/b&gt; Which treatment to apply by which team to each pixel (or no change)&lt;br&gt;
            &lt;b&gt;Contraints:&lt;/b&gt;&lt;br&gt;
            (a) all treat cost * pixel area(pxa) + team on_cost is less than &lt;b&gt;Budget&lt;/b&gt;&lt;br&gt;
            (b) treat cost * pxa is less than &lt;b&gt;budget per treatment&lt;/b&gt;&lt;br&gt;
            (c) treat cost * pxa is less than &lt;b&gt;budget per team&lt;/b&gt;&lt;br&gt;
            (d) all treated area less than total &lt;b&gt;Area&lt;/b&gt;&lt;br&gt; 
            (e) treated area less than &lt;b&gt;area per treatment&lt;/b&gt;&lt;br&gt; 
            (f) treated area less than &lt;b&gt;area per team&lt;/b&gt;&lt;br&gt; 
            (g) at most one treatment by one team per pixel&lt;br&gt;
            (h) linkage between treating (h,w,r,e) and active teams (e) variables&lt;br&gt;
            &lt;b&gt;Inputs:&lt;/b&gt;&lt;br&gt;
            (i) A .csv squared-table of &lt;b&gt;treatment transformation costs(/m2)&lt;/b&gt; (defines index encoding)&lt;br&gt;
            (ii) A raster layer with &lt;b&gt;current treatments&lt;/b&gt; indexed values (encoded: 0..number of treatments-1)&lt;br&gt;
            (iii) A raster layer with &lt;b&gt;current values&lt;/b&gt;&lt;br&gt;
            (iv) A multiband raster layer with &lt;b&gt;target values&lt;/b&gt; (number of treatments == number of bands)&lt;br&gt;
            (vi) &lt;b&gt;Budget&lt;/b&gt; (same units than costs)&lt;br&gt;
            (vii) &lt;b&gt;Area&lt;/b&gt; (same units than pixel size of the raster)&lt;br&gt;
            (viii) A .csv table for each &lt;b&gt;treatment area and budget&lt;/b&gt; capacities&lt;br&gt;
            (viii) A .csv table for each &lt;b&gt;team on_cost, area, budget and abilities&lt;/b&gt; (1s is able)&lt;br&gt;
            &lt;br&gt;
            - consistency between rasters is up to the user&lt;br&gt;
            - rasters &quot;must be saved to disk (for layers to have a publicSource != )&quot;&lt;br&gt;
            - raster no data == -1 &lt;br&gt;
            &lt;br&gt;
            sample: &lt;a href=&apos;</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>RasterTutorial</name>
    <message>
        <location filename="../algorithm_raster_tutorial.py" line="53"/>
        <source>Output raster format .%s not supported</source>
        <translation>Formato de salida raster .%s no soportado</translation>
    </message>
    <message>
        <location filename="../algorithm_raster_tutorial.py" line="42"/>
        <source>Input Raster %s</source>
        <translation>Raster %s de entradash</translation>
    </message>
    <message>
        <location filename="../algorithm_raster_tutorial.py" line="43"/>
        <source>Output Raster</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>SandboxAlgorithm</name>
    <message>
        <location filename="../algorithm_sandbox.py" line="208"/>
        <source>Input File</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_sandbox.py" line="417"/>
        <source>AASandbox</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_sandbox.py" line="448"/>
        <source>This is an example algorithm that takes a vector layer and creates a new identical one.</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_sandbox.py" line="455"/>
        <source>This is an example algorithm that takes a vector layer and creates a new identical one.
        It is meant to be used as an example of how to create your own algorithms and explain methods and variables used to do it. An algorithm like this will be available in all elements, and there is not need for additional work.
        All Processing algorithms should extend the QgsProcessingAlgorithm class.</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>ScarSIMPP</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1032"/>
        <source>Output final scar raster</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1040"/>
        <source>Output propagation scars polygons</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1049"/>
        <source>Output burn probability raster</source>
        <translation type="unfinished">Salida raster de probabilidad de quema</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1195"/>
        <source>Fire Scar</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1198"/>
        <source>Simulator Post Processing</source>
        <translation>Post procesamiento de simulaciones</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1216"/>
        <source> - Input &lt;b&gt;Sample&lt;/b&gt; Fire Scar is any of the ForestGrid files; with it a pattern search for all Grids(any digit)/ForestGrid(any digit).csv will be performed.
            - Output &lt;b&gt;Final&lt;/b&gt; Scar raster needs simulation ran with Final Fire Scar option, each band is a simulation
            - Output &lt;b&gt;Burn Probability&lt;/b&gt; raster is the mean of all simulations, requires &gt;1 simulations
            - Output &lt;b&gt;Propagation&lt;/b&gt; Scars Polygons accumulates fixed-geometry, polygonized, in-memory rasters (4 steps); attributing for each one its: simulation, period, perimeter and area. This is known to fail in some qgis-versions, OSes or low RAM hardware. Mitigations:
            A. Change the default .gpkg format to .shp or test other
            B. Use the advanced options to tweak or disable the fix geometries option
            C. &lt;b&gt;Skip this output altogether by clicking the option button &apos;...&apos; and selecting Skip Output&lt;/b&gt;

            &lt;i&gt;If the Bundle algorithm failed for you, this propagation output is the most likely cause...&lt;/i&gt;</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="1011"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
</context>
<context>
    <name>StatisticSIMPP</name>
    <message>
        <location filename="../algorithm_postsimulation.py" line="805"/>
        <source>Output raster</source>
        <translation type="obsolete">Raster de salida</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="805"/>
        <source>mean &amp; std</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="945"/>
        <source>Simulator Post Processing</source>
        <translation type="unfinished">Post procesamiento de simulaciones</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="954"/>
        <source>Spatial Statistic</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="963"/>
        <source>
            This post processing algorithm, reads the raw output of C2F-W simulator and generates two rasters.
            One has one band per simulation, named &quot;StatName&quot; (so N bands for N simulations), e.g., Surface Flame Lenght
            
            The second one has two bands corresponding to the mean and standard deviation, e.g., &quot;Mean&amp;StdDev Hit Rate Of Spread&quot;.
            The &lt;b&gt;mean statistic&lt;/b&gt; sums, for each pixel, its values divided by &lt;b&gt;burnt count&lt;/b&gt;. 
            The &lt;b&gt;standard deviation&lt;/b&gt; divides against &lt;b&gt;all simulations&lt;/b&gt;, not burnt count of each individual pixel.

            Check the &lt;a href=https://fire2a.github.io/docs/qgis-toolbox/algo_simulator.html#options&gt;table below&lt;a/&gt; for more info
            </source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="757"/>
        <source>Base raster (normally fuel or elevation) to get the geotransform</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster base para posicionar el resultado (normalmente fuels o elevacion)</translation>
    </message>
    <message>
        <location filename="../algorithm_postsimulation.py" line="805"/>
        <source>Output raster</source>
        <comment>BaseContext</comment>
        <translation type="unfinished">Raster de salida</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../algorithm_utils.py" line="195"/>
        <source>This output is written to</source>
        <translation>Este resultado fue escrito en</translation>
    </message>
</context>
</TS>
