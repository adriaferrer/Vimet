import pandas as pd
from scipy.spatial.distance import pdist, squareform


def group_tags(df):
    """
    Adds a Series to a data frame with new food categories based on nutritional grouping
    :param df: (DataFrame) df with the food items. It must contain a feature named 'tags' with the main food description
    :return: New data frame with the group tags added as a new feature
    """

    # We create a dicitonary classifying all the items
    dict_tags = {'Dulces': ['Obleas', 'Chocolate'],
                 'Patata': ['Patata'],
                 'Carne roja': ['Ternera', 'Confit', 'Magret', 'Vaca', 'Filet', 'Solomillo', 'Entrecot'],
                 'Carne procesada': ['Jamón', 'Croquetas', 'Bull', 'Lasagna', 'Chorizo', 'Sumaia', 'salchichón',
                                     'Mortadela', 'Albóndigas', 'Librito', 'Butifarra', 'Salchichas', 'Canelones',
                                     'Fuet', 'Espectec', 'Sobrasada', 'Bull'],
                 'Carne blanca': ['Pollo', 'Pavo', 'Conejo', 'Cerdo', 'Codorniz', 'Costillas'],
                 'Pescado': ['Mero', 'Bonito', 'Merluza', 'Salmón', 'Dorada', 'Mejillón', 'Lubina', 'Calamar', 'Sepia',
                             'Caballa', 'Lenguado', 'Almejas', 'Rape', 'Salmonetes', 'Boquerones', 'Berberechos',
                             'Atun',
                             'Gamba', 'Sardina', 'Pescadilla'],
                 'Huevos': ['Huevos', 'Revuelto', 'Tortilla'],
                 'Legumbres': ['Garbanzo', 'Lenteja', 'Judía', 'Montgeta', 'Alubia', 'Frijoles', 'Azuki', 'Hummus'],
                 'Lácteos': ['Queso', 'Yogures'],
                 'Especias': ['Eneldo', 'Ajo', 'Picantón'],
                 'Frutos secos': ['Nuez', 'Almendra', 'Macadamia', 'Avellana', 'Cacahuetes', 'Pasa', 'Dátiles',
                                  'Anacardo', 'Pistacho', 'Orejones'],
                 'Frutas': ['Plátano', 'Manzana', 'Fresón', 'Naranja', 'Pera', 'Kiwi', 'Paraguayo', 'Mango',
                            'Chirimoya',
                            'Kakis', 'Ciruela', 'Mandarina', 'Melocotón', 'Piña', 'Arándanos', 'Limón', 'Bananas',
                            'Albaricoque', 'Granada', 'Higos', 'Cerezas', 'Frambuesas', 'Sandía', 'Nectarina', 'Pomelo',
                            'Uva', 'Melón', 'Paraguayo'],
                 'Verduras': ['Tomate', 'Cebolla', 'Calabacín', 'Zanahoria', 'Pimiento', 'Aguacate', 'Brócoli',
                              'Lechuga',
                              'Berenjena', 'Calçots', 'Escarola', 'Cogollos', 'Calabaza', 'Acelgas', 'Espinacas',
                              'Puerro',
                              'Endivias', 'Rúcula', 'Alcachofa', 'Esparrago', 'Pepino', 'Canónigos', 'Ensalada',
                              'Coliflor',
                              'Col', 'Apio'],
                 'Cereales': ['Granola', 'Soja', 'Mijo', 'Avena', 'Quinoa', 'Arroz', 'Pan', 'Macarrones', 'Pasta',
                              'Spaghetti', 'Cous-cous', 'Espaguetis'],
                 'Aceite': ['Aceite'],
                 'Others': ['Cep', 'Agua', 'Salsa', 'Girgola', 'Champiñón', 'Caldo', 'Shiitake', 'Rossinyol', 'Others',
                            'Cesta']}

    # We reverse (keys for values), the dictionary so that we can easily assign it to a new series.
    dict_tags2 = {}

    for key, values in dict_tags.items():
        for value in values:
            dict_tags2[value] = key

    # We create a new Series with the 'group tags'
    df['group_tags'] = df['tags']
    df['group_tags'] = df['group_tags'].map(dict_tags2)
    return df


def matrix_best_items(df, tag_list):
    """
    Creates a matrix with the relative frequency a pair of items appear together in all the orders those items appear
    :param df: (DataFrame) df with the food items. It must contain a feature named 'tags' with the main food description
    and a feature named 'Name' with the order id.
    :param tag_list: (list) list of tags that will appear in the matrix
    :return: DataFrame with the items as index and columns and the relative frequency as values.
    """
    # We create a list with all the items we have
    all_tags = tag_list

    # This will be the matrix to store the results
    tag_matrix = []

    # We iterate through the list of items
    for tag_n in all_tags:
        tag_row = []

        # We find the id's of the orders where this item appears
        names_n = list(df[df['tags'] == tag_n]['Name'])
        # For each element, we iterate through all the elements
        for tag_m in all_tags:
            # We find the id's of the orders where this second item appears
            names_m = list(df[df['tags'] == tag_m]['Name'])
            # We calculate the relative frequency of the second item over the times the first item apears
            value = len(set(names_n).intersection(set(names_m))) / len(set(names_n).union(set(names_m)))
            tag_row.append(value)
        tag_matrix.append(tag_row)

    matrix = pd.DataFrame(tag_matrix, columns=all_tags)
    matrix['item'] = all_tags
    matrix = matrix.set_index('item')
    return matrix


def food_matrix(df):
    # We create a list with all the items we have
    tags = list(df['tags'].unique())
    # This will be the matrix to store the results
    matrix = []
    # We iterate through the list of items
    for tag_n in tags:
        row = []

        # We find the id's of the orders where this item appears
        names_n = list(df[df['tags'] == tag_n]['Name'])
        # For each element, we iterate through all the elements
        for tag_m in tags:

            # We find the id's of the orders where this second item appears
            names_m = list(df[df['tags'] == tag_m]['Name'])
            # We calculate the relative frequency of the second item over the times the first item apears
            value = len(set(names_n).intersection(set(names_m)))/len(set(names_n).union(set(names_m)))
            row.append(value)
        matrix.append(row)
    matrix = pd.DataFrame(matrix, columns=tags)
    matrix['item'] = tags
    matrix = matrix.set_index('item')
    return matrix


def user_recommender(df, level, customer_id):
    """
    Provides the similar customers based on the items bought
    :param df: (DataFrame) Register of items bought. The features 'Vendor', 'tags', 'Customer' and 'Lineitem quantity
    are required.
    :param level: (int) level of similarity 1 is the closest and above 3 the similarity is no better than random
    :param customer_id: (int) Customer id reference to find similarities from
    :return: (list) customer id's with the level of similarity provided
    """
    # Drop outliers
    df = df[df['Vendor'] != 'Gran Recapte']
    df = df[df['tags'] != 'Cesta']

    # Build similarity matrix
    rec = df.groupby(['Customer', 'tags']).sum()[['Lineitem quantity']]
    df_pivot = rec.pivot_table(index='tags', columns='Customer', values='Lineitem quantity').fillna(0)
    similarity_matrix = squareform(pdist(df_pivot.T, 'cosine'))
    similarity_df = pd.DataFrame(similarity_matrix, index=df_pivot.columns, columns=df_pivot.columns)

    # Filter by level of similarity
    result = similarity_df[similarity_df >= ((level-1)/10)]
    result = result[result < level/10]

    # Return the list or orders without the order provided
    return list(result[result[customer_id] >= 0][customer_id].index)


def items_for_you(df, similar_users, main_user):
    """
    Provides items that a customer never bought but is could like to buy as similar clients bought them previously
    :param df:(DataFrame) Register of items bought. The features  'tags' and 'Customer' and are required.
    :param similar_users: (list) id's of the similar users
    :param main_user: Customer id reference to find similarities from
    :return: (set) items the reference customer would buy
    """
    set_main = set(df[df['Customer'] == main_user]['tags'])
    for user in similar_users:
        items = []
        if user != main_user:
            set_user = set(df[df['Customer'] == user]['tags'])
            items = set_main - set_user
    if len(items) > 0:
        return items
    else:
        return 'There is nothing to recommend'
