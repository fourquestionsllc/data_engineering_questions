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
