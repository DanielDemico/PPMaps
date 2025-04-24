from flask import Flask, render_template, request
import pandas as pd
import folium 

app = Flask(__name__)

dados = [
    {"nome": "São Paulo", "lat": -23.5505, "lon": -46.6333, "porte": "Grande"},
    {"nome": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "porte": "Médio"},
    {"nome": "Brasília", "lat": -15.7797, "lon": -47.9297, "porte": "Médio"},
    # Adicione mais cidades conforme necessário
]

# Extrai valores únicos para os filtros
cidades = sorted(list(set(dado["nome"] for dado in dados)))
portes = sorted(list(set(dado["porte"] for dado in dados)))

@app.route('/')
def show_map():
    # Lê os valores dos filtros da query string
    cidade_selecionada = request.args.get('cidade')
    porte_selecionado = request.args.get('porte')
    
    # Aplica os filtros sequencialmente
    dados_filtrados = dados
    if cidade_selecionada and cidade_selecionada != "Todas":
        # Filtra pela cidade selecionada
        dados_filtrados = [dado for dado in dados_filtrados if dado["nome"] == cidade_selecionada]
        
    if porte_selecionado and porte_selecionado != "Todas":
        # Filtra pelo porte selecionado (sobre os dados já filtrados por cidade, se aplicável)
        dados_filtrados = [dado for dado in dados_filtrados if dado["porte"] == porte_selecionado]

    # Define a localização inicial do mapa
    # Centraliza se houver um filtro ativo e resultados, caso contrário mostra visão geral
    if (cidade_selecionada and cidade_selecionada != "Todas") or \
       (porte_selecionado and porte_selecionado != "Todas"):
        if dados_filtrados:
            # Centraliza no primeiro resultado do filtro
            map_location = [dados_filtrados[0]["lat"], dados_filtrados[0]["lon"]]
            # Ajusta o zoom se apenas uma cidade/localização for exibida
            map_zoom = 10 if len(dados_filtrados) == 1 else 6 
        else:
            # Se o filtro não retornar resultados, mostra visão geral
            map_location = [-15.77777, -47.7777]
            map_zoom = 4
    else:
        # Visão geral padrão se nenhum filtro estiver ativo
        map_location = [-15.77777, -47.7777]
        map_zoom = 4

    mapa = folium.Map(location=map_location, zoom_start=map_zoom)
    
    for local in dados_filtrados:
        folium.Marker(
            location=[local["lat"],local["lon"]],
            popup=f"{local['nome']} ({local['porte']})", # Mostra nome e porte no popup
            tooltip=local["nome"]
        ).add_to(mapa)
        
    return render_template(
        'index.html', 
        mapa=mapa._repr_html_(), 
        cidades=cidades, 
        portes=portes,
        cidade_selecionada=cidade_selecionada or "Todas",
        porte_selecionado=porte_selecionado or "Todas" 
    )

if __name__ == "__main__":
    app.run(debug=True)
    