from applications.application import Application


class UnsafeDecorator(Application):
    def __init__(self, app):
        self.__app = app

    def exec(self, args, in_stream, out_stream):
        try:
            self.__app.exec(args, in_stream, out_stream)
        except Exception as error:
            out_stream.append(str(error) + "\n")
