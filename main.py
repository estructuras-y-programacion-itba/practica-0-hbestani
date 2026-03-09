import random
import csv
from collections import Counter

# --- FUNCIONES DE SOPORTE ---

def tirar_dados(cant):
    return [random.randint(1, 6) for _ in range(cant)]

def analizar_jugada(dados):
    counts = Counter(dados).values()
    # Para la escalera: ordenamos y quitamos duplicados
    caras = sorted(list(set(dados)))
    es_escalera = (len(caras) == 5 and (caras[-1] - caras[0] == 4)) or (caras in [[1,2,3,4,5], [2,3,4,5,6], [1,3,4,5,6]])
    
    return {
        "G": 5 in counts,
        "P": 4 in counts or 5 in counts,
        "F": (3 in counts and 2 in counts),
        "E": es_escalera
    }

def calcular_puntos(dados, cat, tiro):
    res = analizar_jugada(dados)
    bonus = 5 if tiro == 1 else 0
    
    if cat == "G": return (80 if tiro == 1 and res["G"] else 50) if res["G"] else 0
    if cat == "P": return (40 + bonus) if res["P"] else 0
    if cat == "F": return (30 + bonus) if res["F"] else 0
    if cat == "E": return (20 + bonus) if res["E"] else 0
    if cat.isdigit():
        n = int(cat)
        return dados.count(n) * n
    return 0

def guardar_csv(p1, p2):
    cats = ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"]
    with open("jugadas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["jugada", "j1", "j2"])
        for c in cats:
            writer.writerow([c, p1.get(c, 0) or 0, p2.get(c, 0) or 0])

# --- LÓGICA DEL TURNO ---

def ejecutar_turno(nombre_jugador, planilla):
    print(f"\n>>> TURNO DE: {nombre_jugador}")
    dados = tirar_dados(5)
    tiro_actual = 1
    
    # Bucle de re-tiros (máximo 3 tiros)
    while tiro_actual < 3:
        print(f"Tiro {tiro_actual}: {dados}")
        # Chequeo rápido de Generala Real
        if tiro_actual == 1 and analizar_jugada(dados)["G"]:
            print("¡INCREÍBLE! ¡GENERALA REAL!")
            return dados, 1, True
            
        opcion = input("¿Mantener dados y volver a tirar? (si/no): ").lower()
        if opcion != 'si': break
        
        print("Posiciones a conservar (ej: 0 2 4):")
        indices = input("> ").split()
        conservados = [dados[int(i)] for i in indices if i.isdigit() and int(i) < 5]
        dados = conservados + tirar_dados(5 - len(conservados))
        tiro_actual += 1

    print(f"Dados finales: {dados}")
    
    # Selección de categoría
    while True:
        cats_libres = [c for c, v in planilla.items() if v is None]
        print(f"Categorías disponibles: {cats_libres}")
        eleccion = input("Elegí dónde anotar: ").upper()
        
        if eleccion in cats_libres:
            pts = calcular_puntos(dados, eleccion, tiro_actual)
            planilla[eleccion] = pts
            print(f"Anotaste {pts} puntos en {eleccion}.")
            break
        else:
            print("Categoría no válida o ya ocupada.")
            
    return dados, tiro_actual, False

# --- BUCLE PRINCIPAL DEL JUEGO ---

def jugar_generala():
    # 11 categorías (E, F, P, G y 1-6 son 10, agregamos G2 o simplemente jugamos con 10)
    categorias = ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"]
    p1 = {c: None for c in categorias}
    p2 = {c: None for c in categorias}
    
    for ronda in range(1, 11): # 10 rondas según tus categorías
        print(f"\n=== RONDA {ronda} ===")
        
        # Turno Jugador 1
        _, _, es_real = ejecutar_turno("JUGADOR 1", p1)
        guardar_csv(p1, p2)
        if es_real: 
            print("¡JUGADOR 1 GANA POR GENERALA REAL!"); return

        # Turno Jugador 2
        _, _, es_real = ejecutar_turno("JUGADOR 2", p2)
        guardar_csv(p1, p2)
        if es_real: 
            print("¡JUGADOR 2 GANA POR GENERALA REAL!"); return

    # Fin del juego: Cálculo de ganador
    total1 = sum(v for v in p1.values() if v is not None)
    total2 = sum(v for v in p2.values() if v is not None)
    
    print("\n=== PUNTAJE FINAL ===")
    print(f"Jugador 1: {total1} pts")
    print(f"Jugador 2: {total2} pts")
    
    if total1 > total2: print("¡GANADOR: JUGADOR 1!")
    elif total2 > total1: print("¡GANADOR: JUGADOR 2!")
    else: print("¡EMPATE!")

if __name__ == "__main__":
    jugar_generala()
    