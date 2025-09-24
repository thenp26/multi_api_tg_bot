# bot.py (Updated Version)
import os
import logging
from functools import wraps

# Import new libraries
import google.generativeai as genai
import openai
import anthropic
from googlesearch import search
import wikipediaapi

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# Import our database functions
import database as db

# --- Configuration ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')
BOT_VERSION = "2.0.0" # Updated version

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Force Subscription Decorator ---
def force_subscribe(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not CHANNEL_USERNAME:
            return await func(update, context, *args, **kwargs)

        user_id = update.effective_user.id
        try:
            member_status = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
            if member_status.status not in ['member', 'administrator', 'creator']:
                raise Exception("User not a member")
        except (BadRequest, Exception) as e:
            logger.warning(f"User {user_id} is not a member of {CHANNEL_USERNAME}. Error: {e}")
            join_channel_button = InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
            keyboard = InlineKeyboardMarkup([[join_channel_button]])
            await update.message.reply_text(
                "You must join our channel to use this bot. Please join and then try again.",
                reply_markup=keyboard
            )
            return None
        
        return await func(update, context, *args, **kwargs)
    return wrapper

# --- Bot Command Handlers ---

@force_subscribe
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command after checking for subscription."""
    user_id = update.effective_user.id
    db.add_or_update_user(user_id)
    
    welcome_text = (
        "Welcome to the Telegram AI Chat Bot, where you can search anything on the internet with Artificial Intelligence.\n\n"
        "By default, your queries will search on Google. You can also connect with multiple LLMs like Gemini, GPT, and Claude.\n\n"
        "Press the button below or type /services to see all available services."
    )
    services_button = InlineKeyboardButton("Services", callback_data="services_menu")
    keyboard = InlineKeyboardMarkup([[services_button]])
    await update.message.reply_text(welcome_text, reply_markup=keyboard)

@force_subscribe
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a detailed help message."""
    help_text = (
        "Here's how to use me:\n\n"
        "1. **Send any message**: I will process it using your default provider (Google by default).\n\n"
        "2. **Set API Keys**:\n"
        "   - `/gemini_api YOUR_API_KEY`\n"
        "   - `/gpt_api YOUR_API_KEY`\n"
        "   - `/claude_api YOUR_API_KEY`\n\n"
        "3. **Set Default Provider**:\n"
        "   - `/def_google` - Search Google (default)\n"
        "   - `/def_gemini` - Use Gemini 1.5 Flash\n"
        "   - `/def_gpt` - Use GPT-4o Mini\n"
        "   - `/def_claude` - Use Claude 3 Haiku\n\n"
        "4. **Specialized Searches**:\n"
        "   - `/wikipedia <search query>` - Search directly on Wikipedia.\n\n"
        "Use /services to see a list of all commands."
    )
    await update.message.reply_text(help_text)

@force_subscribe
async def services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays all available services."""
    services_text = (
        "**Available Services:**\n\n"
        "🔍 **Google Search**: The default search provider.\n"
        "💎 **Google Gemini**: Advanced and fast AI model.\n"
        "🤖 **OpenAI GPT**: Powerful and creative AI model.\n"
        "💡 **Anthropic Claude**: State-of-the-art conversational AI.\n"
        "🌐 **Wikipedia**: Direct search on the encyclopedia.\n\n"
        "Use /help for a full list of commands."
    )
    await update.message.reply_text(services_text, parse_mode='Markdown')
    
async def version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the bot version."""
    await update.message.reply_text(f"Bot Version: {BOT_VERSION}")

@force_subscribe
async def set_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the API key for a given service."""
    user_id = update.effective_user.id
    command = update.message.text.split()[0].lower()
    
    if not context.args:
        await update.message.reply_text(f"Please provide an API key. Usage: `{command} YOUR_KEY`")
        return
        
    api_key = context.args[0]
    
    if command == '/gemini_api':
        db.add_or_update_user(user_id, gemini_key=api_key)
        await update.message.reply_text("✅ Gemini API key has been set successfully!")
    elif command == '/gpt_api':
        db.add_or_update_user(user_id, gpt_key=api_key)
        await update.message.reply_text("✅ GPT API key has been set successfully!")
    elif command == '/claude_api':
        db.add_or_update_user(user_id, claude_key=api_key)
        await update.message.reply_text("✅ Claude API key has been set successfully!")
    else:
        await update.message.reply_text("Unknown API command.")

@force_subscribe
async def set_default_provider(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the user's default query provider."""
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    command = update.message.text.split()[0].lower()
    provider_name = command.split('_')[1]

    if provider_name == 'google':
        db.add_or_update_user(user_id, default_provider='google')
        await update.message.reply_text("Default provider set to Google Search.")
        return

    required_key = f"{provider_name}_key"
    if user_data and user_data.get(required_key):
        db.add_or_update_user(user_id, default_provider=provider_name)
        await update.message.reply_text(f"✅ Default provider set to {provider_name.capitalize()}.")
    else:
        await update.message.reply_text(
            f"❗️ API token for {provider_name.capitalize()} not found. "
            f"Please set it first using `/{provider_name}_api YOUR_KEY`."
        )

@force_subscribe
async def wikipedia_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Performs a search on Wikipedia."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a search term. Usage: /wikipedia <query>")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    wiki = wikipediaapi.Wikipedia('MyCoolBot/1.0 (myemail@example.com)', 'en')
    page = wiki.page(query)
    
    if page.exists():
        response = f"**{page.title}**\n\n{page.summary[0:500]}...\n\nRead more: {page.fullurl}"
    else:
        response = f"Sorry, I couldn't find a Wikipedia page for '{query}'."
    
    await update.message.reply_text(response, parse_mode='Markdown')

# --- Core Message Handling ---
@force_subscribe
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The main handler for non-command text messages."""
    user_id = update.effective_user.id
    user_text = update.message.text
    user_data = db.get_user(user_id)
    
    if not user_data:
        db.add_or_update_user(user_id)
        user_data = db.get_user(user_id)
        
    provider = user_data.get('default_provider', 'google')
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    response_text = ""
    try:
        if provider == 'google':
            logger.info(f"Performing Google search for: {user_text}")
            search_results = list(search(user_text, num_results=3, sleep_interval=1))
            
            if not search_results:
                response_text = "Sorry, I couldn't find any results for that search on Google."
            else:
                response_text = "Here are the top Google search results:\n\n"
                for i, result in enumerate(search_results):
                    response_text += f"{i+1}. {result}\n"
        
        elif provider == 'gemini':
            api_key = user_data.get('gemini_key')
            if not api_key:
                response_text = "Your default is Gemini, but no API key is set. Use `/gemini_api YOUR_KEY`."
            else:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_text)
                response_text = response.text
                
        # --- ✨ NEW: GPT Integration ---
        elif provider == 'gpt':
            api_key = user_data.get('gpt_key')
            if not api_key:
                response_text = "Your default is GPT, but no API key is set. Use `/gpt_api YOUR_KEY`."
            else:
                logger.info("Calling OpenAI GPT API...")
                client = openai.OpenAI(api_key=api_key)
                completion = client.chat.completions.create(
                  model="gpt-4o-mini",
                  messages=[{"role": "user", "content": user_text}]
                )
                response_text = completion.choices[0].message.content

        # --- ✨ NEW: Claude Integration ---
        elif provider == 'claude':
            api_key = user_data.get('claude_key')
            if not api_key:
                response_text = "Your default is Claude, but no API key is set. Use `/claude_api YOUR_KEY`."
            else:
                logger.info("Calling Anthropic Claude API...")
                client = anthropic.Anthropic(api_key=api_key)
                message = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": user_text}]
                )
                response_text = message.content[0].text
        
    except Exception as e:
        logger.error(f"Error handling message for provider {provider}: {e}")
        response_text = "Sorry, an error occurred while processing your request. Please check your API key and the service status."
        
    await update.message.reply_text(response_text)

# --- Main Function ---
def main() -> None:
    # ... (The rest of the main function is unchanged)
    if not TELEGRAM_TOKEN or not CHANNEL_USERNAME:
        logger.critical("CRITICAL: TELEGRAM_TOKEN or CHANNEL_USERNAME not found in .env file.")
        return
    db.initialize_db()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("services", services))
    application.add_handler(CommandHandler("version", version))
    application.add_handler(CommandHandler("wikipedia", wikipedia_search))
    application.add_handler(CommandHandler("gemini_api", set_api_key))
    application.add_handler(CommandHandler("gpt_api", set_api_key))
    application.add_handler(CommandHandler("claude_api", set_api_key))
    application.add_handler(CommandHandler("def_google", set_default_provider))
    application.add_handler(CommandHandler("def_gemini", set_default_provider))
    application.add_handler(CommandHandler("def_gpt", set_default_provider))
    application.add_handler(CommandHandler("def_claude", set_default_provider))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()