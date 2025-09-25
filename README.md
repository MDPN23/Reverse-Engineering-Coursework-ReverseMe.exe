# Reverse Engineering Coursework: ReverseMe.exe

**Download sample:**  
[ReverseMe.exe (MediaFire)](http://www.mediafire.com/?34q13so06na9j46)

---

## Description
`ReverseMe.exe` is a simple Windows GUI program that asks the user to enter a **Name** and a **Serial Number**. The program verifies whether the provided serial matches an algorithm derived from the input name.

This analysis was performed with **Ghidra** (disassembly and decompilation). The following functions were identified as the core parts of the key generation and verification logic.

---

## Summary of important functions

### `FUN_00401000`
- **Purpose:** Core hashing routine — implementation of the **SHA-256 compression function**.  
- **Role:** Processes 512-bit input blocks and updates the SHA-256 internal state.  
- **Globals used:** `DAT_00406804 .. DAT_00406820`.  
- **Called by:** `FUN_0040444a` to produce the digest of the Name.

---

### `FUN_00404044`
- **Purpose:** SHA-256 padding helper.  
- **Role:** Appends the `0x80` byte, zero padding, and the 64-bit big-endian message length to the final block.  
- **Globals used:** `DAT_00406784`, `DAT_0040688c`, `DAT_00406884`.  
- **Called by:** `FUN_00401000` when final block padding is required.

---

### `FUN_004040d9`
- **Purpose:** GUI initialization function (equivalent to `WinMain`).  
- **Role:**  
  - Registers a window class (`WNDCLASSEXA`) with `lpfnWndProc = FUN_004043a3`.  
  - Loads resources (icon/bitmap), creates the main window and child controls (edit boxes, labels, buttons).  
  - Stores control handles in globals (e.g. `DAT_004068a8`, `DAT_004068a4`, ...).  
  - Runs the message loop (`GetMessage`/`DispatchMessage`).  

---

### `FUN_004043a3`
- **Purpose:** Window procedure (WndProc).  
- **Role:**  
  - `WM_DESTROY` → `PostQuitMessage(0)`.  
  - `WM_COMMAND` → handle control commands:  
    - Exit/Close commands.  
    - Button Check → calls `FUN_0040444a` (generate) then `FUN_004044a9` (verify).  
  - Displays result via `MessageBoxA` ("Good Job" or "Wrong Serial").

---

### `FUN_0040444a`
- **Purpose:** Generate the serial string from the Name.  
- **Role:**  
  - Reads Name from the UI (`GetWindowTextA`).  
  - Computes SHA-256 via `FUN_00401000`.  
  - Iterates digest bytes and computes:
    ```
    for i from 0..:
      if digest[i] == 0: break
      t = digest[i] * i
      sum += t*t + 0x50   (wrap as 32-bit)
    serial_value = sum ^ 0x12345678
    ```
  - Formats the serial with `wsprintf` and stores the formatted string in `DAT_0040676c`.

---

### `FUN_004044a9`
- **Purpose:** Verify user-supplied serial.  
- **Role:**  
  - Reads Serial text from the UI (`GetWindowTextA`).  
  - Compares the user buffer to `DAT_0040676c` (the generated serial) per 4-byte blocks.  
  - Returns `1` if identical, `0` otherwise.

---

## Program workflow
1. User enters **Name**.  
2. `FUN_0040444a` computes the serial from the Name and stores it internally.  
3. User enters **Serial**.  
4. `FUN_004044a9` compares the entered serial with the generated one.  
5. `FUN_004043a3` shows a message box indicating success (`Good Job`) or failure (`Wrong Serial`).

---

## Important notes
- This analysis is part of a coursework assignment for learning reverse engineering with **Ghidra**.  
- `ReverseMe.exe` is a simple crackme-style exercise and should not be used for illegal activities.  
- The serial generation depends on SHA-256(Name) then a small custom accumulation and a final XOR with `0x12345678`. Examining `DAT_00406078` resource in Ghidra will reveal whether the program formats the serial in decimal (`%u`) or hex (`%08X`) — pick the correct format when testing.

---

## Reference
- [Ghidra Software Reverse Engineering Suite](https://ghidra-sre.org/)  
- Windows API docs (e.g. `CreateWindowEx`, `GetWindowTextA`, `wsprintfA`, `MessageBoxA`)

---

## Example: keygen script usage (brief)
You can implement the keygen logic in Python (example `keygen.py`) to reproduce the serial for any Name. 
