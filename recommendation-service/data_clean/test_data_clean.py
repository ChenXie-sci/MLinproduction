from data_clean import data_streaming
import pandas as pd

def data_check(file):
    data = pd.read_csv(file,usecols=[2])
    array = data.to_string().split('\n')
    movie = array[1]
    movie = movie.split(' ')[2]
    n = len(movie)
    movie = movie[0:n-1]
    try:
        if 0 <= int(movie[-1]) <= 5:
            if movie.islower():
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def test_capital_case():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/keeping+the+promise+1997=4'
    assert data_streaming('rate.txt').iloc[0].to_string() == expected

def test_capital_case2():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/a+boy+called+hate+1996=3'
    assert data_streaming('rate.txt').iloc[1].to_string() == expected

def test_capital_case3():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/dead+tired+1994=4'
    assert data_streaming('rate.txt').iloc[2].to_string() == expected

def test_capital_case4():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/le+nouveau+jean-claude+2002=3'
    assert data_streaming('rate.txt').iloc[3].to_string() == expected

def test_capital_case5():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/mrs.+miniver+1942=4'
    assert data_streaming('rate.txt').iloc[4].to_string() == expected

def test_capital_case6():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/thrill+ride+the+science+of+fun+1997=4'
    assert data_streaming('rate.txt').iloc[5].to_string() == expected

def test_capital_case7():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/partysaurus+rex+2012=3'
    assert data_streaming('rate.txt').iloc[6].to_string() == expected

def test_capital_case8():
    expected = 'GET /rate/hey+happy+2001=3    GET /rate/salut+cousin++1996=3'
    assert data_streaming('rate.txt').iloc[7].to_string() == expected

def test_capital_case9():
    assert data_check('test1.txt') == True

def test_capital_case10():
    assert data_check('test2.txt') == False

def test_capital_case11():
    assert data_check('test3.txt') == False