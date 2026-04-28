#pragma once

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint32_t asc_minimal_version_major(void);
uint32_t asc_minimal_version_minor(void);

uint64_t asc_fnv1a64(const uint8_t* data, size_t len);

int32_t asc_is_valid_utf8_cstr(const char* s);

#ifdef __cplusplus
}
#endif

