from bin import global_var as g


def decorate():
    print("\n ____________________________________________________________________ ")
    print("|     _ _________   ______________  ________  _____    _   ____  __  |\n"
          "|    (_) ____/   | / ___/_  __/   |/_  __/ / / /   |  / | / / / / /  |\n"
          "|   / / /_  / /| | \__ \ / / / /| | / / / /_/ / /| | /  |/ / / / /   |\n"
          "|  / / __/ / ___ |___/ // / / ___ |/ / / __  / ___ |/ /|  / /_/ /    |\n"
          "| /_/_/   /_/  |_/____//_/ /_/  |_/_/ /_/ /_/_/  |_/_/ |_/\____/     |")
    print(" ———————————————————————————————————————————————————————————————————— \n")
    print(" ____________________________________________________________________ \n"
          "|                                                                    |\n"
          "|                     A product of Hugh and Phat                     |\n"
          "|                        Version: " + g.get_current_version() + "                              |\n"
                                                                                    " ———————————————————————————————————————————————————————————————————— \n")
