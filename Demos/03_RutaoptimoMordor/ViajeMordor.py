# Librerias
from arcpy.sa import *

# Variables de ambiente
arcpy.env.overwriteOutput = 1
arcpy.env.extent = arcpy.Describe("LIMITE").extent
arcpy.env.mask = "LIMITE"
arcpy.env.cellSize = 200
arcpy.env.workspace = "in_memory"

#Procesamiento raster
disTropas = EucDistance("MINAS")
pendiente = Slope("MDE", "PERCENT_RISE")
disCaminos = EucDistance("VIAS")
usoRaster = Raster(arcpy.FeatureToRaster_conversion("USO_RURAL", "CAMUFLAJE", "usoRaster"))
alturaCobertura = Raster(arcpy.FeatureToRaster_conversion("USO_RURAL", "ALTURA", "ras_AlturaCobertura"))

# definicion de clases según el peligro
remapTro = RemapRange([[0, 1000, 5], [1000, 2000, 4], [2000, 3000, 3], [3000, 4000, 2], [4000, round(disTropas.maximum), 1]])
remapPen = RemapRange([[0, 5, 1], [5, 10, 2], [10, 20, 3], [20, 30, 4], [30, round(pendiente.maximum), 5]])
remapCam = RemapRange([[0, 100, 5], [100, 200, 4], [200, 300, 3], [300, 400, 2], [400, round(disCaminos.maximum), 1]])
remapAlt = RemapRange([[0, 1, 5], [1, 5, 4], [5, round(alturaCobertura.maximum), 1]])

# reclasificación para normalizar los valores
arcpy.env.workspace = arcpy.env.scratchGDB
peligroTropas = Reclassify(disTropas, "VALUE", remapTro, "NODATA")
topografia = Reclassify(pendiente, "VALUE", remapPen, "NODATA")
proxCaminos = Reclassify(disCaminos, "VALUE", remapCam, "NODATA")
posiCamuflaje = usoRaster
alturaCob = Reclassify(alturaCobertura, "VALUE", remapAlt, "NODATA")

# Superficie de costo
arcpy.env.workspace = "in_memory"
costo = peligroTropas*0.3 + topografia*0.1 + proxCaminos*0.2 + posiCamuflaje*0.15 + alturaCob*0.25

# Cost distance: Cuanto me cuesta moverme a través de la superfice de costo
distanciasAcumuladas = CostDistance("MORDOR", costo, "#", "Backlink")

# Ruta de Frodo y Sam
Ruta = CostPath("THE_SHIRE", distanciasAcumuladas, "Backlink")