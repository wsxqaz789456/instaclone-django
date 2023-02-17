from django.test import TestCase
from colorama import Fore, Style

# Create your tests here.
def message(msg):
    print(Fore.MAGENTA, Style.BRIGHT, "\b\b\b[#]", Fore.RED, msg, Style.RESET_ALL)
