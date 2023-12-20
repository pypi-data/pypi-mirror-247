import math
number=540
roundtype = 0
bijlagex = [9.5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 44,
                  48, 52, 56, 60, 65, 70, 75, 80, 85, 90, 95, 100]


digits = int(math.floor(math.log(number, math.e) / math.log(10, math.e)))

tmpnum = number / 10**(digits-1)


if tmpnum < 10 or tmpnum >= 100:
    print("error in rounding")


for i,n in enumerate(bijlagex):
    # print(i)
    # print(n, tmpnum)
    if roundtype == -1:
        if tmpnum == n:
            pos = i
            break
        elif n > tmpnum:

            newnum = n
            pos = i-1
            print(i)
            break
    elif roundtype == 1:
        # print(n, tmpnum)
        if tmpnum == n:
            pos = i
            break
        elif n > tmpnum:
            pos = i
            # print(n,i)
            # print("pos", pos)
            break
    elif roundtype == 0:
        # print((tmpnum - bijlagex[i - 1]), (bijlagex[i] - tmpnum))
        if tmpnum == n:
            pos = i
            break

        elif n > tmpnum:
            if (tmpnum - bijlagex[i-1]) >= (bijlagex[i] - tmpnum):
                pos = i
            else:
                pos = i-1
            break



newnum = bijlagex[pos] * 10**(digits-1)
print(newnum)



# print(roundx(n,roundtype))