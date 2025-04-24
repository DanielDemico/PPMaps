from flask import Flask, render_template, request
import pandas as pd
import folium 

import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

dados = [
    {"cidade": "São Paulo", "lat": -23.5505, "lon": -46.6333, "porte": "Grande", "nome": "Elite Tower"},
    {"cidade": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "porte": "Médio", "nome": "Vista Mar Plaza"},
    {"cidade": "Salvador", "lat": -13.7797, "lon": -36.9297, "porte": "Médio", "nome": "Capital Business Hub"},
    {"cidade": "Salvador", "lat": -12.9777, "lon": -38.5016, "porte": "Grande", "nome": "Bahia Trade Center"},
    {"cidade": "Fortaleza", "lat": -3.7172, "lon": -38.5433, "porte": "Médio", "nome": "Fortaleza Prime"},
    # ... (restante dos dados)
]

df = pd.DataFrame(dados)

# Extrai valores únicos para os filtros
cidades = sorted(list(set(dado["cidade"] for dado in dados)))
portes = sorted(list(set(dado["porte"] for dado in dados)))

dados2 = []
for group, value in df.groupby('cidade'):
    print(group, value)
    print("-----------")
    len_count = 0
    for i,r in value.iterrows():
        len_count += 1
    dados2.append({"cidade":group,"quantidade_leads":len_count,'lat':float(value['lat'].median()),'lon':float(value['lon'].median())})




print(dados2)
@app.route('/')
def show_map():
    # Lê os valores dos filtros da query string
    cidade_selecionada = request.args.get('cidade')
    porte_selecionado = request.args.get('porte')

    heat_map = request.args.get('hot_map', 'false').lower() == 'true'

    print(heat_map)
    
    # Aplica os filtros sequencialmente
    dados_filtrados = dados
    if cidade_selecionada and cidade_selecionada != "Todas":
        # Filtra pela cidade selecionada
        dados_filtrados = [dado for dado in dados_filtrados if dado["cidade"] == cidade_selecionada]
        
    if porte_selecionado and porte_selecionado != "Todas":
        # Filtra pelo porte selecionado (sobre os dados já filtrados por cidade, se aplicável)
        dados_filtrados = [dado for dado in dados_filtrados if dado["porte"] == porte_selecionado]

    # Define a localização inicial do mapa

    map_location = [-15.77777, -47.7777]
    map_zoom = 4
    mapa = folium.Map(location=map_location, zoom_start=map_zoom)
    
    if heat_map:
        from folium.plugins import HeatMap
        heat_data = [[local["lat"], local["lon"]] for local in dados_filtrados]
        HeatMap(heat_data).add_to(mapa)
    else:
        for local in dados_filtrados:
            folium.Marker(
                location=[local["lat"], local["lon"]],
                popup=f"{local['nome']} ({local['porte']})", 
                tooltip=local["nome"]
            ).add_to(mapa)
        
    return render_template(
        'index.html', 
        mapa=mapa._repr_html_(), 
        cidades=cidades, 
        portes=portes,
        cidade_selecionada=cidade_selecionada or "Todas",
        porte_selecionado=porte_selecionado or "Todas" ,
        heat_map=heat_map
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    