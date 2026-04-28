#
# Optional Rust staticlib integration for qmake.
# This file is intentionally NOT included by default yet (to keep builds stable).
#
# To enable, include from `ASCDocumentEditor.pro` and ensure the Rust toolchain is present.
#

ASC_RUST_MINIMAL_DIR = $$PWD/../rust/asc_minimal

win32 {
    ASC_RUST_MINIMAL_LIB = $$ASC_RUST_MINIMAL_DIR/target/release/asc_minimal.lib
} else {
    ASC_RUST_MINIMAL_LIB = $$ASC_RUST_MINIMAL_DIR/target/release/libasc_minimal.a
}

INCLUDEPATH += $$ASC_RUST_MINIMAL_DIR/include
LIBS += $$ASC_RUST_MINIMAL_LIB

