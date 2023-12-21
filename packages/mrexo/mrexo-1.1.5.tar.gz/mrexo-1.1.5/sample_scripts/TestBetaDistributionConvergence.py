from mrexo.mle_utils_nd import _PDF_Beta, _PDF_Normal
import matplotlib.pyplot as plt
import numpy as np


def TestConvergence(a, b):

	x = np.linspace(0, 1 , 500)

	NormalMean = a/(a+b)
	NormalSigma = np.sqrt((a*b)/(((a+b)**2) * (1+a+b)))

	normalpdf = _PDF_Normal(x, NormalMean, NormalSigma)
	betapdf = _PDF_Beta(x, a, b)


	plt.plot(x, normalpdf, c='r', lw=2)
	plt.plot(x, betapdf, c='b', lw=3)
	plt.plot(x, betapdf - normalpdf)
	plt.text(NormalMean, np.max(normalpdf)*1.1, "({}, {}): SSE = {:.2f}".format(a, b, np.sum((normalpdf-betapdf)**2)), size=15)


	# plt.ylim(-0.5, np.max(_PDF_Normal(x, NormalMean, NormalSigma))*1.2)

TestConvergence(10, 10)
TestConvergence(50, 50)
TestConvergence(70, 70)
TestConvergence(100, 50)
TestConvergence(50, 100)
TestConvergence(50, 120)
# TestConvergence(50, 140)
# TestConvergence(200, 200)

plt.title("Blue: Beta +  Red: Normal")
plt.show(block=False)

