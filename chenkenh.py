import warnings
from src import Application

def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    App = Application()
    App.run()

if __name__ == "__main__":
    main()