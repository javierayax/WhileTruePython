# Ejecutar el comando 'jupyter notebook' para iniciar la aplicación

#Realizar la conexión con el portal
from arcgis.gis import GIS
gis = GIS("http://whiletruepy.maps.arcgis.com", "whiletruepy", "Esrico123")

# Acceder a información de usuarios
legolas = gis.users.get('whiletruepy')
legolas
legolas["firstName"]

# Buscar contenido de la organización
from IPython.display import display
items = gis.content.search('Middle Earth', add_org=True)
for item in items:
    display(item)

# Buscar contenido tipificado por web map
items = gis.content.search('Uruk', item_type = 'Web Map' ,  add_org=True)
for item in items:
    display(item)
mapa = items[0]

# Buscar contenido tipificado por feature service
items = gis.content.search('Uruk', item_type = 'Feature Service' ,  add_org=True)
for item in items:
    display(item)
featureService = items[0]

# Acceder a información de grupos
listaGrupos = gis.groups.list()
grupo = listaGrupos[0]
grupoid = grupo.groupid

#mapa.unshare(grupoid)
#featureService.unshare(grupoid)
featureService.share(everyone=False, org=False, groups= grupoid)
mapa.share(everyone=False, org=False, groups= grupoid)
