from aiogram.utils import markdown as md


def md_quote(text):
    return md.markdown_decoration.quote(text)


def md_bold(text):
    return md.markdown_decoration.bold(text)


def valid_answer(text: str):
    text = text.replace(' ', '')
    if not text or len(text) > 5:
        return False
    if text.isdigit():
        nums = [int(n) for n in text]
        if min(nums) >= 1 and max(nums) <= 5:
            return True
    return False


def get_correct_answer(task_info: str, word_list: list) -> str:
    correct_options = ''
    for i, word_info in enumerate(task_info.split(';')):
        word_id, is_correct = map(int, word_info.split('.'))
        correct_form, in_correct_form = word_list[word_id][1], word_list[word_id][2]
        if not is_correct:
            correct_options += md_quote(str(i+1) + '. ') + md.strikethrough(in_correct_form) + ' 👉 ' + \
                               md.bold(correct_form) + '\n'
        else:
            correct_options += md_quote(str(i+1) + '. ') + md.bold(correct_form) + '✅' + '\n'
    return correct_options
