from mean_shift import mean_shift
from norm_cut import norm_cut
from split_and_merge import split_and_merge

INPUT_IMG = 'chen_64.jpg'
name = INPUT_IMG.split('.')[0]

# square
# split_and_merge(INPUT_IMG, name + '_split_and_merge.png')

# infinite 
# norm_cut(INPUT_IMG, name + '_output_norm_cut.png')

# 
mean_shift(INPUT_IMG, name + '_output_mean_shift.png')
