from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("BOT_TOKEN")
if not token:
    raise ValueError("No se encontró BOT_TOKEN en el archivo .env")

# Cargar notas
try:
    with open("notas.json", "r") as f:
        notas = json.load(f)
except FileNotFoundError:
    notas = {}

def guardar_notas():
    with open("notas.json", "w") as f:
        json.dump(notas, f)

async def agregar_nota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = str(update.message.from_user.id)
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("Escribe algo después de /nota")
        return
    notas.setdefault(user_id, []).append(texto)
    guardar_notas()
    await update.message.reply_text(f"Nota guardada: {texto}")

async def listar_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = str(update.message.from_user.id)
    if user_id not in notas or not notas[user_id]:
        await update.message.reply_text("No tienes notas guardadas.")
        return
    lista = "\n".join([f"{i+1}. {n}" for i, n in enumerate(notas[user_id])])
    await update.message.reply_text(f"📒 Tus notas:\n{lista}")

async def borrar_nota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
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
        guardar_notas()
        await update.message.reply_text(f"Nota eliminada: {eliminada}")
    else:
        await update.message.reply_text("Número inválido.")

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("nota", agregar_nota))
    app.add_handler(CommandHandler("notas", listar_notas))
    app.add_handler(CommandHandler("borrar", borrar_nota))

    print("🤖 Bot de notas iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
