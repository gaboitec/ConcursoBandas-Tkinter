import tkinter as tk
from clases import BandaEscolar, Concurso

class ConcursoBandasApp:
    def __init__(self):
        self.concurso = Concurso("Concurso de Bandas", "2025-09-14")
        self.concurso.cargar_desde_archivo("bandas.txt")
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")
        self.info = tk.Label(self.ventana, text = "")
        self.info.pack()

        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        self.info.config(text="")
        ventana_inscripcion = tk.Toplevel(self.ventana)
        ventana_inscripcion.title("Inscribir Banda")

        tk.Label(ventana_inscripcion, text="Nombre de la Banda").pack()
        entrada_nombre = tk.Entry(ventana_inscripcion)
        entrada_nombre.pack()

        tk.Label(ventana_inscripcion, text="Institución").pack()
        entrada_institucion = tk.Entry(ventana_inscripcion)
        entrada_institucion.pack()

        tk.Label(ventana_inscripcion, text="Categoría").pack()
        categoria_var = tk.StringVar(value="Primaria")
        tk.OptionMenu(ventana_inscripcion, categoria_var, "Primaria", "Básico", "Diversificado").pack()

        def guardar():
            try:
                banda = BandaEscolar(
                    entrada_nombre.get(),
                    entrada_institucion.get(),
                    categoria_var.get()
                )
                self.concurso.inscribir_banda(banda)
                self.concurso.guardar_en_archivo("bandas.txt")
                self.info.config(text="Exito, Inscripcion de banda realizada!")
                ventana_inscripcion.destroy()
            except Exception as e:
                self.info.config(text=f"Error {e}")

        tk.Button(ventana_inscripcion, text="Guardar", command=guardar).pack(pady=10)

    def registrar_evaluacion(self):
        self.info.config(text="")
        ventana_eval = tk.Toplevel(self.ventana)
        ventana_eval.title("Registrar Evaluación")

        tk.Label(ventana_eval, text="Nombre de la Banda").pack()
        entrada_nombre = tk.Entry(ventana_eval)
        entrada_nombre.pack()

        criterios = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]
        entradas = {}

        for criterio in criterios:
            tk.Label(ventana_eval, text=f"{criterio.capitalize()} (0-10)").pack()
            entrada = tk.Entry(ventana_eval)
            entrada.pack()
            entradas[criterio] = entrada

        def guardar():
            try:
                puntajes = {c: int(entradas[c].get()) for c in criterios}
                self.concurso.registrar_evaluacion(entrada_nombre.get(), puntajes)
                self.concurso.guardar_en_archivo("bandas.txt")
                self.info.config(text ="Éxito, Evaluación registrada")
                ventana_eval.destroy()
            except Exception as e:
                self.info.config(text=f"Error {e}")

        tk.Button(ventana_eval, text="Guardar", command=guardar).pack(pady=10)

    def listar_bandas(self):
        self.info.config(text="")
        ventana_listado = tk.Toplevel(self.ventana)
        ventana_listado.title("LISTADO DE BANDAS")

        texto = tk.Text(ventana_listado, width=80, height=20)
        texto.pack()

        if not self.concurso.bandas:
            texto.insert(tk.END, "No hay bandas inscritas.\n")
        else:
            for banda in self.concurso.bandas.values():
                texto.insert(tk.END, banda.mostrar_info() + "\n")

    def ver_ranking(self):
        self.info.config(text="")
        ventana_ranking = tk.Toplevel(self.ventana)
        ventana_ranking.title("Ranking final")

        texto = tk.Text(ventana_ranking, width=80, height=20)
        texto.pack()

        ranking = self.concurso.ranking()
        if not ranking:
            texto.insert(tk.END, "No hay bandas evaluadas aún.\n")
        else:
            texto.insert(tk.END, "RANKING DE BANDAS:\n\n")
            for i, banda in enumerate(ranking, start=1):
                texto.insert(tk.END,
                             f"{i}. {banda.nombre} ({banda.institucion}) - {banda._categoria} - Total: {banda.total} - Promedio: {banda.promedio:.2f}\n")


if __name__ == "__main__":
    ConcursoBandasApp()
