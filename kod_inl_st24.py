# Det här programmet analyserar och visualiserar data från CSV-filer.
# Programmet läser in KPI-data och data om varu- och tjänstegrupper,
# och presenterar resultaten i form av tabeller och diagram.


# Placera dina modulimpoter här:
import csv
import matplotlib.pyplot as plt

# Placera ev. funktioner som används i flera deluppgifter här:


def read_file(filnamn):
    """Öppnar och läser innehåll från en CSV-fil och returnerar detta som en lista av rader."""
    with open(filnamn, mode='r', encoding='UTF-8') as file:  # öppnar filen enligt angivet sätt för att kunna vara kompatibelt med csv filerna
        # läser av csv filen och har korrekt avgränsare, i det här fallet ett semikolon
        reader = csv.reader(file, delimiter=';')
        # Här konverterar vi filens innehåll till en lista. Det gör att det blir enklare att hantera sen
        data = [row for row in reader]
    return data  # Här returneras datan vi kommer använda i samtliga av de andra funktionerna. Den här uppgiften utgör dock, så att jag är tydlig, uppgift 1 a men den får ligga här

# Deluppgift 1: Funktioner från deluppgift 1 i ordning.


def task1():  # Det här är då egentligen uppgift 1)b men den används bara här och inte i hela filen vilket är varför den är separerad från 1 a.
    # Den här funktionen har vi för att läsa in filen kpi.csv. Den döper vi till KkpiData .Den ligger i samma folder som den här uppgiften vilket gör att jag kan skriva namnet direkt.
    kpiData = read_file('kpi2023.csv')
    # Den här gör samma som ovan fast med filen varutjanstegrupp. Den heter livsData
    livsData = read_file('Varutjanstegrupp.csv')
    # uppgiften bad oss printa de två första raderna. Print skriver ut och kpi data tar de två första raderna vi skapade i första funktionen o skriver ut.
    print("De två första raderna av kpiData är:", kpiData[:2])
    # samma som ovan fast för livsdata som kommer från varutjanstegrupp.
    print("De två första raderna av livsData är:", livsData[:2])

# Deluppgift 2: Funktioner från deluppgift 2 i ordning.


def plottaKPI(kpiData):
    # Be användaren ange vilka månader som ska analyseras så vi kan ta fram särskild data
    months_input = input(
        "Ange vilka månader som ska analyseras (ex: 1, 3, 5, 13): ")
    # ta användarens input och tolka den inmatningen som en lista av heltal. Det gör att vi kan välja rätt data. Vi kan ha heltal då kpi filen inte har floats
    months = [int(month.strip()) for month in months_input.split(',')]
    # tar år från datan så vi kan lägga dem på X-axeln enligt angivelse
    years = [int(row[0]) for row in kpiData[1:]]
    # Lägg till defenitioner på storlek så att vi kan läsa enklare och det ser snyggare ut.
    plt.figure(figsize=(10, 6))
    # loopa igenom månaderna för att kunna plotta specifik data baserat på vad användaren valt.
    for month in months:
        # Här kollar vi om intervallet är rimligt för att undvika fel. Vi kan t.ex. inte ha 17 månader.
        if month >= 1 and month <= 12:
            month_data = [float(row[month].replace(',', '.'))
                          # tar fram data från månaden och konverterar den så att det blir konsekvent
                          for row in kpiData[1:]]
            # plottar datan så vi kan se den.
            plt.plot(years, month_data, label=kpiData[0][month])
    # om användaren anger 13 (vilket är utanför det intervall vi angav ovan), så ska det inte bli fel utan då ska vi extrahera och konvertera årsmedel
    if 13 in months:
        annual_averages = [float(row[-1].replace(',', '.'))
                           for row in kpiData[1:]]
        # plottar årsmedelvärdet med lite annan stil så vi kan skilja dem från övrig data. Blir lite snyggare
        plt.plot(years, annual_averages, label="Årsmedel", linestyle='--')
    # Här märker vi x-axeln med år så man ska förstå att det är år som visas.
    plt.xlabel('År')
    # Vi märker y-axeln med kpi så man ska första att det är kpi som visas.
    plt.ylabel('Konsumentprisindex')
    # titeln på plotten är konsumenttprisindex år 1980-2023 för att likna det i uppgiften.
    plt.title('Konsumentprisindex År 1980-2023')
    # här lägger vi in en anvisning på vilka linjer det är som plottas så det blir tydligt. Den ser man i vänstra hörnet.
    plt.legend()
    # om vi inte hade den här hade inte plotten visats, så vi har den så att användaren kan se plotten.
    plt.show()

# Deluppgift 3: Funktioner från deluppgift 3 i ordning.


def varortjanster(livsData):
    # Meny tillagd för att ännu visa tydligt för användaren vilka val som finns.
    print('Varu-/tjänstegrupp \n', '1.   Livsmedel och alkoholfria drycker \n', '2.   Kläder och skor \n', '3.   boende \n',
          '4.   hälso- och sjukvård \n', '5.   post och telekommunikationer \n', '6.   rekreation och kultur \n', '7.   restauranger och logi')
    # Be användaren ange vilka grupper som ska analyseras
    groups_input = input("Vilka grupper? (ex: 1, 2): ")
    # Be användaren ange för vilka år analysen ska vara
    period_input = input("Vilka år? (ex: 1996-2004): ")

    # Här tolkar vi det användaren matade in för grupper och period
    groups = [int(x) for x in groups_input.split(',')]
    start_year, end_year = map(int, period_input.split('-'))

    # Tar år från data för att använda som x-axel i diagrammet
    years = [int(year) for year in livsData[0][1:]]

    # Kontrollera om de angivna åren ligger inom tillgängligt dataområde
    if start_year < years[0] or end_year > years[-1]:
        print(f"Åren måste vara mellan {years[0]} och {years[-1]}.")
        return

    # Hitta index som motsvarar start- och slutåren
    start_index = years.index(start_year)
    end_index = years.index(end_year) + 1  # +1 för att inkludera slutåret

    # Justerar storleken på figuren för bättre läsbarhet
    plt.figure(figsize=(10, 6))

    for group in groups:
        group_name = livsData[group][0]
        values = [float(value.replace(',', '.'))
                  for value in livsData[group][1:]]

        # Filtrera datan så att den bara inkluderar åren inom det specificerade intervallet
        filtered_values = values[start_index:end_index]
        filtered_years = years[start_index:end_index]

        # Plottar bara den filtrerade datan
        plt.plot(filtered_years, filtered_values, label=group_name)

    # Märkning av x-axel och titel
    plt.xlabel('År')
    # Märkning av y-axel och titel
    plt.ylabel('Prisutvecklingen')
    # Titel för hela diagrammet, dynamisk inkorporering av start year och end year för att titel ska matcha de angivna åren
    plt.title(f'Prisindexutveckling olika kategorier av varor och tjänster år {
              start_year}-{end_year}')
    # Visar en legend som beskriver varje linje
    plt.legend()
    # Visar ett rutnät i diagrammet för bättre läsbarhet
    plt.grid(True)
    # Visar diagrammet
    plt.show()

# Deluppgift 4: Funktioner från deluppgift 4 i ordning.


def ff(livsData):
    print('Varu-/tjänstegrupp \n', '1.   Livsmedel och alkoholfria drycker \n', '2.   Kläder och skor \n', '3.   boende \n',
          '4.   hälso- och sjukvård \n', '5.   post och telekommunikationer \n', '6.   rekreation och kultur \n', '7.   restauranger och logi')

  # användaren får välja varugrupp så vi kan ta ut den specifika datan
    group_input = input("Välj varugrupp (ex: 1): ")
    # här gör vi om det ovan angivna till en int då ovan bara tar in string och datan i csv är inte string.
    group = int(group_input)
    # tar ut gruppens namn för att visa i diagrammets titel så man förstår vad man tittar på. Koden blir också mer dynamisk på det här sättet.
    group_name = livsData[group][0]
    # konverterar datan till float eftersom att det förekommer floats i csv filen. Gör vi inte det får vi fel i programmet.
    values = [float(value.replace(',', '.')) for value in livsData[group][1:]]
    change_factors = [(values[i] - values[i-1]) / values[i-1]
                      # beräknar förändringsfaktor för att visa procentuell förändring vöer tid.
                      * 100 for i in range(1, len(values))]
    years = range(1981, 2024)  # definierar tidsram för x-axeln
    # här skapas en barchart som kan visa förändringarna
    plt.bar(years, change_factors)
    # skriver x som titel på x för att tydliggöra samt för att uppgiften bad om det
    plt.xlabel('År')
    # Skriver förändringsfaktor på y för att tydliggöra samt för att uppgiften bad om det.
    plt.ylabel('Förändringsfaktor')
    # här är förändringsfaktor för kopplad till raden ovan som tog ut gruppen. Detta för att visa vad som analyseras.
    plt.title(f'Förändringsfaktor för {group_name} År 1980-2020')
    plt.grid(True)  # lägger till rutnät
    # visar grafen för användaren. Hade den inte funnits kan intet användaren se.
    plt.show()


# Deluppgift 5: Funktioner från deluppgift 5 i ordning.


def statistik(livsData):
    # Förbereder att lagra gruppnamn och statistikvärden.
    group_names = []
    max_values = []
    median_values = []
    mean_values = []

    # Gör det tydligt vad som visas
    print("Varu-/tjänstegrupp\t\t\tMax\t\tMedian\t\tMedelvärden")
    # Förbättrar läsbarheten.
    print("---------------------------------------------------------------------------")

    for row in livsData[1:]:  # loopa igenom varje rad i data för att gå ingemo alla grupper o skapa statistik. VI börjar från 1an för att inte ta med rubriken
        group_name = row[0]  # Används senare för att märka staplarna
        # Gör om värdena till floats då datan i csv är en float
        values = [float(value.replace(',', '.')) for value in row[1:]]

        highest = max(values)  # Identifierar toppvärdet
        # sorterar värdena för att hitta medianen sen
        sorted_values = sorted(values)
        n = len(sorted_values)  # Längden av de sorterade värdena
        if n % 2 == 0:
            # Här kollar jag om mägnden datapunkter är jämna för att kunna hantera det fall att man måste ta en genomsnittlig median
            median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            # Här kollar jag det fall att mängden datapunkter är udda och att man därmed kan hitta medianen direkt.
            median = sorted_values[n//2]
        # hittar medelvärde för att visa genomsnit.
        mean = sum(values) / len(values)

        # Lägger till beräknade värden för att kunna visa dem senare
        group_names.append(group_name)
        max_values.append(highest)
        median_values.append(median)
        mean_values.append(mean)
        # Skriver ut statistik för att visa beräknade värden i tabellformat. Linjen bättrar läsbarhet
        print(f"{group_name:30}\t{highest:10.2f}\t{
              median:10.2f}\t{mean:10.2f}")
        print("---------------------------------------------------------------------------")

    # Skapar index för varje grupp: Används för att placera staplarna korrekt.
    x = range(len(group_names))

    # initiera diagram med dimensionerna för att öka läsbarhet
    plt.figure(figsize=(12, 6))
    # Skapar staplar: Visar max-, median- och medelvärden med olika färger och bredder. Alpha inlagt för att justera genomskinlighet
    plt.bar(x, max_values, width=0.6, label='Maxvärde', color='b', alpha=0.5)
    plt.bar(x, median_values, width=0.4,
            label='Medianvärde', color='r', alpha=0.7)  # skapar igen staplar.
    plt.bar(x, mean_values, width=0.2,  # återigen skapar staplar
            label='Medelvärde', color='g', alpha=0.9)
    # rubrik på y enligt anvisning. Vi har ingen x den här gången då det inte var anvisat.
    plt.ylabel('Maxvärde, medianvärde och medelvärde')
    # titel på hela diagrammet enligt anvisat
    plt.title(
        'Maxvärde, medianvärde och medelvärde för varu-/tjänstegrupp år 1980-2023')
    # Justerar x-ticks för att visa gruppnamnen och roterar dem för bättre läsbarhet. Det var även anvisat som så. Då blir texten där nere lite sne.
    plt.xticks(x, group_names, rotation=45)
    # lägger till beskrivning av staplarna för att underlätta förståelse.
    plt.legend()
    # förhindrar att staplar överlappar. Annars blandar man lätt ihop data.
    plt.tight_layout()
    plt.show()  # visa diagrammet.

# Huvudprogram med Meny från deluppgift 0.


def main():
    while True:  # Här loopar vi "för alltid" tills det att användaren trycker avsluta. Annars hade vi avslutat efter ett kommando och det vill vi inte.
        # visar menyn med alternativ för anvädaren
        print("\n1. Visa KPI-data\n2. Plotta KPI\n3. Analysera varor och tjänster\n4. Beräkna förändringsfaktor\n5. Visa statistik\n6. Avsluta")
        # låter användaren skriva in vilket av de 6 alternativen den vill ha.
        val = input("Välj ett alternativ: ")
        if val == '1':
            task1()  # i det fall att användaren anger 1 så oberopas funktionen vi definerade i uppgift 1
        elif val == '2':  # anger användaren två läses uppgift 2 in. readfile är inlagd igen för att vara säkra att datan är tillgänglig
            kpiData = read_file('kpi2023.csv')
            plottaKPI(kpiData)
        # om användaren anger 3 åberopas uppgift 3. Vi har readfile för att säkerställa att datan är tillgänglig.
        elif val == '3':
            livsData = read_file('Varutjanstegrupp.csv')
            varortjanster(livsData)
        elif val == '4':  # om anvädaren anger 4 åberopas uppgift 4. Då har vi readfile för att säkerställa tillgänglighet
            livsData = read_file('Varutjanstegrupp.csv')
            ff(livsData)
        # anger användaren 5 så åberopas uppgift 5. Read file återigen för att säkerställa tillgänglighet.
        elif val == '5':
            livsData = read_file('Varutjanstegrupp.csv')
            statistik(livsData)
        elif val == '6':  # om användaren anger 6 så avslutar vi
            break
        else:  # skulle användaren ange något ogiligt såsom 7 så kommer vi att ge ett felmeddelande, annars kraschar programmet o det vill vi itne.
            print("Ogiltigt alternativ, försök igen.")


# Starta menyprogrammet
# här säkerställs att vårat script körs direkt för att starta menyn.
if __name__ == "__main__":
    main()  # main körs för att köra menyn.
