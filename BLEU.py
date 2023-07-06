
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

# #referenced & generated sentences 가 완전히 일치하는 경우
# reference = [["this", "is", "the", "sample"]]
# candidate = ["this", "is", "the", "sample"]
# score1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)) #1.0
# print(score1)

# #generated sentence 에서 일치하는 단어가 각각 다른 reference에 있는 경우
# reference = [["this", "is", "the", "good", "choice"], ["it", "is", "a", "sample"]]
# candidate = ["this", "is", "the", "sample"]
# score2 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method3)
# print(score2)

# #generated 문장의 단어가 reference에 포함되지 않은 경우 -> a 하나가 refernece에 들어있지 않기 때문에 4/5가 나옴
# reference = [["this", "is", "the", "sample"], ["this", "is", "the", "good", "sample"]]
# candidate = ["this", "is", "a", "good", "sample"]
# score3 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method3)
# print(score3)

# #여러 개의 문장에 대해서 한번에 계산하고 싶다면,
# from nltk.translate.bleu_score import corpus_bleu
# reference = [[["this", "is", "a", "sample"]], [["another", "sentence"], ["other", "sentence"]]]
# candidate = [["this", "is", "a", "sample"], ["just", "another", "sentence"]]
# score4 = corpus_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method4)
# print(score4)

reference = []
gen_tmp = []
ref_msg = "현재일시 기준으로 결품 상품 정보 안내 드립니다."
gen_msg = "현재일시 기준으로 찾으시는 내용이 'LG 식기세척기 (2명)  2등: LG 코드제로 R5 물걸레 로봇청소기 (4명)  3등: 스마트카라 음식물처리기 PCS 400 (8명) ⚫ CJ 대표행사 상품  CJ) 햇반 작은공기 130g, 햇반 300g 3입, 비비고칩 오리지널 40g, 병아리콩 그레인보울 160g, 맥스봉 프 로틴 45g, 닭가슴살직화스테이크 100g, 맥스봉 팝비엔나 120g, 햇반현미 귀리곤약밥 150g' 맞으실까요? 더 자세한 사항은 아래 문서를 참조해주세요."

end = ["?", "!", "."]

for endStr in end:
    gen = gen_msg.split(endStr)
    gen_tmp.append([gen])

ref_msg = ref_msg.replace(".", "").replace(",", "")
ref = ref_msg.split(" ")
generate = gen_msg.split(" ")

for str in ref:
    reference.append([str])

score5 = sentence_bleu(reference, generate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=SmoothingFunction().method3)
print(score5)