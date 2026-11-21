// Week 14: validator.rs
//
// Implement password strength validation.
// The tests at the bottom verify your implementations.

#![allow(dead_code)]
use std::fmt;

/// Describes how strong a password is.
#[derive(Debug, PartialEq)]
pub enum PasswordStrength {
    Weak,
    Medium,
    Strong,
    VeryStrong,
}

impl fmt::Display for PasswordStrength {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let label = match self {
            PasswordStrength::Weak => "Weak",
            PasswordStrength::Medium => "Medium",
            PasswordStrength::Strong => "Strong",
            PasswordStrength::VeryStrong => "Very strong",
        };
        write!(f, "{}", label)
    }
}

/// Rates the strength of `password` using these rules:
///
/// Start with score 0, add points for each criterion met:
///   +1  length ≥ 8
///   +1  length ≥ 12
///   +1  length ≥ 16
///   +1  contains at least one lowercase letter
///   +1  contains at least one uppercase letter
///   +1  contains at least one digit
///   +1  contains at least one symbol (non-alphanumeric character)
///
/// Map score to strength:
///   0–2 → Weak
///   3–4 → Medium
///   5–6 → Strong
///   7   → VeryStrong
pub fn validate_strength(password: &str) -> PasswordStrength {
    let mut score = 0;

    if password.len() >= 8 {
        score += 1;
    }
    if password.len() >= 12 {
        score += 1;
    }
    if password.len() >= 16 {
        score += 1;
    }
    if password
        .chars()
        .any(|character| character.is_ascii_lowercase())
    {
        score += 1;
    }
    if password
        .chars()
        .any(|character| character.is_ascii_uppercase())
    {
        score += 1;
    }
    if password.chars().any(|character| character.is_ascii_digit()) {
        score += 1;
    }
    if password
        .chars()
        .any(|character| !character.is_alphanumeric())
    {
        score += 1;
    }

    match score {
        0..=2 => PasswordStrength::Weak,
        3..=4 => PasswordStrength::Medium,
        5..=6 => PasswordStrength::Strong,
        _ => PasswordStrength::VeryStrong,
    }
}

/// Returns `true` if `password` matches a common weak pattern.
///
/// Check for these patterns (case-insensitive):
///   - All characters are the same (e.g. "aaaa", "1111")
///   - The password is one of the 10 common passwords listed in COMMON_PASSWORDS
pub fn check_common_patterns(password: &str) -> bool {
    let mut characters = password.chars();
    let Some(first) = characters.next() else {
        return false;
    };

    if characters.all(|character| character == first) {
        return true;
    }

    let normalized = password.to_ascii_lowercase();
    COMMON_PASSWORDS
        .iter()
        .any(|common| common.eq_ignore_ascii_case(&normalized))
}

/// Estimates the Shannon entropy of `password` in bits.
///
/// Entropy = length × log₂(charset_size)
///
/// Determine charset_size by which character classes are present:
///   lowercase only          → 26
///   + uppercase             → 52
///   + digits                → 62
///   + any non-alphanumeric  → 94
///
/// Use `f64::log2(charset_size as f64) * length as f64`.
pub fn calculate_entropy(password: &str) -> f64 {
    if password.is_empty() {
        return 0.0;
    }

    let lower = password
        .chars()
        .any(|character| character.is_ascii_lowercase());
    let upper = password
        .chars()
        .any(|character| character.is_ascii_uppercase());
    let digit = password.chars().any(|character| character.is_ascii_digit());
    let symbol = password
        .chars()
        .any(|character| !character.is_alphanumeric());

    let charset_size = if symbol {
        94
    } else if digit && (lower || upper) {
        62
    } else if lower && upper {
        52
    } else if lower || upper {
        26
    } else if digit {
        10
    } else {
        0
    };

    password.len() as f64 * f64::log2(charset_size as f64)
}

/// Ten common passwords to flag as weak patterns.
pub const COMMON_PASSWORDS: &[&str] = &[
    "password",
    "123456",
    "password123",
    "qwerty",
    "letmein",
    "iloveyou",
    "admin",
    "welcome",
    "monkey",
    "dragon",
];

// ============================================================================
// TESTS: DO NOT MODIFY
// ============================================================================
#[cfg(test)]
mod tests {
    use super::*;

    // --- validate_strength ---

    #[test]
    fn test_strength_weak_short() {
        // "hi": length 2, no upper, has lower, no digit, no symbol → score ~1
        assert_eq!(validate_strength("hi"), PasswordStrength::Weak);
    }

    #[test]
    fn test_strength_medium() {
        // "Password": length 8 (+1), has lower (+1), has upper (+1), no digit, no symbol → score 3
        assert_eq!(validate_strength("Password"), PasswordStrength::Medium);
    }

    #[test]
    fn test_strength_strong() {
        // "Password1": length 8 (+1), lower (+1), upper (+1), digit (+1), no symbol → score 4…
        // "Password1!": length 10 (+1 for ≥8), lower (+1), upper (+1), digit (+1), symbol (+1) → score 5
        assert_eq!(validate_strength("Password1!"), PasswordStrength::Strong);
    }

    #[test]
    fn test_strength_very_strong() {
        // All 7 criteria met
        assert_eq!(
            validate_strength("MyStr0ng!Pass2024"),
            PasswordStrength::VeryStrong
        );
    }

    #[test]
    fn test_strength_display() {
        assert_eq!(format!("{}", PasswordStrength::Weak), "Weak");
        assert_eq!(format!("{}", PasswordStrength::Medium), "Medium");
        assert_eq!(format!("{}", PasswordStrength::Strong), "Strong");
        assert_eq!(format!("{}", PasswordStrength::VeryStrong), "Very strong");
    }

    // --- check_common_patterns ---

    #[test]
    fn test_common_password_detected() {
        assert!(check_common_patterns("password"));
        assert!(check_common_patterns("123456"));
        assert!(check_common_patterns("PASSWORD")); // case-insensitive
    }

    #[test]
    fn test_all_same_char_detected() {
        assert!(check_common_patterns("aaaa"));
        assert!(check_common_patterns("1111"));
        assert!(check_common_patterns("ZZZZ"));
    }

    #[test]
    fn test_unique_password_not_flagged() {
        assert!(!check_common_patterns("X7#kP2@mQ9"));
    }

    // --- calculate_entropy ---

    #[test]
    fn test_entropy_lowercase_only() {
        // charset = 26, length = 4 → 4 * log2(26) ≈ 18.8
        let e = calculate_entropy("abcd");
        assert!((e - 4.0 * f64::log2(26.0)).abs() < 1e-9);
    }

    #[test]
    fn test_entropy_mixed_case() {
        // charset = 52 (lower + upper), length = 4
        let e = calculate_entropy("abCD");
        assert!((e - 4.0 * f64::log2(52.0)).abs() < 1e-9);
    }

    #[test]
    fn test_entropy_alphanumeric() {
        // charset = 62 (lower + upper + digits), length = 4
        let e = calculate_entropy("aB3d");
        assert!((e - 4.0 * f64::log2(62.0)).abs() < 1e-9);
    }

    #[test]
    fn test_entropy_with_symbols() {
        // charset = 94 (lower + upper + digits + symbols), length = 4
        let e = calculate_entropy("aB3!");
        assert!((e - 4.0 * f64::log2(94.0)).abs() < 1e-9);
    }

    #[test]
    fn test_entropy_empty() {
        assert_eq!(calculate_entropy(""), 0.0);
    }
}
