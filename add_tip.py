from model import DailyTip


tips_fa = list()
tips_en = list()

with open("tip.fa.txt") as fp:
    tips_fa = fp.read().split("\n")

with open("tip.en.txt") as fp:
    tips_en = fp.read().split("\n")

i = 0
for tip_fa, tip_en in zip(tips_fa, tips_en):
    DailyTip.create(
        id = i,
        tip_en = tip_en,
        tip_fa = tip_fa,
    )
    print(i)
    i += 1
