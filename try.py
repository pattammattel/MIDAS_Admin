from StackCalcs import *
from RefChooser import *
dff,col_name = create_df_from_nor(athenafile='marked2.nor')

w = RefChooser(col_name)
w.show()