import logging

# cbv - Current Book Value
# obv - Old Book Value
# years - Number of years between old and current book value
def calc_avg_bv_change_pc(cbv, obv, years):
	upper = 1/years
	base = cbv/obv
	a = pow(base,upper)
	bvcp = 100*(a-1)
	return bvcp

# div_per_year - average dividend amount per year
# cbv - current book value
# bvcp - average book value change percentage. Can be calculated from calc_avg_bv_change_pc
# years - duration of a zero-risk investment
# rate - rate of interest (as percentage value) of zero-risk investment
def calc_intrinsic_value(div_per_year, cbv, bvcp, years, rate):
	perc = (1 + bvcp / 100)
	base = pow(perc, years)
	parr = cbv * base
	rate = rate / 100
	extra = pow((1 + rate), years)
	iv = (div_per_year) * (1 - (1 / extra)) / (rate + (parr / extra))
	return iv
