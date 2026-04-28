use wasm_bindgen::prelude::*;
use regex::Regex;

// Base64 decode hook 
#[wasm_bindgen]
pub fn decode_base64_fast(input: &str) -> Vec<u8> {
    use base64::{Engine as _, engine::general_purpose};
    match general_purpose::STANDARD.decode(input.trim()) {
        Ok(res) => res,
        Err(_) => {
            match general_purpose::STANDARD_NO_PAD.decode(input.trim()) {
                Ok(res) => res,
                Err(_) => vec![],
            }
        }
    }
}

// 2. OOXML String Node Parser / Optimizer hook
#[wasm_bindgen]
pub fn parse_ooxml_tags_fast(xml_string: &str) -> String {
    // A classic OOXML bottleneck is replacing namespaces and formatting heavy tags.
    // Instead of JS doing regexes, we compile a fast Rust regex.
    let re = Regex::new(r"<(w|p|m):([a-zA-Z]+)([^>]*)>").unwrap();
    
    // As an optimization we standardize namespaces natively
    let result = re.replace_all(xml_string, |caps: &regex::Captures| {
        format!("<{}:{}{}>", &caps[1], &caps[2], &caps[3])
    });
    
    // Also strip out entirely empty text nodes that bloat layout tree
    let re_empty = Regex::new(r"<w:t>\s*</w:t>").unwrap();
    let cleaned = re_empty.replace_all(&result, "");
    
    cleaned.into_owned()
}
