from storage.strategy.quiz_storage_strategy import quiz_tsv_file


def load_quiz(quiz_name,strategy=quiz_tsv_file):
    return strategy(quiz_name)

