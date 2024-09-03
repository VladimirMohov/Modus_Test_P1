class StartMessage(object):

    @staticmethod
    def old(object):
        return """<b><i>👋 Здравствуйте, @{1}</i></b>!\n\n
            ➖➖➖➖➖➖➖➖➖➖➖➖\n
            <b>ℹ️ Информация о вас:</b>\n\n
            📇 Мой ID: <u>{0}</u>\n""".format(*object)