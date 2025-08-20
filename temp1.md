Perfect 👍 since you’re running it with

```bash
python -m exp.test
```

you’ll want VS Code to debug it the **same way (as a module)** instead of just executing the file path.

Here’s how:

---

### 1. Select your interpreter

Make sure VS Code is using your conda env (`doc-search-3119-new`) as the Python interpreter:

* `Ctrl+Shift+P` → **Python: Select Interpreter** → pick `Anaconda3\envs\doc-search-3119-new\python.exe`.

---

### 2. Create/modify `.vscode/launch.json`

1. Go to the **Run and Debug** tab (left sidebar, or `Ctrl+Shift+D`).
2. Click **create a launch.json** (if you don’t already have one).
3. Add a configuration like this:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Module exp.test",
            "type": "python",
            "request": "launch",
            "module": "exp.test",       // 👈 run as module
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

---

### 3. Debug it

* Open `exp/test.py`.
* Set breakpoints where you need them.
* In the top of VS Code’s debugger (Run → Start Debugging or `F5`), pick **Python: Module exp.test**.
* It will launch exactly like `python -m exp.test` but under the VS Code debugger.

---

⚡ Do you want me to also show you how to pass **command-line arguments** to `exp.test` when debugging (like `python -m exp.test --foo bar`)?
