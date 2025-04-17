from flask import Flask

from Web_Layer.map_api import MapAPI



def main():
    api = MapAPI()
    api.run()


if __name__ == '__main__':
    main()