import time
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）

df = pd.read_csv('Metadata.csv')
accounts = df['account'].values
names = df['中译'].values
account2name = dict(zip(accounts, names))
token = 'http://api.moemoe.tokyo/anime/v1/twitter/follower/status?accounts='
for account in accounts:
    token += account + ','
token = token[:-2]

with open('201901accounts', 'w') as f:
    f.write(token)

res = pd.read_json(os.popen("curl -v " + token + ' | jq . '))

s = res.iloc[0]
s_names = [account2name[account] for account in s.index]
new_s = pd.Series(list(s), index=s_names)
new_s = new_s.sort_values(ascending=False)

ax = new_s.plot(kind='barh', figsize=(10,7), color="slateblue", fontsize=13);
ax.set_alpha(0.1)
ax.set_title('2019年1月主要新作推特关注数', fontsize=15)
ax.set_xlabel('关注数', fontsize=15);

# set individual bar values
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width() + 100, i.get_y()+0.31, str(round((i.get_width()), 2)), fontsize=15, color='dimgrey')
ax.text(0.6*new_s[0], len(new_s) - 1, '统计时间:{}'.format(time.strftime("%Y-%m-%d", time.localtime())), fontsize=20)

ax.invert_yaxis() # largest at top
fig = ax.get_figure()
fig.savefig('{}.png'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))