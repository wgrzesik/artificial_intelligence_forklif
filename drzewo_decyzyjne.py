import graphviz
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

def make_tree():
    plikZPrzecinkami = open("training_data.txt", 'w')

    with open('DecisionTree/200permutations_table.txt', 'r') as plik:
        for linia in plik:
            liczby = linia.strip()
            wiersz = ""
            licznik = 0
            for liczba in liczby:
                wiersz += liczba
                wiersz += ";"
            wiersz = wiersz[:-1]
            wiersz += '\n'
            plikZPrzecinkami.write(wiersz)

    plikZPrzecinkami.close()

    x = pd.read_csv('DecisionTree/training_data.txt', delimiter=';',
                    names=['wielkosc', 'waga,', 'priorytet', 'ksztalt', 'kruchosc', 'dolna', 'gorna', 'g > d'])
    y = pd.read_csv('DecisionTree/decisions.txt', names=['polka'])


    # Tworzenie instancji klasyfikatora ID3
    clf = DecisionTreeClassifier(criterion='entropy')

    # Trenowanie klasyfikatora
    clf.fit(x.values, y.values)

    # Zapis drzewa do pliku
    joblib.dump(clf, 'DecisionTree/wyuczone_drzewo.pkl')

    return clf


def stworz_plik_drzewa_w_pdf(clf, feature_names, class_names):
    # Wygenerowanie pliku .dot reprezentującego drzewo
    dot_data = export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=class_names, filled=True,
                               rounded=True)
    # Tworzenie obiektu graphviz z pliku .dot
    graph = graphviz.Source(dot_data)

    # Wyświetlanie drzewa
    graph.view()