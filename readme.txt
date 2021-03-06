README

Autorzy:
	Christian Konopczyński, nr indeksu: 293 126
    	Wojciech Maciejewski, nr indeksu: 293 143

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
    python program.py -help - wyświetlenie listy możliwych parametrów i krótkie objaśnienie.
    python program.py 1 file.npz - rozwiązanie wszystkich map w pliku uprzednio tam zamieszczonych za pomocą numpy.savez("file.npz", ...)
    python program.py 2 [n] [width length] [gdp] [fnp] - rozwiązanie n map o wielkości width x length wygenerowanych przez program na podstawie
            dodatkowych parametrów: gdp - good direction probability, fnp - floor noise probability
        Domyślne wartości parametrów: n = 1, width = 10, height = 10, gdp = 0.5, fnp = 0.7
		Ograniczenia: 2 <= width, height <= 100, min_size != 2 i max_size != 2 (jednocześnie)
		0.0 <= gdb <= 1.0, 0.0 <= fnp <= 1.0
		Dodatkowo: Jeśli width == 'random' lub width == 'r', to wartość width jest dla każdej mapy losowana z przedziału [3, 100]. 
			Analogicznie dla height == 'random' lub height == 'r'
        Przy zwracaniu wyniku w oddzielnym oknie wyświetlana jest mapa magazynu reprezentowana za pomocą kolorowanych kwadratów.
    python program.py 3 [n] [min_size max_size] [gdp] [fnp] - rozwiązanie n map o wielkościach interplowanych liniowo między min_size x min_size, a max_size x max_size
		    wygenerowanych przez program na podstawie dodatkowych parametrów: gdp - good direction probability, fnp - floor noise probability.
	    Na wyjściu pokazuje tabelkę zgodną z wymaganiami.
        Domyślne wartości parametrów: n = 1, min_size= 3, max_size = 100, gdp = 0.5, fnp = 0.7
	    Ograniczenia: 2 <= min_size, max_size <= 100, min_size < max_size, min_size != 2 i max_size != 2 (jednocześnie)
							0.0 <= gdb <= 1.0, 0.0 <= fnp <= 1.0

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
    >>> np.savez("file.npz", a=a, b=b) # Zapisuje obie mapy do pliku file.npz

Metoda rozwiązania:
	Zaimplementowane zostały dwa algorytmy: jeden służący do generowania problemu, drugi służący do jego rozwiązania.
    Algorytm rozwiązujący problem bazuje na algorytmie grafowym A* z funkcją heurystyczną stworzoną na podstawie metryki miejskiej.

Pliki źródłowe i najważniejsze elementy:
    map_generation.py:
	    generate_map(width, height, good_direction_prob=0.5, floor_noise_prob=0.7) - funkcja generująca mapy o zadanych właściwościach
	    visualize_field(field) - funkcja rysująca na ekran zadaną mapę
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

Decyzje projektowe:
	Zadana wielkość mapy do wygenerowania (2-gi tryb uruchomienia) musi mieć wielkość co najmniej 3 pola
	i nie może być planszą kwadratową o boku 2 (żeby mogła być możliwa do przejścia),
	dodatkowo szerokość i wysokość muszą być mniejsze lub równe 100.
 
