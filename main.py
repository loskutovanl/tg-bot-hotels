from loader import bot
import handlers
from utils.set_bot_commands import set_commands
import logging

if __name__ == '__main__':
    logging.basicConfig(filename="bot.log",
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt="%d/%m/%Y %I:%M:%S")
    logging.info("Started")

    set_commands(bot)
    bot.polling(non_stop=True, interval=0)

    logging.info("Finished")
