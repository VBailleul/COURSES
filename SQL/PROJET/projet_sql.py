import mysql.connector
from mysql.connector import Error

def continent_data(continent):
    try:
        # Connexion à la db
        connection = mysql.connector.connect(
            host='localhost',
            database='world',
            user='bailleul',
            password='Victor76**'
        )

        # Création du curseur
        cursor = connection.cursor()

        # Procédure "continent"
        cursor.callproc('continent', [continent])
        for result in cursor.stored_results():
            records = result.fetchall()
            countries = []
            for record in records:
                countries.append(record[0])

        filename = f'{continent}.html'
        with open(filename, 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f'<title>{continent}</title>\n')
            f.write('</head>\n')
            f.write('<body>\n')

            f.write(f'<h1> Projet SQL: Données "{continent}" </h1>\n')

            for country in countries:
                # Procédure 'pays'
                cursor.callproc('pays', [country])
                for result in cursor.stored_results():
                    records = result.fetchall()
                    cities = []
                    for record in records:
                        cities.append(record[0])

                f.write(f'<h2>{country}</h2>\n')
                f.write('<ul>\n')

                for city in cities:
                    # Procédure 'ville'
                    cursor.callproc('ville', [city])
                    for result in cursor.stored_results():
                        records = result.fetchall()
                        for info in records:
                            f.write('<li>\n')
                            f.write(f'{info[1]} ({info[2]}), {info[3]} - {info[4]} habitants\n')
                            f.write('</li>\n')

                f.write('</ul>\n')

            f.write('</body>\n')
            f.write('<footer>\n')
            f.write("<p> Victor BAILLEUL, 2023\n")
            f.write('</footer>\n')
            f.write('</html>\n')

        # Fin de connexion
        connection.close()

    except Error as e:
        print('Error:', e)


# Un petit essai avec le continent "Africa"

continent_data('Africa')


