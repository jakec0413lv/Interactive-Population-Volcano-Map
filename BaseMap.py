import folium
import pandas

def colorSelection(elev):
    if elev < 1000:
        return "yellow"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location=[36.107168393631724, -115.1866820366176], tiles = "Stamen Terrain")

df=pandas.read_csv("Volcanoes.txt")

lat = list(df["LAT"])
lon = list(df["LON"])
elevations = list(df["ELEV"])
names = list(df["NAME"])

html = """<h4>Volcano Information:</h4>
<strong>Name:</strong> <em>%s </em> <br>
<strong>Height:</strong> <em>%s m </em>
"""

fg = folium.FeatureGroup(name="My Map")
color = ""

fgv=folium.FeatureGroup(name="Volcanoes")
#Volcano Addition
for lt, ln, elev, n in zip(lat, lon, elevations, names): #zip() allows for iteration of multiple variables from multiple lists
    color = colorSelection(elev)
    iframe = folium.IFrame(html=html %  (n, str(elev)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius = 6, popup= folium.Popup(iframe), fill_color=colorSelection(elev), color ="grey", fill_opacity=0.7))



fgp = folium.FeatureGroup(name="Population")
 
fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<10000000 else 'orange' if 100000000 <= x['properties']
['POP2005']<20000000 else 'red'}))



map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("Map1.html")