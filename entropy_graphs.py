import matplotlib.pyplot as plt

# Data
categories1 = ['B,R,G', 'B,R,R', 'B,B,B']
values1 = [0.4784936329649067, 0.5047541229928431, 0.4886438096813204]

categories2 = ['B,R,G,Y', 'B,R,G,G', 'B,B,R,R', 'B,R,R,R', 'B,B,B,B']
values2 = [0.39673065124556744, 0.3997827623831965, 0.4159706854984625, 0.4431775470464976, 0.5300951968594705]

categories3 = ['B,R,G,Y,P', 'B,R,G,Y,Y', 'B,R,R,G,G', 'B,R,G,G,G', 'B,B,R,R,R', 'B,R,R,R,R', 'B,B,B,B,B']
values3 = [0.3563877115911314, 0.3390807089218662, 0.3320989312287672, 0.34963719114782105, 0.3578384855575457, 0.39881423212912803, 0.5255209302441819]

fig, axs = plt.subplots(1,3, figsize=(20, 5))

# Create bar plots
axs[0].bar(categories1, values1)
axs[1].bar(categories2, values2)
axs[2].bar(categories3, values3)

# Set titles
axs[0].set_title('First Guess Entropy for Three pegs')
axs[1].set_title('First Guess Entropy for Four pegs')
axs[2].set_title('First Guess Entropy for Five pegs')

# Display the plot
plt.tight_layout()
plt.show()
