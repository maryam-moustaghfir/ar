# application/views.py
import os
import pandas as pd
from django.shortcuts import render
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import plotly.express as px

#-------------------------------aymen-------------------------
def index(request):
    return render(request,"index.html")
def datatables(request):
    return render(request,"datatables.html")
def classement(request):
    return render(request,"classement.html")
def dashboard(request):
    return render(request,"dashboard.html")
def prediction(request):
    return render(request,"prediction.html")
#-------------------------------aymen-------------------------


def display_data(request):
    chemin_absolu = os.path.join(os.getcwd(), 'data', 'C:\\Users\\Maryam\\Downloads\\archi-main\\data\\final.xlsx')
    donnees_excel = pd.read_excel(chemin_absolu)

    # Obtenir la liste des pays uniques
    countries = donnees_excel['country_name'].unique()

    if request.method == 'POST':
        selected_country = request.POST.get('selected_country')
        selected_category = request.POST.get('selected_category', 'Films')  # Par défaut, sélectionner Films

        # Filtrer les données pour le pays et la catégorie sélectionnés
        filtered_data = donnees_excel[(donnees_excel['country_name'] == selected_country) & (donnees_excel['category'] == selected_category)].head(10)
        data = filtered_data.to_dict(orient='records')
    else:
        # Par défaut, afficher les 10 premières lignes de données pour le premier pays et la catégorie Films
        default_country = countries[0]
        default_data = donnees_excel[(donnees_excel['country_name'] == default_country) & (donnees_excel['category'] == 'Films')].head(10)
        data = default_data.to_dict(orient='records')

    return render(request, 'display_data.html', {'data': data, 'countries': countries})


# Définir une palette de couleurs personnalisée inspirée du style Netflix
netflix_colors = ['#E50914', '#B9090B', '#8A8A8A', '#000000', '#FFFFFF', '#F5F5F1']

def create_bar_chart(data, x_col, y_col, y_label, title):
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        labels={'y': y_label},
        title=title,
        color_discrete_sequence=netflix_colors  # Utiliser la palette de couleurs personnalisée
    )

    # Désactiver le zoom et le déplacement (pan)
    fig.update_layout(
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',
        font=dict(color='#FFFFFF'),  # Changer la couleur du texte du titre en blanc
        showlegend=False  # Masquer la légende (si nécessaire)
    )

    # Convertir le graphique en format HTML
    plot_html = fig.to_html(full_html=False)

    return plot_html

def dash(request):
    # Étape 1 : Charger les données depuis le fichier CSV
    data = pd.read_csv('netflix_titles.csv')

    # Étape 2 : Filtrer les données par type (TV Show ou Movie)
    tv_shows = data[data['type'] == 'TV Show']
    movies = data[data['type'] == 'Movie']

    # Étape 3 : Obtenir les 10 pays avec le plus grand nombre de séries télévisées
    top_10_tv_show_countries = tv_shows['country'].value_counts().head(10)

    # Étape 4 : Obtenir les 10 pays avec le plus grand nombre de films
    top_10_movie_countries = movies['country'].value_counts().head(10)

    # Étape 5 : Créer des graphiques avec Plotly Express en utilisant la palette de couleurs personnalisée
    plot_tv_shows_html = create_bar_chart(
        top_10_tv_show_countries,
        x_col=top_10_tv_show_countries.index,
        y_col=top_10_tv_show_countries.values,
        y_label='Number of TV Shows',
        title='Top 10 Countries with Most TV Shows'
    )

    plot_movies_html = create_bar_chart(
        top_10_movie_countries,
        x_col=top_10_movie_countries.index,
        y_col=top_10_movie_countries.values,
        y_label='Number of Movies',
        title='Top 10 Countries with Most Movies'
    )

    # Étape 6 : Compter le nombre de TV Shows et de Films
    count_by_type = data['type'].value_counts()

    # Étape 7 : Créer un graphique secteur avec Plotly Express en utilisant la palette de couleurs personnalisée
    fig_pie = px.pie(
    count_by_type,
    labels=count_by_type.index,
    values=count_by_type.values,
    title='Percentage of TV Shows and Movies on Netflix',
    color_discrete_sequence=netflix_colors,  # Utiliser la palette de couleurs personnalisée
    names=count_by_type.index)  # Ajouter une légende en utilisant les noms des catégories


    # Désactiver le zoom et le déplacement (pan)
    fig_pie.update_layout(
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',
        font=dict(color='#FFFFFF')  # Changer la couleur du texte du titre en blanc
    )

   
    # Étape 8 : Créer le Word Cloud des titres Netflix
    titles_text = ' '.join(data['title'].dropna())  # Concaténer tous les titres en un seul texte
    wordcloud = WordCloud(
        background_color='black',
        width=800,
        height=400,
        colormap='Reds',  # Choose a color map that matches the Netflix theme
        collocations=False,  # Disable grouping of frequent words
    ).generate(titles_text)


    # Convertir le Word Cloud en image
    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    # Construire la balise HTML pour l'image
    wordcloud_html = f'<img src="data:image/png;base64, {img_str}" alt="Word Cloud">'
    
    # Étape 9 : Créer un graphique horizontal avec les pourcentages de TV Shows et Movies
    fig_horizontal = px.bar(
        x=[count_by_type['TV Show'], count_by_type['Movie']],
        y=['TV Show', 'Movie'],
        orientation='h',
        text=[f"{int(count_by_type['TV Show'] / len(data) * 100)}%",
              f"{int(count_by_type['Movie'] / len(data) * 100)}%"],
        labels={'x': 'Percentage'},
        color_discrete_sequence=netflix_colors
    )

    # Désactiver le zoom et le déplacement (pan)
    fig_horizontal.update_layout(
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',
        font=dict(color='#FFFFFF'),  # Changer la couleur du texte
        bargap=0,  # Supprimer les lignes verticales blanches entre les barres
    )

    # Convertir le graphique horizontal en format HTML
    fig_horizontal_html = fig_horizontal.to_html(full_html=False)

    
        # ...

    # Étape 10 : Créer un graphique horizontal avec les pourcentages de TV Shows et Movies pour les top 10 pays
    top_countries_data = pd.DataFrame({
        'country': top_10_tv_show_countries.index,
        'TV Show': top_10_tv_show_countries.values / len(tv_shows) * 100,
        'Movie': top_10_movie_countries.values / len(movies) * 100,
    })

    fig_horizontal_top_countries = px.bar(
        top_countries_data.melt(id_vars='country', var_name='type', value_name='percentage'),
        x='percentage',
        y='country',
        orientation='h',
        text=top_countries_data.melt(id_vars='country', var_name='type', value_name='percentage')['percentage'].apply(lambda x: f"{int(x)}%"),
        color='type',
        color_discrete_map={'TV Show': netflix_colors[0], 'Movie': netflix_colors[1]},
        category_orders={'country': top_10_tv_show_countries.index},
        labels={'percentage': 'Percentage'},
        height=400,
        width=800,
    )

    # Désactiver le zoom et le déplacement (pan)
    fig_horizontal_top_countries.update_layout(
    plot_bgcolor='#303030',  # Couleur de fond du graphique
    paper_bgcolor='#303030',
    font=dict(color='#FFFFFF'),  # Changer la couleur du texte
    bargap=0,  # Supprimer les lignes verticales blanches entre les barres
    margin=dict(t=0, b=0, l=0, r=0),  # Adjust the left and right margins to shift the chart
    showlegend=False,  # Hide legend
)

    # Désactiver les lignes de la grille verticale
    fig_horizontal_top_countries.update_xaxes(showgrid=False)

    # Ajouter un titre
    fig_horizontal_top_countries.update_layout(title='Percentage of TV Shows and Movies in Top 10 Countries on Netflix')

    # Ajouter une légende avec un titre
    fig_horizontal_top_countries.update_layout(legend_title_text='Type')

    # Convertir le graphique horizontal pour les top 10 pays en format HTML
    fig_horizontal_top_countries_html = fig_horizontal_top_countries.to_html(full_html=False)

    total_tv_shows_count = len(tv_shows)
    total_movies_count = len(movies)

    #----------------------------------------------------------------
    
        
   

    # Compter le nombre de films ou émissions par catégorie d'âge
    rating_counts = data['rating'].value_counts()

    # Créer un diagramme circulaire avec des sections concentriques
    fig = px.pie(
        names=rating_counts.index,
        values=rating_counts.values,
        title='Distribution of Age Ratings on Netflix',
        hole=0.4,  # Contrôle le rayon du trou central (plus petit => sections concentriques)
        color_discrete_sequence=netflix_colors,  # Utiliser la palette de couleurs personnalisée
    )

    # Désactiver le zoom et le déplacement (pan)
    fig.update_layout(
        plot_bgcolor='#303030',  # Couleur de fond du graphique
        paper_bgcolor='#303030',
        font=dict(color='#FFFFFF'),  # Changer la couleur du texte du titre en blanc
    )

    # Convertir le graphique en format HTML
    fig_html = fig.to_html(full_html=False)

    # Mettre à jour le graphique HTML
    fig_html = fig.to_html(full_html=False)



    #-----------------------------------------------------------


    # Transmettre les données et les graphiques à la page HTML
    context = {
        'plot_tv_shows': plot_tv_shows_html,
        'plot_movies': plot_movies_html,
        'plot_pie': fig_pie.to_html(full_html=False),
        'wordcloud': wordcloud_html,
        'plot_horizontal': fig_horizontal_html,
        'plot_horizontal_top_countries': fig_horizontal_top_countries_html,
        'total_tv_shows_count': total_tv_shows_count,  # Ajouter cette ligne
        'total_movies_count' : total_movies_count,
        'age_rating_pie_chart': fig_html,

    }

    return render(request, 'dash.html', context)


