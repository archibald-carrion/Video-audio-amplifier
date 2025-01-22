import tkinter as tk
from frontend import VideoAmplifierGUI

def main():
    root = tk.Tk()
    app = VideoAmplifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()