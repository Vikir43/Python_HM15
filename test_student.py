from student import Student


def test_name():
    st = Student('Иван Васильевич', 'subjects.csv')
    assert st.name == 'Иван Васильевич'


def adding_student_list():
    st = Student('Иван Васильевич', 'subjects.csv')
    st.add_grade('Литература', 3)
    st.add_test_score("Литература", 45)
    st.add_grade('Математика', 4)
    st.add_test_score('Математика', 89)
    return st


def test_average_grade():
    st = adding_student_list()
    average_grade = st.average_grade()
    assert average_grade == 3.5


def test_average_score_test():
    st = adding_student_list()
    average_test_score = st.average_score_test('Математика')
    assert average_test_score == 89.0