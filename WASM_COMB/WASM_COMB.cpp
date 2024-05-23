#include <emscripten.h>
#include <string>
#include <cctype> // Include for isalpha and isupper
#include <cstdint>
#include <cmath>
#include <vector>
#include <algorithm>

extern "C" {

// Caesar Cipher Function
EMSCRIPTEN_KEEPALIVE
const char* caesarCipher(const char* input, int shift) {
    std::string encrypted = input;
    int len = encrypted.length();

    for (int i = 0; i < len; i++) {
        if (isalpha(encrypted[i])) {
            char offset = isupper(encrypted[i]) ? 'A' : 'a';
            encrypted[i] = (char)(((encrypted[i] + shift - offset) % 26) + offset);
        }
    }

    char* output = new char[len + 1];
    std::copy(encrypted.begin(), encrypted.end(), output);
    output[len] = '\0';

    return output;
}

// Vigenère Cipher Function
    const char* vigenereEncrypt(const char* message, const char* key) {
        std::string messageStr = message;
        std::string keyStr = key;
        std::string encryptedMessage = "";
        size_t keyLength = keyStr.length();
        size_t keyIndex = 0;

        for (char c : messageStr) {
            if (std::isalpha(c)) {
                char base = std::isupper(c) ? 'A' : 'a';
                char keyChar = std::toupper(keyStr[keyIndex % keyLength]);
                char encryptedChar = (c - base + keyChar - 'A') % 26 + base;
                encryptedMessage += encryptedChar;
                keyIndex++;
            } else {
                encryptedMessage += c;
            }
        }

        char* result = new char[encryptedMessage.length() + 1];
        std::strcpy(result, encryptedMessage.c_str());
        return result;
    }

    EMSCRIPTEN_KEEPALIVE
    const char* vigenereCipher(const char* message, const char* key) {
        return vigenereEncrypt(message, key);
    }

// Function to apply Gaussian blur to an image
void applyGaussianBlur(uint8_t* imageData, int width, int height) {
    // Gaussian kernel 5x5
    const int kernel[5][5] = {
        {1, 4, 7, 4, 1},
        {4, 16, 25, 16, 4},
        {7, 26, 41, 26, 7},
        {4, 16, 25, 16, 4},
        {1, 4, 7, 4, 1}
    };
    const int kernelSize = 5;
    const int half = kernelSize / 2;

    std::vector<uint8_t> blurredData(imageData, imageData + width * height * 4);

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int totalRed = 0, totalGreen = 0, totalBlue = 0, totalWeight = 0;

            for (int ky = -half; ky <= half; ky++) {
                for (int kx = -half; kx <= half; kx++) {
                    int pixelY = std::min(height - 1, std::max(0, y + ky));
                    int pixelX = std::min(width - 1, std::max(0, x + kx));
                    int weight = kernel[ky + half][kx + half];

                    int pixelIndex = (pixelY * width + pixelX) * 4;
                    totalRed += blurredData[pixelIndex] * weight;
                    totalGreen += blurredData[pixelIndex + 1] * weight;
                    totalBlue += blurredData[pixelIndex + 2] * weight;
                    totalWeight += weight;
                }
            }

            int index = (y * width + x) * 4;
            if (totalWeight > 0) {
                imageData[index] = totalRed / totalWeight;
                imageData[index + 1] = totalGreen / totalWeight;
                imageData[index + 2] = totalBlue / totalWeight;
            }
        }
    }
}

// Function to apply Sobel filter to an image
void applySobelFilter(uint8_t* imageData, int width, int height) {
    const int sobelX[3][3] = { {-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1} };
    const int sobelY[3][3] = { {-1, -2, -1}, {0, 0, 0}, {1, 2, 1} };

    std::vector<uint8_t> sobelData(imageData, imageData + width * height * 4);
    std::vector<uint8_t> grayscaleData(width * height);

    // Convert to grayscale
    for (int i = 0; i < width * height * 4; i += 4) {
        uint8_t avg = (sobelData[i] + sobelData[i + 1] + sobelData[i + 2]) / 3;
        grayscaleData[i / 4] = avg;
    }

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int pixelX = 0, pixelY = 0;
            for (int ky = -1; ky <= 1; ky++) {
                for (int kx = -1; kx <= 1; kx++) {
                    int pixelY = y + ky;
                    int pixelX = x + kx;
                    if (pixelY >= 0 && pixelY < height && pixelX >= 0 && pixelX < width) {
                        int pixel = grayscaleData[pixelY * width + pixelX];
                        pixelX += pixel * sobelX[ky + 1][kx + 1];
                        pixelY += pixel * sobelY[ky + 1][kx + 1];
                    }
                }
            }
            int magnitude = std::sqrt(pixelX * pixelX + pixelY * pixelY);
            int index = (y * width + x) * 4;
            sobelData[index] = magnitude;
            sobelData[index + 1] = magnitude;
            sobelData[index + 2] = magnitude;
            sobelData[index + 3] = 255; // Set alpha channel to 255
        }
    }

    std::copy(sobelData.begin(), sobelData.end(), imageData);
}

// Function to apply Sepia tone to an image
void applySepiaTone(uint8_t* imageData, int width, int height) {
    int totalPixels = width * height;

    for (int i = 0; i < totalPixels * 4; i += 4) {
        int red = imageData[i];
        int green = imageData[i + 1];
        int blue = imageData[i + 2];

        int newRed = std::min(255, static_cast<int>(red * 0.393 + green * 0.769 + blue * 0.189));
        int newGreen = std::min(255, static_cast<int>(red * 0.349 + green * 0.686 + blue * 0.168));
        int newBlue = std::min(255, static_cast<int>(red * 0.272 + green * 0.534 + blue * 0.131));

        imageData[i] = newRed;
        imageData[i + 1] = newGreen;
        imageData[i + 2] = newBlue;
    }
}

} // extern "C"
