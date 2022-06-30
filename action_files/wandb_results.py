import pandas as pd
from tabulate import tabulate
import os
import requests

nwo = os.getenv('GITHUB_REPOSITORY')
token = os.getenv('GITHUB_TOKEN')
pr_num = os.getenv('PR_NUM')

# you changed directories in the action so it will be here
df = pd.read_csv('wandb_report.csv')

print(f'Formatting Results For PR Number: {pr_num}')

entity_name = df['run.entity'].iloc[0]
proj_name = df['run.project'].iloc[0]
proj_url = f"https://app.wandb.ai/{entity_name}/{proj_name}"

def reformat_df(df):
    # add links to run id
    df['Run ID'] = df.apply(lambda x: "["+x['run.id']+"]("+x['run.url'] +")", axis=1)
    # remove brackets run tags
    df['run.tags'] = df['run.tags'].str.get(0)
    # select columns
    clean_df = df[['run.tags', 'Run ID', 'eval/loss', 'eval/accuracy', '_num_train_epochs', '_num_hidden_layers']].round(3)
    # rename columns
    clean_df.columns=['Category', 'Run ID', 'Val Loss', 'Val Acc', 'Epochs', 'Hidden Layers']
    # emphasize candidate runs
    clean_df.loc[clean_df.Category == 'candidate'] = clean_df[clean_df.Category == 'candidate'].apply(lambda x: ['**'+str(x)+'**' for x in x.values])
    return clean_df

clean_df = reformat_df(df)
# clean_df = df
table = tabulate(clean_df, tablefmt="github", headers="keys", showindex=False)
message = f"### Model Evaluation Results\n\n{table}\n\nResults queried from W&B project [{entity_name}/{proj_name}]({proj_url})"

print(message)

headers = {'Accept': 'application/vnd.github.v3+json',
           'Authorization': f'token {token}'}
url = f"https://api.github.com/repos/{nwo}/issues/{pr_num}/comments"
data = {'body': f"{message}"}
result = requests.post(url=url, headers=headers, json=data)

assert result.status_code == 201, f'Data summary did not post to PR successfully, received error code: {result.status_code}'
