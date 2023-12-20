from bestErrors import OutOfRangeError


def readabform(num):
    abbrs = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Qa",
        "Qt",
        "Sx",
        "Sp",
        "Oc",
        "No",
        "Dc",
        "UDc",
        "DDc",
        "TDc",
        "QaDc",
        "QiDc",
        "SxDc",
        "SpDc",
        "OcDc",
        "NmDc",
        "Vg",
        "UVg",
        "DVg",
        "TVg",
        "QaVg",
        "QiVg",
        "SxVg",
        "SpVg",
        "OcVg",
        "NmVg",
        "Tg",
        "UTg",
        "DTg",
        "TTg",
        "QaTg",
        "QiTg",
        "SxTg",
        "SpTg",
        "OcTg",
        "NmTg",
        "Qa",
        "UQa",
        "DQa",
        "TQa",
        "QaQa",
        "QiQa",
        "SxQa",
        "SpQa",
        "OcQa",
        "NoQa",
        "Qi",
        "UQi",
        "DQi",
        "TQi",
        "QaQi",
        "QiQi",
        "SxQi",
        "SpQi",
        "OcQi",
        "NoQi",
        "Se",
        "USe",
        "DSe",
        "TSe",
        "QaSe",
        "QiSe",
        "SxSe",
        "SpSe",
        "OcSe",
        "NoSe",
        "St",
        "USt",
    ]
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    try:
        return "{} {}".format(
            "{:f}".format(num).rstrip("0").rstrip("."), abbrs[magnitude]
        )
    except Exception as e:
        raise OutOfRangeError(
            "Out of range... (cannot be over USt)\nError Message: {}".format(e)
        )
