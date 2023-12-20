import g4f7
import g4f7.api

if __name__ == "__main__":
    print(f'Starting server... [g4f v-{g4f7.version}]')
    g4f7.api.Api(engine = g4f7, debug = True).run(ip = "0.0.0.0:10000")
