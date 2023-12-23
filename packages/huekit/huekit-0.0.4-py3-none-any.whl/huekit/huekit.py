def color(clr):
    colors = {
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "brown": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "light_gray": "\033[0;37m",
        "dark_gray": "\033[1;30m",
        "light_red": "\033[1;31m",
        "light_green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "light_blue": "\033[1;34m",
        "light_purple": "\033[1;35m",
        "light_cyan": "\033[1;36m",
        "white": "\033[0m"
    }

    try:
        return(colors[clr])
    except KeyError:
        print(f"\033[1;33mInvalid Argument: '{clr}' is not a text color.\nConsequence: Text will be printed without changes.\033[0m")
        return("")

def style(styl):
    styles = {
        "bold": "\033[1m",
        "faint": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "negative": "\033[7m",
        "crossed": "\033[9m"
    }

    try:
        return(styles[styl])
    except KeyError:
        print(f"\033[1;33mInvalid Argument: '{styl}' is not a text style.\nConsequence: Text will be printed without changes.\033[0m")
        return("")
    
def colors():
    print("\033[0;30mblack\n\033[0;31mred\n\033[0;32mgreen\n\033[0;33mbrown\n\033[0;34mblue\n\033[0;35mpurple\n\033[0;36mcyan\n\033[0;37mlight_gray\n\033[1;30mdark_gray\n\033[1;31mlight_red\n\033[1;32mlight_green\n\033[1;33myellow\n\033[1;34mlight_blue\n\033[1;35mlight_purple\n\033[1;36mlight_cyan\n\033[0mwhite")

def styles():
    print("\033[1mbold\033[0m\n\033[2mfaint\033[0m\n\033[3mitalic\n\033[4munderline\033[0m\n\033[5mblink\033[0m\n\033[7mnegative\033[0m\n\033[9mcrossed\033[0m")

if __import__("platform").system() == "Windows":
    kernel32 = __import__("ctypes").windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    del kernel32