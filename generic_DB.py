from config import *


class GenericDB:

    def open(self, *args, **kwargs):
        assert False

    def close(self):
        assert False

    def connection(self, *args, **kwargs):
        assert False

    def table_exist(self, table=TABLE):
        assert False

    def table_type(self, table=TABLE):
        assert False

    def drop_table(self, table=TABLE):
        assert False

    def create_table(self, format, table=TABLE):
        assert False

    def append_line(self, line, table=TABLE):
        assert False

    def append_lines(self, tab, table=TABLE):
        assert False

    def __enter__(self, *args, **kwargs):
        return self.open(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()
