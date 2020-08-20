import glob
import importlib.util
import os


def main():
    choice = 0
    while choice == 0:
        folder = os.path.join('projects', '*.py')

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
        pick = input("Choose module you'd like to play: ")
        game_modules[pick].play()

        x = input("Would you like to play something else (y) or end? (n) > ")
        if x == "y":
            pass
        elif x == "n":
            choice = 1
        else:
            print("I have crashed...")

if __name__ == '__main__':
    main()