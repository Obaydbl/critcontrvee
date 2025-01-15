unkw = ",.'! ? ؟,\n"

def toshift(message, c, shift):
    toshift = 1
    shifted = 0
    while True:
        if (message[c - toshift] in unkw):
            toshift += 1
        else:
            shifted += 1
            if shifted == shift:
                return toshift
            toshift += 1

message = input("Enter your message: ")
while(True):
    try:
        shift = int(input("how much shift?: "))
        break
    except ValueError:
        pass

message_cpy = list(message)

for c in range(0, len(message), 1):
    if message[c] in unkw:

        message_cpy[c] = message[c]
    else:
        message_cpy[c - toshift(message, c, shift)] = message[c]

print()
text2 = (''.join(message_cpy)).lower()
print(text2)
with open("Lciphered.txt", "w") as file:
    file.write(text2)
