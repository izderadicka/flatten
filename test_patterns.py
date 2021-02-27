from flatten import Pattern, PatternError
import pytest


### Tests ###


def test_pattern__basic():
    p = r"Disc \d+/.+\.opus"
    sep = " - "
    pat = Pattern(p, sep)

    assert pat.new_name("Disc 18/03.opus") == "Disc 18 - 03.opus"
    assert pat.new_name("Disc 1/08.opus") == "Disc 1 - 08.opus"
    assert pat.new_name("Disc 1/info.tx") is None
    assert pat.new_name("Disc 1/neco.txt") is None

def test_pattern_remove():
    p = r"(Disc )\d+/.+\.opus"
    sep = " - "
    pat = Pattern(p, sep)

    assert pat.new_name("Disc 18/03.opus") == "18 - 03.opus"

def test_glob_pattern1():
    p = r"**/(Disc )\d+/.+\.opus"
    sep = "-"
    pat = Pattern(p, sep)
    assert pat.new_name('usak/kulisak/Disc 01/neco 03.opus') == '01-neco 03.opus'

def test_glob_pattern2():
    p = r"(Disc )\d+/**/.+\.opus"
    sep = "-"
    pat = Pattern(p, sep)
    assert pat.new_name('Disc 01/usak/kulisak/neco 03.opus') == '01-neco 03.opus'

def test_glob_pattern3():
    p = r"(Disc )\d+/*/*/.+\.opus"
    sep = "-"
    pat = Pattern(p, sep)
    assert pat.new_name('Disc 01/usak/kulisak/neco 03.opus') == '01-neco 03.opus'    


def test_glob_pattern4():
    p = r"(Disc )\d+/**/.+\.opus"
    sep = "-"
    pat = Pattern(p, sep)
    assert pat.new_name('Disc 01/usak/kulisak/neco 03.mp3') is None    


def test_pattern_fail():
    p = r"(Disc )\d+/**/.++\.opus"
    sep = "-"
    with pytest.raises(PatternError):
        _pat = Pattern(p, sep)

    p = r"(Disc )\d+/**/*"
    sep = "-"
    with pytest.raises(PatternError):
        _pat = Pattern(p, sep)
    