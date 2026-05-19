import subprocess
import sys

result = subprocess.run(
    [sys.executable, "app.py"],
    capture_output=True,
    text=True,
    cwd="c:\\Users\\30906\\Desktop\\作业\\简历匹配系统\\算法接口"
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print("\nReturn code:", result.returncode)