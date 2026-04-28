#![allow(non_snake_case)]

use core::ffi::c_char;

// Very small, dependency-free Rust staticlib intended to host hot paths over time.
// Exposed API must remain C-compatible.

#[no_mangle]
pub extern "C" fn asc_minimal_version_major() -> u32 {
    0
}

#[no_mangle]
pub extern "C" fn asc_minimal_version_minor() -> u32 {
    1
}

/// Compute a fast 64-bit FNV-1a hash over a byte buffer.
/// Useful for cache keys and quick content fingerprinting.
#[no_mangle]
pub extern "C" fn asc_fnv1a64(data: *const u8, len: usize) -> u64 {
    if data.is_null() || len == 0 {
        return 0;
    }
    let bytes = unsafe { core::slice::from_raw_parts(data, len) };
    let mut hash: u64 = 0xcbf29ce484222325;
    for &b in bytes {
        hash ^= b as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

/// Return 1 if `s` is a valid, NUL-terminated UTF-8 string, else 0.
#[no_mangle]
pub extern "C" fn asc_is_valid_utf8_cstr(s: *const c_char) -> i32 {
    if s.is_null() {
        return 0;
    }
    unsafe {
        let mut p = s as *const u8;
        let mut len: usize = 0;
        while *p != 0 {
            len += 1;
            p = p.add(1);
            if len > (16 * 1024 * 1024) {
                // Hard cap to avoid scanning arbitrary memory on malformed inputs.
                return 0;
            }
        }
        let bytes = core::slice::from_raw_parts(s as *const u8, len);
        core::str::from_utf8(bytes).is_ok() as i32
    }
}

