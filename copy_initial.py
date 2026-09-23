import json
import os
import shutil

os.makedirs("delivery/scripts", exist_ok=True)

# 复制先前已验证的纯SQL脚本到 delivery/scripts/
shutil.copy("docs/scripts/all_vm_modules_queries.sql", "delivery/scripts/all_vm_modules_queries.sql")
shutil.copy("docs/sql-inventory.md", "delivery/03_sql_code_inventory.md")
shutil.copy("docs/vm-modules-sql-statements.md", "delivery/02_vm_modules_sql_statements.md")

print("Copied SQL scripts and initial statements.")
