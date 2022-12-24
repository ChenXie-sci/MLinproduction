from main import mean
from main import getRecommendation

def testGetRecommendation():
    duration = getRecommendation(12)
    assert duration is not None

def testMean():
    avg = mean()
    assert avg is not None