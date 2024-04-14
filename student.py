import csv
import functools
import argparse
import logging

logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()


class Student:
    def load_findings(self, findings_file):
        with open(findings_file, encoding="utf8", newline='\n') as csvfile:
            subject_reader = csv.reader(csvfile, delimiter=' ', quotechar=',')
            for row in subject_reader:
                self.subjects = {subject: {'test_score': [], 'grade': []} for subject in row[0].split(',')}

    def __init__(self, name, findings_file):
        self.name = name
        self.subjects = {}
        self.load_findings(findings_file)

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.istitle() or not functools.reduce(lambda a, b: a * b, [i.isalpha() for i in value.split()]):
                logger.error('ФИО должно состоять только из букв и начинаться с заглавной буквы')
                raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == 'name':
            return f'{self.name}'
        else:
            raise AttributeError(f'Предмет {name} не найден')

    def __str__(self):
        subjec = list(filter(lambda x: len(self.subjects[x]['grade']) > 0, self.subjects.keys()))
        return f'Студент: {self.name}\nПредметы: {", ".join(subjec)}'

    def add_grade(self, subject, grade):
        if 2 <= grade <= 5:
            if subject in self.subjects.keys():
                self.subjects[subject]['grade'].append(grade)
            else:
                logger.error(f'Предмет {subject} не найден')
                raise ValueError(f'Предмет {subject} не найден')
        else:
            logger.warning('Оценка должна быть целым числом от 2 до 5')

    def add_test_score(self, subject, test_score):
        if 0 < test_score < 100:
            self.subjects[subject]['test_score'].append(test_score)
        else:
            logger.warning('Результат теста должен быть целым числом от 0 до 100')

    def average_score_test(self, subject):
        if subject in self.subjects.keys():
            length = len(self.subjects[subject]['test_score'])
            if length > 0:
                return sum(self.subjects[subject]['test_score'])/length
        else:
            logger.error(f'Предмет {subject} не найден')
            raise ValueError(f'Предмет {subject} не найден')
    def average_grade(self):
        ls = []
        for subject in self.subjects.keys():
            length = len(self.subjects[subject]['grade'])
            if length > 0:
                ls.append(sum(self.subjects[subject]['grade']) / length)
        newLst = list(filter(lambda x: x is not None, ls))
        length = len(newLst)
        if length > 0:
            return sum(newLst)/length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('nameFile', type=str, nargs='*', help='выберите файл')
    args = parser.parse_args()
    logger.info(f'Передано: {args}')
    if args.nameFile:
        NameFileCsv = args.fileName[0]
        logger.info(f'Имя файла: {args.fileName[0]}')
    else:
        NameFileCsv = 'subjects.csv'
        logger.info(f'Не переданы аргументы: {NameFileCsv}')

    student = Student('Иван Васильевич', NameFileCsv)

    student.add_grade('Литература', 3)
    student.add_test_score('Литература', 45)

    student.add_grade('Математика', 4)
    student.add_test_score('Математика', 89)

    average_grade = student.average_grade()
    logger.info(f'Средний балл: {average_grade}')

    average_test_score = student.average_score_test('Математика')
    logger.info(f'Средний бал по математике: {average_test_score}')

    logger.info(student)

if __name__ == '__main__':
    main()