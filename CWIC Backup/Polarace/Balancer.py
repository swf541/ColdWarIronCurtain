import pandas as pd
import seaborn as sns
from os import listdir
from os.path import isfile, join

def get_files(path: str) -> list:
    """
    :param path: A directory in which all containing folders will be added to a list
    """
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

#focus_trees = get_files(path='C:/Users/Luke/Documents/GitHub/ColdWarIronCurtain/Cold War Iron Curtain/common/national_focus')

#print(focus_trees)

# def focus_as_csv():
#     focus_tree_columnated = pd.read_csv(focus_trees[0], header=None, delim_whitespace="/t")
#     focus_tree_columnated.columns = ["modifiers", "equals_sign", "values"]
#     return focus_tree_columnated

# test = focus_as_csv()

focus_tree = pd.read_csv('C:/Users/Luke/Documents/GitHub/ColdWarIronCurtain/Cold War Iron Curtain/common/national_focus/50s_DDR.txt', header=None, delim_whitespace="/t")
focus_tree.columns = ["modifiers", "equals_sign", "values"]

focus_tree = (focus_tree
    .query("modifiers.str.contains('manpower')", engine='python')
)

sns.barplot(focus_tree, x=focus_tree.iloc[0], y=focus_tree.iloc[2])

print(focus_tree)


# focus_tree.to_csv('C:/Users/Luke/Documents/GitHub/ColdWarIronCurtain/CWIC Backup/Polarace/ddr.csv')