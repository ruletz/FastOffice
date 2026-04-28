import winreg as reg
import sys

def patch_assoc(prog_id):
    try:
        path = fr'{prog_id}\shell\open\command'
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, path, 0, reg.KEY_ALL_ACCESS) as key:
            val, _ = reg.QueryValueEx(key, '')
            if '--no-proxy-server' not in val:
                # Add flags just before "%1"
                new_val = val.replace('%1', '--no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --js-flags="--max-old-space-size=256 --optimize-for-size" "%1"')
                reg.SetValueEx(key, '', 0, reg.REG_SZ, new_val)
                print(f'Updated {prog_id}: {new_val}')
            else:
                print(f'Already updated {prog_id}: {val}')
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error for {prog_id}: {e}")

patch_assoc('OnlyOffice.Document')
patch_assoc('.docx')
print("Registry patched.")
