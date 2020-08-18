import glob
import importlib.util
import os


def main():
    folder = os.path.join('games', '*.py')

    game_modules = {}

    # Thanks Honza for this part of code
    
    for filename in glob.glob(folder):
        module_name = os.path.splitext(os.path.basename(filename))[0]
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        game_modules[module_name] = module

    for name in game_modules.keys():
        print(name)


if __name__ == '__main__':
    main()