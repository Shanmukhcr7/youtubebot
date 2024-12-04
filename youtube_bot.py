import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define a function to handle the '/start' command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Send me the name of a YouTube video.')

# Define a function to handle messages
def handle_message(update, context):
    # Get the text message sent by the user
    video_name = update.message.text

    # Use youtube-dl to get the video URL
    import youtube_dl
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{video_name}", download=False)
        video_url = info_dict['entries'][0]['webpage_url']

    # Send the video URL to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=video_url)

def main():
    # Create an Updater object with your bot's API token
    updater = Updater(token='6089867106:AAH3uZksFJo79Oij9ObeUI11DBVGp6gdaKs', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for the '/start' command and messages
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
