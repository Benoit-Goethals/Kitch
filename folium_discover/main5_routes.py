import webbrowser
import folium
from folium.plugins import AntPath
import random


def main():
    # Center of the map
    map_center = [50.8503, 4.3517]  # Center of Belgium (Brussels)
    m = folium.Map(location=map_center, zoom_start=8)

    # List of destinations (streetname, house_number, postcode, municipality, lat, lon)
    destinations = [
        ("Vogelkerslaan", 1, 2950, "Kapellen", 51.35115, 4.45248),
        ("Jozef Stormsstraat", 42, 2660, "Antwerpen", 51.18409, 4.35690),
        ("Lange Zavelstraat", 47, 2060, "Antwerpen", 51.22303, 4.42761),

        ("Uilenstraat", 13, 9100, "Sint-Niklaas", 51.18499, 4.16375),
        ("Wolterslaan", 127, 9040, "Gent", 51.04856, 3.75008),
        ("Boelenaar", 4, 9031, "Gent", 51.05297, 3.65608),

        ("Boudewijnlaan", 49, 8300, "Knokke-Heist", 51.34239, 3.28732),
        ("Brandstraat", 20, 9870, "Zulte", 50.94962, 3.50233),
        ("Wallestraat", 2, 9506, "Geraardsbergen", 50.77866, 3.97185),

        ("Bruggestraat", 103, 8830, "Hooglede", 50.98116, 3.09038),
        ("Geraniumlaan", 20, 8790, "Waregem", 50.88631, 3.41482),
        ("Langenbos", 4, 8791, "Waregem", 50.86413, 3.35023),

        ("Terheydestraat", 22, 1640, "Sint-Genesius-Rode", 50.73961, 4.35479),
        ("Félix Wittouckstraat", 43, 1600, "Sint-Pieters-Leeuw", 50.80714, 4.29064),
        ("Tongerlostraat", 4, 2380, "Ravels", 51.36464, 4.98818),

        ("Molenstraat", 58, 8800, "Roeselare", 50.94270, 3.11718),
        ("Larenstraat", 68, 3560, "Lummen", 51.00312, 5.18914),
        ("Kattenbos", 82, 1750, "Lennik", 50.83202, 4.15246),
        ("Lange Haagstraat", 60, 1700, "Dilbeek", 50.86155, 4.24110),
        ("Luciëndallaan", 36, 3800, "Sint-Truiden", 50.82742, 5.18163),
        ("Korte Lindenstraat", 17, 9300, "Aalst", 50.93993, 4.02011),
        ("Turnhoutsebaan", 197, 2970, "Schilde", 51.24123, 4.58379),
        ("Kruisbergstraat", 9, 9230, "Wetteren", 51.00564, 3.89330),
        ("Kwakkelstraat", 134, 1800, "Vilvoorde", 50.90842, 4.37956),
        ("Meldertsebaan", "1B", 3560, "Lummen", 50.99711, 5.14377),
        ("Eikenstraat", 3, 8530, "Harelbeke", 50.84002, 3.31102),
        ("Zonnelaan", 15, 8500, "Kortrijk", 50.83947, 3.27873),
        ("Vaartstraat", 25, 2340, "Beerse", 51.32382, 4.82949),
        ("Groot-Bijgaardenstraat", 368, 1601, "Sint-Pieters-Leeuw", 50.79041, 4.29206),
        ("Ganzenkoor", 43, 2570, "Duffel", 51.09292, 4.48953),
        ("Sparrenstraat", 3, 2020, "Antwerpen", 51.18433, 4.39251),
        ("Goorbaan", 59, 2230, "Herselt", 51.04939, 4.91743),
        ("Burgemeester Lemmensstraat", "40A", 9220, "Hamme", 51.06518, 4.15710),
        ("Grote Steenweg", 376, 3350, "Linter", 50.84911, 5.05648),
        ("Lijsterlaan", 55, 8790, "Waregem", 50.88085, 3.44504),
        ("Lindestraat", 19, 1785, "Merchtem", 50.91714, 4.28596),
        ("Veldstraat", 197, 9140, "Temse", 51.14068, 4.21996),
        ("Provenplein", 1, 8972, "Poperinge", 50.88943, 2.65798),
        ("Boezingestraat", 22, 8920, "Langemark-Poelkapelle", 50.91210, 2.92077),
        ("Fregatstraat", 14, 9000, "Gent", 51.08871, 3.72216),
        ("Sint-Katarinastraat", 177, 8310, "Brugge", 51.19779, 3.23708),
        ("Het Schoemeken", 3, 2970, "Schilde", 51.23916, 4.58671),
        ("O. L. Vrouwstraat", 203, 3570, "Alken", 50.90352, 5.26562),
        ("Leuvenselaan", 88, 3300, "Tienen", 50.81062, 4.92621),
        ("Kerkplein", 20, 3582, "Beringen", 51.05922, 5.27231),
        ("Merelstraat", 1, 9340, "Lede", 50.97011, 3.99596),
        ("Schoonzichtstraat", 4, 8670, "Koksijde", 51.11871, 2.63741),
        ("Bruggestraat", 245, 8770, "Ingelmunster", 50.93499, 3.25024),
        ("Louisastraat", 46, 3120, "Tremelo", 50.99954, 4.72241),
    ]

     # Add CircleMarkers for all destinations
    for idx, (street, house_number, postcode, municipality, lat, lon) in enumerate(destinations, start=1):
        random_color = random.choice(["red", "blue", "green", "purple", "orange"])  # Random color
        random_radius = random.randint(10, 20)  # Random radius
        folium.CircleMarker(
            location=[lat, lon],
            radius=random_radius,
            color=random_color,
            fill=True,
            fill_color=random_color,
            fill_opacity=0.3,
            tooltip=f"{street} {house_number}, {postcode} {municipality}",
        ).add_to(m)

    # Use only the first 10 destinations for the route
    selected_destinations_1 = destinations[:3]
    selected_destinations_2 = destinations[3:6]
    selected_destinations_3 = destinations[6:9]
    selected_destinations_4 = destinations[9:12]
    selected_destinations_5 = destinations[12:15]

    # Add AntPath for each group of selected destinations
    for selected_destinations in [
        selected_destinations_1,
        selected_destinations_2,
        selected_destinations_3,
        selected_destinations_4,
        selected_destinations_5,
    ]:
        ant_path = AntPath(
            locations=[[lat, lon] for _, _, _, _, lat, lon in selected_destinations],
            color="blue",
            weight=5,
            delay=1000
        )
        m.add_child(ant_path)



    # Save the map to HTML
    m.save("map_with_routes.html")
    print("Map with routes saved as 'map_with_routes.html'")


if __name__ == "__main__":
    main()
    webbrowser.open("map_with_routes.html")