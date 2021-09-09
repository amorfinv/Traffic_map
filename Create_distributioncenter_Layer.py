import pandas as pd
import geopandas
import numpy as np


"""
Distribution Centers:

"""

df = pd.DataFrame(
    {'Latitude': [48.179141106442856, 48.20218497556507, 48.2374228446001, 48.235288533405026, 48.22090057904532,
                  48.208564827131205, 48.19381099750839, 48.18172745428605, 48.15038084460396, 48.241170048341935,
                  48.21863224600427, 48.181085814146044, 48.15305348714484, 48.19627260215861, 48.26124929704659,
                  48.25227837428879],
     
     'Longitude': [16.413526360203182, 16.40683285882645, 16.427807502497064, 16.358330898525026, 16.374786611284815,
                   16.34976021459994, 16.338824566771162, 16.36469818917773, 16.33116336359848, 16.34024576775175,
                   16.310253241457172, 16.350557716240093, 16.39272614884457, 16.27298229498073, 16.41248016786417,
                   16.30885995564679],
     
     'x': [605075.98186553316190839, 604531.54011397552676499, 606017.18194049131125212, 600862.72997154016047716, 602113.2443926160922274,
                   600278.51819347240962088, 599494.65698712039738894, 601441.260923080611974, 599008.64646360033657402, 599508.43952706654090434,
                   597324.37805510649923235, 600391.44045293156523257, 603582.33386281959246844, 594597.15198645240161568, 604830.41054744774010032,
                   597157.1566472165286541],
     
     'y': [5337177.35229714214801788, 5339729.4551335945725441, 5343674.75914492830634117, 5343343.96212801896035671, 5341766.52990576438605785,
                   5340362.4893431905657053, 5338708.43971354141831398, 5337399.22188809607177973, 5333871.07623823825269938, 5343974.08288992661982775,
                   5341430.64420210011303425, 5337309.34168784320354462, 5334249.60747597180306911, 5338898.89520060829818249, 5346301.95066336076706648,
                   5345168.55262735765427351],
     
     'Relative_size': [np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10),
                       np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10),
                       np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10),
                       np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10), np.random.normal(1, 0.10)],
          
     'Number_of_ports': [3, 3, 3, 3,
                       3, 3, 3, 3,
                       3, 3, 3, 3,
                       3, 3, 3, 3]})


#15128084460396

#the following distribution centers are outside the boundary circle:
48.31226639216305, 16.35304863735171
48.26583834811154, 16.435988148803034
48.117808345212715, 16.318936215162697

df.to_csv('Distribution_centers_locations.csv')

gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))


print(gdf)


gdf.to_file("Distribution_centers2.gpkg", layer='Distribution_centers2', driver="GPKG")











