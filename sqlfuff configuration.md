The `.sqlfluff` configuration file is usually located in one of the following places:  

1. **Project Root Directory**  
   - Check if there's a `.sqlfluff` file in your project directory (where you're running `sqlfluff lint`).  
   - Run:  
     ```bash
     ls -la | grep .sqlfluff
     ```

2. **User Home Directory (~/.sqlfluff)**  
   - Some configurations are stored globally in your home directory.  
   - Run:  
     ```bash
     ls -la ~/.sqlfluff
     ```

3. **In `pyproject.toml` (Alternative Configuration Method)**  
   - Instead of a `.sqlfluff` file, your settings might be inside `pyproject.toml`.  
   - Check by running:  
     ```bash
     cat pyproject.toml | grep sqlfluff -A 10
     ```

### If You Don't Have a `.sqlfluff` File  
You can create one in the project root:  
```bash
touch .sqlfluff
```
Then add the configuration:  
```ini
[core]
large_file_skip_byte_limit = 30000
```




If `.sqlfluff` is not being recognized, try these steps to troubleshoot and fix the issue:

### 1. **Verify the `.sqlfluff` File is Being Used**
Run the following command to check which configuration file `sqlfluff` is using:
```bash
sqlfluff config
```
This will output the active configuration, including the location of the config file. If it does not show your `.sqlfluff` settings, the file may not be in the correct location.

### 2. **Ensure Proper File Format**
Check that the `.sqlfluff` file has the correct format and no syntax errors. It should look like this:
```ini
[core]
large_file_skip_byte_limit = 30000
```
If using `pyproject.toml`, ensure it looks like this:
```toml
[tool.sqlfluff.core]
large_file_skip_byte_limit = 30000
```

### 3. **Explicitly Specify the Config File**
Try running `sqlfluff` with the `--config` flag:
```bash
sqlfluff lint --config .sqlfluff src/steps/deployopt-daily-forecast-dgtl/sql/dgtl-daily-forecast-metrics-snapshotting.sql --dialect snowflake
```
This forces `sqlfluff` to use your `.sqlfluff` file.

### 4. **Check for Multiple Config Files**
If you have multiple config files (`.sqlfluff` and `pyproject.toml`), `sqlfluff` might be prioritizing the wrong one. Try renaming `.sqlfluff` to something else and see if `pyproject.toml` is being used instead.

### 5. **Upgrade SQLFluff**
Ensure you're using the latest version of `sqlfluff`, as older versions may not support all settings:
```bash
pip install --upgrade sqlfluff
```

### 6. **Try Setting the Config in Environment Variables**
If `sqlfluff` still doesn’t recognize `.sqlfluff`, try setting the limit via an environment variable:
```bash
export SQLFLUFF_LARGE_FILE_SKIP_BYTE_LIMIT=30000
```
Then rerun `sqlfluff lint`.

Let me know if you're still facing issues! 🚀
