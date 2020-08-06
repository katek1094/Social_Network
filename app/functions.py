from text_unidecode import unidecode



# this function takes people as an argument (in forat showed below) and a search phrase that was in the serach form field
def search_for_users(people, search):

    results = []

    # # pobieramy dane od użytkownika
    # search = input("im looking for:")
    #
    # # pobieramy dane z bazy danych
    # people = [
    #     {"id": 1, "first_name": "Mikołaj", "last_name": "Staniul"},
    #     {"id": 2, "first_name": "Adam", "last_name": "Głogowski"},
    #     {"id": 3, "first_name": "Franek", "last_name": "Borys"},
    #     {"id": 4, "first_name": "Ola", "last_name": "Melzacka"},
    #     {"id": 5, "first_name": "Kajetan", "last_name": "Jabłoński"},
    #     {"id": 6, "first_name": "Michał", "last_name": "Sawicki"},
    # ]

    # dajemy obydwa w lowercase i usuwamy polskie znaki
    search = unidecode(search.lower())
    lower_people = []
    for person in people:
        lower_person = dict()
        lower_person['id'] = person['id']
        lower_person["first_name"] = unidecode(person['first_name'].lower())
        lower_person['last_name'] = unidecode(person['last_name'].lower())
        lower_people.append(lower_person)
    people = lower_people

    # dzielimy search na części rozdielone spacjami
    search = search.split()

    # wykluczam więcej niż 3-częściowe żądanie
    if len(search) >= 3:
        return []

    # szukam dla każdej frazy (1 albo 2)
    first_names = []
    last_names = []
    for phrase in search:
        first_names.append([])
        last_names.append([])
        for person in people:
            result = person['first_name'].find(phrase)
            if result == 0:
                first_names[-1].append(person['id'])
            result = person['last_name'].find(phrase)
            if result == 0:
                last_names[-1].append(person['id'])

    # zapisuje do wyników
    if len(search) == 1:
        for x in first_names[0]:
            results.append(x)
        for x in last_names[0]:
            results.append(x)
    if len(search) == 2:
        first1 = set(first_names[0])
        last1 = set(last_names[0])
        first2 = set(first_names[1])
        last2 = set(last_names[1])
        for x in first1.intersection(last2):
            results.append(x)
        for x in last1.intersection(first2):
            results.append(x)
    results = list(set(results))

    return results




