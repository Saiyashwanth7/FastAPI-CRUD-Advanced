def test_equal():
    assert 3==3
    
def test_not_equal():
    assert 3!=2
    
class Student:
    def __init__(self,firstname,lastname,course,years):
        self.firstname=firstname
        self.lastname=lastname
        self.course=course
        self.years=years

def test_student_object():
    s=Student("Sai","Dasari","AIML",4)
    assert s.firstname=='Sai'
    assert s.lastname=='Dasari'
    assert s.course=='AIML'
    assert s.years==4
    
import pytest
    
@pytest.fixture
def s():
    return Student("Sai Yashwanth","Dasari","AIML",4)

def test_student(s):
    assert s.firstname=='Sai Yashwanth'
    assert s.lastname=='Dasari'
    assert s.course=='AIML'
    assert s.years==4