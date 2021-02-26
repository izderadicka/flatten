from flatten import Pattern


### Tests ###


def test_pattern__basic():
    print("This will fail")
    p = r"Disc \d+/.+\.opus"
    sep = " - "
    pat = Pattern(p, sep)

    assert pat.new_name("Disc 18/03.opus") == "Disc 18 - 03.opus"


    pass