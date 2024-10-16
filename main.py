from decimal import Decimal as dec
from fractions import Fraction as frac
from math import pow


"""Расчет в соответствии с Методами расчетов рассеивания вредных веществ"""


def max_concentration(
    M, F: int, H: dec, V1: dec, Tc: dec, w0: dec, L: dec, b: dec
) -> dec:
    Ta = dec("24.5")
    dT = abs(Tc - Ta)
    d = diameter(L, b)
    vmap_var = vmap(w0, d, H)
    f_var = f(w0, d, H, dT, vmap_var)
    vm_var = vm(V1, dT, H)
    m_var = m(f_var)
    n_var = n(f_var, vm_var, vmap_var)
    if f_var < 100 or not (0 <= dT < dec("0.5")):
        return dec(180 * M * F * m_var * n_var / H**2 * dec(pow((V1 * dT), 1 / 3)))
    elif vmap_var >= dec("0.5"):
        return dec(180 * M * F * n_var * K(d, V1) / dec(pow(H, dec(4) / dec(3))))
    else:
        return dec(180 * M * F * Map(vm_var, m_var) / dec(pow(H, (dec(7) / dec(3)))))


def m(f: dec) -> dec:
    if f < 100:
        return dec(
            1
            / (
                dec("0.67")
                + dec("0.1") * dec(pow(f, dec("0.5")))
                + dec("0.34") * dec(pow(f, dec(dec(1) / dec(3))))
            )
        )
    else:
        return dec(dec("1.47") / dec(pow(f, dec(dec(1) / dec(3)))))


def n(f: dec, vm: dec, vmap: dec) -> dec:
    if f >= 100:
        vm = vmap
    if vm < dec("0.5"):
        return dec(4.4)
    elif dec("0.5") <= vm < 2:
        return dec(dec("0.532") * dec(pow(vm, 2)) - dec("2.13") * vm + dec("3.13"))
    else:
        return 1


def f(w0: dec, D: dec, H: dec, dT: dec, vmap: dec) -> dec:
    f = dec(dec(1000 * dec(pow(w0, 2)) * D) / dec(dec(pow(H, 2)) * dT))
    fe_var = fe(vmap)
    if fe_var < f < 100:
        return fe_var
    else:
        return f


def fe(vmap: dec) -> dec:
    return dec(800 * vmap**3)


def vmap(w0: dec, D: dec, H: dec) -> dec:
    return dec(dec("1.3") * w0 * D / H)


def vm(V1: dec, dT: dec, H: dec) -> dec:
    return dec("0.65") * dec(pow((V1 * dT / H), 1 / 3))


def K(D: dec, V1: dec) -> dec:
    return dec(D / 8 * V1)


def Map(vm: dec, m: dec) -> dec:
    if vm < dec("0.5"):
        return dec("2.86") * m
    else:
        return dec("0.9")


def diameter(L: dec, b: dec) -> dec:
    if L == b:
        return L
    else:
        return 2 * L * b / (L + b)


def xm(F: int, H: dec, Tc: dec, w0: dec, L: dec, b: dec, V1: dec) -> dec:
    Ta = dec("24.5")
    dT = Tc - Ta
    D = diameter(L, b)
    vmap_var = vmap(w0, D, H)
    if 0 <= vmap_var < 0.5 and -0.5 <= dT <= 0:
        return dec(dec("5.7") * H)
    dT = abs(dT)
    vm_var = vm(V1, dT, H)
    f_var = f(w0, D, H, dT, vmap_var)
    fe_var = fe(vmap_var)
    d = d_func(f_var, vm_var, fe_var, dT, vmap_var)
    return dec(dec(5 - F) / dec(4) * d * H)


def d_func(f: dec, vm: dec, fe: dec, dT: dec, vmap: dec) -> dec:
    if f < 100 and 0 <= dT <= 0.5:
        if vm <= 0.5:
            return dec(
                dec("2.48") * (1 + dec("0.28") * dec(pow(fe, dec(dec(1) / dec(3)))))
            )
        elif vm <= 2:
            return dec(
                dec("4.95") * vm * (1 + dec("0.28") * dec(pow(f, dec(dec(1) / dec(3)))))
            )
        else:
            return dec(
                7 * vm**0.5 * (1 + dec("0.28") * dec(pow(f, dec(dec(1) / dec(3)))))
            )
    else:
        if vmap <= 0.5:
            return dec("5.7")
        elif vmap <= 2:
            return dec(dec("11.4") * vmap)
        else:
            return dec(16 * vmap**0.5)


def um(L: dec, b: dec, Tc: dec, w0: dec, H: dec, V1: dec) -> dec:
    D = diameter(L, b)
    Ta = dec("24.5")
    dT = Tc - Ta
    vmap_var = vmap(w0, D, H)
    if 0 <= vmap_var < 0.5 and -0.5 <= dT <= 0:
        return dec(0.5)
    dT = abs(dT)
    f_var = f(w0, D, H, dT, vmap_var)
    vm_var = vm(V1, dT, H)
    if f_var >= 100 or 0 <= dT <= 0.5:
        if vmap_var <= 0.5:
            return dec(0.5)
        elif vmap_var <= 2:
            return vmap_var
        else:
            return vmap_var * dec("2.2")
    if vm_var <= 0.5:
        return dec(0.5)
    elif vm_var <= 2:
        return vm_var
    else:
        return vm_var * (1 + dec("0.12") * f_var**0.5)


if __name__ == "__main__":
    with open("master project/dlya_rasschetov.txt", encoding="utf-8") as inp, open(
        "master project/output.txt", "w", encoding="utf-8"
    ) as out:
        inp.readline()
        inp.readline()
        inp.readline()
        inp.readline()
        print(
            "Номер источника",
            "Код ЗВ",
            "Наименование ЗВ",
            "Максимальная концентрация, мг/м3",
            "Опасная скорость ветра, м/с",
            "Расстояние от источника, м",
            sep=";",
            file=out,
        )
        for row in inp:
            row_as_list = row.split(";")
            source = {
                "num_of_source": row_as_list[0],
                "height": row_as_list[1],
                "length": row_as_list[2],
                "width": row_as_list[3],
                "speed": row_as_list[4],
                "flow": row_as_list[5],
                "temperature": row_as_list[6],
                "code_of_pollutant": row_as_list[7],
                "name_of_pollutant": row_as_list[8],
                "f_speed_of_deposition": row_as_list[9],
                "power_of_release": row_as_list[10],
            }
            # if row_as_list[7] not in ["330", "337", "301", "304"]:
            #     continue
            # print(f"Номер источника: {row_as_list[0]}", file=out)
            # print(f"Код ЗВ: {row_as_list[7]}", file=out)
            # print(f"Наименование ЗВ: {row_as_list[8]}", file=out)
            cm = max_concentration(
                dec(source["power_of_release"]),
                int(source["f_speed_of_deposition"]),
                dec(source["height"]),
                dec(source["flow"]),
                dec(source["temperature"]),
                dec(source["speed"]),
                dec(source["length"]),
                dec(source["width"]),
            )
            distance = xm(
                int(source["f_speed_of_deposition"]),
                dec(source["height"]),
                dec(source["temperature"]),
                dec(source["speed"]),
                dec(source["length"]),
                dec(source["width"]),
                dec(source["flow"]),
            )
            wind_speed = um(
                dec(source["length"]),
                dec(source["width"]),
                dec(source["temperature"]),
                dec(source["speed"]),
                dec(source["height"]),
                dec(source["flow"]),
            )
            print(
                source["num_of_source"],
                source["code_of_pollutant"],
                source["name_of_pollutant"],
                cm,
                wind_speed,
                distance,
                sep=";",
                file=out,
            )
            # print(f"Максимальная концентрация: {cm}, мг/м3", file=out)
            # print(file=out)
