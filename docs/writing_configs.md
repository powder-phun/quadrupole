# Tworzenie plików konfiguracyjnych

## Skrócony opis formatu JSON

Pliki konfiguracyjne mają format JSON. [Specyfikacja](https://www.json.org/json-en.html). W skrócie,
w formacie json występują dwa elementy: obiekty ("{}") i listy ("[]").
Obiekt to zbiór kluczy i odpowiadającym im wartości rozdzielonych dwukropkiem ":", np:

```json
{
  "enabled": true,
  "name": "Quadrupole",
  "age": 18,
}
```

Klucze muszą zawierać się w cudzysłowach i być wartościami tekstowymi.
Wartość może być liczbą, tekstem, wartością true/false, bądź innym obiektem lub listą.
Wartości tekstowe muszą zawierać się w cudzysłowie.
Lista to uporządkowany zbiór wartości, np:

```json
[
  "First",
  "Second",
  3,
  True,
  {
    "name": "jan"
  },
]
```

Podobnie jak w przypadku obiektu, każda wartość w liście może być liczbą, tekstem, itp.

Po każdym elemencie w liście lub obiekcie musi znaleźć się przecinek!.

## Konstrukcja pliku konfiguracyjnego

Każdy plik konfiguracyjny zawiera jeden obiekt JSON. W obiekcie musi znaleźć się lista kontrolerów "controllers"
i opcjonalnie obiekt "defaults":

```json
{
  "controllers": [
    ...
  ],
  "defaults": {
    ...
  },
}
```

Kontroler to inaczej pojedyncze urządzenie pomiarowe np: multimetr, system EuroMeasure, próżniomierz.
Każdy kontroler musi zawierać pole typu "type" definiujące rodzaj urządzenia, np. "HP34401A" oraz listę parametrów
jakie chcemy obsługiwać: "params". Parametry i dostępne kontrolery opisane są dalej. Poza nimi może zawierać opcjonalne elementy konfigurujące urządzenie i połączenie z nim.

```json
{
    "type": "HP34401A",
    "ip": "169.254.100.30",
    "speed": "Slow",
    "params": [
        {
            "type": "VDC",
            "name": "Voltage",
        }
    ]
},

```

## Dostępne kontrolery
