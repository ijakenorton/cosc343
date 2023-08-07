import re

data = """
Sample: 0.01, Lower bound: 300
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 250.56195545196533
Sample: 0.01, Lower bound: 400
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 262.32014632225037
Sample: 0.01, Lower bound: 500
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 259.22157740592957
Sample: 0.01, Lower bound: 600
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 261.08715319633484
Sample: 0.01, Lower bound: 700
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 260.6836097240448
Sample: 0.01, Lower bound: 800
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 258.16564655303955
Sample: 0.01, Lower bound: 900
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 259.81779408454895
Sample: 0.05, Lower bound: 300
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 257.7449507713318
Sample: 0.05, Lower bound: 400
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 259.3352930545807
Sample: 0.05, Lower bound: 500
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 257.39712595939636
Sample: 0.05, Lower bound: 600
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 257.43964529037476
Sample: 0.05, Lower bound: 700
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 256.8101568222046
Sample: 0.05, Lower bound: 800
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 257.00703620910645
Sample: 0.05, Lower bound: 900
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 257.7362458705902
Sample: 0.1, Lower bound: 300
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 256.79678869247437
Sample: 0.1, Lower bound: 400
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 256.4346466064453
Sample: 0.1, Lower bound: 500
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 257.6855685710907
Sample: 0.1, Lower bound: 600
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 259.51310300827026
Sample: 0.1, Lower bound: 700
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 257.7303810119629
Sample: 0.1, Lower bound: 800
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 256.491840839386
Sample: 0.1, Lower bound: 900
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 258.831773519516
Sample: 0.2, Lower bound: 300
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 257.32952213287354
Sample: 0.2, Lower bound: 400
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 257.2199492454529
Sample: 0.2, Lower bound: 500
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 256.49737882614136
Sample: 0.2, Lower bound: 600
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 256.5583109855652
Sample: 0.2, Lower bound: 700
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 253.98967361450195
Sample: 0.2, Lower bound: 800
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 256.27025055885315
Sample: 0.2, Lower bound: 900
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 254.33030891418457
Sample: 0.3, Lower bound: 300
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 254.24397540092468
Sample: 0.3, Lower bound: 400
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 255.00421619415283
Sample: 0.3, Lower bound: 300
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 243.5371549129486
Sample: 0.3, Lower bound: 400
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 255.62688755989075
Sample: 0.3, Lower bound: 500
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 260.07699823379517
Sample: 0.3, Lower bound: 600
Round 500/500 | Avg score: 4.80 | Avg time/game: 0.5 s Total expected time: 266.12309074401855
Sample: 0.3, Lower bound: 700
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 263.4785933494568
Sample: 0.3, Lower bound: 800
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 268.7733495235443
Sample: 0.3, Lower bound: 900
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 265.37500166893005
Sample: 0.4, Lower bound: 300
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 265.15859150886536
Sample: 0.4, Lower bound: 400
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 267.05470728874207
Sample: 0.4, Lower bound: 500
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 265.734947681427
Sample: 0.4, Lower bound: 600
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 266.1185004711151
Sample: 0.4, Lower bound: 700
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 265.402498960495
Sample: 0.4, Lower bound: 800
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 265.42645835876465
Sample: 0.4, Lower bound: 900
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 267.7906503677368
Sample: 0.5, Lower bound: 300
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 270.03368973731995
Sample: 0.5, Lower bound: 400
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.6 s Total expected time: 277.1805100440979
Sample: 0.5, Lower bound: 500
Round 500/500 | Avg score: 4.80 | Avg time/game: 0.5 s Total expected time: 272.74782514572144
Sample: 0.5, Lower bound: 600
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 268.3822224140167
Sample: 0.5, Lower bound: 700
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 270.78865361213684
Sample: 0.5, Lower bound: 800
Round 500/500 | Avg score: 4.73 | Avg time/game: 0.5 s Total expected time: 269.5309636592865
Sample: 0.5, Lower bound: 900
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 267.3947422504425
Sample: 0.6, Lower bound: 300
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 267.8988082408905
Sample: 0.6, Lower bound: 400
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 268.334664106369
Sample: 0.6, Lower bound: 500
Round 500/500 | Avg score: 4.77 | Avg time/game: 0.5 s Total expected time: 270.46358919143677
Sample: 0.6, Lower bound: 600
Round 500/500 | Avg score: 4.70 | Avg time/game: 0.5 s Total expected time: 268.28271555900574
Sample: 0.6, Lower bound: 700
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 272.61152172088623
Sample: 0.6, Lower bound: 800
Round 500/500 | Avg score: 4.73 | Avg time/game: 0.5 s Total expected time: 266.53843426704407
Sample: 0.6, Lower bound: 900
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 269.77204990386963
Sample: 0.7, Lower bound: 300
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 269.4015564918518
Sample: 0.7, Lower bound: 400
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 269.481929063797
Sample: 0.7, Lower bound: 500
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 269.12932300567627
Sample: 0.7, Lower bound: 600
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 268.7834270000458
Sample: 0.7, Lower bound: 700
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 270.4876232147217
Sample: 0.7, Lower bound: 800
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 268.47736978530884
Sample: 0.7, Lower bound: 900
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 270.02819204330444
Sample: 0.8, Lower bound: 300
Round 500/500 | Avg score: 4.81 | Avg time/game: 0.5 s Total expected time: 269.5380549430847
Sample: 0.8, Lower bound: 400
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 267.2695240974426
Sample: 0.8, Lower bound: 500
Round 500/500 | Avg score: 4.80 | Avg time/game: 0.5 s Total expected time: 270.6505091190338
Sample: 0.8, Lower bound: 600
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 268.46295380592346
Sample: 0.8, Lower bound: 700
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 267.6710512638092
Sample: 0.8, Lower bound: 800
Round 500/500 | Avg score: 4.76 | Avg time/game: 0.5 s Total expected time: 267.20979285240173
Sample: 0.8, Lower bound: 900
Round 500/500 | Avg score: 4.74 | Avg time/game: 0.5 s Total expected time: 270.5145857334137
Sample: 0.9, Lower bound: 300
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 267.9156973361969
Sample: 0.9, Lower bound: 400
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 269.0197193622589
Sample: 0.9, Lower bound: 500
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 273.51514196395874
Sample: 0.9, Lower bound: 600
Round 500/500 | Avg score: 4.78 | Avg time/game: 0.5 s Total expected time: 268.0191173553467
Sample: 0.9, Lower bound: 700
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.6 s Total expected time: 274.9988250732422
Sample: 0.9, Lower bound: 800
Round 500/500 | Avg score: 4.75 | Avg time/game: 0.5 s Total expected time: 271.8913998603821
Sample: 0.9, Lower bound: 900
Round 500/500 | Avg score: 4.79 | Avg time/game: 0.5 s Total expected time: 270.5533685684204
"""

lines = data.split("\n")
lines = [line for line in lines if line]

results = []

for i in range(0, len(lines), 2):
    sample_line = lines[i]
    sample = re.search(r"Sample: (.*?),", sample_line).group(1)
    lower_bound = re.search(r"Lower bound: (.*?)$", sample_line).group(1)

    if i + 1 < len(lines):
        round_line = lines[i+1]
        avg_score = re.search(r"Avg score: (.*?) \|", round_line).group(1)
        total_expected_time = re.search(r"Total expected time: (.*?)$", round_line).group(1)

        result_dict = {
            'sample': float(sample),
            'lower_bound': int(lower_bound),
            'score': float(avg_score),
            'time': float(total_expected_time)
        }

        results.append(result_dict)

for res in results:
    print(res)
