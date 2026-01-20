import sqlite3
import time
import sys

# ==================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==================================================

conexion = sqlite3.connect("biblioteca.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    editorial TEXT NOT NULL,
    cantidad INTEGER NOT NULL
)
""")
conexion.commit()

PALABRAS_PROHIBIDAS = [
    "DROP", "ALTER", "TRUNCATE", "CREATE",
    "ATTACH", "PRAGMA"
]

# ==================================================
# INTERFAZ Echo por Ing. Yahir Sampayo
# ==================================================

def linea():
    print("─" * 72)

def titulo():
    print("\n" + "=" * 72)
    print("📚  SISTEMA DE PRÁCTICA SQL – BIBLIOTECA ".center(72))
    print("🎓  Modo educativo | Práctica de comandos SQL echo por Ing.Yahir Sampayo" .center(72))
    print("=" * 72)

def ayuda():
    print("▶ INSERT  – Agregar libros        |  INSERT INTO libros (...)")
    print("▶ SELECT  – Consultar libros      |  SELECT * FROM libros;")
    print("▶ UPDATE  – Modificar registros   |  UPDATE libros SET ...")
    print("▶ DELETE  – Eliminar registros    |  DELETE FROM libros WHERE id = ?;")
    linea()
    print("Reglas:")
    print(" • Escribe los comandos manualmente")
    print(" • Finaliza cada comando con ;")
    print(" • Escribe SALIR para cerrar el sistema")
    linea()

def instrucciones_tabla():
    print("📘 ESTRUCTURA DE LA TABLA: libros\n")
    print("Campos:")
    print(" • id        → automático (NO se escribe)")
    print(" • titulo    → texto   (entre comillas simples)")
    print(" • autor     → texto   (entre comillas simples)")
    print(" • editorial → texto   (entre comillas simples)")
    print(" • cantidad  → número entero (sin comillas)")
    linea()
    print("Ejemplo de INSERT (GUÍA):")
    print(" INSERT INTO libros (titulo, autor, editorial, cantidad)")
    print(" VALUES ('Título', 'Autor', 'Editorial', 5);")
    linea()

# ==================================================
# LECTOR SQL (ANTI PEGADO)
# ==================================================

def leer_sql():
    print("\nSQL> ", end="", flush=True)
    inicio = time.time()
    texto = ""

    while True:
        char = sys.stdin.read(1)
        if char == "\n":
            break
        texto += char

        if len(texto) > 300:
            print("\n⛔ Entrada demasiado larga (posible pegado)")
            return None

    duracion = time.time() - inicio

    if duracion < 0.5 and len(texto) > 20:
        print("⛔ Pegado de texto detectado. Escribe el comando manualmente.")
        return None

    return texto.strip()

# ==================================================
# SALIDA SEGURA
# ==================================================

def salir():
    linea()
    print("👋 Cerrando sistema... Gracias por practicar SQL")
    linea()
    conexion.close()
    time.sleep(1)
    exit()

# ==================================================
# PROGRAMA PRINCIPAL
# ==================================================

titulo()
ayuda()
instrucciones_tabla()

while True:
    sql = leer_sql()
    if sql is None:
        continue

    if sql.upper() == "SALIR":
        salir()

    sql_upper = sql.upper()

    if any(p in sql_upper for p in PALABRAS_PROHIBIDAS):
        print("⛔ Comando bloqueado por seguridad")
        continue

    try:
        if sql_upper.startswith("INSERT"):
            cursor.execute(sql)
            conexion.commit()
            print("✅ Libro insertado correctamente")

        elif sql_upper.startswith("SELECT"):
            cursor.execute(sql)
            filas = cursor.fetchall()
            linea()
            print("📖 RESULTADOS DE LA CONSULTA")
            linea()
            if filas:
                for f in filas:
                    print(f)
            else:
                print("No hay registros que mostrar")
            linea()

        elif sql_upper.startswith("UPDATE"):
            cursor.execute(sql)
            conexion.commit()
            print(f"✏ Registros modificados: {cursor.rowcount}")

        elif sql_upper.startswith("DELETE"):
            cursor.execute(sql)
            conexion.commit()
            print(f"🗑 Registros eliminados: {cursor.rowcount}")

        else:
            print("⚠ Comando no reconocido")

    except Exception as e:
        print("❌ Error SQL:", e)