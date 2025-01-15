#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdint.h>
typedef uint8_t  BYTE;
typedef uint32_t DWORD;
typedef int32_t  LONG;
typedef uint16_t WORD;

typedef struct
{
    WORD   bfType;
    DWORD  bfSize;
    WORD   bfReserved1;
    WORD   bfReserved2;
    DWORD  bfOffBits;
} __attribute__((__packed__))
BITMAPFILEHEADER;

typedef struct
{
    DWORD  biSize;
    LONG   biWidth;
    LONG   biHeight;
    WORD   biPlanes;
    WORD   biBitCount;
    DWORD  biCompression;
    DWORD  biSizeImage;
    LONG   biXPelsPerMeter;
    LONG   biYPelsPerMeter;
    DWORD  biClrUsed;
    DWORD  biClrImportant;
} __attribute__((__packed__))
BITMAPINFOHEADER;

typedef struct
{
    BYTE  rgbtBlue;
    BYTE  rgbtGreen;
    BYTE  rgbtRed;
} __attribute__((__packed__))
RGBTRIPLE;


typedef struct {
    uint8_t x;
    uint8_t y;

} letter;

void cipher(int height, int width, RGBTRIPLE image[height][width], letter message1[], int length) {
    for (int h = height - 1; h > -1; h -= 20){
        for (int h2 = h - 4; h2 > h - 19; h2 -= 4){
            for (int w = 0; w < width; w++) {
                image[h2][w].rgbtRed = image[h2][w].rgbtRed * 0.9;
                image[h2][w].rgbtGreen = image[h2][w].rgbtGreen * 0.9;
                image[h2][w].rgbtBlue = image[h2][w].rgbtBlue * 0.9;
            }
        }
        for (int w = 0; w < width; w++) {
            image[h][w].rgbtRed = image[h][w].rgbtRed * 0.7;
            image[h][w].rgbtGreen = image[h][w].rgbtGreen * 0.7;
            image[h][w].rgbtBlue = image[h][w].rgbtBlue * 0.7;
        }
    }
    for (int w = 0; w < width; w += 20){
        for (int w2 = w + 4; w2 < w + 19; w2 += 4){
            for (int h = 0; h < width; h++) {
                image[h][w2].rgbtRed = image[h][w2].rgbtRed * 0.9;
                image[h][w2].rgbtGreen = image[h][w2].rgbtGreen * 0.9;
                image[h][w2].rgbtBlue = image[h][w2].rgbtBlue * 0.9;
            }
        }
        for (int h = 0; h < height; h++) {
            image[h][w].rgbtRed = image[h][w].rgbtRed * 0.7;
            image[h][w].rgbtGreen = image[h][w].rgbtGreen * 0.7;
            image[h][w].rgbtBlue = image[h][w].rgbtBlue * 0.7;
        }
    }
    int letter = 0;
    for(int h = height - 1; h > -1; h -= 20) {
        for (int w = 0; w < width; w += 20){
            if(message1[letter].x == 32) {
                for (int a = 1; a < 20; a++) {
                    image[h - 1][w + a].rgbtRed = image[h - 1][w + a].rgbtRed  * 1.5 > 255 ? 255 : image[h - 1][w + a].rgbtRed * 1.5;
                    image[h - 1][w + a].rgbtGreen = 0;
                    image[h - 1][w + a].rgbtBlue = 0;
                    image[h - 19][w + a].rgbtRed = image[h - 19][w + a].rgbtRed  * 1.5 > 255 ? 255 : image[h - 19][w + a].rgbtRed * 1.5;
                    image[h - 19][w + a].rgbtGreen = 0;
                    image[h - 19][w + a].rgbtBlue = 0;
                }
                for (int b = 2; b < 19; b++) {
                    image[h - b][w + 20 - b].rgbtRed = image[h - b][w + 20 - b].rgbtRed  * 1.7 > 255 ? 255 : image[h - b][w + 20 - b].rgbtRed*1.7;
                    image[h - b][w + 20 - b].rgbtGreen *= 0.8;
                    image[h - b][w + 20 - b].rgbtBlue *= 0.8;
                }
            }
            else if (!message1[letter].x) {
                ;
            }
            else {
                for (int a = 0; a < 3; a++) {
                    for (int b = 0; b < 3; b++) {
                        image[h - 1 - 4 * (message1[letter].y - 1) - a][w + 1 + 4 * (message1[letter].x - 1) + b].rgbtRed = image[h - 1 - 4 * (message1[letter].y - 1) - a][w + 1 + 4 * (message1[letter].x - 1) + b].rgbtRed * 1.7 > 255 ? 255 : image[h - 1 - 4 * (message1[letter].y - 1) - a][w + 1 + 4 * (message1[letter].x - 1) + b].rgbtRed*1.7;
                        image[h - 1 - 4 * (message1[letter].y - 1) - a][w + 1 + 4 * (message1[letter].x - 1) + b].rgbtGreen *= 0.8;
                        image[h - 1 - 4 * (message1[letter].y - 1) - a][w + 1 + 4 * (message1[letter].x - 1) + b].rgbtBlue *= 0.8;
                    }
                }
            }
            letter++;
            if (letter >= length) {
                goto z;
            }
        }
    }
    z:
    return;
}




int main(int argc, char *argv[])
{
    char *infile = argv[1];
    char *outfile = argv[2];

    FILE *text = fopen(argv[3], "r");
    if (text == NULL)
    {
        printf("Could not open %s.\n", argv[3]);
        return 8;
    }
    fseek(text, 0, SEEK_END);
    int length = ftell(text);
    fseek(text, 0, SEEK_SET);
    char *message = malloc(length + 1);
    fread(message, 1, length, text);
    message[length] = '\0';
    letter message1[length];
    fclose(text);

    for (int i = 0; i < length; i++) {
        if (isalpha(message[i])) {
            if (tolower(message[i]) == 'z')
            {
                message1[i].x = 32;
                message1[i].y = 32;
            }
            else {
            message1[i].x = ((tolower(message[i]) - 'a') % 5 + 1);
            message1[i].y = (int)floor((tolower(message[i]) - 'a') / 5.0) + 1;
            }
        }
        else {
            message1[i].x = 0;
        }
    }


    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 4;
    }

    // Open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 5;
    }

    // Read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // Read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // Ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 6;
    }

    // Get image's dimensions
    int height = abs(bi.biHeight);
    int width = bi.biWidth;

    // Allocate memory for image
    RGBTRIPLE(*image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (image == NULL)
    {
        printf("Not enough memory to store image.\n");
        fclose(outptr);
        fclose(inptr);
        return 7;
    }

    // Determine padding for scanlines
    int padding = (4 - (width * sizeof(RGBTRIPLE)) % 4) % 4;

    // Iterate over infile's scanlines
    for (int i = 0; i < height; i++)
    {
        // Read row into pixel array
        fread(image[i], sizeof(RGBTRIPLE), width, inptr);

        // Skip over padding
        fseek(inptr, padding, SEEK_CUR);
    }
        cipher(height, width, image, message1, length);

    // Write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // Write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // Write new pixels to outfile
    for (int i = 0; i < height; i++)
    {
        // Write row to outfile
        fwrite(image[i], sizeof(RGBTRIPLE), width, outptr);

        // Write padding at end of row
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // Free memory for image
    free(image);

    // Close files
    fclose(inptr);
    fclose(outptr);
    return 0;
}
