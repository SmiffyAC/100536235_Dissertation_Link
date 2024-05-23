function caesarCipher(str, shift) {
    return str.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            let code = char.charCodeAt(0);
            // Uppercase letters
            if (code >= 65 && code <= 90) {
                return String.fromCharCode(((code - 65 + shift) % 26) + 65);
            }
            // Lowercase letters
            else if (code >= 97 && code <= 122) {
                return String.fromCharCode(((code - 97 + shift) % 26) + 97);
            }
        }
        // Non-alphabetical characters remain unchanged
        return char;
    }).join('');
}

function vigenereEncrypt(message, key) {
    let encryptedMessage = "";
    let keyLength = key.length;
    let keyIndex = 0;

    for (let i = 0; i < message.length; i++) {
        let char = message[i];
        if (/[a-zA-Z]/.test(char)) {
            let base = char >= 'a' && char <= 'z' ? 'a'.charCodeAt(0) : 'A'.charCodeAt(0);
            let keyChar = key[keyIndex % keyLength].toUpperCase().charCodeAt(0);
            let encryptedCharCode = ((char.charCodeAt(0) - base + keyChar - 'A'.charCodeAt(0)) % 26) + base;
            encryptedMessage += String.fromCharCode(encryptedCharCode);
            keyIndex++;
        } else {
            encryptedMessage += char;
        }
    }

    return encryptedMessage;
}