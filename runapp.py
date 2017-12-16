# -*- coding: utf-8 -*-

from app import App


if __name__ == '__main__':
    main_app = App()

    try:
        main_app.start()

        while True:
            main_app.loop()

    except Exception as ex:
        print(ex)