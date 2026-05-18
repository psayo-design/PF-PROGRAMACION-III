import random
import os
import subprocess
import webbrowser
from tkinter import *
from tkinter import messagebox, simpledialog, Toplevel

# =========================
# RUTA FIJA
# =========================
RUTA_SALIDA = r"D:\DOC P.SAY\UMG\PROGRAMACION III\Programación\TAREA\PF"

# =========================
# CONFIG VISUAL
# =========================
BG = "#0f172a"
CARD = "#1e293b"
BTN = "#334155"
TXT = "#e2e8f0"
X_COLOR = "#ef4444"
O_COLOR = "#22c55e"
ACCENT = "#38bdf8"

# =========================
# PARTIDA
# =========================
class Partida:

    def __init__(self, id_partida, puntaje,
                 resultado, tablero, proceso=None):

        self.id = id_partida
        self.puntaje = puntaje
        self.resultado = resultado
        self.tablero = tablero
        self.proceso = proceso

# =========================
# NODO PROCESO
# =========================
class NodoProceso:

    def __init__(self, descripcion,
                 cambio, acumulado):

        self.descripcion = descripcion
        self.cambio = cambio
        self.acumulado = acumulado

        self.hijos = []

# =========================
# ÁRBOL B
# =========================
class NodoB:

    def __init__(self, grado):

        self.grado = grado
        self.claves = []
        self.hijos = []
        self.hoja = True

class ArbolB:

    def __init__(self, grado):

        self.raiz = NodoB(grado)
        self.grado = grado

    def insertar(self, partida):

        raiz = self.raiz

        if len(raiz.claves) == (2*self.grado)-1:

            nueva = NodoB(self.grado)

            nueva.hoja = False

            nueva.hijos.append(raiz)

            self.dividir(nueva, 0)

            self.insertar_no_lleno(
                nueva,
                partida
            )

            self.raiz = nueva

        else:

            self.insertar_no_lleno(
                raiz,
                partida
            )

    def insertar_no_lleno(self, nodo, partida):

        i = len(nodo.claves)-1

        if nodo.hoja:

            nodo.claves.append(None)

            while (
                i >= 0 and
                partida.puntaje >
                nodo.claves[i].puntaje
            ):

                nodo.claves[i+1] = nodo.claves[i]

                i -= 1

            nodo.claves[i+1] = partida

        else:

            while (
                i >= 0 and
                partida.puntaje >
                nodo.claves[i].puntaje
            ):
                i -= 1

            i += 1

            if len(
                nodo.hijos[i].claves
            ) == (2*self.grado)-1:

                self.dividir(nodo, i)

                if (
                    partida.puntaje >
                    nodo.claves[i].puntaje
                ):
                    i += 1

            self.insertar_no_lleno(
                nodo.hijos[i],
                partida
            )

    def dividir(self, padre, i):

        grado = self.grado

        nodo = padre.hijos[i]

        nuevo = NodoB(grado)

        nuevo.hoja = nodo.hoja

        padre.claves.insert(
            i,
            nodo.claves[grado-1]
        )

        padre.hijos.insert(i+1, nuevo)

        nuevo.claves = nodo.claves[grado:]

        nodo.claves = nodo.claves[:grado-1]

        if not nodo.hoja:

            nuevo.hijos = nodo.hijos[grado:]

            nodo.hijos = nodo.hijos[:grado]

# =========================
# CLONAR ÁRBOL
# =========================
def clonar_nodo(nodo):

    nuevo = NodoB(nodo.grado)

    nuevo.claves = nodo.claves.copy()

    nuevo.hoja = nodo.hoja

    nuevo.hijos = [
        clonar_nodo(h)
        for h in nodo.hijos
    ]

    return nuevo

def clonar_arbol(arbol):

    nuevo = ArbolB(arbol.grado)

    nuevo.raiz = clonar_nodo(arbol.raiz)

    return nuevo

# =========================
# IA
# =========================
class IA:

    def elegir(self, tablero):

        libres = [
            i for i in range(9)
            if tablero[i] == " "
        ]

        return random.choice(libres)

# =========================
# LÓGICA
# =========================
def verificar(tab):

    comb = [
        (0,1,2),
        (3,4,5),
        (6,7,8),

        (0,3,6),
        (1,4,7),
        (2,5,8),

        (0,4,8),
        (2,4,6)
    ]

    for a,b,c in comb:

        if (
            tab[a] ==
            tab[b] ==
            tab[c]
            and
            tab[a] != " "
        ):
            return tab[a]

    if " " not in tab:
        return "Empate"

    return None

def puntaje(resultado):

    if resultado == "X":
        return 20

    elif resultado == "O":
        return 5

    return 10

# =========================
# EXPORTAR ÁRBOL B
# =========================
def exportar(arbol, nombre):

    if not os.path.exists(RUTA_SALIDA):
        os.makedirs(RUTA_SALIDA)

    ruta_dot = os.path.join(
        RUTA_SALIDA,
        f"{nombre}.dot"
    )

    ruta_png = os.path.join(
        RUTA_SALIDA,
        f"{nombre}.png"
    )

    with open(
        ruta_dot,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("""
digraph G {

rankdir=TB;
splines=true;
nodesep=0.8;
ranksep=1;

node [
shape=record,
style=filled,
fillcolor="#38bdf8",
fontname="Arial",
fontsize=12
];

edge [
color="#94a3b8"
];
""")

        contador = [0]

        def rec(nodo):

            actual = contador[0]

            campos = []

            for p in nodo.claves:

                campos.append(
                    f"ID:{p.id}\\nP:{p.puntaje}"
                )

            if not campos:
                campos.append("Vacío")

            label = " | ".join(campos)

            f.write(
                f'n{actual} [label="{label}"];\n'
            )

            contador[0] += 1

            mi_id = actual

            hijos_ids = []

            for h in nodo.hijos:

                hijo_id = contador[0]

                hijos_ids.append(hijo_id)

                rec(h)

            for hid in hijos_ids:

                f.write(
                    f'n{mi_id} -> n{hid};\n'
                )

        rec(arbol.raiz)

        f.write("}")

    subprocess.run(
        ["dot", "-Tpng",
         ruta_dot,
         "-o",
         ruta_png],
        check=True
    )

    webbrowser.open(ruta_png)

# =========================
# EXPORTAR PROCESO
# =========================
def exportar_proceso(raiz, nombre):

    if not os.path.exists(RUTA_SALIDA):
        os.makedirs(RUTA_SALIDA)

    ruta_dot = os.path.join(
        RUTA_SALIDA,
        f"{nombre}.dot"
    )

    ruta_png = os.path.join(
        RUTA_SALIDA,
        f"{nombre}.png"
    )

    with open(
        ruta_dot,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("""
digraph G {

rankdir=TB;
splines=true;
nodesep=0.8;
ranksep=1.2;

node [
shape=record,
style=filled,
fillcolor="#22c55e",
fontname="Arial",
fontsize=11
];

edge [
color="#94a3b8",
penwidth=2
];
""")

        contador = [0]

        def rec(nodo, padre=None):

            actual = contador[0]

            label = (
                f"{{"
                f"{nodo.acumulado}"
                f"|"
                f"{nodo.descripcion}"
                f"|"
                f"{nodo.cambio:+}"
                f"}}"
            )

            f.write(
                f'n{actual} [label="{label}"];\n'
            )

            contador[0] += 1

            if padre is not None:

                f.write(
                    f'n{padre} -> n{actual};\n'
                )

            mi_id = actual

            # SOLO RECORRER HIJOS EXISTENTES
            for h in nodo.hijos:

                rec(h, mi_id)

        rec(raiz)

        f.write("}")

    subprocess.run(
        ["dot", "-Tpng",
         ruta_dot,
         "-o",
         ruta_png],
        check=True
    )

    webbrowser.open(ruta_png)

# =========================
# APP
# =========================
class App:

    def __init__(self):

        self.arbol = ArbolB(2)

        self.historial_arboles = []

        self.ia = IA()

        self.id_partida = 1

        self.root = Tk()

        self.root.title(
            "TicTacToe IA PRO"
        )

        self.root.geometry("450x700")

        self.root.configure(bg=BG)

        self.menu()

        self.root.mainloop()

    # =========================
    # LIMPIAR
    # =========================
    def limpiar(self):

        for w in self.root.winfo_children():
            w.destroy()

    # =========================
    # BOTÓN
    # =========================
    def boton(self, txt, cmd):

        Button(
            self.root,
            text=txt,
            command=cmd,
            bg=BTN,
            fg=TXT,
            relief="flat",
            height=2,
            font=("Segoe UI", 11, "bold")
        ).pack(
            fill="x",
            padx=40,
            pady=5
        )

    # =========================
    # MENÚ
    # =========================
    def menu(self):

        self.limpiar()

        Label(
            self.root,
            text="TicTacToe IA PRO",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        self.boton(
            "🎮 Jugar",
            self.jugar
        )

        self.boton(
            "🤖 Entrenar IA",
            self.entrenar
        )

        self.boton(
            "📊 Historial",
            self.historial
        )

        self.boton(
            "🌳 Árboles por Partida",
            self.ver_arboles
        )

        self.boton(
            "🧠 Procesos de Partidas",
            self.ver_procesos
        )

        self.boton(
            "👥 Integrantes",
            self.integrantes
        )

        self.boton(
            "♻ Reiniciar",
            self.reset
        )

        self.boton(
            "❌ Salir",
            self.root.quit
        )

    # =========================
    # JUGAR
    # =========================
    def jugar(self):

        self.limpiar()

        self.tab = [" "]*9

        self.proceso_raiz = NodoProceso(
            "Inicio",
            0,
            0
        )

        self.nodo_actual = self.proceso_raiz

        frame = Frame(
            self.root,
            bg=BG
        )

        frame.pack()

        self.btns = []

        for i in range(9):

            b = Button(
                frame,
                text=" ",
                width=5,
                height=2,
                font=("Segoe UI", 20),
                bg=CARD,
                fg=TXT,
                command=lambda i=i:
                self.click(i)
            )

            b.grid(
                row=i//3,
                column=i%3,
                padx=5,
                pady=5
            )

            self.btns.append(b)

        self.boton(
            "Volver",
            self.menu
        )

    # =========================
    # CLICK
    # =========================
    def click(self, i):

        if self.tab[i] != " ":
            return

        # =========================
        # JUGADOR
        # =========================
        self.tab[i] = "O"

        self.btns[i].config(
            text="O",
            fg=O_COLOR
        )

        ramas = random.randint(2, 4)

        nuevos = []

        for r in range(ramas):

            cambio = random.randint(-300, 600)

            nuevo = NodoProceso(
                f"Jugador {i} Rama {r+1}",
                cambio,
                self.nodo_actual.acumulado + cambio
            )

            self.nodo_actual.hijos.append(nuevo)

            nuevos.append(nuevo)

        # Elegir una rama aleatoria
        self.nodo_actual = random.choice(nuevos)

        if self.fin():
            return

        # =========================
        # IA
        # =========================
        mov = self.ia.elegir(self.tab)

        self.tab[mov] = "X"

        self.btns[mov].config(
            text="X",
            fg=X_COLOR
        )

        ramas = random.randint(2, 4)

        nuevos = []

        for r in range(ramas):

            cambio = random.randint(-300, 600)

            nuevo = NodoProceso(
                f"IA {mov} Rama {r+1}",
                cambio,
                self.nodo_actual.acumulado + cambio
            )

            self.nodo_actual.hijos.append(nuevo)

            nuevos.append(nuevo)

        # Elegir rama aleatoria
        self.nodo_actual = random.choice(nuevos)

        self.fin()

    # =========================
    # FINAL
    # =========================
    def fin(self):

        res = verificar(self.tab)

        if res:

            self.historial_arboles.append(
                clonar_arbol(self.arbol)
            )

            self.arbol.insertar(
                Partida(
                    self.id_partida,
                    puntaje(res),
                    res,
                    self.tab.copy(),
                    self.proceso_raiz
                )
            )

            self.id_partida += 1

            messagebox.showinfo(
                "Resultado",
                f"Ganador: {res}"
            )

            self.menu()

            return True

        return False

    # =========================
    # ENTRENAR
    # =========================
    def entrenar(self):

        n = simpledialog.askinteger(
            "Entrenar",
            "Número de partidas:"
        )

        if not n:
            return

        for _ in range(n):

            tab = [" "]*9

            turno = "X"

            raiz = NodoProceso(
                "Inicio",
                0,
                0
            )

            actual = raiz

            while True:

                libres = [
                    i for i in range(9)
                    if tab[i] == " "
                ]

                mov = random.choice(libres)

                tab[mov] = turno

                ramas = random.randint(2, 4)

                nuevos = []

                for r in range(ramas):

                    cambio = random.randint(-300, 600)

                    nuevo = NodoProceso(
                        f"{turno} {mov} Rama {r+1}",
                        cambio,
                        actual.acumulado + cambio
                    )

                    actual.hijos.append(nuevo)

                    nuevos.append(nuevo)

                actual = random.choice(nuevos)

                res = verificar(tab)

                if res:

                    self.historial_arboles.append(
                        clonar_arbol(self.arbol)
                    )

                    self.arbol.insertar(
                        Partida(
                            self.id_partida,
                            puntaje(res),
                            res,
                            tab.copy(),
                            raiz
                        )
                    )

                    self.id_partida += 1

                    break

                turno = (
                    "O"
                    if turno == "X"
                    else "X"
                )

        messagebox.showinfo(
            "IA",
            "Entrenamiento completado"
        )

    # =========================
    # HISTORIAL
    # =========================
    def historial(self):

        v = Toplevel(self.root)

        v.title("Historial")

        v.configure(bg=BG)

        def rec(n):

            for p in n.claves:

                Label(
                    v,
                    text=f"ID:{p.id} | Puntaje:{p.puntaje} | Resultado:{p.resultado}",
                    bg=BG,
                    fg=TXT
                ).pack()

            for h in n.hijos:
                rec(h)

        rec(self.arbol.raiz)

    # =========================
    # VER ÁRBOLES
    # =========================
    def ver_arboles(self):

        v = Toplevel(self.root)

        v.title("Árboles")

        v.geometry("400x500")

        v.configure(bg=BG)

        canvas = Canvas(v, bg=BG)

        scrollbar = Scrollbar(
            v,
            orient="vertical",
            command=canvas.yview
        )

        frame = Frame(canvas, bg=BG)

        frame.bind(
            "<Configure>",
            lambda e:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0,0),
            window=frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for i, arb in enumerate(
            self.historial_arboles,
            start=1
        ):

            Button(
                frame,
                text=f"Partida {i}",
                bg=BTN,
                fg=TXT,
                command=lambda a=arb, n=i:
                exportar(a, f"partida_{n}")
            ).pack(
                fill="x",
                padx=20,
                pady=5
            )

    # =========================
    # VER PROCESOS
    # =========================
    def ver_procesos(self):

        v = Toplevel(self.root)

        v.title("Procesos")

        v.geometry("400x500")

        v.configure(bg=BG)

        canvas = Canvas(v, bg=BG)

        scrollbar = Scrollbar(
            v,
            orient="vertical",
            command=canvas.yview
        )

        frame = Frame(canvas, bg=BG)

        frame.bind(
            "<Configure>",
            lambda e:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0,0),
            window=frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        partidas = []

        def rec(n):

            for p in n.claves:
                partidas.append(p)

            for h in n.hijos:
                rec(h)

        rec(self.arbol.raiz)

        for p in partidas:

            Button(
                frame,
                text=f"Partida {p.id}",
                bg=BTN,
                fg=TXT,
                command=lambda p=p:
                exportar_proceso(
                    p.proceso,
                    f"proceso_{p.id}"
                )
            ).pack(
                fill="x",
                padx=20,
                pady=5
            )

    # =========================
    # INTEGRANTES
    # =========================
    def integrantes(self):

        v = Toplevel(self.root)

        v.title("Integrantes")

        v.configure(bg=BG)

        Label(
            v,
            text="INTEGRANTES",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        integrantes = [

            "Pablo Andrés Say Oliva",
            "Daniel Alexander Ovalle Estrada",
            "Jorge Mario Romualdo Castillo Jiménez",
            "David Estuardo Arevalo Zeceña"
        ]

        for i in integrantes:

            Label(
                v,
                text=i,
                bg=BG,
                fg=TXT,
                font=("Segoe UI", 11)
            ).pack(pady=5)

    # =========================
    # RESET
    # =========================
    def reset(self):

        self.arbol = ArbolB(2)

        self.historial_arboles = []

        self.id_partida = 1

        messagebox.showinfo(
            "Sistema",
            "Reiniciado"
        )

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    App()