import os
base_dir = os.path.abspath(os.path.dirname(__file__))

local_db = "sqlite:///%s/test.db" % base_dir

if __name__ == '__main__':
    print local_db
