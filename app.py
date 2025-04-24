from flask import Flask, render_template
import pandas as pd
import folium 

app = Flask(__name__)

dados = [
    {"nome": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"nome": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"nome": "Brasília", "lat": -15.7797, "lon": -47.9297},
]

@app.route('/')
def show_map():
    mapa = folium.Map(location=[-15.77777, -47.7777], zoom_start=4)
    
    for local in dados:
        folium.Marker(
            location=[local["lat"],local["lon"]],
            popup=local["nome"],
            tooltip=local["nome"]
        ).add_to(mapa)
        
    return render_template('mapa.html', mapa=mapa._repr_html_())

if __name__ == "__main__":
    app.run(debug=True)
    