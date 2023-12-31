import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def monte_carlo_brownian_motion(n_steps):
    # Początkowe położenie cząsteczki
    x = 0
    y = 0

    # Lista przechowująca położenia cząsteczki po każdym kroku
    x_positions = [x]
    y_positions = [y]

    for _ in range(n_steps):
        # Generowanie losowego kąta w radianach <0, 2pi>
        angle = np.random.uniform(0, 2 * np.pi)

        # # Generowanie losowej długości kroku
        # step_length = np.random.normal(0, 1)

        # Aktualizacja położenia cząsteczki
        x += np.cos(angle)
        y += np.sin(angle)

        # Zapisanie aktualnego położenia
        x_positions.append(x)
        y_positions.append(y)

    return (x_positions, y_positions)


def displacement_vector(x_positions, y_positions):
    # Obliczenie wektorów przesunięcia dla każdego kroku
    displacements = []
    for i in range(len(x_positions)):
        displacements.append(np.sqrt(x_positions[i] ** 2 + y_positions[i] ** 2))

    return displacements


def save_to_excel(x_positions, y_positions, displacements, filename):
    # Tworzenie DataFrame z wynikami
    data = {
        "X": x_positions,
        "Y": y_positions,
        "Przesunięcie": list(
            displacements
        ),  # Dodanie 0 na początku dla równości długości list
    }  # Dodanie 0 na początku dla równości długości list
    df = pd.DataFrame(data)

    # Zapisanie do pliku Excel z użyciem openpyxl
    df.to_excel(filename, index=False, engine="openpyxl")


def plot_trajectory(x_positions, y_positions, steps, displacements):
    margin = {"bottom": 0.2, "top": 0.90}

    # Wykres trajektorii ruchu cząsteczki
    plt.figure(figsize=(10, 10), num="Trajektoria ruchu cząsteczki")
    plt.gcf().set_facecolor("#121212")

    plt.gcf().subplots_adjust(top=margin["top"], bottom=margin["bottom"])

    plt.plot(x_positions, y_positions, "w--", marker="o")
    plt.gca().set_facecolor("#181818")
    plt.gca().tick_params(colors="w")
    plt.gca().annotate(
        f"""
        Średnia długość wektora przesunięcia: {round(np.mean(displacements), 4)}
        
        Długość wektora przesunięcia po {steps} krokach: {round(displacements[-1],4)}

        """,
        xy=(0.5, 0.02),
        xycoords="figure fraction",
        color="w",
        fontsize=12,
        ha="center",
    )
    plt.title(
        f"Trajektoria ruchu cząsteczki po wykonaniu {str(steps)} kroków",
        color="w",
        fontdict={"fontsize": 20},
    )
    plt.xlabel("X", color="w")
    plt.ylabel("Y", color="w")

    plt.grid(True)
    # Zapisz wykres do pliku png
    plt.savefig("source\\Wykres.png")
    plt.show()


if __name__ == "__main__":
    while True:
        try:
            # Liczba kroków
            n_steps = int(input("\nPodaj liczbę kroków: "))
            break
        except ValueError:
            print("Podaj liczbę całkowitą!")
        except KeyboardInterrupt:
            print("Przerwano przez użytkownika!")
            exit(0)
        except:
            print("Wystąpił nieoczekiwany błąd!")
            exit(1)

    # Wywołanie funkcji Monte-Carlo
    x_positions, y_positions = monte_carlo_brownian_motion(n_steps)

    # # Obliczenie wektora przesunięcia ostatniego kroku
    # displacement = np.sqrt(((x_positions[-1] ** 2) + (y_positions[-1] ** 2)))
    displacements = displacement_vector(x_positions, y_positions)
    # Zapis do pliku Excel
    save_to_excel(x_positions, y_positions, displacements, "source\\brown.xls")

    print(
        f"""
-----------------------------------------------------

Długość wektora przesunięcia po {n_steps} krokach: {displacements[-1]}

------

Położenie cząsteczki po {n_steps} krokach: X = {x_positions[-1]} Y = {y_positions[-1]}

------

Średnia długość przesunięcia: {np.mean(displacements)}

-----------------------------------------------------
"""
    )

    # Wygenerowanie wykresu trajektorii
    plot_trajectory(x_positions, y_positions, n_steps, displacements)
