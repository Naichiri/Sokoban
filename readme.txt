README

Autorzy:
	Christian Konopczyński
    	Wojciech Maciejewski

Treść projektu:
	Zbliża się koniec zmiany w hurtowni. Wszyscy pracownicy poszli już do domu, a ostatni z nich zorientował się,
    iż ktoś pozostawił w magazynie paczkę, która nie została umieszczona na odpowiednim regale.
    Pracownik musi zatem w jak najkrótszym czasie umieścić paczkę na właściwym miejscu. Paczka jest ciężka,
    zatem trzeba ją pchać po podłodze, zaś magazyn zastawiony regałami, pomiędzy którymi trzeba się przemieszczać.
    Dany jest pełny plan magazynu w postaci tablicy dwuwymiarowej n x m (gdzie 1 =< n,m =< 100),
    gdzie pojedynczy element tablicy może przyjmować następujące wartości:
        0 - pusta podłoga (pole) magazynu,
        1 - regał,
        2 - startowa pozycja paczki,
        3 - startowa pozycja pracownika,
        4 - docelowa pozycja paczki.
    Pracownik może poruszać się po wszystkich pustych polach magazynu, w jednym kroku o jedno pole,
    w czterech kierunkach (góra, dół, prawo, lewo), jeśli stoi obok paczki to może ją przesunąć.
    Zaproponuj algorytm, który obliczy minimalną liczbę kroków potrzebną by paczka znalazła się na pozycji docelowej.

Sposoby uruchomienia programu:
	Program działa poprzez uruchomienie wynikowego pliku z dodatkowymi parametrami.
    Wszystkie możliwe opcje i ich objaśnienie:
    program -help - wyświetlenie listy możliwych parametrów i krótkie objaśnienie.
    program 1 file.npz - rozwiązanie wszystkich map w pliku uprzednio tam zamieszczonych za pomocą numpy.savez("file.npz", ...)
    program 2 [n] [width length] [gdp] [fnp] - rozwiązanie n map o wielkości width x length wygenerowanych przez program na podstawie
                                                dodatkowych parametrów: gdp - good direction probability, fnp - floor noise probability
                                                Domyślne wartości parametrów: n = 1, width = 10, length = 10, gdp = 0.5, fnp = 0.7

Dane wejściowe:
	Program akceptuje pliki .npyz z danymi testowymi, utworzone za pomocą numpy.savez(file, ...).
    Format danych testowych to numpy.array stworzony z dwuwymiarowej listy,
    zawierającej liczby w zakresie od 0 do 4 włącznie (według oznaczeń z treści zadania).
    Przykładowy sposób przygotowania danych do testów za pomocą interpretera Python:
    >>> import numpy as np
    >>> a = np.array([[3, 4, 0, 0],
    ...               [0, 1, 0, 0],
    ...               [0, 0, 2, 0],
    ...               [0, 0, 0, 0]])
    >>> b = np.array([[1, 4, 2, 3]])
    >>> np.savez("file.npz", a=a, b=b)

Metoda rozwiązania:
	Zaimplementowane zostały dwa algorytmy: jeden służący do generowania problemu, drugi służący do jego rozwiązania.
    Algorytm rozwiązujący problem bazuje na algorytmie grafowym A* z funkcją heurystyczną stworzoną na podstawie metryki miejskiej.

Pliki źródłowe i najważniejsze elementy:
    map_generation.py:
        #TODO
    program.py:
        Program - klasa zawierająca metody dotyczące sposobów uruchomienia programu
        print_output(solve_output) - funkcja wypisująca wynik wykonania algorytmu w przejrzystej postaci
    search.py:
        Action - typ wyliczeniowy określający ruch pracownika
        State - klasa zawierająca zmieniające się parametry problemu
        Problem - klasa zawierająca niezmienne parametry problemu oraz metody na nich działające
        Node - klasa zawierająca pola wymagane przy tworzeniu grafu do przemierzania dla algorytmu A*
        search(problem) - funkcja tworząca graf i przemierzająca go dla danego problemu, w celu znalezienie optymalnego rozwiązania,
                            zwraca dane potrzebne do dalszej analizy implementacji algorytmu
    sokoban.py:
        solve(field) - funkcja tworząca obiekt klasy Problem dla danej planszy, 
    utils.py:
        zawiera wykorzystywane stałe oraz funkcje wspierające analizę danych
    map_generation.py:
	generate_map(width, height, good_direction_prob=0.5, floor_noise_prob=0.7) - funkcja generująca mapy o zadanych właściwościach
	visualize_field(field) - funkcja rysująca na ekran zadaną mapę
	
