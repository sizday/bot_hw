def open_file_name(file_name_answer, file_name_test):
    answer_file = open(file_name_answer)
    answer = file_to_list(answer_file)
    answer_file.close()
    test_file = open(file_name_test)
    test = file_to_list(test_file)
    test_file.close()
    return compare_answer(answer, test)


def open_file(answer_file, test_file):
    """
    answer = file_to_list(answer_file.getvalue())
    test = file_to_list(test_file.getvalue())
    return compare_answer(answer, test), answer, test
    """
    return answer_file.getvalue(), test_file.getvalue(), 0


def file_to_list(answer):
    answer_list = []
    for line in answer:
        if line.endswith('\n'):
            line = line[:-1]
        line = line[3:]
        answer_list.append(line)
    return answer_list


def compare_answer(answer_list, test_list):
    count = 0
    for i in range(len(answer_list)):
        if answer_list[i] == test_list[i]:
            count += 1
    mark = round(count/len(answer_list)*100) // 20
    return mark


# print(open_file_name('text_file/answer.txt', 'text_file/hw_test.txt'))
