from StackCalcs import *
from RefChooser import *
dff,col_name = create_df_from_nor(athenafile='marked2.nor')

elist = pd.read_csv('Site4um.txt', header=None)

new_ref = interploate_E(dff.values,elist.values)

print(elist.head())