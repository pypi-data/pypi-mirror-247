from colorama import Fore, init

init(autoreset=True)

# ASCII art lines with different colors
lines = [
    f"{Fore.RED}██████╗    ██╗  ██╗    █████╗    ██╗",
    f"{Fore.GREEN}██╔══██╗   ██║  ██║   ██╔══██╗   ██║",
    f"{Fore.YELLOW}██████╔╝   ███████║   ███████║   ██║",
    f"{Fore.BLUE}██╔══██╗   ██╔══██║   ██╔══██║   ██║",
    f"{Fore.MAGENTA}██████╔╝██╗██║  ██║██╗██║  ██║██╗██║",
    f"{Fore.CYAN}╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝",
    f"",
    f"                 {Fore.BLUE}Made By {Fore.WHITE}:{Fore.MAGENTA} HK4CRPRASAD",
    f" {Fore.RED}B{Fore.WHITE}.{Fore.YELLOW}H{Fore.WHITE}.{Fore.GREEN}A{Fore.WHITE}.{Fore.BLUE}I {Fore.WHITE}- {Fore.CYAN}Best High Quality Artificial Intelligence",
]

# Print each line
def logo():
    for line in lines:
        print(line)