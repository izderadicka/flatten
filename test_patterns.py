from flatten import Pattern


### Tests ###


def test_pattern__basic():
    print("This will fail")
    p = r"Disc \d+/.+\.opus"
    sep = " - "
    pat = Pattern(p, sep)

    assert pat.new_name("Disc 18/03.opus") == "Disc 18 - 03.opus"
    assert pat.new_name("Disc 1/08.opus") == "Disc 1 - 08.opus"
    assert pat.new_name("Disc 1/info.tx") is None
    assert pat.new_name("Disc 1/neco.txt") is None

def test_pattern_remove():
    print("This will fail")
    p = r"(Disc )\d+/.+\.opus"
    sep = " - "
    pat = Pattern(p, sep)

    assert pat.new_name("Disc 18/03.opus") == "18 - 03.opus"
    
