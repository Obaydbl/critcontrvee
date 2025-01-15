# how this works:
# it checks if the letter is a bi-lettered element in the table, if so it appends it to ciphers
# and then moves the index by an extra spot to compensate and not double the next letter
# else it checks if its a mono letter
# else it returns the letter itself
import sys
periodic_table = [
    "placeholder, accurating the position in list with position in periodic table.",
    "H", "He",
    "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
    "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt",
    "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf",
    "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]

print("Enter your message, then press CTRL+D:")
message=sys.stdin.read()
ciphered=[]
ciphered2=[]

def periodize(index):
    for e in range(1, 119, 1):
        if message[index:index+2].lower() == periodic_table[e].lower():
            ciphered.append(periodic_table[e])
            ciphered2.append("["+str(e)+"]")
            return 1

    for e in range(1, 119, 1):
        if message[index].lower() == periodic_table[e].lower():
            ciphered.append(periodic_table[e])
            ciphered2.append("["+str(e)+"]")
            return 0

    ciphered.append(message[index])
    ciphered2.append(message[index])
    return 0




def main():
    i = 0
    while i < len(message):
        if(periodize(i)):
            i+=1
        i+=1

    print()
    print(''.join(ciphered))
    print()
    print(''.join(ciphered2))

    with open("periodic_ciphered.txt", "w") as file:
        file.write(''.join(ciphered2))

main()
