import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the model and tokenizer
model_name = "facebook/opt-350m"  # A smaller model that works better on M1
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
logger.info(f"Using device: {device}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I am your AI assistant. You can chat with me about anything!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Just send me a message and I will respond using AI!'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and generate AI responses."""
    try:
        # Get the user's message
        user_message = update.message.text
        
        # Create a prompt with better context
        prompt = f"Human: {user_message}\nAssistant:"
        
        # Prepare the input
        inputs = tokenizer(prompt, return_tensors="pt", max_length=100, truncation=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate response with better parameters
        outputs = model.generate(
            inputs["input_ids"],
            max_length=150,  # Reduced max length for faster responses
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        
        # Decode and clean up the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response
        try:
            response = response.split("Assistant:")[-1].strip()
        except:
            response = response.strip()
        
        # If response is too short or empty, generate a fallback response
        if len(response) < 10:
            response = "I understand your message. Could you please provide more details or ask a different question?"
        
        # Send the response back to the user
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await update.message.reply_text(
            "I apologize, but I encountered an error. Please try again later."
        )

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 