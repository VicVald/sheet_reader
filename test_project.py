from project import askUntilValid, prompts, answerSheetStructure
from unittest.mock import patch

def main():
    test_askUntilValid()
    test_prompts()
    test_answerSheetStructure()

def test_askUntilValid():
    with patch('builtins.input', return_value=1):
        assert askUntilValid("Quantas questões tem a prova? ", "Digite um número válido de questões! (1-15)", lambda x: 0 < x <= 15) == 1
    with patch('builtins.input', return_value=16):
        assert askUntilValid("Quantas questões tem a prova? ", "Digite um número válido de questões! (1-15)", lambda x: 0 < x <= 15) == "Digite um número válido de questões! (1-15)"

    with patch('builtins.input', return_value='d'):
        assert askUntilValid("Até qual letra vão as questões? ", "Digite um valor válido de letras! (D ou E)", lambda x: x.upper() in ['D', 'E']) == 'd'
    with patch('builtins.input', return_value='f'):
        assert askUntilValid("Até qual letra vão as questões? ", "Digite um valor válido de letras! (D ou E)", lambda x: x.upper() in ['D', 'E']) == "Digite um valor válido de letras! (D ou E)"

    
    with patch('builtins.input', return_value='f'):
        assert askUntilValid("Digite a resposta da questão 1: ", "Digite uma resposta válida! (A, B, C, D ou E)", lambda x: x.upper() in ['A', 'B', 'C', 'D', 'E']) == "Digite uma resposta válida! (A, B, C, D ou E)"
    with patch('builtins.input', return_value='a'):
        assert askUntilValid("Digite a resposta da questão 1: ", "Digite uma resposta válida! (A, B, C, D ou E)", lambda x: x.upper() in ['A', 'B', 'C', 'D', 'E']) == 'a'


def test_prompts():
    with patch('builtins.input', side_effect=[2, 'E', 'A', 'B']):
        assert prompts() == (2, 5, ['1A', '2B'])
    with patch('builtins.input', side_effect=[1, 'D', 'C']):
        assert prompts() == (1, 4, ['1C'])


def test_answerSheetStructure():
    assert answerSheetStructure(1, 4) == [(48, 0, 48, 25), (96, 0, 48, 25), (144, 0, 48, 25), (192, 0, 48, 25)]
    assert answerSheetStructure(2, 4) == [(48, 0, 48, 25), (96, 0, 48, 25), (144, 0, 48, 25), (192, 0, 48, 25), (48, 26.5, 48, 25), (96, 26.5, 48, 25), (144, 26.5, 48, 25), (192, 26.5, 48, 25)]
    assert answerSheetStructure(1, 5) == [(48, 0, 48, 25), (96, 0, 48, 25), (144, 0, 48, 25), (192, 0, 48, 25), (240, 0, 48, 25)]
    assert answerSheetStructure(2, 5) == [(48, 0, 48, 25), (96, 0, 48, 25), (144, 0, 48, 25), (192, 0, 48, 25), (240, 0, 48, 25), (48, 26.5, 48, 25), (96, 26.5, 48, 25), (144, 26.5, 48, 25), (192, 26.5, 48, 25), (240, 26.5, 48, 25)]


if __name__ == "__main__":
    main()