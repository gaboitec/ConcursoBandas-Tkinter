class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        return f"{self.nombre} - {self.institucion}"


class BandaEscolar(Participante):
    categorias_validas = ["Primaria", "Básico", "Diversificado"]
    criterios_validos = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria in self.categorias_validas:
            self._categoria = categoria
        else:
            raise ValueError("Categoría inválida")

    def registrar_puntajes(self, puntajes):
        if set(puntajes.keys()) != set(self.criterios_validos):
            raise ValueError("Criterios incompletos o inválidos")
        if not all(0 <= v <= 10 for v in puntajes.values()):
            raise ValueError("Puntajes fuera de rango")
        self._puntajes = puntajes

    @property
    def total(self):
        return sum(self._puntajes.values())

    @property
    def promedio(self):
        return self.total / len(self._puntajes)

    def mostrar_info(self):
        info = super().mostrar_info()
        info += f" | Categoría: {self._categoria}"
        if self._puntajes:
            info += f" | Total: {self.total}"
        return info


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self, banda):
        if banda.nombre in self.bandas:
            raise ValueError("Ya existe una banda con ese nombre")
        self.bandas[banda.nombre] = banda

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            raise ValueError("Banda no encontrada")
        self.bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        for banda in self.bandas.values():
            print(banda.mostrar_info())

    def ranking(self):
        evaluadas = [b for b in self.bandas.values() if b._puntajes]
        return sorted(evaluadas, key=lambda b: (-b.total, -b.promedio))

    def guardar_en_archivo(self, ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            for banda in self.bandas.values():
                linea = f"{banda.nombre}:{banda.institucion}:{banda._categoria}:"
                if banda._puntajes:
                    puntajes_str = ",".join(f"{k}:{v}" for k, v in banda._puntajes.items())
                    linea += puntajes_str
                f.write(linea + "\n")

    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(":")
                    nombre, institucion, categoria = partes[:3]
                    banda = BandaEscolar(nombre, institucion, categoria)
                    if len(partes) == 4 and partes[3]:
                        puntajes = dict(item.split(":") for item in partes[3].split(","))
                        puntajes = {k: int(v) for k, v in puntajes.items()}
                        banda.registrar_puntajes(puntajes)
                    self.inscribir_banda(banda)
        except ValueError:
            pass

