import pandas as pd

# Sample data
views_df = pd.DataFrame({'project_id': [1, 2, 3], 'views': [100, 150, 200]})
projects_df = pd.DataFrame({'@id': [1, 2, 3], '@name': ['Project A', 'Project B', 'Project C']})

# Perform the left join
views_df = views_df.merge(projects_df, left_on='project_id', right_on='@id', how='left')

# Rename the column
views_df.rename(columns={'@name': 'project_name'}, inplace=True)

# Drop the redundant @id column if not needed
views_df.drop(columns=['@id'], inplace=True)

print(views_df)
