from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import STREAM_MODE, URL, LOG_CHANNEL
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
import humanize

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    if not STREAM_MODE:
        return await message.reply("**Streaming is disabled.**")

    # Ask user for file
    msg = await client.ask(
        message.chat.id, 
        "**Now send me your file/video to generate stream and download links.**"
    )

    # Check if valid media
    if not msg.media or msg.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        return await message.reply("**Please send a valid video or document.**")

    # Extract file details
    file = getattr(msg, msg.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention

    # Send media to log channel and get message ID
    log_msg = await client.send_cached_media(chat_id=LOG_CHANNEL, file_id=fileid)
    encoded_file_name = quote_plus(get_name(log_msg))
    file_hash = get_hash(log_msg)

    # Generate URLs
    stream_url = f"{URL}watch/{log_msg.id}/{encoded_file_name}?hash={file_hash}"
    download_url = f"{URL}{log_msg.id}/{encoded_file_name}?hash={file_hash}"

    # Buttons
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🖥 Stream", url=stream_url)],
            [InlineKeyboardButton("📥 Download", url=download_url)],
        ]
    )

    # Send response to user
    await message.reply_text(
        text=f"**𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱!**\n\n"
             f"📂 **File Name:** `{filename}`\n"
             f"📦 **File Size:** `{filesize}`\n\n"
             f"👇 **Choose an option below:**",
        reply_markup=buttons,
        disable_web_page_preview=True
    )
