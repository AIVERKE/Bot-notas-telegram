import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

#Cargado de las variables de entorno
load_dotenv()

# ===============================
# CONFIGURACIÓN
# ===============================

# Obtener token de la variable de entorno
token = os.environ.get("BOT_TOKEN")
if not token:
    raise ValueError("No se encontró BOT_TOKEN en las variables de entorno.")

# Archivo donde se guardarán las notas
NOTAS_FILE = "notas.json"

# ===============================
# FUNCIONES DE PERSISTENCIA
# ===============================

def cargar_notas():
    """Cargar notas desde el archivo JSON."""
    try:
        with open(NOTAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_notas(notas):
    """Guardar notas en el archivo JSON."""
    with open(NOTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=4)

# Cargar notas al iniciar
notas = cargar_notas()

# ===============================
# HANDLERS DEL BOT
# ===============================

# Comando /nota -> agrega una nota
async def agregar_nota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    texto = " ".join(context.args)
    
    if not texto:
        await update.message.reply_text("Escribe algo después de /nota")
        return
    
    if user_id not in notas:
        notas[user_id] = []
    
    notas[user_id].append(texto)
    guardar_notas(notas)
    await update.message.reply_text(f"✅ Nota guardada: {texto}")

# Comando /notas -> lista todas las notas
async def listar_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    
    if user_id not in notas or not notas[user_id]:
        await update.message.reply_text("No tienes notas guardadas.")
        return
    
    lista = "\n".join([f"{i+1}. {n}" for i, n in enumerate(notas[user_id])])
    await update.message.reply_text(f"📒 Tus notas:\n{lista}")

# Comando /borrar -> elimina una nota
async def borrar_nota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    
    if user_id not in notas or not notas[user_id]:
        await update.message.reply_text("No tienes notas para borrar.")
        return
    
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usa /borrar <número>")
        return
    
    indice = int(context.args[0]) - 1
    if 0 <= indice < len(notas[user_id]):
        eliminada = notas[user_id].pop(indice)
        guardar_notas(notas)
        await update.message.reply_text(f"🗑️ Nota eliminada: {eliminada}")
    else:
        await update.message.reply_text("Número inválido.")

# ===============================
# INICIO DEL BOT
# ===============================

def main():
    app = Application.builder().token(token).build()

    # Registrar comandos
    app.add_handler(CommandHandler("nota", agregar_nota))
    app.add_handler(CommandHandler("notas", listar_notas))
    app.add_handler(CommandHandler("borrar", borrar_nota))

    print("🤖 Bot de notas iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
